from copy import copy

from board.board import PCBBoard


def crossover_operator(first_parent, second_parent):
    first_parent_paths = first_parent.get_paths()
    second_parent_paths = second_parent.get_paths()

    child_paths = []
    for i in range(0, len(first_parent_paths)):
        if i % 2 == 0:
            child_paths.append(copy(first_parent_paths[i]))
        else:
            child_paths.append(copy(second_parent_paths[i]))
    child = PCBBoard(first_parent.get_width(), first_parent.get_height())
    for path in child_paths:
        child.add_connected_points(path)
    return child
