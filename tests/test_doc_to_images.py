import pdf_util

from io import BytesIO
from pathlib import Path

from pypdf import PdfReader
import fitz


repository_root = Path(__file__).parent.parent
pdf_path = str(repository_root/"tests/pdfs/ai/translated_pages.pdf")


def test_doc_to_images():
    images = list(pdf_util.doc_to_images(fitz.Document(pdf_path)))
    assert len(images) == len(PdfReader(pdf_path).pages)

    for image in images:
        bio = BytesIO()
        image.save(bio, format="png")

