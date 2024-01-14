import sys
sys.path.append('../')

from coggle.text.segment import (
    CharacterSegment,
    SentenceSegment,
    WordSegment,
    CodeSegment,
    MarkdownSegment
)

from coggle.text.tokenizer import JiebaTokenizer, NLTKTokenizer


def test_CharacterSegment():
    segmenter = CharacterSegment(chunk_size=2)
    assert segmenter.segment("我们开始") == ["我们", "开始"]

    segmenter = CharacterSegment(chunk_size=2, chunk_overlap=1)
    assert segmenter.segment("我们开始") == ["我们", "们开", "开始"]

    try:
        segmenter = CharacterSegment(chunk_size=2, chunk_overlap=2)
    except:
        assert 1 == 1


def test_WordSegment():
    segmenter = WordSegment(chunk_size=2, chunk_overlap=0, separator=' ')
    assert segmenter.segment("I want go to school today.") == ['I want', 'go to', 'school today.']

    segmenter = WordSegment(chunk_size=2, chunk_overlap=1, separator=' ')
    assert segmenter.segment("I want go to school today.") == ['I want', 'want go', 'go to', 'to school', 'school today.']

    segmenter = WordSegment(chunk_size=2, chunk_overlap=0, tokenizer=JiebaTokenizer())
    assert segmenter.segment("我们开始学习机器学习") == ['我们开始', '学习机器', '学习']

    segmenter = WordSegment(chunk_size=2, chunk_overlap=1, tokenizer=JiebaTokenizer())
    assert segmenter.segment("我们开始学习机器学习") == ['我们开始', '开始学习', '学习机器', '机器学习']

    segmenter = WordSegment(chunk_size=2, chunk_overlap=0, tokenizer=NLTKTokenizer())
    assert segmenter.segment("I want go to school today.") == ['I want', 'go to', 'school today', '.']

    segmenter = WordSegment(chunk_size=2, chunk_overlap=1, tokenizer=NLTKTokenizer())
    assert segmenter.segment("I want go to school today.") == ['I want', 'want go', 'go to', 'to school', 'school today', 'today .']

    try:
        segmenter = WordSegment(chunk_size=2, chunk_overlap=2)
    except:
        assert 1 == 1


def test_SentenceSegment():
    segmenter = SentenceSegment(chunk_size=1, chunk_overlap=0)
    assert segmenter.segment("今天天气很好。但我不想出门。") == ['今天天气很好。', '但我不想出门。']

    segmenter = SentenceSegment(chunk_size=2, chunk_overlap=0)
    assert segmenter.segment("今天天气很好。但我不想出门。但是还是要出去。因为要跑步。出门啦！") == ['今天天气很好。但我不想出门。', '但是还是要出去。因为要跑步。', '出门啦！']

    segmenter = SentenceSegment(chunk_size=2, chunk_overlap=1)
    assert segmenter.segment("今天天气很好。但我不想出门。但是还是要出去。因为要跑步。出门啦！") == ['今天天气很好。但我不想出门。', '但我不想出门。但是还是要出去。', '但是还是要出去。因为要跑步。', '因为要跑步。出门啦！']

    try:
        segmenter = SentenceSegment(chunk_size=2, chunk_overlap=2)
    except:
        assert 1 == 1

    try:
        tokenizer_unsupported = SentenceSegment(model_name='invalid_method')
    except:
        assert 1 == 1