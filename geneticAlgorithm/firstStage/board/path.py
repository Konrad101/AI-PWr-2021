from board.segment import Direction


class Path:
    # segments - tablica segmentow
    def __init__(self, src_x, src_y, dst_x, dst_y, segments):
        self.__source_point_x = src_x
        self.__source_point_y = src_y
        self.__destination_point_x = dst_x
        self.__destination_point_y = dst_y

        self.__segments = segments

    def get_length(self):
        length = 0
        for segment in self.__segments:
            length += segment.length
        return length

    def get_source_point(self):
        return self.__source_point_x, self.__source_point_y

    def get_destination_point(self):
        return self.__destination_point_x, self.__destination_point_y

    def get_segments(self):
        return self.__segments

    def set_segments(self, segments):
        self.__segments = segments

    def get_occupied_fields(self):
        occupied_fields = []
        for segment in self.__segments:
            # iteruje pomijajac poczatek segmentu zeby uniknac powtorzen
            current_x = segment.initial_x
            current_y = segment.initial_y
            occupied_fields.append((current_x, current_y))
            length = segment.length
            # jezeli nie jest to ostatni segment
            if segment != self.__segments[len(self.__segments) - 1]:
                length -= 1
            for i in range(0, length):
                if segment.direction == Direction.up:
                    current_y -= 1
                elif segment.direction == Direction.down:
                    current_y += 1
                elif segment.direction == Direction.right:
                    current_x += 1
                else:
                    current_x -= 1
                occupied_fields.append((current_x, current_y))

        return occupied_fields
