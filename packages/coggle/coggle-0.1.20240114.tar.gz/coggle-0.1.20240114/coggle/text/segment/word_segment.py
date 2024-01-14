from typing import Union, List, Any


class WordSegment:
    def __init__(
        self,
        chunk_size: int = 30,
        chunk_overlap: int = 0,
        separator: Union[str, None] = None,
        tokenizer: Any = None,
        language: str = "zh"
    ):
        """
        初始化CharacterSegment对象

        参数:
        - chunk_size: 切分文档的块大小
        - chunk_overlap: 块之间的重叠大小
        - separator: 文档中的分隔符
        - tokenizer: 分词器
        - language: 文档的语言，中文（zh）或 英文（en）
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separator = separator
        self.tokenizer = tokenizer
        self.language = language
        
        if tokenizer is not None and 'NLTK' in str(tokenizer):
            self.language = 'en'
        
        if self.chunk_size <= self.chunk_overlap:
            raise Exception("chunk_size must greate then chunk_overlap!")

        if self.separator is None and self.tokenizer is None:
            raise Exception("separator and tokenizer can not both set None in WordSegment")

    def __call__(self, document: str) -> List[str]:
        if self.separator is not None:
            words = document.split(self.separator)
        elif self.tokenizer is not None:
            words = self.tokenizer.tokenize(document)

        segments = []
        start = 0

        while start < len(words):
            end = start + self.chunk_size
            if end > len(words):
                end = len(words)

            segment = words[start:end]

            if self.separator is not None:
                segments.append(self.separator.join(segment))
            else:
                if self.language == 'zh':
                    segments.append(''.join(segment))
                else:
                    segments.append(' '.join(segment))

            start += self.chunk_size - self.chunk_overlap
        
        if self.chunk_overlap > 0 and segments[-1] == words[-1]:
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
