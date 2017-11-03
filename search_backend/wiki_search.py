import lightgbm as lgb
import numpy as np
import pickle
import rethinkdb as r

from put_wiki_in_rethinkdb import table_name, DOC_ID, DOC_TITLE, DOC_TEXT
from read_wiki import read_wiki_index_from_pkl, pkl_index_path
from search_backend import prepare_arguments_eng_stopwords
from search_backend.build_features import get_features_vector


def load_cls(filename):
    with open(filename, 'rb') as fin:
        pkl_bst = pickle.load(fin)
    return pkl_bst

class WikiSearch:
    def __init__(self):
        # load classifier
        path = '/home/gelkin/harbour.space/classes/Web_Search/iRnWs/res/'
        model_filename = 'model.pkl'
        self.pkl_bst = load_cls(path + model_filename)
        # load index
        index_filename = 'wiki_index.pkl'
        self.index = read_wiki_index_from_pkl(path + index_filename)

    def search(self, query, max_docs_n=10):
        args = prepare_arguments_eng_stopwords(query)
        if not args:
            return []
        doc_ids = self.index.AND_boolean_search(args)
        r.connect("localhost", 28015).repl()
        list_of_features = []
        for doc_id in doc_ids:
            res = r.table(table_name).get_all(int(doc_id), index=DOC_ID).run()
            res = next(res, None)
            assert res is not None
            doc_title = res[DOC_TITLE]
            doc_text = res[DOC_TEXT]
            features = get_features_vector(query_prepared=args, doc_text=doc_text, doc_title=doc_title)
            list_of_features.append(features)
        if not list_of_features:
            return []
        np_array = np.array(list_of_features)
        y_pred = self.pkl_bst.predict(np_array, num_iteration=self.pkl_bst.best_iteration)
        ranks = list(y_pred)
        doc_id_with_ranks = sorted(list(zip(ranks, doc_ids)))[::-1][:max_docs_n]
        doc_titles = []
        for _, doc_id in doc_id_with_ranks:
            res = r.table(table_name).get_all(int(doc_id), index=DOC_ID).run()
            res = next(res, None)
            assert res is not None
            doc_title = res[DOC_TITLE]
            # doc_text = res[DOC_TEXT]
            doc_titles.append(doc_title)
        return doc_titles

