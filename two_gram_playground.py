import re


def get_letters_of_alphabet(text):
    return list(sorted({char for char in text}))


def get_prob_of_word_in_lang(word, probs):
    word = '$' + word + '&'
    prob = 1
    for ch_first, ch_second in zip(word[:-1], word[1:]):
        if ch_first in probs and ch_second in probs[ch_first]:
            prob *= probs[ch_first][ch_second]
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


def prepare_text(filename):
    with open(filename) as f:
        text = f.read()
        text = text.lower()
        return "".join(["$" + re.sub('\W+', '', word) + "&" for word in text.split()])

ukr_text = prepare_text("./res/ukr_tigrolovi.txt")
rus_text = prepare_text("./res/moskva_petushki.txt")

ukr_alphabet = get_letters_of_alphabet(ukr_text)
rus_alphabet = get_letters_of_alphabet(rus_text)
print(get_letters_of_alphabet(ukr_text))
print(get_letters_of_alphabet(rus_text))

ukr_probs = build_probs(ukr_text)
rus_probs = build_probs(rus_text)

word = "кур"
ukr_prob = get_prob_of_word_in_lang(word, ukr_probs)
rus_prob = get_prob_of_word_in_lang(word, rus_probs)
print(ukr_prob)
print(rus_prob)
if ukr_prob > rus_prob:
    print("Ukranian")
else:
    print("Russian")

