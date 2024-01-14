from typing import Union, List
import spacy


class SentenceSegment:
    def __init__(
        self,
        chunk_size: int = 1,
        chunk_overlap: int = 0,
        separator: Union[str, None] = None,
        model_name: str = "zh_core_web_sm",
        language: str = "zh"
    ):
        """
        初始化CharacterSegment对象

        参数:
        - chunk_size: 切分文档的块大小
        - chunk_overlap: 块之间的重叠大小
        - separator: 文档中的分隔符
        - model_name: spaCy句子划分模型
        - language: 文档的语言，中文（zh）或 英文（en）
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separator = separator
        self.model_name = model_name
        self.language = language

        if self.separator is None and self.model_name is None:
            raise Exception("separator and model_name can not both set None in WordSegment")

        if self.chunk_size <= self.chunk_overlap:
            raise Exception("chunk_size must greate then chunk_overlap!")

        try:
            self.nlp = spacy.load(self.model_name)
        except IOError:
            raise NotImplementedError("SpaCy模型需要单独下载，如果想要快速安装，可以查看库主页安装教程：https://github.com/coggle-club/coggle")

    def __call__(self, document: str) -> List[str]:
        if self.separator is not None:
            sents = document.split(self.separator)
        elif self.model_name is not None:
            doc = self.nlp(document)
            sents = [x.text for x in doc.sents]

        sents = [x for x in sents if len(sents) > 0]

        segments = []
        start = 0

        while start < len(sents):
            end = start + self.chunk_size
            if end > len(sents):
                end = len(sents)

            segment = sents[start:end]

            if self.separator is not None:
                segments.append(self.separator.join(segment))
            else:
                if self.language == 'zh':
                    segments.append(''.join(segment))
                else:
                    segments.append(' '.join(segment))

            start += self.chunk_size - self.chunk_overlap

        if self.chunk_overlap > 0 and segments[-1] == sents[-1]:
            segments.pop()
            
        return segments

    def segment(self, document: str) -> List[str]:
        """
        将文档切分成块，按照预定的块大小和重叠大小

        参数:
        - document: 输入的文档字符串

        返回:
        - 切分后的文档块列表
        """
        return self.__call__(document)
