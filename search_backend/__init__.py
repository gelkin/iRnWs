import os

from nltk import RegexpTokenizer, defaultdict


def search(query_string):
    result_list = []

    for i in range(10):
        result_list.append({
            'title': 'Dummy title for result #{} of query “{}”'.format(i + 1, query_string),
            'snippet': 'Dummy snippet',
            'href': 'http://www.example.com'
        })

    return result_list


def my_search(query_string):
    arg_tokens = prepare_arguments(query_string)


def prepare_arguments(query_string):
    tokens = query_string.split()




def get_all_docs(path):
    docs = sorted([os.path.join(dp, f) for dp, dn, fn in os.walk(path) for f in fn])
    print(len(docs))
    print(docs)


# todo make index - defaultdict(list)
# todo do we need to return 'index' or it's just updated by link
def add_doc_to_index(index: defaultdict, doc: str, doc_id: int, stop_words: set):
    doc = doc.lower()
    tokens = doc.split()
    cnt = 1
    for token in tokens:
        if token not in stop_words:
            index[token] = index[token].append((doc_id, cnt))
        cnt += 1


