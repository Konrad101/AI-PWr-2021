from random import Random

from board import PCBBoard, Path


def generate_random_population(population_size, board_width, board_height, board_points):
    random_population = []
    for i in range(population_size):
        board = PCBBoard(board_width, board_height)
        for points in board_points:
            points_pair = create_random_path(points, board_width, board_height)
            board.add_connected_points(points_pair)
        random_population.append(board)
    return random_population


def create_random_path(points, board_width, board_height):
    connection_points = []

    completed_path = False
    current_x = points[0]
    current_y = points[1]
    while not completed_path:
        possible_points = []
        if current_x > 1:
            possible_points.append((current_x - 1, current_y))
        if current_y > 1:
            possible_points.append((current_x, current_y - 1))
        if current_x < board_width:
            possible_points.append((current_x + 1, current_y))
        if current_y < board_height:
            possible_points.append((current_x, current_y + 1))

        random_point = get_random_point(possible_points)
        connection_points.append((random_point[0], random_point[1]))
        if reached_finish(random_point[0], random_point[1], points[2], points[3]):
            completed_path = True

        current_x = random_point[0]
        current_y = random_point[1]

    return Path(points[0], points[1], points[2], points[3], connection_points)


def get_random_point(possible_points):
    return possible_points[Random().randint(0, len(possible_points) - 1)]


def reached_finish(x1, y1, x2, y2):
    reached = False
    if x1 == x2 and abs(y1 - y2) <= 1:
        reached = True
    elif y1 == y2 and abs(x1 - x2) <= 1:
        reached = True

    return reached
