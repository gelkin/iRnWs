import os
import pickle

from nltk import RegexpTokenizer, defaultdict, re
from nltk.stem.porter import *


def search(query_string):
    result_list = []
    for i in range(10):
        result_list.append({
            'title': 'Dummy title for result #{} of query “{}”'.format(i + 1, query_string),
            'snippet': 'Dummy snippet',
            'href': 'http://www.example.com'
        })
    return result_list


def prepare_arguments(query, stopwords=set()):
    tokens = query.split()
    prepared_tokens = []
    stemmer = PorterStemmer()
    for token in tokens:
        token = re.sub('\W+', '', token)
        token = stemmer.stem(token)
        if token and token not in stopwords:
            prepared_tokens.append(token)
    return prepared_tokens


def get_english_stopwords():
    with open("./res/stopwords/english") as f:
        return set(f.read().split(','))


def get_all_docs(path):
    return sorted([os.path.join(dp, f) for dp, dn, fn in os.walk(path) for f in fn])


def serialize_index(path_to_base, path_to_index):
    with open(path_to_index, 'wb') as output:
        english_stopword = get_english_stopwords()
        index = Index(path_to_base, english_stopword)
        pickle.dump(index, output, pickle.HIGHEST_PROTOCOL)


def read_index(path_to_index):
    with open(path_to_index, 'rb') as input:
        return pickle.load(input)


class Index:
    def __init__(self, path, stopwords):
        self.stopwords = stopwords
        self.docs = get_all_docs(path)
        self.index = defaultdict(list)
        self.build_index(path)

    def __getitem__(self, item):
        return self.index[item]

    def build_index(self, path):
        stemmer = PorterStemmer()
        for doc_id, doc_name in enumerate(self.docs):
            with open(doc_name) as f:
                doc_text = f.read()
                self.add_doc_to_index(doc_text, doc_id, stemmer)

    def add_doc_to_index(self, doc_text: str, doc_id: int, stemmer):
        doc_text = doc_text.lower()
        tokens = doc_text.split()
        cnt = 0
        for token in tokens:
            token = re.sub('\W+', '', token)
            if not token:
                continue
            token = stemmer.stem(token)
            if token not in self.stopwords:
                self.index[token].append((doc_id, cnt))
                cnt += 1

    def first(self, term):
        is_empty = len(self[term]) == 0 if term in self.index else False
        if not is_empty:
            return self[term][0]

    def last(self, term):
        is_empty = len(self[term]) == 0 if term in self.index else False
        if not is_empty:
            return self[term][-1]

    def next(self, term, cur):
        if cur is None:
            return
        l = len(self[term]) if term in self.index else 0
        if l == 0 or self[term][-1] <= cur:
            return  # None
        if self[term][0] > cur:
            return self[term][0]
        return self[term][self.bin_search(term, 0, l, cur)]

    def prev(self, term, cur):
        if cur is None:
            return
        l = len(self[term]) if term in self.index else 0
        if l == 0 or self[term][0] >= cur:
            return  # None
        if self[term][-1] < cur:
            return self[term][-1]
        return self[term][self.bin_search(term, 0, l, cur, is_right=False)]

    def bin_search(self, term, left, right, cur, is_right=True):
        while right - left > 1:
            mid = (left + right) // 2
            if self[term][mid] <= cur:
                left = mid
            else:
                right = mid
        if is_right:
            return right
        else:
            if self[term][left] < cur:
                return left
            else:
                return left - 1

    def AND_boolean_search(self, args):
        # check if all the args are there
        for arg in args:
            if arg not in self.index:
                return []
        arg_ind_min = min(range(len(args)), key=lambda pos: len(self[args[pos]]))
        left_args = args[:arg_ind_min] + args[arg_ind_min + 1:]
        cand_docs = self[args[arg_ind_min]]
        acc_docs = set()
        rej_docs = set()
        for doc_id, _ in cand_docs:
            if doc_id in acc_docs or doc_id in rej_docs:
                continue
            # need to find documents that contain all the words
            is_acc = True
            for arg in left_args:
                pos = self.prev(arg, (doc_id + 1, 0))
                if pos is not None and pos[0] == doc_id:
                    continue
                else:
                    is_acc = False
                    break
            if is_acc:
                acc_docs.add(doc_id)
            else:
                rej_docs.add(doc_id)
        return acc_docs

    def OR_boolean_search(self, args):
        acc_docs = set()
        for arg in args:
            acc_docs |= {doc_id for doc_id, _ in self[arg]}
        return acc_docs

    def next_phrase(self, terms, pos=(-1, -1)):
        last_pos = pos
        cur_doc_id = -1
        for one_term in terms:
            last_pos = self.next(one_term, last_pos)
            if last_pos is None:
                return None
            if cur_doc_id == -1:
                cur_doc_id = last_pos[0]
            elif cur_doc_id != last_pos[0]:  # didn't find the phrase in current doc
                # then let's start searching from the next doc
                next_doc_pos = last_pos[0], -1
                return self.next_phrase(terms, pos=next_doc_pos)
        first_pos = last_pos
        for one_term in reversed(terms[:-1]):
            first_pos = self.prev(one_term, first_pos)
        if last_pos[1] - first_pos[1] == len(terms) - 1:
            return first_pos, last_pos
        else:
            return self.next_phrase(terms, first_pos)

