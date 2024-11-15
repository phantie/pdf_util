from .writer_from_page_iterable import writer_from_page_iterable
from .page_index import PageIndex

from pypdf import PdfReader, PdfWriter
from typing import Sequence
from typing import TypeVar



def paste_pages(
    original: PdfReader,
    pages: PdfReader,
    page_indeces: Sequence[PageIndex]
) -> tuple[PdfWriter, Sequence[PageIndex], dict[PageIndex, PageIndex]]:
    """
    Integrate specific pages from a secondary PDF into an original PDF at specified positions.

    Args:
        original (PdfReader): The PDF reader object for the original PDF.
        pages (PdfReader): The PDF reader object containing the pages to be inserted.
        page_indices (Sequence[PageIndex]): A sequence of unique indices indicating the positions 
                                            in the original PDF where new pages should be inserted.

    Returns:
        PdfWriter: A PDF writer object that contains the merged content of the original PDF and the inserted pages.
        Sequence[PageIndex]: The new indices of the inserted pages.
        dict[PageIndex, PageIndex]: A mapping from original page indices to their new indices after insertion.

    Raises:
        AssertionError: If any of the following conditions are not met:
            - The number of pages in the 'pages' PDF matches the length of 'page_indices'.
            - All indices in 'page_indices' are valid (i.e., they are all less than the number of pages in the 'original' PDF).
            - All indices in 'page_indices' are unique.
            - 'page_indices' is sorted in ascending order.
            
    Example:
        original_pdf = PdfReader('original.pdf')
        extra_pages_pdf = PdfReader('pages_to_insert.pdf')
        indices_to_insert = [1, 3, 5]

        writer, new_indices, original_old_to_new = paste_pages(original_pdf, extra_pages_pdf, indices_to_insert)
        writer.write('merged_output.pdf')

    Note:
        This function assumes the indices provided in 'page_indices' are in ascending order and each index 
        corresponds to a unique page from the 'pages' PDF to be inserted immediately after the page 
        at that index in the 'original' PDF.
    """
    assert len(pages.pages) == len(page_indeces)
    assert all(n < len(original.pages) for n in page_indeces)
    assert len(set(page_indeces)) == len(page_indeces)
    assert sorted(page_indeces) == page_indeces

    pages = iter(pages.pages)
    inserted_at = []
    result = []
    original_old_to_new = {}
    shift = 0

    for i in range(len(original.pages)):
        # Map the original index to its new index, considering the shift
        original_old_to_new[i] = i + shift
        result.append(original.pages[i])
        
        if i in page_indeces:
            inserted_at.append(len(result))
            result.append(next(pages))
            shift += 1  # Increment the shift as we add a page

    return writer_from_page_iterable(result), inserted_at, original_old_to_new
