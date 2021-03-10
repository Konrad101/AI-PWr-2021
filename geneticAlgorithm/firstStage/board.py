LENGTH_FACTOR = 0.35
INTERSECTION_FACTOR = 2.5
SEGMENTS_FACTOR = 0.9


class PCBBoard:
    # plytka przechowuje rozmiar 1 boku i tablice punktow razem z x i y polaczen
    # points - tablica obiektow PointsPair
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__paths = []

    def get_total_length(self):
        if len(self.__paths) > 0:
            total_length = 0
            for points_pair in self.__paths:
                total_length += points_pair.get_length()
            return total_length

        return 0

    def add_connected_points(self, connected_points):
        self.__paths.append(connected_points)

    def evaluate_board(self):
        print("Length:", self.get_total_length())
        print("Intersections:", self.__get_intersections_amount())
        if self.__get_intersections_amount() == 0:
            self.print_board()
        print("Segments:", self.__count_segments_amount())

        quality = self.get_total_length() * LENGTH_FACTOR
        quality += self.__get_intersections_amount() * INTERSECTION_FACTOR
        quality = self.__count_segments_amount() * SEGMENTS_FACTOR

        return quality

    def __get_intersections_amount(self):
        board = []
        for i in range(0, self.__width):
            board.append([])
            for j in range(0, self.__height):
                board[i].append(0)
        # cala plansza to tablica tablic wypelniona 0

        # jesli jest okupowane to dodaje 1
        for points_pair in self.__paths:
            occupied_fields = points_pair.get_occupied_fields()
            for field in occupied_fields:
                # odejmuje 1, bo x, y zaczynaja sie od 1, a nie od 0 jak index
                board[field[0] - 1][field[1] - 1] += 1

        intersections_amount = 0
        # jezeli jest wiecej polaczen w 1 polu niz 1 to naliczaj przeciecia
        for i in range(0, self.__width):
            for j in range(0, self.__height):
                if board[i][j] > 1:
                    intersections_amount += 1

        return intersections_amount

    def __count_segments_amount(self):
        segments_amount = 0
        for path in self.__paths:
            last_field = None
            current_segment_is_vertical = False
            for occupied_field in path.get_occupied_fields():
                if last_field is None:
                    segments_amount += 1
                # x ten sam - horyzontalny
                elif last_field[0] == occupied_field[0]:
                    if current_segment_is_vertical:
                        current_segment_is_vertical = False
                        segments_amount += 1
                # jesli nie horyzontalny to na 100% wertykalny
                else:
                    if not current_segment_is_vertical:
                        current_segment_is_vertical = True
                        segments_amount += 1
                last_field = occupied_field
        return segments_amount

    def print_board(self):
        if self.__get_intersections_amount() > 0:
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


class Path:
    # connection fields - tablica krotek (x, y)
    def __init__(self, src_x, src_y, dst_x, dst_y, connection_fields):
        self.__source_point_x = src_x
        self.__source_point_y = src_y
        self.__destination_point_x = dst_x
        self.__destination_point_y = dst_y

        self.__connection_fields = connection_fields

    def get_length(self):
        return len(self.__connection_fields)

    def get_occupied_fields(self):
        occupied_fields = [(self.__source_point_x, self.__source_point_y)]
        occupied_fields += self.__connection_fields
        occupied_fields.append((self.__destination_point_x, self.__destination_point_y))
        return occupied_fields
