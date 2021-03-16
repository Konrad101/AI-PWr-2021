import enum


class Segment:
    def __init__(self, length, direction, initial_x, initial_y):
        if length <= 0:
            raise ValueError

        self.length = length
        self.direction = direction
        self.initial_x = initial_x
        self.initial_y = initial_y

    def get_destination_point(self):
        if self.direction == Direction.up:
            return self.initial_x, self.initial_y - self.length
        elif self.direction == Direction.down:
            return self.initial_x, self.initial_y + self.length
        elif self.direction == Direction.left:
            return self.initial_x - self.length, self.initial_y
        else:
            return self.initial_x + self.length, self.initial_y


class Direction(enum.Enum):
    up = 1
    down = 2
    left = 3
    right = 4
