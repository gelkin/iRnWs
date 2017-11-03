import itertools
import math
import networkx as nx

from search_backend import prepare_arguments_eng_stopwords


def get_snippet_similarity(snippet_one_words: set, snippet_two_words: set):
    sim_words = snippet_one_words & snippet_two_words
    # print('snippet_one_words:' + str(snippet_one_words))
    # print('snippet_two_words:' + str(snippet_two_words) + "\n")
    return len(sim_words) / (math.log(1 + len(snippet_one_words)) + math.log(1 + len(snippet_two_words)))


def split_text_into_paragraphs(text):
    paragraphs = []
    paragraphs_words = []
    for paragraph in text.splitlines():
        if paragraph:
            paragraph_words = set(prepare_arguments_eng_stopwords(paragraph))
            if paragraph_words:
                paragraphs.append(paragraph)
                paragraphs_words.append(paragraph_words)
    return paragraphs, paragraphs_words


def get_best_paragraph(text):
    paragraphs, paragraphs_words = split_text_into_paragraphs(text)
    G = nx.Graph()
    G.add_nodes_from(list(range(len(paragraphs))))
    for one, two in itertools.combinations(range(len(paragraphs)), 2):
        weight = get_snippet_similarity(paragraphs_words[one], paragraphs_words[two])
        G.add_edge(one, two, weight=weight)
    ranks = nx.pagerank(G)
    # print(ranks)
    highest_rank_paragraph_ind = max(ranks, key=ranks.get)
    return paragraphs[highest_rank_paragraph_ind]
