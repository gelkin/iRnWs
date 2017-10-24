import search_backend


python_docs_base_path = './res/python-3.6.3-docs-text'
path_to_index = './res/python_lib_index.pkl'
# serialize_index(python_docs_base_path, path_to_index)
index = search_backend.read_index(path_to_index)
# query = "These documents are generated when function"
query = "Drake bpython"
args = search_backend.prepare_arguments(query, stopwords=index.stopwords)
# # todo: fix, now it returns None but should return smth as it's in the about.txt document
res = index.OR_boolean_search(args)
print(res)

# res = (-1, -1), (-1, -1)
# set_one = set()
# while res is not None:
#     set_one.add(res)
#     if res is not None:
#         print("pos = {}, document name = {}".format(res, index.docs[res[0][0]]))
