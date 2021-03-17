from board.board import PCBBoard
from board.path import Path
from board.segment import Segment, Direction


def get_population_from_file(filename):
    population = []

    f = open("populations/" + filename, "r")
    for row in f:
        if row.replace('\n', '') == "BOARD":
            board_size = f.readline().replace('\n', '').split(';')
            width = int(board_size[0])
            height = int(board_size[1])
            board = PCBBoard(width, height)

            while True:
                line = f.readline()
                if line.__contains__("END"):
                    break
                path_points = line.replace('\n', '').split(';')
                src_x = int(path_points[0])
                src_y = int(path_points[1])
                dst_x = int(path_points[2])
                dst_y = int(path_points[3])

                segments = f.readline().replace('\n', '').split('|')
                path_segments = []
                for s in segments:
                    segment_data = s.split(';')
                    length = int(segment_data[0])
                    direction = Direction(int(segment_data[1]))
                    initial_x = int(segment_data[2])
                    initial_y = int(segment_data[3])
                    path_segments.append(Segment(length, direction, initial_x, initial_y))

                board.add_connected_points(Path(src_x, src_y, dst_x, dst_y, path_segments))
            population.append(board)

    return population
# jaka struktura?
# 5;5 - wielkosc plytki
# 1;1;1;1 punkty poczatek i koniec
# 2;1;2;3| - segmenty - dlugosc, kierunek, poczatek x, pocztek y
# segmenty punktow np. 1;1 2;1 2;2
# itd
