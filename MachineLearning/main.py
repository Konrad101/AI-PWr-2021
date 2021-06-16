from data_modifier import get_reviews_from_data_set, get_ratings_from_data_set
from data_reader import get_representation_data
from exploratory_analysis import print_least_used_words, print_most_used_words, print_reviews_statistics, \
    print_counted_classes, extraction
from learning import hyperparameter_optimization, train_and_test
from tests import test_hyper_parameters, test_classifiers, test_tuning, compare_classes_amount, \
    test_size_and_random_state
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
        'vect__ngram_range': [(1, 1), (1, 2), (2, 3), (2, 4)],
        'vect__min_df': [2, 1, 0.2, 0.4],
        'vect__max_df': [0.95, 0.7, 0.6, 0.45],
        'clf__alpha': [0.9, 0.1, 0.05, 0.01],
    }
    hyperparameter_optimization(reviews, ratings, parameters)


def test_parameters():
    reviews, ratings = get_all_reviews_and_ratings()
    test_classifiers(reviews, ratings)
    test_hyper_parameters(reviews, ratings)


def test_hyperparameters_tuning():
    reviews, ratings = get_all_reviews_and_ratings()
    test_tuning(reviews, ratings)


def test_different_classes():
    reviews, ratings = get_all_reviews_and_ratings()
    compare_classes_amount(reviews, ratings)


def get_all_reviews_and_ratings():
    data_set = []
    for data_directory in AVAILABLE_DATA_DIRECTORIES:
        data_set += get_representation_data(data_directory)

    train_reviews = get_reviews_from_data_set(data_set)
    train_ratings = get_ratings_from_data_set(data_set)
    return train_reviews, train_ratings


if __name__ == '__main__':
    # basic_analyze()
    # learn_model()

    reviews, ratings = get_all_reviews_and_ratings()
    test_size_and_random_state(reviews, ratings)

    test_different_classes()
    test_hyperparameters_tuning()
    test_parameters()

    reviews, ratings = get_all_reviews_and_ratings()
    optimize_parameters(reviews, ratings)
