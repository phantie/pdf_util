from pdf_util.visually_sign_doc.params import SignDocParams
from pdf_util.visually_sign_doc._util import pages_to_sign_to_indeces
from pdf_util.visually_sign_doc.visually_sign_page import visually_sign_page

import fitz



def visually_sign_doc(pdf_contents: bytes, params: SignDocParams) -> bytes:
    pdf_document = fitz.open(stream=pdf_contents, filetype="pdf")

    for idx in pages_to_sign_to_indeces(pages_to_sign=params.pages_to_sign, page_count=pdf_document.page_count):
        page: fitz.Page = pdf_document[idx]
        visually_sign_page(page=page, params=params.page_params)

    pdf_output = pdf_document.write()
    pdf_document.close()

    # IMPORTANT step for pyhanko to not break when opening returned bytes
    # no idea what it actually does, but it works
    import pypdf
    from io import BytesIO
    import pdf_util
    w = pypdf.PdfWriter(BytesIO(pdf_output))
    value = pdf_util.bytes_from_writer(w)

    return value
