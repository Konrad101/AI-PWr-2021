def get_reviews_from_data_set(data_set):
    reviews = []
    for data in data_set:
        reviews.append(data[0])
    return reviews


def get_ratings_from_data_set(data_set):
    ratings = []
    for data in data_set:
        ratings.append(data[1])
    return ratings
