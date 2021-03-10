def get_file_data(filename="data/population_data.txt"):
    data_separator = ';'

    f = open(filename, "r")
    first_row_data = f.readline().split(data_separator)
    width = int(first_row_data[0])
    height = int(first_row_data[1])
    points = []
    for row in f:
        row_data = row.split(data_separator)
        points.append((int(row_data[0]), int(row_data[1]),
                       int(row_data[2]), int(row_data[3])))

    return width, height, points
