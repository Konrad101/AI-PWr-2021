from random import Random

from board.board import PCBBoard
from generator.generator_constants import MIN_BOARD_Y, MAX_PATH_OFFSET_OVER_BOARD, MIN_BOARD_X
from board.segment import Direction, Segment
from board.path import Path


def generate_random_population(population_size, board_width, board_height, board_points):
    random_population = []
    for i in range(population_size):
        board = PCBBoard(board_width, board_height)
        for points in board_points:
            points_pair = create_random_path(points, board_width, board_height, correction_probability=0.05)
            board.add_connected_points(points_pair)
        random_population.append(board)
    return random_population


# generowanie sciezki poza mapa
def create_random_path(points, board_width, board_height, correction_probability=0.1):
    path_segments = []

    completed_path = False
    current_x = points[0]
    current_y = points[1]

    last_direction = 0
    current_segment = None
    while not completed_path:
        # losuj kierunek
        # sprawdz czy w tym kierunku mozna cos dodac
        if Random().random() < correction_probability:
            direction = get_correct_direction(current_x, current_y, points[2], points[3])
        else:
            direction = get_random_direction(board_width, board_height, current_x, current_y)

        # kierunek jest ustawiony, teraz tworze albo zwiekszam segment
        if direction != last_direction:
            if current_segment is not None:
                path_segments.append(current_segment)
            current_segment = Segment(1, direction, current_x, current_y)
        else:
            current_segment.length += 1

        # uzupelniam aktualne x i y
        if direction == Direction.up:
            current_y -= 1
        elif direction == Direction.down:
            current_y += 1
        elif direction == Direction.left:
            current_x -= 1
        elif direction == Direction.right:
            current_x += 1

        if reached_finish(points[2], points[3], current_segment):
            completed_path = True
            path_segments.append(current_segment)
        last_direction = direction

    return Path(points[0], points[1], points[2], points[3], path_segments)


def get_random_direction(board_width, board_height, current_x, current_y):
    direction = Direction(Random().randint(1, 4))
    while not direction_is_available(board_width, board_height, current_x, current_y, direction):
        dir_number = (direction.value + 1) % 5
        if dir_number == 0:
            dir_number = 1
        direction = Direction(dir_number)
    return direction


def get_correct_direction(current_x, current_y, dst_x, dst_y):
    if __count_distance(current_x, dst_x) > __count_distance(current_x + 1, dst_x):
        return Direction.right
    elif __count_distance(current_x, dst_x) > __count_distance(current_x - 1, dst_x):
        return Direction.left
    elif __count_distance(current_y, dst_y) > __count_distance(current_y + 1, dst_y):
        return Direction.down

    return Direction.up


def __count_distance(first_coordinate, second_coordinate):
    return abs(first_coordinate - second_coordinate)


def reached_finish(dst_x, dst_y, segment):
    reached = False
    if segment.direction == Direction.up and segment.initial_x == dst_x:
        if segment.initial_y - segment.length == dst_y:
            reached = True
    elif segment.direction == Direction.down and segment.initial_x == dst_x:
        if segment.initial_y + segment.length == dst_y:
            reached = True
    elif segment.direction == Direction.left and segment.initial_y == dst_y:
        if segment.initial_x - segment.length == dst_x:
            reached = True
    elif segment.direction == Direction.right and segment.initial_y == dst_y:
        if segment.initial_x + segment.length == dst_x:
            reached = True

    return reached


def direction_is_available(board_width, board_height, start_x, start_y, direction):
    is_available = True
    if direction == Direction.up and start_y <= MIN_BOARD_Y - MAX_PATH_OFFSET_OVER_BOARD:
        is_available = False
    elif direction == Direction.down and start_y >= abs(board_height + MAX_PATH_OFFSET_OVER_BOARD):
        is_available = False
    elif direction == Direction.left and start_x <= MIN_BOARD_X - MAX_PATH_OFFSET_OVER_BOARD:
        is_available = False
    elif direction == Direction.right and start_x >= abs(board_width + MAX_PATH_OFFSET_OVER_BOARD):
        is_available = False
    return is_available
