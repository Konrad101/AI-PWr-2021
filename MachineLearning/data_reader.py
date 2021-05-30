def get_representation_data(file_extension: str):
    directory_beginning = f'data/{file_extension}'
    rating_prefix = 'label.4class'
    subj_prefix = 'subj'
    ratings = __get_file_data(f'{directory_beginning}/{rating_prefix}.{file_extension}')
    reviews = __get_file_data(f'{directory_beginning}/{subj_prefix}.{file_extension}')
    if len(ratings) != len(reviews):
        raise Exception('Wrong ratings or reviews count in data set.')

    representation_data = []
    for i in range(0, len(reviews)):
        representation_data.append((reviews[i], float(ratings[i])))
    return representation_data


def __get_file_data(filename: str):
    file_lines = []
    file = open(filename, "r")
    for line in file:
        file_lines.append(line.replace('\n', ''))
    return file_lines
