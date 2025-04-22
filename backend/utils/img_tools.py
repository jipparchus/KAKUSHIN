import zipfile
from io import BytesIO
from typing import List
import base64


def make_zip(images: List[bytes]) -> BytesIO:
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for idx, img_bytes in enumerate(images):
            zip_file.writestr(f"annotated_{idx}.jpg", img_bytes)
    zip_buffer.seek(0)
    return zip_buffer


def encode_images(images):
    return [base64.b64encode(img).decode() for img in images]
