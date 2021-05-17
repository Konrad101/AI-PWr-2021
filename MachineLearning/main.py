from data_modifier import get_reviews_from_data_set, get_ratings_from_data_set
from data_reader import get_representation_data
from exploratory_analysis import print_least_used_words, print_most_used_words, print_reviews_statistics, \
    print_counted_classes
from text_analyzer import count_reviews_words


def analyze():
    data_set = get_representation_data('Steve+Rhodes')
    reviews = get_reviews_from_data_set(data_set)

    counted_words = count_reviews_words(reviews)
    print_most_used_words(counted_words)
    print_least_used_words(counted_words)

    print_reviews_statistics(reviews)
    print_counted_classes(get_ratings_from_data_set(data_set))


if __name__ == '__main__':
    analyze()
