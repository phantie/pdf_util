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


from pdf_util import doc_to_images
from pdf_util import image_to_bytes
import fitz

images = []
for image in doc_to_images(fitz.Document(stream=value)):
    images.append(image_to_bytes(image))

for i, image in enumerate(images):
    with open(f"{i}.png", "wb+") as f:
        f.write(image)
