from learning import train_and_test

# parameters = {
#         'vect__ngram_range': [(1, 1), (1, 2), (2, 3)],
#         'vect__min_df': [2, 1, 0.2],
#         'vect__max_df': [0.95, 0.7, 0.55],
#     }

default_min_df = 2
default_max_df = 0.95
default_n_gram = (2, 3)
default_alpha = 0.1
default_max_features = 4000
classifier_name = 'MultinomialNB'


def test_hyper_parameters(reviews_data, rates_data):
    # min_df
    run_parameters_test(reviews_data, rates_data, classifier_name, 2, default_max_df, default_n_gram,
                        default_alpha, default_max_features, 'min df')

    run_parameters_test(reviews_data, rates_data, classifier_name, 1, default_max_df, default_n_gram,
                        default_alpha, default_max_features, 'min df')

    run_parameters_test(reviews_data, rates_data, classifier_name, 0.2, default_max_df, default_n_gram,
                        default_alpha, default_max_features, 'min df')

    run_parameters_test(reviews_data, rates_data, classifier_name, 0.4, default_max_df, default_n_gram,
                        default_alpha, default_max_features, 'min df')

    # max_df
    run_parameters_test(reviews_data, rates_data, classifier_name, default_min_df, 0.95, default_n_gram,
                        default_alpha, default_max_features, 'max df')

    run_parameters_test(reviews_data, rates_data, classifier_name, default_min_df, 0.7, default_n_gram,
                        default_alpha, default_max_features, 'max df')

    run_parameters_test(reviews_data, rates_data, classifier_name, default_min_df, 0.6, default_n_gram,
                        default_alpha, default_max_features, 'max df')

    run_parameters_test(reviews_data, rates_data, classifier_name, default_min_df, 0.45, default_n_gram,
                        default_alpha, default_max_features, 'max df')

    # ngram
    run_parameters_test(reviews_data, rates_data, classifier_name, default_min_df, default_max_df, (1, 1),
                        default_alpha, default_max_features, 'ngram')

    run_parameters_test(reviews_data, rates_data, classifier_name, default_min_df, default_max_df, (1, 2),
                        default_alpha, default_max_features, 'ngram')

    run_parameters_test(reviews_data, rates_data, classifier_name, default_min_df, default_max_df, (2, 3),
                        default_alpha, default_max_features, 'ngram')

    run_parameters_test(reviews_data, rates_data, classifier_name, default_min_df, default_max_df, (2, 4),
                        default_alpha, default_max_features, 'ngram')

    # alpha
    run_parameters_test(reviews_data, rates_data, classifier_name, default_min_df, default_max_df, default_n_gram,
                        0.9, default_max_features, 'alpha')

    run_parameters_test(reviews_data, rates_data, classifier_name, default_min_df, default_max_df, default_n_gram,
                        0.1, default_max_features, 'alpha')

    run_parameters_test(reviews_data, rates_data, classifier_name, default_min_df, default_max_df, default_n_gram,
                        0.05, default_max_features, 'alpha')

    run_parameters_test(reviews_data, rates_data, classifier_name, default_min_df, default_max_df, default_n_gram,
                        0.01, default_max_features, 'alpha')


def run_parameters_test(reviews, rates, classifier, min_df, max_df, n_gram, alpha, max_features, test_type):
    print('\n', classifier, f'{test_type} test')
    print(f'min_df: {min_df} | max_df: {max_df} | ngram: {n_gram} | alpha: {alpha} '
          f'| max_features: {max_features} ')
    print('f1 score:', train_and_test(reviews, rates,
                                      min_df=min_df, max_df=max_df, ngram_range=n_gram,
                                      alpha=alpha, clf=classifier, max_features=max_features))


