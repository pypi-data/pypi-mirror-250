import pytest

import sys
sys.path.append('../')
from coggle.text.statistics import (
    sentence_length,
    character_count,
    whitespaces_count,
    duplicates_character_count,
    english_character_count,
    emoji_character_count,
    chinese_character_count,
    punctuations_count
)

@pytest.mark.parametrize("test_input, expected", [
    ("Hello World", 11),  # Including space
    ("你好，世界", 5),
    ("😊🌍", 2),
    ("123 456", 7),
    ("", 0),
])
def test_sentence_length(test_input, expected):
    assert sentence_length(test_input) == expected

@pytest.mark.parametrize("test_input, expected", [
    ("Hello World", 8),
    ("你好，世界", 5),
    ("😊🌍", 2),
    ("123 456", 7),
    ("", 0),
])
def test_character_count(test_input, expected):
    assert character_count(test_input) == expected

@pytest.mark.parametrize("test_input, expected", [
    ("Hello World", 1),
    ("你好，世界", 0),
    ("😊🌍", 0),
    ("123 456", 1),
    ("", 0),
])
def test_whitespaces_count(test_input, expected):
    assert whitespaces_count(test_input) == expected

@pytest.mark.parametrize("test_input, expected", [
    ("Hello World", 3), 
    ("你好，世界", 0),
    ("😊🌍", 0),
    ("123 456", 0),
    ("", 0),
])
def test_duplicates_character_count(test_input, expected):
    assert duplicates_character_count(test_input) == expected

@pytest.mark.parametrize("test_input, expected", [
    ("Hello World 😊🌍", 2),
    ("你好，世界", 0),
    ("😊🌍", 2),
    ("123 456", 0),
    ("", 0),
])
def test_emoji_character_count(test_input, expected):
    assert emoji_character_count(test_input) == expected

@pytest.mark.parametrize("test_input, expected", [
    ("Hello World", 10),  # Including space
    ("你好，世界", 0),
    ("😊🌍", 0),
    ("123 456", 0),
    ("", 0),
])
def test_english_character_count(test_input, expected):
    assert english_character_count(test_input) == expected

@pytest.mark.parametrize("test_input, expected", [
    ("Hello World 你好，世界", 4),
    ("你好，世界", 4),
    ("😊🌍", 0),
    ("123 456", 0),
    ("", 0),
])
def test_chinese_character_count(test_input, expected):
    assert chinese_character_count(test_input) == expected

@pytest.mark.parametrize("test_input, expected", [
    ("Hello World! 你好，世界！", 3),
    ("😊🌍", 0),
    ("123 456", 0),
    ("", 0),
])
def test_punctuations_count(test_input, expected):
    assert punctuations_count(test_input) == expected