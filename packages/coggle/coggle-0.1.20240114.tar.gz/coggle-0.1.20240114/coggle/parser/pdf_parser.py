from typing import List, Any, Tuple
import pdfplumber

class PDFParser:
    def __init__(self, file_path: str = None):
        '''
        初始化PDFParser对象，用于解析PDF内容
        '''
        self.file_path : str = file_path
        self.doc : pdfplumber.pdf.PDF = pdfplumber.open(file_path)
        self.page_size : int = len(self.doc.pages)

    def extract_text(self, page_idx: int) -> Tuple[List[Any], str]:
        text_info = self.doc.pages[page_idx].extract_words()
        text_content = self.doc.pages[page_idx].extract_text()
        return text_info, text_content

    def extract_image(self, page_idx: int):
        raise NotImplementedError()

    def extract_table(self, page_idx: int):
        raise NotImplementedError()

    def extract_content(self, page_idx: int):
        raise NotImplementedError()

    def __del__(self):
        self.doc.close()