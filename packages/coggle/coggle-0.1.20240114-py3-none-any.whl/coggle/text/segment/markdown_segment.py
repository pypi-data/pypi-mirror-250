from typing import Union


class MarkdownSegment:
    def __init__(
        self,
        chunk_size: int = 30,
        chunk_overlap: int = 0,
        separator: Union[str, None] = None,
        language: Union[str, None] = None
    ):
        raise NotImplementedError(f"Unsupported in MarkdownSegment.")
