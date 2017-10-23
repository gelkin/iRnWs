import search_backend

docs_base_path = './res/python-3.6.3-docs-text'
english_stopword = search_backend.get_english_stopwords()
index = search_backend.Index(docs_base_path, english_stopword)
query = "These documents are generated"
args = search_backend.prepare_arguments(query, stopwords=english_stopword)
# todo: fix, now it returns None but should return smth as it's in the about.txt document
res = index.next_phrase(args)
print(res)
