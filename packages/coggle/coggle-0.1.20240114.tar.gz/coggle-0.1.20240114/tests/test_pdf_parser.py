import os, sys
sys.path.append('../')

from coggle.parser import PDFParser

def test_PDFParser():
    parser = PDFParser("../assets/demo_pdf.pdf")
    assert parser.page_size == 1
    assert len(parser.extract_text(0)) > 0