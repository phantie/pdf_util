from pypdf import PdfReader, PageObject, PdfWriter
from typing import Iterator, Sequence
from .page_index import PageIndex
from .writer_from_page_iterable import writer_from_page_iterable




def page_subset(open_pdf: PdfReader | PdfWriter, subset: Sequence[PageIndex]) -> PdfWriter:
    """
    Generates a subset of pages from a PDF reader or writer based on the provided page indices.
    
    Args:
    - open_pdf (PdfReader | PdfWriter): The PdfReader object containing the pages to extract from.
    - subset (Sequence[int]): A sequence of integers representing the page indices to include in the subset.

    Returns: PdfWriter

    Raises:
    - AssertionError: If the maximum index in `subset` is greater than or equal to the number of pages in the PDF.

    Example:
    ```python
    from pypdf import PdfReader
    
    open_pdf = PdfReader("example.pdf")
    subset = [0, 2, 4]  # Get pages 1, 3, and 5
    
    for page in page_subset(open_pdf, subset).pages:
        print(page.extract_text())  # Process each selected page
    ```

    The function iterates over the PDF pages and filters them to yield only those whose indices are specified in the `subset`.
    It ensures that all specified indices are valid by asserting that the highest index is within the range of available pages.
    This approach allows for efficient and lazy evaluation, as pages are yielded one by one as they are filtered.
    """

    assert not subset or max(subset) < len(open_pdf.pages)

    def generator():
        for (page_number, page) in enumerate(open_pdf.pages):
            if page_number in subset:
                yield page
    
    return writer_from_page_iterable(generator())
