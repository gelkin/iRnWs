import datetime
import rethinkdb as r
from itertools import islice

import read_wiki
from read_wiki import readPages
from search_backend import prepare_arguments_eng_stopwords

r.connect("localhost", 28015).repl()
table_name = 'wiki_docs'
DOC_ID = 'doc_id'
DOC_TITLE = 'doc_title'
DOC_TEXT = 'doc_text'


def create_db_if_not_exist():
    r.connect("localhost", 28015).repl()
    if table_name in r.table_list().run():
        return
    r.table_create(table_name).run()
    r.table(table_name).index_create(DOC_ID).run()
    r.table(table_name).index_wait(DOC_ID).run()


def load_wiki_to_db(docs_number=5000):
    create_db_if_not_exist()
    docs_iter = islice(readPages(read_wiki.path + read_wiki.filename), docs_number)
    cnt = 1
    time_beginning = datetime.datetime.now()
    for doc_id, doc_title, doc_text in docs_iter:
        # doc_title_prepared = prepare_arguments_eng_stopwords(doc_title)
        # doc_text_prepared = prepare_arguments_eng_stopwords(doc_text)
        r.table(table_name).insert(
            {
                DOC_ID: int(doc_id),
                DOC_TITLE: doc_title,
                DOC_TEXT: doc_text
            }
        ).run()
        print("processed: {}/{}".format(cnt, docs_number))
        cnt += 1
        if cnt % 10 == 0:
            time_diff = datetime.datetime.now() - time_beginning
            print("time passed: " + "{}:{}".format(time_diff.seconds // 60, time_diff.seconds % 60))


# load_wiki_to_db()

