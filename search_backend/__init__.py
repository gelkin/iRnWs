import os

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


class Index:
    def __init__(self, path, stopwords):
        self.index = Index.build_index(path, stopwords)
        self.stopwords = stopwords

    def __getitem__(self, item):
        return self.index[item]

    @staticmethod
    def build_index(path, stopwords):
        docs = get_all_docs(path)
        print(sorted(docs))
        index = defaultdict(list)
        stemmer = PorterStemmer()
        for doc_id, doc_name in enumerate(docs):
            with open(doc_name) as f:
                doc_text = f.read()
                Index.add_doc_to_index(index, doc_text, doc_id, stopwords, stemmer)
        return index

    @staticmethod
    def add_doc_to_index(index: defaultdict, doc_text: str, doc_id: int, stopwords: set, stemmer):
        doc_text = doc_text.lower()
        tokens = doc_text.split()
        cnt = 0
        for token in tokens:
            token = re.sub('\W+', '', token)
            if not token:
                continue
            token = stemmer.stem(token)
            if token not in stopwords:
                index[token].append((doc_id, cnt))
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

    def AND_boolean_search(self, query):
        args = prepare_arguments(query, stopwords=self.stopwords)
        # check if all the args are there

        for arg in args:
            if arg not in self.index:
                return []
        arg_ind_min = min(range(len(args)), key=lambda pos: self[args[pos]])
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
            if is_acc:
                acc_docs.add(doc_id)
            else:
                rej_docs.add(doc_id)
        return acc_docs

    def OR_boolean_search(self, query):
        args = prepare_arguments(query, stopwords=self.stopwords)
        acc_docs = set()
        for arg in args:
            acc_docs |= {doc_id for doc_id, _ in self[arg]}
        return acc_docs

    def next_phrase(self, terms, pos=(-1, -1)):
        v = pos
        doc_id = v[1]
        for term in terms:
            v = self.next(term, v)
            if v is None or v[1] != doc_id:
                return None
        u = v
        for term in reversed(terms[:-1]):
            u = self.prev(term, u)
        if v - u == len(terms) - 1:
            return u, v
        else:
            return self.next_phrase(terms, u)

