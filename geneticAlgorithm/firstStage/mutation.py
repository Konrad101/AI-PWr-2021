from random import Random

from generator.random_generator import create_random_path

COMPLETE_MUTATION_PROBABILITY = 0.08


def mutation_operator(board, small_mutation_probability=0.37):
    if Random().random() < small_mutation_probability:
        paths = board.get_paths()
        path_to_mutation_index = Random().randint(0, len(paths) - 1)
        __mutate_path(board, path_to_mutation_index)
    elif Random().random() < COMPLETE_MUTATION_PROBABILITY:
        paths = board.get_paths()
        for i in range(0, len(paths)):
            __mutate_path(board, i)

    return board


def __mutate_path(board, path_index):
    paths = board.get_paths()
    path_to_mutation = paths[path_index]

    src_x, src_y = path_to_mutation.get_source_point()
    dst_x, dst_y = path_to_mutation.get_destination_point()
    points = [src_x, src_y, dst_x, dst_y]

    paths[path_index] = create_random_path(points, board.get_width(), board.get_height())
