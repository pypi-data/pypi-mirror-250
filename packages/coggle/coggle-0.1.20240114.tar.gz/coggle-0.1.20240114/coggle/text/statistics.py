from typing import AnyStr
import emoji
import string
import re


chinese_re = re.compile(r'[\u4e00-\u9fff]+')
english_punctuation = string.punctuation
chinese_punctuation = "！？｡。＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏."


def sentence_length(s: AnyStr) -> int:
    return len(s)


def character_count(s: AnyStr) -> int:
    return len(set(s))


def whitespaces_count(s: AnyStr) -> int:
    return len([x for x in s if x == ' '])


def duplicates_character_count(s: AnyStr) -> int:
    count = 0
    for idx, c in enumerate(s):
        if c in s[:idx]:
            count += 1
    return count


def emoji_character_count(s: AnyStr) -> int:
    return len([c for c in s if c in emoji.EMOJI_DATA])


def english_character_count(s: AnyStr) -> int:
    return len([c for c in s if c in string.ascii_letters])


def chinese_character_count(s: AnyStr) -> int:
    result = chinese_re.findall(s)
    return len(''.join(result))


def punctuations_count(s: AnyStr) -> int:
    return len([c for c in s if c in english_punctuation or c in chinese_punctuation])