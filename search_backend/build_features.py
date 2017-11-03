from statistics import mean, variance

from nltk import RegexpTokenizer, defaultdict, re
from nltk.stem.porter import *

from search_backend import get_english_stopwords, prepare_arguments

stemmer = PorterStemmer()
stopwords = get_english_stopwords()


def get_features_vector(query_prepared, doc_text, doc_title):
    query_prepared_set = set(query_prepared)
    text_prepared_list = prepare_arguments(doc_text, stopwords)
    title_prepared_list = prepare_arguments(doc_title, stopwords)
    title_prepared_set = set(title_prepared_list)
    # feature initialization
    features = [0] * 24
    features[0] = covered_query_term_number(query_prepared_set, title_prepared_set)
    features[1] = covered_query_term_ratio(query_prepared_set, title_prepared_set)
    # get_stream_length
    text_stream_length = get_stream_length(text_prepared_list)
    title_stream_length = get_stream_length(title_prepared_list)
    features[2] = text_stream_length
    features[3] = title_stream_length
    # freqs:
    text_freqs = get_term_frequency(query_prepared_set, text_prepared_list)
    title_freqs = get_term_frequency(query_prepared_set, title_prepared_list)
    # sum_of_term_frequency
    features[4] = sum_of_term_frequency(text_freqs)
    features[5] = sum_of_term_frequency(title_freqs)
    # min_of_term_frequency
    features[6] = min_of_term_frequency(text_freqs)
    features[7] = min_of_term_frequency(title_freqs)
    # max_of_term_frequency
    features[8] = max_of_term_frequency(text_freqs)
    features[9] = max_of_term_frequency(title_freqs)
    # mean_of_term_frequency
    features[10] = mean_of_term_frequency(text_freqs)
    features[11] = mean_of_term_frequency(title_freqs)
    # variance_of_term_frequency
    features[12] = variance_of_term_frequency(text_freqs)
    features[13] = variance_of_term_frequency(title_freqs)
    # sum_of_stream_length_normalized_term_frequency
    features[14] = sum_of_stream_length_normalized_term_frequency(text_freqs, text_stream_length)
    features[15] = sum_of_stream_length_normalized_term_frequency(title_freqs, title_stream_length)
    # min_of_stream_length_normalized_term_frequency
    features[16] = min_of_stream_length_normalized_term_frequency(text_freqs, text_stream_length)
    features[17] = min_of_stream_length_normalized_term_frequency(title_freqs, title_stream_length)
    # max_of_stream_length_normalized_term_frequency
    features[18] = max_of_stream_length_normalized_term_frequency(text_freqs, text_stream_length)
    features[19] = max_of_stream_length_normalized_term_frequency(title_freqs, title_stream_length)
    # mean_of_stream_length_normalized_term_frequency
    features[20] = mean_of_stream_length_normalized_term_frequency(text_freqs, text_stream_length)
    features[21] = mean_of_stream_length_normalized_term_frequency(title_freqs, title_stream_length)
    # variance_of_stream_length_normalized_term_frequency
    features[22] = variance_of_stream_length_normalized_term_frequency(text_freqs, text_stream_length)
    features[23] = variance_of_stream_length_normalized_term_frequency(title_freqs, title_stream_length)
    return features


# 0
def covered_query_term_number(query_prepared_set: set, title_prepared_set: set):
    return len(query_prepared_set & title_prepared_set)


# 1
def covered_query_term_ratio(query_prepared_set: set, title_prepared_set: set):
    return covered_query_term_number(query_prepared_set, title_prepared_set) / len(query_prepared_set)


# 2, 3
def get_stream_length(words):
    return len(words)


def get_term_frequency(query_prepared_set: set, text_prepared: list):
    freqs = {word: 0 for word in query_prepared_set}
    for word in text_prepared:
        if word in freqs:
            freqs[word] += 1
    return freqs


# 4, 5
def sum_of_term_frequency(freqs: dict):
    return sum(freqs.values())


# 6, 7
def min_of_term_frequency(freqs: dict):
    return min(freqs.values())


# 8, 9
def max_of_term_frequency(freqs: dict):
    return max(freqs.values())


# 10, 11
def mean_of_term_frequency(freqs: dict):
    return mean(freqs.values())


# 12, 13
def variance_of_term_frequency(freqs: dict):
    if len(list(freqs.keys())) == 1:
        return 0
    return variance(freqs.values())


# 14, 15
def sum_of_stream_length_normalized_term_frequency(freqs: dict, stream_length: int):
    return sum_of_term_frequency(freqs) / stream_length


# 16, 17
def min_of_stream_length_normalized_term_frequency(freqs: dict, stream_length: int):
    return min_of_term_frequency(freqs) / stream_length


# 18, 19
def max_of_stream_length_normalized_term_frequency(freqs: dict, stream_length: int):
    return max_of_term_frequency(freqs) / stream_length


# 20, 21
def mean_of_stream_length_normalized_term_frequency(freqs: dict, stream_length: int):
    return mean_of_term_frequency(freqs) / stream_length


# 22, 23
def variance_of_stream_length_normalized_term_frequency(freqs: dict, stream_length: int):
    if len(list(freqs.keys())) == 1:
        return 0
    return variance_of_term_frequency(freqs) / stream_length
