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
from pdf_util.visually_sign_doc.params import UK_LOCALE_SIGN_PAGE_PARAMS
from pdf_util.visually_sign_doc.params import EN_LOCALE_SIGN_PAGE_PARAMS
from pdf_util.visually_sign_doc.params import LocaleSignPageParams
from pdf_util.visually_sign_doc.params import CalculatedDatetimeSignPageParams
from pdf_util.visually_sign_doc.params import ScalarDatetimeSignPageParams
from pdf_util.visually_sign_doc._util import now
from datetime import datetime
from datetime import timedelta
from datetime import timezone


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
        locale=EN_LOCALE_SIGN_PAGE_PARAMS,
        datetime=ScalarDatetimeSignPageParams(datetime=datetime.now(tz=timezone(timedelta(hours=2)))),
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
        locale=UK_LOCALE_SIGN_PAGE_PARAMS,
        datetime=CalculatedDatetimeSignPageParams(calculate_datetime=lambda: now(utc_tz_offset=timedelta(hours=7))),
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
        locale=LocaleSignPageParams(
            digitally_signed_by="Signé numériquement par ",
            date="Date: ",
            signature="(signature)",
        ),
        datetime=CalculatedDatetimeSignPageParams(calculate_datetime=lambda: now(utc_tz_offset=timedelta(hours=-3))),
    ),
))


with open("signed.pdf", "wb+") as f:
    f.write(value)
```

## Result

<img width="613" alt="Screenshot 2024-11-15 at 19 31 09-min" src="https://github.com/user-attachments/assets/91012424-c27d-4602-bf1a-575d79f0b519">


## Avalable customizations
| **Parameter**                 | **Description**                                                   | **Type/Values**                                                                             |
|-------------------------------|-------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| **SignDocParams**             | Main parameters for document where signature is rendered.         |                                                                                             |
| `page_params`                 | Parameters related to rendering a signature on a PDF page.        | `SignPageParams`                                                                            |
| `pages_to_sign`               | Specifies which pages in the PDF should include the signature.    | `PagesToSign` (FirstPage, LastPage, AllPages, SomePages)                                    |
| **SignPageParams**            | Details rendering of the signature on a page.                     |                                                                                             |
| `signer_name`                 | Displays the name of the signer next to the signature.            | `str`                                                                                       |
| `left_box_text_align`         | Alignment of text within the left box area of the signature.      | `Align` ("left", "center", "right")                                                         |
| `under_text_align`            | Alignment of text located under the signature box.                | `"align_with_right"`, `"center"`                                                            |
| `scale`                       | Adjusts size of the signature box and text.                       | `PositiveFloat`                                                                             |
| `margins`                     | Sets space around the signature box.                              | `Margins`                                                                                   |
| `align_horizontal`            | Horizontal position of the signature on the page.                 | `"right"`, `"center"`, `"left"`                                                             |
| `align_vertical`              | Vertical position of the signature on the page.                   | `"bottom"`, `"center"`, `"up"`                                                              |
| `locale`                      | Locale-specific parameters for signature rendering.               | `LocaleSignPageParams`                                                                      |
| `datetime`                    | Specifies date and time for the signature.                        | `CalculatedDatetimeSignPageParams` or `ScalarDatetimeSignPageParams`                        |
| **CalculatedDatetimeSignPageParams** | Allows dynamic calculation of the signing datetime.        |                                                                                             |
| `calculate_datetime`          | Function that returns the datetime to use when signing the page.  | `Callable[[], datetime]`                                                                    |
| **ScalarDatetimeSignPageParams**    | Specifies a fixed datetime for the signature.               |                                                                                             |
| `datetime`                    | Defines a static datetime value for signing.                      | `datetime`                                                                                  |
| **LocaleSignPageParams**      | Locale-specific rendering details.                                |                                                                                             |
| `digitally_signed_by`         | "Digitally signed by " translation.                               | `str`                                                                                       |
| `date`                        | "Date: " translation.                                             | `str`                                                                                       |
| `signature`                   | "(signature)" translation.                                        | `str`                                                                                       |
| **Margins**                   | Parameters for signature rendering margins.                       |                                                                                             |
| `left`                        | Space on the left of the signature box.                           | `NonNegativeFloat`                                                                          |
| `right`                       | Space on the right of the signature box.                          | `NonNegativeFloat`                                                                          |
| `top`                         | Space above the signature box.                                    | `NonNegativeFloat`                                                                          |
| `bottom`                      | Space below the signature box.                                    | `NonNegativeFloat`                                                                          |
| **PagesToSign Options**       | Defines page selection for signature rendering.                   |                                                                                             |
| `choice`                      | Indicates which pages contain the signature.                      | `"first_page"`, `"last_page"`, `"all_pages"`, `"some_pages"`                                |
| `pages`                       | Specific pages for signature when `choice` is `some_pages`.       | `Set[NonNegativeInt]`                                                                       |


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
