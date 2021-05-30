import statistics

from text_analyzer import is_word

WORDS_TO_PRINT_AMOUNT = 10
MIN_RATING = 0.
MAX_RATING = 1.


def print_least_used_words(counted_reviews_words):
    print('\nLeast used words:')
    counted_reviews_words = {k: v for k, v in sorted(counted_reviews_words.items(), key=lambda item: item[1])}
    __print_words(counted_reviews_words)


def print_most_used_words(counted_reviews_words):
    print('\nMost used words:')
    __print_words(counted_reviews_words)


def __print_words(counted_reviews_words, words_amount=WORDS_TO_PRINT_AMOUNT):
    printed_words = 0
    for word_with_count in counted_reviews_words.items():
        print(f'{word_with_count[0]}: {word_with_count[1]}')
        printed_words += 1
        if printed_words == words_amount:
            break


def print_reviews_statistics(reviews):
    reviews_amount = []
    for review in reviews:
        review_length = 0
        for word in review.split():
            if is_word(word):
                review_length += 1
        reviews_amount.append(review_length)

    avg = sum(reviews_amount) / len(reviews_amount)
    median = statistics.median(reviews_amount)
    max_amount = max(reviews_amount)
    min_amount = min(reviews_amount)
    print('\nReviews statistics:')

    print('Average:', avg)
    print('Median:', median)
    print('Max:', max_amount)
    print('Min:', min_amount)


def print_counted_classes(classes):
    classes_amount = {MIN_RATING: 0, MAX_RATING: 0}
    for review_class in classes:
        if review_class in classes_amount:
            classes_amount[review_class] += 1
        else:
            classes_amount[review_class] = 1

    classes_amount = {k: v for k, v in sorted(classes_amount.items(), key=lambda item: item[0])}
    print('\nClasses occurrence frequency')
    for review_class_amount in classes_amount.items():
        print(f'{review_class_amount[0]}: {review_class_amount[1]}')
