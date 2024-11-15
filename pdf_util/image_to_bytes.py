from io import BytesIO
from PIL.Image import Image



def image_to_bytes(image: Image) -> bytes:
    bio = BytesIO()
    image.save(bio, format="png")
    return bio.getvalue()