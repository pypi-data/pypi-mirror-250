from typing import List


class CharacterSegment:
    def __init__(
        self,
        chunk_size: int = 30,
        chunk_overlap: int = 0,
    ):
        """
        初始化CharacterSegment对象

        参数:
        - chunk_size: 切分文档的块大小
        - chunk_overlap: 块之间的重叠大小
        - separator: 文档中的分隔符（可选）
        - language: 文档的语言（可选）
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        if self.chunk_size <= self.chunk_overlap:
            raise Exception("chunk_size must greate then chunk_overlap!")

    def __call__(self, document: str) -> List[str]:
        if len(document) <= self.chunk_size:
            return [document]

        segments = []
        start = 0

        while start < len(document):
            end = start + self.chunk_size
            if end > len(document):
                end = len(document)
            
            segment = document[start:end]
            segments.append(segment)

            start += self.chunk_size - self.chunk_overlap
        
        if self.chunk_overlap > 0 and len(segment) != self.chunk_size:
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
