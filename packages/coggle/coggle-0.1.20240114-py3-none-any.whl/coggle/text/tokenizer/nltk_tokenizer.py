from typing import Union, List
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count

from nltk.tokenize import word_tokenize
from nltk.tokenize import wordpunct_tokenize
from nltk.tokenize import TweetTokenizer


class NLTKTokenizer:
    def __init__(self, method: str = 'word'):
        """
        初始化JiebaTokenizer对象

        参数:
        - method: NLTK内置的tokenizer方法名
            word: `from nltk.tokenize import word_tokenize`
            wordpunct: `from nltk.tokenize import wordpunct_tokenize`
            tweet: `from nltk.tokenize import TweetTokenizer`
            nltkword: `from nltk.tokenize import NLTKWordTokenizer`
        """
        if method == "word":
            self.token_funct = word_tokenize
        elif method == "wordpunct":
            self.token_funct = wordpunct_tokenize
        elif method == "tweet":
            self.tknzr = TweetTokenizer()
            self.token_funct = self.tknzr.tokenize
        else:
            raise NotImplementedError(f"Unsupported method: {method} in NLTKTokenizer.")

        self.cpu_count = cpu_count()

    def __call__(self, text: Union[str, List[str]]) -> List:
        return self.tokenize(text)

    def _tokenize(self, text: str) -> List:
        return list(self.token_funct(text))

    def tokenize(self, text: Union[str, List[str]]) -> List:
        if isinstance(text, str):
            return self._tokenize(text)

        if len(text) < 1000:
            with ProcessPoolExecutor(max_workers=1) as executor:
                result = list(executor.map(self._tokenize, text))
        else:
            with ProcessPoolExecutor(max_workers=self.cpu_count) as executor:
                result = list(executor.map(self._tokenize, text))
        return result
