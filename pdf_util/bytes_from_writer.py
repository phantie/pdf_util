from io import BytesIO
from pypdf import PdfWriter


def bytes_from_writer(writer: PdfWriter) -> bytes:
    bio = BytesIO()
    writer.write(bio)
    return bio.getvalue()


