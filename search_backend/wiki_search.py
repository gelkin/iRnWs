import numpy as np
import pickle
import rethinkdb as r

from put_wiki_in_rethinkdb import table_name, DOC_ID, DOC_TITLE, DOC_TEXT
from read_wiki import read_wiki_index_from_pkl
from search_backend import prepare_arguments_eng_stopwords
from search_backend.build_features import get_features_vector
from search_backend.paragraph_ranking import get_best_paragraph


def load_cls(filename):
    with open(filename, 'rb') as fin:
        pkl_bst = pickle.load(fin)
    return pkl_bst


class WikiSearch:
    search_engine = None

    @staticmethod
    def get_search_engine():
        if WikiSearch.search_engine is None:
            WikiSearch.search_engine = WikiSearch()
            WikiSearch.search_engine.__init()
        return WikiSearch.search_engine

    def __init(self):
        # load classifier
        path = '/home/gelkin/harbour.space/classes/Web_Search/iRnWs/res/'
        model_filename = 'model.pkl'
        self.pkl_bst = load_cls(path + model_filename)
        # load index
        index_filename = 'wiki_index.pkl'
        self.index = read_wiki_index_from_pkl(path + index_filename)

    def raw_search(self, query, max_docs_n=20):
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
        # doc_text_best_paragraphs = []
        for _, doc_id in doc_id_with_ranks:
            res = r.table(table_name).get_all(int(doc_id), index=DOC_ID).run()
            res = next(res, None)
            assert res is not None
            doc_title = res[DOC_TITLE]
            doc_text = res[DOC_TEXT]
            # best_paragraph = get_best_paragraph(doc_text)
            doc_titles.append(doc_title)
            # doc_text_best_paragraphs.append(best_paragraph)
        return doc_titles
            # , doc_text_best_paragraphs

    def search(self, query):
        doc_titles = self.raw_search(query)
        result_list = [{'title': "TYPE OF SEARCH", 'snippet': 'SNIPPET', 'href': "fuu"}]
        for title in doc_titles:
            result_list.append(
                {
                    'title': title,
                    'snippet': "NO SNIPPET",
                    'href': "fuu"
                }
            )
        return result_list



