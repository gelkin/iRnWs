import re


def get_letters_of_alphabet(text):
    return list(sorted({char for char in text}))


def correct_two_letters_exchange(word, letter_probs):
    candidate_words = [word]
    for i in range(len(word) - 1):
        candidate_words.append(word[:i] + word[i + 1] + word[i] + word[i + 2:])
    words_probs = {}
    for candidate_word in candidate_words:
        prob = get_prob_of_word(candidate_word, letter_probs)
        words_probs[candidate_word] = prob
    return max(words_probs, key=words_probs.get)


def get_prob_of_word(word, letter_probs):
    """
    :param word:
    :param letter_probs: Map of probabilities of one letter to be followed by another one
    :return: Probability of a 'word' to be build having a probability distribution
             of one letter to be followed by another one.
    """
    word = '$' + word + '&'
    prob = 1
    for ch_first, ch_second in zip(word[:-1], word[1:]):
        if ch_first in letter_probs and ch_second in letter_probs[ch_first]:
            # conditional probability
            prob *= letter_probs[ch_first][ch_second] / sum(letter_probs[ch_first].values())
        else:
            return 0
    return prob


def build_probs(text):
    probs = {}
    for ch_first, ch_second in zip(text[:-1], text[1:]):
        if ch_first in probs:
            if ch_second in probs[ch_first]:
                probs[ch_first][ch_second] += 1
            else:
                probs[ch_first][ch_second] = 1
        else:
            probs[ch_first] = {ch_second: 1}
    # normalize
    total_number = 0
    for ch_first in probs.keys():
        for ch_second in probs[ch_first].keys():
            total_number += probs[ch_first][ch_second]
    for ch_first in probs.keys():
        for ch_second in probs[ch_first].keys():
            probs[ch_first][ch_second] /= total_number
    return probs


def prepare_text(filename, encoding='utf-8'):
    with open(filename, encoding=encoding) as f:
        text = f.read()
        text = text.lower()
        return "".join(["$" + re.sub('\W+', '', word) + "&" for word in text.split()])


def run_example_of_lang_detection(word="як"):
    ukr_text = prepare_text("./res/books/simya.txt", encoding='windows-1251')
    rus_text = prepare_text("./res/books/voina_i_mir.txt", encoding='windows-1251')
    ukr_probs = build_probs(ukr_text)
    rus_probs = build_probs(rus_text)
    ukr_prob = get_prob_of_word(word, ukr_probs)
    rus_prob = get_prob_of_word(word, rus_probs)
    print(ukr_prob)
    print(rus_prob)
    if ukr_prob > rus_prob:
        print("Ukranian")
    else:
        print("Russian")


def run_example_of_letter_exchange_typos(word='броьш'):
    rus_text = prepare_text("./res/voina_i_mir.txt", encoding='windows-1251')
    rus_probs = build_probs(rus_text)
    best_word = correct_two_letters_exchange(word, rus_probs)
    print(best_word)

run_example_of_letter_exchange_typos()


