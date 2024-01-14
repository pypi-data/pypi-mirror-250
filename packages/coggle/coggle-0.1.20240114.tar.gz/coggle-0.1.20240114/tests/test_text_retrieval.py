import sys
sys.path.append('../')

from coggle.text.retrieval import (
    InvertedIndex,
    TFIDF,
    BM25Okapi,
    TextEmbedding
)
import numpy as np

def test_InvertedIndex():
    index = InvertedIndex()
    index.add_document(1, ["a", "b", "c"])
    index.add_document(2, ["b", "c", "d"])
    assert 1 == index.query("a")[0][0]
    assert 1 in [x[0] for x in index.query("b")] and 2 in [x[0] for x in index.query("b")]

    assert index.update_document(3, ['1']) == False

    index.delete_term("a")
    assert index.query("a") == []

    assert index.total_size == 2
    index.delete_document(1)
    assert index.total_size == 1

    index = InvertedIndex([1, 2], [["a", "b", "c"], ["b", "c", "d"]])
    index.update_document(1, ["b", "c"])
    assert index.query("a") == []


def test_TFIDF():
    index = TFIDF()
    index.add_document(1, ["a", "b", "c"])
    index.add_document(2, ["b", "c", "d"])
    index.add_document(3, ["e", "d", "g"])
    index.add_document(4, ["d", "f", "g"])
    assert 1 in [x[0] for x in index.query("b")] and 2 in [x[0] for x in index.query("b")]

    assert index.query("e")[0][0] == 3

    assert index.query(["b", "d"])[0][0] == 2

    assert index.total_size == 4

    index.delete_document(1)
    assert index.total_size == 3

    index.delete_term("b")
    assert "b" not in index.invert_index

    index = TFIDF([1, 2], [["a", "b", "c"], ["b", "c", "d"]])
    index.update_document(2, ["a"])
    assert 1 in [x[0] for x in index.query("a")] and 2 in [x[0] for x in index.query("a")]


def test_BM25Okapi():
    index = BM25Okapi()
    index.add_document(1, ["a", "b", "c"])
    index.add_document(2, ["b", "c", "d"])
    index.add_document(3, ["e", "d", "g"])
    index.add_document(4, ["d", "f", "g"])
    assert 1 in [x[0] for x in index.query("b")] and 2 in [x[0] for x in index.query("b")]

    assert index.query("e")[0][0] == 3

    assert index.query(["b", "d"])[0][0] == 2

    assert index.total_size == 4

    index.delete_document(1)
    assert index.total_size == 3

    index.delete_term("b")
    assert "b" not in index.invert_index

    index = BM25Okapi([1, 2], [["a", "b", "c"], ["b", "c", "d"]])
    index.update_document(2, ["a"])
    assert 1 in [x[0] for x in index.query("a")] and 2 in [x[0] for x in index.query("a")]


def test_TextEmbedding():
    index = TextEmbedding('all-MiniLM-L6-v2', [1,2], ["1", "2"])
    assert index.total_size == 2

    assert index.query_by_text(["1"])[0][0] == 1

    index.add_document(3, "3")
    index.delete_document(3)
    assert index.total_size == 2

    index.update_document(1, "3")
    assert index.query_by_text(["3"])[0][0] == 1

    assert isinstance(index.query_by_feat(np.zeros(384)), list) == True

