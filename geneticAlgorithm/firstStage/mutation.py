from random import Random

from board.segment import Direction
from generator.generator_constants import MIN_BOARD_X, MIN_BOARD_Y, MAX_PATH_OFFSET_OVER_BOARD
from generator.random_generator import create_random_path

COMPLETE_MUTATION_PROBABILITY = 0.01


def mutation_operator(board, small_mutation_probability=0.33):
    # wylosuj sciezke do mutacji
    if Random().random() < small_mutation_probability:
        path_index = __get_random_path_index(board)
        paths = board.get_paths()
        path = paths[path_index]
        path = mutate_path_segment(path, board)
        paths[path_index] = path
    elif Random().random() < COMPLETE_MUTATION_PROBABILITY:
        # mutacja jednej sciezki
        path_to_mutation_index = __get_random_path_index(board)
        paths = board.get_paths()
        path = paths[path_to_mutation_index]
        path_src_x, path_src_y = path.get_source_point()
        path_dst_x, path_dst_y = path.get_destination_point()
        path_points = path_src_x, path_src_y, path_dst_x, path_dst_y
        paths[path_to_mutation_index] = create_random_path(path_points,
                                                           board.get_width(),
                                                           board.get_height())

    return board


def __get_random_path_index(board):
    paths = board.get_paths()
    return Random().randint(0, len(paths) - 1)


def mutate_path_segment(path, board):
    segments = path.get_segments()
    if len(segments) > 2:
        segment_to_mutation = segments[Random().randint(1, len(segments) - 2)]
        __move_segment(segment_to_mutation, board)
        repaired_segments = __repair_path(path, segment_to_mutation)
        path.set_segments(repaired_segments)
    return path


def __move_segment(segment, board):
    segment_offset = 1
    if Random().randint(0, 1) % 2 == 0:
        segment_offset *= -1

    # i nie wyjdzie poza mape za bardzo
    if segment.direction == Direction.up or segment.direction == Direction.down:
        if __segment_offset_available(segment, segment_offset, board):
            segment.initial_x += segment_offset
        else:
            segment.initial_x -= segment_offset
    else:
        if __segment_offset_available(segment, segment_offset, board):
            segment.initial_y += segment_offset
        else:
            segment.initial_y -= segment_offset


def __segment_offset_available(segment, segment_offset, board):
    if segment.direction == Direction.up or segment.direction == Direction.down:
        if segment.initial_x + segment_offset < MIN_BOARD_X - MAX_PATH_OFFSET_OVER_BOARD or \
                segment.initial_x + segment_offset > board.get_width() + MAX_PATH_OFFSET_OVER_BOARD:
            return False
    else:
        if segment.initial_y + segment_offset < MIN_BOARD_Y - MAX_PATH_OFFSET_OVER_BOARD or \
                segment.initial_y + segment_offset > board.get_height() + MAX_PATH_OFFSET_OVER_BOARD:
            return False

    return True


def __repair_path(path, mutated_segment):
    mutated_segment_index = path.get_segments().index(mutated_segment)
    segments = path.get_segments()
    optimized_previous = False
    optimized_next = False

    repaired_segments = []
    for i in range(0, mutated_segment_index):
        if i == mutated_segment_index - 1:
            if mutated_segment.initial_x == segments[i].initial_x and \
                    mutated_segment.initial_y == segments[i].initial_y:
                optimized_previous = True
            else:
                repaired_segments.append(segments[i])
        else:
            repaired_segments.append(segments[i])
            dst_x, dst_y = segments[i].get_destination_point()
            if mutated_segment.initial_x == dst_x and mutated_segment.initial_y == dst_y:
                optimized_previous = True
                break

    repaired_segments.append(mutated_segment)

    next_segments = []
    mutated_dst_x, mutated_dst_y = mutated_segment.get_destination_point()
    for i in range(len(segments) - 1, mutated_segment_index, -1):
        if i == mutated_segment_index + 1:
            segment_dst_x, segment_dst_y = segments[i].get_destination_point()
            if mutated_dst_x == segment_dst_x \
                    and mutated_dst_y == segment_dst_y:
                optimized_next = True
            else:
                next_segments.append(segments[i])
        else:
            next_segments.append(segments[i])
            src_x = segments[i].initial_x
            src_y = segments[i].initial_y
            if mutated_dst_x == src_x and mutated_dst_y == src_y:
                optimized_next = True
                break

    for i in range(0, len(next_segments)):
        repaired_segments.append(next_segments[len(next_segments) - 1 - i])

    if not optimized_previous:
        previous_segment = segments[mutated_segment_index - 1]
        offset_direction = __get_offset_direction(mutated_segment, previous_segment)
        if previous_segment.direction == offset_direction:
            previous_segment.length += 1
        else:
            previous_segment.length -= 1
            if previous_segment.length == 0:
                repaired_segments.remove(previous_segment)
    if not optimized_next:
        next_segment = segments[mutated_segment_index + 1]
        next_segment.initial_x = mutated_dst_x
        next_segment.initial_y = mutated_dst_y
        offset_direction = __get_offset_direction(mutated_segment, next_segment)
        if next_segment.direction != offset_direction:
            next_segment.length += 1
        else:
            next_segment.length -= 1
            if next_segment.length == 0:
                repaired_segments.remove(next_segment)
    return repaired_segments


def __get_offset_direction(mutated_segment, neighbour_segment):
    neigh_dst_x, neigh_dst_y = neighbour_segment.get_destination_point()
    if mutated_segment.initial_x < neigh_dst_x:
        return Direction.left
    if mutated_segment.initial_x > neigh_dst_x:
        return Direction.right
    if mutated_segment.initial_y > neigh_dst_y:
        return Direction.down

    return Direction.up
