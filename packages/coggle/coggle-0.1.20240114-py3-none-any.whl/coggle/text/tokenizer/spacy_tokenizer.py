from concurrent.futures import ProcessPoolExecutor
import spacy
import traceback
from typing import Union, List

class SpaCyTokenizer:
    def __init__(self, model_name='zh_core_web_sm'):
        '''
        初始化SpaCyTokenizer对象

        参数:
        - method: SpaCy模型待选链接 https://spacy.io/models/
        '''
        self.model_name = model_name
        try:
            self.nlp = spacy.load(self.model_name)
        except IOError:
            raise NotImplementedError("SpaCy模型需要单独下载，可以查看库主页安装教程：https://github.com/coggle-club/coggle")

    def __call__(self, text: Union[str, List[str]]) -> List:
        return self.tokenize(text)

    def _tokenize(self, text: str) -> List:
        if text is None:
            return []
        
        doc = self.nlp(text)
        return [x.text for x in doc]

    def tokenize(self, text: Union[str, List[str]]) -> List:
        """
        将文档进行分词

        参数:
        - text: 输入的文档字符串

        返回:
        - 切分后的文档块列表
        """
        if isinstance(text, str):
            return self._tokenize(text)

        with ProcessPoolExecutor(max_workers=1) as executor:
            result = list(executor.map(self._tokenize, text))
        return result
