from typing import Union


class CodeSegment:
    def __init__(
        self,
        chunk_size: int = 30,
        chunk_overlap: int = 0,
        separator: Union[str, None] = None,
        language: Union[str, None] = None
    ):
        raise NotImplementedError(f"Unsupported method: {language} in CodeSegment.")
