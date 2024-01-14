import sys
sys.path.append('../')

from coggle.text.tokenizer import (
    JiebaTokenizer,
    NLTKTokenizer,
    SpaCyTokenizer,
    HuggingFaceTokenizer
)

def test_JiebaTokenizer():
    tokenizer = JiebaTokenizer()
    text = "我爱自然语言处理"
    result = tokenizer.tokenize(text)
    assert result == ['我', '爱', '自然语言', '处理']

    result = tokenizer(text)
    assert result == ['我', '爱', '自然语言', '处理']

    texts = ["我爱自然语言处理", "人工智能是未来"]
    result = tokenizer.tokenize(texts)
    assert result == [['我', '爱', '自然语言', '处理'], ['人工智能', '是', '未来']]

    texts = ["我爱自然语言处理"] * 1001
    result = tokenizer.tokenize(texts)
    assert isinstance(result, list)


def test_NLTKTokenizer():
    # Test case with word_tokenize method
    tokenizer_word = NLTKTokenizer(method='word')
    text_word = "Natural language processing is fascinating."
    result_word = tokenizer_word.tokenize(text_word)
    assert result_word == ['Natural', 'language', 'processing', 'is', 'fascinating', '.']

    result_word = tokenizer_word(text_word)
    assert result_word == ['Natural', 'language', 'processing', 'is', 'fascinating', '.']

    texts = ["NLTK is powerful."] * 1001
    result = tokenizer_word.tokenize(texts)
    assert isinstance(result, list)
    
    # Test case with wordpunct_tokenize method
    tokenizer_wordpunct = NLTKTokenizer(method='wordpunct')
    text_wordpunct = "Don't hesitate to ask questions!"
    result_wordpunct = tokenizer_wordpunct.tokenize(text_wordpunct)
    assert result_wordpunct == ['Don', "'", 't', 'hesitate', 'to', 'ask', 'questions', '!']

    # Test case with TweetTokenizer method
    tokenizer_tweet = NLTKTokenizer(method='tweet')
    text_tweet = "Loving the weather! #sunny"
    result_tweet = tokenizer_tweet.tokenize(text_tweet)
    assert result_tweet == ['Loving', 'the', 'weather', '!', '#sunny']

    # Test case with unsupported method
    try:
        tokenizer_unsupported = NLTKTokenizer(method='invalid_method')
        tokenizer_unsupported.tokenize("This should raise an exception.")
    except NotImplementedError as e:
        assert str(e) == "Unsupported method: invalid_method in NLTKTokenizer."

    # Test case with a list of strings
    texts = ["NLTK is powerful.", "Use it wisely!"]
    result_list = tokenizer_word.tokenize(texts)
    assert result_list == [['NLTK', 'is', 'powerful', '.'], ['Use', 'it', 'wisely', '!']]


def test_SpaCyTokenizer():
    # Test case with a single string
    tokenizer = SpaCyTokenizer(model_name='zh_core_web_sm')
    text = "我爱自然语言处理"
    result = tokenizer.tokenize(text)
    assert result == ['我', '爱', '自然', '语言', '处理']

    result = tokenizer(text)
    assert result == ['我', '爱', '自然', '语言', '处理']

    result = tokenizer(None)
    assert result == []

    # Test case with unsupported model name
    try:
        unsupported_tokenizer = SpaCyTokenizer(model_name='invalid_model')
    except NotImplementedError as e:
        assert 1 == 1

    texts = ["NLTK is powerful.", "Use it wisely!"]
    result_list = tokenizer.tokenize(texts)
    assert isinstance(result_list, list)


def test_HuggingFaceTokenizer():
    tokenizer = HuggingFaceTokenizer()
    text = "我爱自然语言处理"
    result = tokenizer.tokenize(text)
    assert isinstance(result, list)