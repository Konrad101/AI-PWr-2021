import sklearn
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC

DEFAULT_CROSS_VALIDATION = 10

# classifier = SVC(kernel='linear')
# classifier = SVC(kernel='rbf')
classifier = MultinomialNB(alpha=0.01)


def hyperparameter_optimization(reviews_train_data, rates_train_data, param_grid,
                                cross_validation=DEFAULT_CROSS_VALIDATION):
    # split data to train set and test set
    train_set, test_set, y_train, y_test = train_test_split(reviews_train_data, rates_train_data,
                                                            test_size=0.3, random_state=0)
    # test_size - set size in % when float, when int then fixed value
    # train_size - train set size - j.w. + przy braku bierze wartosc test_size

    text_classifier = Pipeline([
        ('vect', TfidfVectorizer()),
        ('clf', MultinomialNB()),
    ])
    grid_search_classifier = GridSearchCV(text_classifier, param_grid, cv=cross_validation, n_jobs=-1)
    grid_search_classifier = grid_search_classifier.fit(train_set, y_train)

    print(f"Best score: {grid_search_classifier.best_score_}")
    print(f"Best parameters: {grid_search_classifier.best_params_}")
    print(f"Average score: {grid_search_classifier.cv_results_['mean_test_score']}")

    for param_name in sorted(param_grid.keys()):
        print(f'{param_name}: {grid_search_classifier.best_params_[param_name]}')


def train_and_test(reviews_train_data, rates_train_data, reviews_test_data, rates_test_data,
                   cross_validation=DEFAULT_CROSS_VALIDATION):
    vectorizer = TfidfVectorizer(min_df=2, max_df=0.95, ngram_range=(2, 3), max_features=4000)

    # split data to train set and test set
    train_set, test_set, y_train, y_test = train_test_split(reviews_train_data, rates_train_data,
                                                            test_size=0.2, train_size=0.25, random_state=42)

    docs_train_counts = vectorizer.fit_transform(train_set)

    transformer = TfidfTransformer()
    train_set_tfidf = transformer.fit_transform(docs_train_counts)
    test_set_tfidf = transformer.transform(vectorizer.transform(test_set))

    classifier.fit(train_set_tfidf, y_train)

    y_prediction = classifier.predict(test_set_tfidf)
    print("\nAccuracy score of test data:")
    print(sklearn.metrics.accuracy_score(y_test, y_prediction))

    text_classifier = Pipeline([
        ('vect', vectorizer),
        ('clf', classifier),
    ])

    cv_score = cross_val_score(text_classifier, reviews_train_data, rates_train_data, cv=cross_validation)
    print(f'\nCross validation scores: {cv_score}')

    reviews_counts = vectorizer.transform(reviews_test_data)
    reviews_tfidf = transformer.transform(reviews_counts)
    test_prediction(reviews_test_data, rates_test_data, reviews_tfidf)


def test_prediction(reviews_test_data, rates_test_data, reviews_tfidf):
    prediction = classifier.predict(reviews_tfidf)

    print('\nPrediction test:')
    for real_rate, predicted_rate, review in zip(rates_test_data, prediction, reviews_test_data):
        print(f'real rate: {real_rate}, prediction: {predicted_rate}, review text: {review}')
