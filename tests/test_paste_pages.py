import pdf_util.paste_pages
import pdf_util

from io import BytesIO
from pathlib import Path

from pypdf import PdfReader



repository_root = Path(__file__).parent.parent
original_pdf_path = str(repository_root/"tests/pdfs/ai/original.pdf")
translated_pdf_path = str(repository_root/"tests/pdfs/ai/translated_pages.pdf")


def test_paste_pages():
    original = PdfReader(original_pdf_path)
    translated_pages = PdfReader(translated_pdf_path)
    (writer, inserted_at, original_old_to_new) = pdf_util.paste_pages(original, translated_pages, [0, 1, 2])

    assert inserted_at == [1, 3, 5]
    assert original_old_to_new == {0: 0, 1: 2, 2: 4, 3: 6, 4: 7}

    tf = BytesIO()
    writer.write(tf)
    written_file = PdfReader(tf)

    assert len(written_file.pages) == len(original.pages) + len(translated_pages.pages)
    assert all(written_file.pages[l].extract_text() == original.pages[r].extract_text() for (l, r) in [(0, 0)])
    assert all(written_file.pages[l].extract_text() == translated_pages.pages[r].extract_text() for (l, r) in [(1, 0)])
