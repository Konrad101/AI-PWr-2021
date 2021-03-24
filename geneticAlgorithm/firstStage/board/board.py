import time

from generator.generator_constants import MIN_BOARD_X, MIN_BOARD_Y

LENGTH_FACTOR = 0.24
INTERSECTION_FACTOR = 5.4
SEGMENTS_FACTOR = 1.85
SEGMENTS_OVER_BOARD_FACTOR = 4.2


class PCBBoard:
    # plytka przechowuje rozmiar 1 boku i tablice punktow razem z x i y polaczen
    # points - tablica obiektow PointsPair
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__paths = []

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def get_total_length(self):
        if len(self.__paths) > 0:
            total_length = 0
            for points_pair in self.__paths:
                total_length += points_pair.get_length()
            return total_length

        return 0

    def get_paths(self):
        return self.__paths

    def add_connected_points(self, connected_points):
        self.__paths.append(connected_points)

    def evaluate_board(self, print_info=True):
        length = self.get_total_length()
        intersections_amount = self.get_intersections_amount()
        segments_amount = self.__count_segments_amount()
        segments_over_board_amount = self.count_segments_over_board()

        if print_info:
            print("Length:", length)
            print("Intersections:", intersections_amount)
            print("Segments:", segments_amount)
            print("Segments over board:", segments_over_board_amount)
            if intersections_amount == 0:
                self.print_board()

        quality = length * LENGTH_FACTOR
        quality += intersections_amount * INTERSECTION_FACTOR
        quality += segments_amount * SEGMENTS_FACTOR
        quality += segments_over_board_amount * SEGMENTS_OVER_BOARD_FACTOR

        return quality

    def get_intersections_amount(self):
        occupied_points = {}
        intersections_amount = 0

        # jesli jest okupowane to dodaje 1
        for points_pair in self.__paths:
            occupied_fields = points_pair.get_occupied_fields()
            for field in occupied_fields:
                # jezeli jest wiecej polaczen w 1 polu niz 1 to naliczaj przeciecia
                if (field[0], field[1]) in occupied_points:
                    intersections_amount += 1
                else:
                    occupied_points[(field[0], field[1])] = 1

        return intersections_amount

    def __count_segments_amount(self):
        segments_amount = 0
        for path in self.__paths:
            segments_amount += len(path.get_segments())
        return segments_amount

    def count_segments_over_board(self):
        segments_over_board = 0

        # jezeli poczatek segmentu lub koniec jest poza mapa to naliczaj
        for path in self.__paths:
            segments = path.get_segments()
            for segment in segments:
                segment_x_dst, segment_y_dst = segment.get_destination_point()
                if segment.initial_x < MIN_BOARD_X or segment.initial_y < MIN_BOARD_Y \
                        or segment_x_dst < MIN_BOARD_X or segment_y_dst < MIN_BOARD_Y\
                        or segment.initial_x > self.__width or segment.initial_y > self.__height\
                        or segment_x_dst > self.__width or segment_y_dst > self.__height:
                    segments_over_board += 1

        return segments_over_board

    def print_board(self):
        if self.get_intersections_amount() > 0 or self.count_segments_over_board() > 0:
            return
        board_imitation = []
        for i in range(0, self.__width):
            board_imitation.append([])
            for j in range(0, self.__height):
                board_imitation[i].append(0)

        path_number = 1
        for path in self.__paths:
            occupied_fields = path.get_occupied_fields()
            for field in occupied_fields:
                # -1, poniewaz to sa wspolrzedne, a nie indexy
                board_imitation[field[1] - 1][field[0] - 1] = path_number
            path_number += 1

        for i in range(0, self.__width):
            for j in range(0, self.__height):
                print(board_imitation[i][j], "", end="")
            print()
