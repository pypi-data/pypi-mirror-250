import sys
sys.path.append('../')
from coggle.text.similarity import (
    longest_substr_length,
    edit_distance,
    cosine_distance,
    prefix_length,
    hamming_distance,
    jaccard_distance
)

import math

def test_longest_substr_length():
    assert longest_substr_length("abcde", "ababcde") == 5
    assert longest_substr_length("xyz", "abc") == 0
    assert longest_substr_length("abcdef", "xyzabcdefuvw") == 6

def test_edit_distance():
    assert edit_distance("kitten", "sitting") == 3
    assert edit_distance("flaw", "lawn") == 2
    assert edit_distance("book", "back") == 2

def test_cosine_distance():
    assert math.isclose(cosine_distance("cat", "dog"), 1)

def test_jaccard_distance():
    assert math.isclose(jaccard_distance("apple", "apple"), 0)

def test_prefix_length():
    assert prefix_length("abcdef", "abcxyz") == 3
    assert prefix_length("hello", "world") == 0
    assert prefix_length("python", "pyramid") == 2

def test_hamming_distance():
    assert hamming_distance("karolin", "kathrin") == 3
    assert hamming_distance("hello", "world") == 4