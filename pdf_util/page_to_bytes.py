from io import BytesIO
from pypdf import PageObject
from pypdf import PdfWriter



def page_to_bytes(page: PageObject) -> bytes:
    writer = PdfWriter()
    writer.add_page(page)

    buffer = BytesIO()
    writer.write(buffer)
    buffer.seek(0)

    return buffer.read()


