import pdf_util

from pathlib import Path

import pytest
from pypdf import PdfReader

repository_root = Path(__file__).parent.parent
pdf_path = str(repository_root/"tests/pdfs/ai/original.pdf")


def test_page_subset_full_range():
    reader = PdfReader(pdf_path)
    assert len(pdf_util.page_subset(reader, range(0, len(reader.pages))).pages) # full range


def test_page_subset_excessive_pages():
    reader = PdfReader(pdf_path)
    with pytest.raises(AssertionError):
        len(pdf_util.page_subset(reader, [len(reader.pages) + 1]).pages) # excessive pages

