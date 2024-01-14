from typing import Union, List
import jieba
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count


class JiebaTokenizer:
    def __init__(self):
        """
        初始化JiebaTokenizer对象，用于jieba分词
        """

        # 获取CPU核心数
        self.cpu_count = cpu_count()

    def __call__(self, text: Union[str, List[str]]) -> List:
        return self.tokenize(text)

    def _tokenize(self, text: str) -> List:
        return jieba.lcut(text)

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

        if len(text) < 1000:
            with ProcessPoolExecutor(max_workers=1) as executor:
                result = list(executor.map(self._tokenize, text))
        else:
            with ProcessPoolExecutor(max_workers=self.cpu_count) as executor:
                result = list(executor.map(self._tokenize, text))
        
        return result