def test_classifiers(reviews_data, rates_data):
    # MultinomialNB
    print(classifier_name)
    print(f'\nmin_df: {default_min_df} | max_df: {default_max_df} | ngram: {default_n_gram} | alpha: {default_alpha} '
          f'| max_features: {default_max_features}')
    print('f1 score:', train_and_test(reviews_data, rates_data,
                                      min_df=default_min_df, max_df=default_max_df, ngram_range=default_n_gram,
                                      alpha=default_alpha, clf=classifier_name, max_features=default_max_features))

    # SVC_linear
    classifier = 'SVC_linear'
    print('\n', classifier)
    print(f'min_df: {default_min_df} | max_df: {default_max_df} | ngram: {default_n_gram} | alpha: {default_alpha} '
          f'| max_features: {default_max_features}')
    print('f1 score:', train_and_test(reviews_data, rates_data,
                                      min_df=default_min_df, max_df=default_max_df, ngram_range=default_n_gram,
                                      alpha=default_alpha, clf=classifier, max_features=default_max_features))

    # SVC_rbf
    classifier = 'SVC_rbf'
    print('\n', classifier)
    print(f'min_df: {default_min_df} | max_df: {default_max_df} | ngram: {default_n_gram} | alpha: {default_alpha} '
          f'| max_features: {default_max_features}')
    print('f1 score:', train_and_test(reviews_data, rates_data,
                                      min_df=default_min_df, max_df=default_max_df, ngram_range=default_n_gram,
                                      alpha=default_alpha, clf=classifier, max_features=default_max_features))


def compare_classes_amount(reviews_data, rates_data):
    less_classes_reviews, less_classes_rates = split_by_rates(reviews_data, rates_data)
    print('two classes:')
    print('f1 score:', train_and_test(less_classes_reviews, less_classes_rates,
                                      min_df=default_min_df, max_df=default_max_df, ngram_range=default_n_gram,
                                      alpha=default_alpha, clf=classifier_name, max_features=default_max_features))

    print('four classes:')
    print('f1 score:', train_and_test(reviews_data, rates_data,
                                      min_df=default_min_df, max_df=default_max_df, ngram_range=default_n_gram,
                                      alpha=default_alpha, clf=classifier_name, max_features=default_max_features))


def split_by_rates(reviews_data, rates_data):
    two_classes_reviews = []
    two_classes_rates = []
    for i in range(0, len(rates_data)):
        if rates_data[i] == 0:
            two_classes_reviews.append(reviews_data[i])
            two_classes_rates.append(0)
        elif rates_data[i] == 3:
            two_classes_reviews.append(reviews_data[i])
            two_classes_rates.append(1)

    return two_classes_reviews, two_classes_rates


def test_tuning(reviews_data, rates_data):
    print('Before:')
    print('f1 score:', train_and_test(reviews_data, rates_data,
                                      min_df=default_min_df, max_df=default_max_df, ngram_range=default_n_gram,
                                      alpha=default_alpha, clf=classifier_name, max_features=default_max_features))

    print('After:')
    print('f1 score:', train_and_test(reviews_data, rates_data,
                                      min_df=2, max_df=0.6, ngram_range=(1, 2),
                                      alpha=0.01, clf=classifier_name, max_features=default_max_features))


def test_size_and_random_state(reviews_data, rates_data):
    default_test_size = 0.2
    default_train_size = 0.25
    default_random_state = 40
    print('test_size')
    print('f1 score:', train_and_test(reviews_data, rates_data, test_size=0.1, train_size=default_train_size,
                                      random_state=default_random_state))

    print('test_size')
    print('f1 score:', train_and_test(reviews_data, rates_data, test_size=0.2, train_size=default_train_size,
                                      random_state=default_random_state))

    print('test_size')
    print('f1 score:', train_and_test(reviews_data, rates_data, test_size=0.3, train_size=default_train_size,
                                      random_state=default_random_state))

    print('train_size')
    print('f1 score:', train_and_test(reviews_data, rates_data, test_size=default_test_size,
                                      train_size=0.1, random_state=default_random_state))

    print('train_size')
    print('f1 score:', train_and_test(reviews_data, rates_data, test_size=default_test_size,
                                      train_size=0.2, random_state=default_random_state))

    print('train_size')
    print('f1 score:', train_and_test(reviews_data, rates_data, test_size=default_test_size,
                                      train_size=0.3, random_state=default_random_state))

    print('random_state')
    print('f1 score:', train_and_test(reviews_data, rates_data, test_size=default_test_size,
                                      train_size=default_train_size, random_state=5))

    print('random_state')
    print('f1 score:', train_and_test(reviews_data, rates_data, test_size=default_test_size,
                                      train_size=default_train_size, random_state=15))

    print('random_state')
    print('f1 score:', train_and_test(reviews_data, rates_data, test_size=default_test_size,
                                      train_size=default_train_size, random_state=25))
