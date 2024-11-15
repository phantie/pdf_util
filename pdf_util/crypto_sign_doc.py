from io import BytesIO
from typing import Optional

from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.sign import signers
import tempfile


async def crypto_sign_doc(pdf_contents: bytes, pfx_data: bytes, passphrase: Optional[bytes] = None) -> bytes:
    with tempfile.NamedTemporaryFile("wb+") as f:
        f.write(pfx_data)
        signer = signers.SimpleSigner.load_pkcs12(pfx_file=f.name, passphrase=passphrase)
        assert signer is not None

    meta = signers.PdfSignatureMetadata(field_name='Signature_' + str(0))

    out: BytesIO = await signers.async_sign_pdf(
        IncrementalPdfFileWriter(BytesIO(pdf_contents)),
        meta,
        signer=signer,
    )

    result = out.getvalue()

    return result

