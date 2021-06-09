from data_modifier import get_reviews_from_data_set, get_ratings_from_data_set
from data_reader import get_representation_data
from exploratory_analysis import print_least_used_words, print_most_used_words, print_reviews_statistics, \
    print_counted_classes, extraction
from learning import hyperparameter_optimization, train_and_test
from text_analyzer import count_reviews_words

AVAILABLE_DATA_DIRECTORIES = ['Dennis+Schwartz', 'James+Berardinelli', 'Scott+Renshaw', 'Steve+Rhodes']


def basic_analyze():
    data_set = []
    for data_directory in AVAILABLE_DATA_DIRECTORIES:
        data_set += get_representation_data(data_directory)

    reviews = get_reviews_from_data_set(data_set)

    counted_words = count_reviews_words(reviews)
    print_most_used_words(counted_words)
    print_least_used_words(counted_words)

    print_reviews_statistics(reviews)
    print_counted_classes(get_ratings_from_data_set(data_set))

    extraction(reviews)


def learn_model():
    test_data_set = get_representation_data(AVAILABLE_DATA_DIRECTORIES[3])
    prediction_data_set = get_representation_data(AVAILABLE_DATA_DIRECTORIES[3])

    train_reviews = get_reviews_from_data_set(test_data_set)
    train_ratings = get_ratings_from_data_set(test_data_set)
    prediction_reviews = get_reviews_from_data_set(prediction_data_set)
    prediction_ratings = get_ratings_from_data_set(prediction_data_set)

    # optimize_parameters(train_reviews, train_ratings)
    train_and_test(train_reviews, train_ratings, prediction_reviews, prediction_ratings)


def optimize_parameters(reviews, ratings):
    parameters = {
        'vect__ngram_range': [(1, 1), (1, 2), (2, 3)],
        'vect__min_df': [2, 1, 0.2, 0.4],
        'vect__max_df': [0.95, 0.7, 0.6, 0.45],
        'clf__alpha': (0.9, 0.1, 0.01),
    }
    hyperparameter_optimization(reviews, ratings, parameters)


if __name__ == '__main__':
    learn_model()
