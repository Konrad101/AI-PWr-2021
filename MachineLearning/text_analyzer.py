import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')


def count_reviews_words(reviews):
    counted_reviews_words = {}
    for review in reviews:
        counted_words = get_counted_words(review)
        for word_amount in counted_words.items():
            if word_amount[0] in counted_reviews_words:
                counted_reviews_words[word_amount[0]] += word_amount[1]
            else:
                counted_reviews_words[word_amount[0]] = word_amount[1]
    counted_reviews_words = filter_stop_words(counted_reviews_words)
    return {k: v for k, v in sorted(counted_reviews_words.items(), key=lambda item: item[1], reverse=True)}


def get_counted_words(text: str):
    counted_words = {}
    words = text.split()

    for word in words:
        if word in counted_words:
            counted_words[word] += 1
        elif is_word(word):
            counted_words[word] = 1

    return counted_words


def is_word(word: str):
    for i in range(len(word)):
        if word[i].upper() < 'A' or word[i].upper() > 'Z':
            if word[i] != "'":
                return False
    return True


def filter_stop_words(words: dict):
    return {k: v for k, v in words.items() if k not in stopwords.words('english')}
