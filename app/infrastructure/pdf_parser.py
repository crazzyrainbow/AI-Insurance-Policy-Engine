import fitz
import pytesseract
from PIL import Image
import io


def extract_text(file_path: str):
    doc = fitz.open(file_path)
    pages = []

    for page_number, page in enumerate(doc):
        text = page.get_text()

        # OCR fallback if text empty
        if not text.strip():
            pix = page.get_pixmap()
            img_bytes = pix.tobytes("png")
            image = Image.open(io.BytesIO(img_bytes))
            text = pytesseract.image_to_string(image)

        pages.append({
            "page": page_number + 1,
            "text": text.strip()
        })

    return pages
