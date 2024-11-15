import pdf_util

from io import BytesIO
from pathlib import Path

from pypdf import PdfReader




repository_root = Path(__file__).parent.parent
original_pdf_path = str(repository_root/"tests/pdfs/ai/original.pdf")
translated_pdf_path = str(repository_root/"tests/pdfs/ai/translated_pages.pdf")


def test_replace_pages():
    original = PdfReader(original_pdf_path)
    translated_pages = PdfReader(translated_pdf_path)
    writer = pdf_util.replace_pages(original, translated_pages, [0, 1, 2])

    tf = BytesIO()
    writer.write(tf)
    written_file = PdfReader(tf)

    assert len(written_file.pages) == len(original.pages)
    assert all(written_file.pages[i].extract_text() == translated_pages.pages[i].extract_text() for i in [0])
    assert all(written_file.pages[i].extract_text() == original.pages[i].extract_text() for i in [3])

