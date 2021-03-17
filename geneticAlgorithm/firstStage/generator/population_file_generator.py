from board.segment import get_direction_number
from generator.random_generator import generate_random_population


def save_population_to_file(population_size, board_width, board_height, board_points):
    population = generate_random_population(population_size, board_width, board_height, board_points)
    f = open("populations/generated_population_" + str(population_size) + ".txt", "w+")
    for board in population:
        f.write("BOARD\n")
        f.write(str(board_width) + ';' + str(board_height) + '\n')
        for path in board.get_paths():
            src_x, src_y = path.get_source_point()
            dst_x, dst_y = path.get_destination_point()

            f.write(str(src_x) + ';' + str(src_y) + ';' + str(dst_x) + ';' + str(dst_y) + '\n')
            segments = path.get_segments()
            for segment in segments:
                f.write(str(segment.length) + ';' + str(get_direction_number(segment.direction)) + ';' + str(
                    segment.initial_x) + ';' + str(segment.initial_y))
                if segments.index(segment) < len(segments) - 1:
                    f.write('|')
                else:
                    f.write('\n')
        f.write("END OF BOARD\n")
    f.close()
