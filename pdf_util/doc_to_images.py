from typing import Iterator

import fitz 
from PIL import Image



def doc_to_images(doc: fitz.Document) -> Iterator[Image.Image]:
    """
    Example:
    ```
    import fitz
    doc = "doc.pdf"
    images = pdf_util.doc_to_images(fitz.Document(doc))
    next(images).save("doc.png")
    ```
    """

    def page_to_image(page: fitz.Page) -> Image.Image:
        scale = 2
        pix: fitz.Pixmap = page.get_pixmap(matrix=fitz.Matrix(scale, scale))
        mode = "RGB" if pix.n == 3 else "RGBA"
        image: Image.Image = Image.frombytes(mode, (pix.width, pix.height), pix.samples)
        bbox: fitz.IRect = pix.irect
        image: Image.Image = image.crop(tuple(bbox[i] for i in range(4)))
        return image

    return \
        map(page_to_image, 
        map(doc.load_page,
            range(len(doc))))


def doc_to_images_without_processing(doc: fitz.Document) -> Iterator[Image.Image]:
    """
    Example:
    ```
    import fitz
    doc = "doc.pdf"
    images = pdf_util.doc_to_images(fitz.Document(doc))
    next(images).save("doc.png")
    ```
    """

    def page_to_image(page: fitz.Page) -> Image.Image:
        """
        Converts a single PDF page to a PIL Image without scaling or cropping.

        :param page: PDF page object from PyMuPDF.
        :return: Image of the page as a PIL Image object.
        """
        # Obtain the page image without scaling
        pix: fitz.Pixmap = page.get_pixmap()  # No scaling matrix applied
        mode = "RGB" if pix.n == 3 else "RGBA"  # Set color mode based on color channels

        # Create a PIL Image from pixmap data
        image: Image.Image = Image.frombytes(mode, (pix.width, pix.height), pix.samples)

        return image

    return \
        map(page_to_image,
        map(doc.load_page,
            range(len(doc))))
