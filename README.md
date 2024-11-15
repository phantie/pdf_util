### Adobe Acrobat styled pdf document signing

```python
from pathlib import Path

repository_root = Path(__file__).parent.parent

pdf_path = str(repository_root/"tests"/"pdfs"/"blank.pdf")

with open(pdf_path, "rb") as f:
    value = f.read()

from pdf_util.visually_sign_doc import visually_sign_doc
from pdf_util.visually_sign_doc.params import SignDocParams
from pdf_util.visually_sign_doc.params import SignPageParams
from pdf_util.visually_sign_doc.params import SomePages
from pdf_util.visually_sign_doc.params import FirstPage
from pdf_util.visually_sign_doc.params import LastPage
from pdf_util.visually_sign_doc.params import AllPages
from pdf_util.visually_sign_doc.params import Margins


margins = Margins.equal(50)

value = visually_sign_doc(value, params=SignDocParams(
    pages_to_sign=SomePages(pages=[0]), # sign 1st page
    page_params=SignPageParams(
        signer_name="Ali Baba Babababa",
        align_horizontal="left",
        align_vertical="up",
        margins=margins,
        scale=2,
        under_text_align="center",
        left_box_text_align="left",
    ),
))


value = visually_sign_doc(value, params=SignDocParams(
    pages_to_sign=SomePages(pages=[0]), # sign 1st page
    page_params=SignPageParams(
        signer_name="First Middle Last",
        align_horizontal="right",
        align_vertical="center",
        margins=margins,
        scale=2,
        left_box_text_align="right",
    ),
))

value = visually_sign_doc(value, params=SignDocParams(
    pages_to_sign=SomePages(pages=[0]), # sign 1st page
    page_params=SignPageParams(
        signer_name="Alexander Alexandrovich Alexandro",
        align_horizontal="center",
        align_vertical="bottom",
        margins=margins,
        scale=2,
        under_text_align="align_with_right",
        left_box_text_align="center",
    ),
))


with open("signed.pdf", "wb+") as f:
    f.write(value)
```

## Result

<img width="734" alt="Screenshot 2024-11-15 at 18 47 41" src="https://github.com/user-attachments/assets/c9ff1c52-4b8d-4bc2-9b13-5b474f1ab637">


## Avalable customizations

| **Parameter**             | **Description**                                                   | **Type/Values**                                                                             |
|---------------------------|-------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| **SignDocParams**         | Main parameters for the document where the signature is to be rendered. |                                                                                             |
| `page_params`             | Parameters related to the rendering of a signature on a PDF page. | `SignPageParams`                                                                            |
| `pages_to_sign`           | Specifies which pages in the PDF should include the signature.    | `PagesToSign` (FirstPage, LastPage, AllPages, SomePages)                                    |
| **SignPageParams**        | Details the rendering of the signature on a page.                 |                                                                                             |
| `signer_name`             | Displays the name of the signer next to the signature.            | `str`                                                                                       |
| `left_box_text_align`     | Alignment of text within the left box area of the signature.      | `Align` ("left", "center", "right")                                                         |
| `under_text_align`        | Alignment of text located under the signature box.                | `"align_with_right"`, `"center"`                                                            |
| `scale`                   | Adjusts the size of the signature box and text.                   | `PositiveFloat`                                                                             |
| `margins`                 | Sets the space around the signature box.                          | `Margins`                                                                                   |
| `align_horizontal`        | Horizontal position of the signature on the page.                 | `"right"`, `"center"`, `"left"`                                                             |
| `align_vertical`          | Vertical position of the signature on the page.                   | `"bottom"`, `"center"`, `"up"`                                                              |
| **Margins**               | Parameters specifying the margins for the signature rendering.    |                                                                                             |
| `left`                    | Space on the left side of the signature box.                      | `NonNegativeFloat`                                                                          |
| `right`                   | Space on the right side of the signature box.                     | `NonNegativeFloat`                                                                          |
| `top`                     | Space above the signature box.                                    | `NonNegativeFloat`                                                                          |
| `bottom`                  | Space below the signature box.                                    | `NonNegativeFloat`                                                                          |
| **PagesToSign Options**   | Defines the selection of pages to render a signature.             |                                                                                             |
| `choice`                  | Indicates which pages will contain the signature.                 | `"first_page"`, `"last_page"`, `"all_pages"`, `"some_pages"`                                |
| `pages`                   | Specifies exact pages for signature when `choice` is `some_pages`.| `Set[NonNegativeInt]`                                                                       |


### All utilities
   - `visually_sign_doc.visually_sign_doc`
   - `page_subset`
   - `replace_pages`
   - `paste_pages`
   - `writer_from_page_iterable`
   - `doc_to_images`
   - `bytes_from_writer`
   - `page_to_bytes`
   - `image_to_bytes`
   - `crypto_sign_doc.crypto_sign_doc`
   - `certificate.debug_certificate_info`
