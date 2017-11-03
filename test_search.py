import search_backend


def test_next_phrase():
    # get index
    path_to_index = './res/python_lib_index.pkl'
    index = search_backend.read_index(path_to_index)

    query = "int int"
    args = search_backend.prepare_arguments(query, stopwords=index.stopwords)
    res = (-1, -1), (-1, -1)
    set_one = set()
    while res is not None:
        res = index.next_phrase(args, pos=res[0])
        if res is not None:
            set_one.add(res)

    res = (-1, -1), (-1, -1)
    set_two = set()
    while res is not None:
        res = index.next_phrase(args, pos=res[1])
        if res is not None:
            set_two.add(res)

    query = "int int int"
    args = search_backend.prepare_arguments(query, stopwords=index.stopwords)
    res = (-1, -1), (-1, -1)
    set_three = set()
    while res is not None:
        res = index.next_phrase(args, pos=res[0])
        if res is not None:
            set_three.add(res)
    assert set_one - set_two == {((400, 2351), (400, 2352)), ((407, 712), (407, 713))}
    assert set_three == {((400, 2350), (400, 2352)), ((407, 711), (407, 713))}


def test_AND_boolean_search():
    path_to_index = './res/python_lib_index.pkl'
    index = search_backend.read_index(path_to_index)
    query = "int document search double"
    args = search_backend.prepare_arguments(query, stopwords=index.stopwords)
    res = index.AND_boolean_search(args)
    true_res = {89, 416, 451, 452, 454, 104, 169, 458, 463, 80, 241, 338, 57, 91, 30}
    assert set(res) == true_res


def test_OR_boolean_search():
    path_to_index = './res/python_lib_index.pkl'
    index = search_backend.read_index(path_to_index)
    query = "Drake bpython"
    args = search_backend.prepare_arguments(query, stopwords=index.stopwords)
    res = index.OR_boolean_search(args)
    true_res = {0, 449, 450, 451, 448, 453, 454, 332, 176, 338, 435}
    assert set(res) == true_res
