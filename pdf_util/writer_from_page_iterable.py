from pypdf import PdfWriter, PageObject
from typing import Iterable


def writer_from_page_iterable(pages: Iterable[PageObject]) -> PdfWriter:
    """
    Example:
    ```
    new_file_path = "file.pdf"
    writer = writer_from_page_iterable([])
    with open(new_file_path, "wb") as f:
        writer.write(f)
    ```
    """

    writer = PdfWriter()
    for page in pages:
        writer.add_page(page)
    return writer
