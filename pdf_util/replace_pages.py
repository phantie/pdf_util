from .writer_from_page_iterable import writer_from_page_iterable
from .page_index import PageIndex

from pypdf import PdfReader, PdfWriter
from typing import Sequence





def replace_pages(original: PdfReader, pages: PdfReader, page_indeces: Sequence[PageIndex]) -> PdfWriter:
    """
    Combines pages from an original PDF and a other PDF to create a new PDF.

    This function replaces specific pages in the original PDF with corresponding pages from another PDF.
    It ensures that the other pages are inserted at the specified indices, effectively pasting them into the original PDF.

    Args:
    - original (PdfReader): The PdfReader object for the original PDF.
    - pages (PdfReader): The PdfReader object containing pages to be inserted.
    - page_indeces (Sequence[int]): A sequence of integers indicating the indices in the original PDF
      where the other pages should replace the original pages.

    Returns:
    - PdfWriter: A PdfWriter object containing the combined PDF with the other pages inserted at the specified indices.

    Raises:
    - AssertionError: If the number of pages does not match the length of `page_indeces`.
    - AssertionError: If any page number in `page_indeces` exceeds the number of pages in the other PDF.
    - AssertionError: If there are duplicate entries in `page_indeces`.
    - AssertionError: If `page_indeces` are not sorted.

    Example:
    ```python
    from pypdf import PdfReader, PdfWriter

    original_pdf_path = "original.pdf"
    translated_pdf_path = "translated.pdf"
    output_pdf_path = "combined.pdf"

    original_reader = PdfReader(original_pdf_path)
    translated_reader = PdfReader(translated_pdf_path)

    # Replace pages 2 and 4 in the original PDF with the first two pages of the translated PDF
    translated_page_numbers = [1, 3]  # Replace pages 2 and 4 in 0-based index

    writer = paste_translated_pages(original_reader, translated_reader, translated_page_numbers)

    # Save the combined PDF
    with open(output_pdf_path, "wb") as output_file:
        writer.write(output_file)

    print(f"Combined PDF saved to {output_pdf_path}")
    ```
    
    The function validates that the number of other pages matches the number of specified indices and that there are no duplicate indices.
    It iterates over the pages of the original PDF, replacing the pages at the specified indices with the corresponding other pages.
    The resulting `PdfWriter` object contains the new combined PDF, which can be saved to a file.
    """

    assert len(pages.pages) == len(page_indeces)
    assert all(n < len(pages.pages) for n in page_indeces)
    assert len(set(page_indeces)) == len(page_indeces)
    assert sorted(page_indeces) == page_indeces

    pages = iter(pages.pages)

    return writer_from_page_iterable(
        next(pages) if page_number in page_indeces
        else original.pages[page_number]
        for page_number in range(len(original.pages)))


