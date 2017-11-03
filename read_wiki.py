import bz2
import re

from itertools import islice

import datetime

import search_backend
from search_backend import IndexWiki, get_english_stopwords


def getNumArticles(filename):
    m = re.search(r'p(\d+)p(\d+)\.bz2', filename)
    if m:
        return int(m.group(2)) - int(m.group(1)) + 1
    return 0


def readPages(filename):
    with bz2.open(filename) as file:
        page_text = None
        page_title = ''
        page_id = None
        for line in file:
            line = str(line, encoding='utf-8').strip()
            if line.startswith('<title>'):
                page_title = line[len('<title>'):-len('</title>')]
            elif page_id is None and line.startswith('<id>'):
                page_id = int(line[len('<id>'):-len('</id>')])
            elif line.startswith('<text xml:space="preserve">'):
                page_text = line[len('<text xml:space="preserve">'):]
            elif line.endswith('</text>'):
                yield page_id, page_title, page_text
                page_text = None
                page_title = ''
                page_id = None
            elif page_text is not None:
                page_text += '\n' + line

path = '../data/'
filename = 'enwiki-20171020-pages-articles1.xml-p10p30302.bz2'
pkl_index_path = './res/wiki_index.pkl'


def create_wiki_index(docs_number=5000):
    # num_articles = getNumArticles(path + filename)
    # print(num_articles)
    eng_stopwords = get_english_stopwords()
    docs_iter = islice(readPages(path + filename), docs_number)
    index = IndexWiki(eng_stopwords, docs_iter, docs_number)
    search_backend.serialize_index_wiki(index, pkl_index_path)
    # print(index.titles)
    # print(index.index)


def read_wiki_index_from_pkl(filename):
    # time_beginning = datetime.datetime.now()
    index = search_backend.read_index(filename)
    # print(len(index.titles))
    # time_diff = datetime.datetime.now() - time_beginning
    # print("time passed: " + "{}:{}".format(time_diff.seconds // 60, time_diff.seconds % 60))
    return index
