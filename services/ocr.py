# services/ocr.py
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import re
import os
from PyPDF2 import PdfReader

# ✅ Poppler path (update if needed)
POPLER_PATH = r"C:\Users\Lakhan Pal\Downloads\Release-25.07.0-0\poppler-25.07.0\Library\bin"

# ✅ Tesseract path (update if installed elsewhere)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# ---------------------------------------------------------------------
# 🧩 OCR Text Extraction (supports PDF & image)
# ---------------------------------------------------------------------
def extract_text_from_image(file_path: str) -> str:
    """
    Extract text from PDFs and image files using OCR.
    Automatically detects file type and handles multi-page PDFs.
    """
    text_all = ""

    # 🔹 If it's a PDF
    if file_path.lower().endswith(".pdf"):
        try:
            # Try to extract text directly (digital PDF)
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            if text.strip():
                return text.strip()
        except Exception:
            pass  # fallback to OCR below if text extraction fails

        # 🔹 Fallback to OCR (scanned PDF)
        pages = convert_from_path(file_path, dpi=200, poppler_path=POPLER_PATH)
        for i, page in enumerate(pages):
            img_path = f"{file_path}_page_{i}.jpg"
            page.save(img_path, "JPEG")
            text = pytesseract.image_to_string(Image.open(img_path))
            text_all += text + "\n"
            os.remove(img_path)
        return text_all.strip()

    # 🔹 If it's an image
    else:
        text = pytesseract.image_to_string(Image.open(file_path))
        return text.strip()


# ---------------------------------------------------------------------
# 🧩 Document Type Detection
# ---------------------------------------------------------------------
def detect_document_type(text: str) -> str:
    """
    Identify the type of document based on extracted text.
    """
    text_lower = text.lower()

    if any(keyword in text_lower for keyword in ["invoice", "amount", "bill", "gst", "total due", "billed to"]):
        return "invoice"

    elif any(keyword in text_lower for keyword in ["resume", "curriculum vitae", "experience", "education", "skills", "objective"]):
        return "resume"

    elif any(keyword in text_lower for keyword in ["report", "summary", "findings", "analysis", "project report"]):
        return "report"

    else:
        return "unknown"


# ---------------------------------------------------------------------
# 🧩 Key Field Extraction
# ---------------------------------------------------------------------
def extract_key_fields(doc_type: str, text: str) -> dict:
    """
    Extract structured fields based on the document type.
    """
    fields = {}

    # ==============================================================
    # 🧾 INVOICE
    # ==============================================================
    if doc_type == "invoice":
        clean_text = text.replace("\n", " ").replace("\r", " ")

        # 🔹 Invoice Number
        invoice_no = re.search(
            r"(?:invoice\s*(?:no|number|#)[:\s-]*([A-Z0-9-]+))", clean_text, re.IGNORECASE
        )

        # 🔹 Total / Amount
        total = re.search(
            r"(?:total\s*(?:amount)?|amount\s*(?:due|payable)?)[\s:₹$]*([\d,]+(?:\.\d{1,2})?)",
            clean_text, re.IGNORECASE
        )

        # 🔹 Date (DD/MM/YYYY or YYYY-MM-DD)
        date = re.search(
            r"\b(?:\d{2}[/-]\d{2}[/-]\d{4}|\d{4}[/-]\d{2}[/-]\d{2})\b", clean_text
        )

        fields = {
            "invoice_no": invoice_no.group(1).strip() if invoice_no else None,
            "total_amount": total.group(1).strip() if total else None,
            "date": date.group(0) if date else None
        }

    # ==============================================================
    # 👨‍💻 RESUME
    # ==============================================================
    elif doc_type == "resume":
        # 🔹 Clean OCR text
        clean_text = text.replace("\n", " ").replace("\r", " ").strip()

        # 🔹 Email
        email_match = re.search(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", clean_text
        )
        email = email_match.group(0).lower() if email_match else None

        # 🔹 Phone Number
        phone_match = re.search(r"\b(?:\+91[-\s]?)?\d{10}\b", clean_text)
        phone = phone_match.group(0) if phone_match else None

        # 🔹 Name Detection (better)
        name = None
        name_match = re.search(r"Name[:\s]*([A-Z][A-Za-z\s]+)", text)
        if name_match:
            name = name_match.group(1).strip()
        else:
            # Look at first few lines for capitalized full name
            lines = text.strip().splitlines()
            for line in lines[:5]:
                line = line.strip()
                if re.match(r"^[A-Z][a-zA-Z\s]{2,25}$", line):
                    name = line
                    break

        # 🔹 Skills (AI stack)
        skill_keywords = [
            "Python", "Java", "C++", "AI", "Machine Learning", "Deep Learning",
            "Data Science", "NLP", "TensorFlow", "PyTorch", "SQL", "Flask", "Django"
        ]
        skills = [s for s in skill_keywords if re.search(s, text, re.IGNORECASE)]

        fields = {
            "name": name,
            "email": email,
            "phone": phone,
            "skills": skills
        }

    # ==============================================================
    # 📊 REPORT
    # ==============================================================
    elif doc_type == "report":
        title = re.search(r"(?:Report Title|Title)[:\s]*(.*)", text)
        date = re.search(
            r"\b(?:\d{2}[/-]\d{2}[/-]\d{4}|\d{4}[/-]\d{2}[/-]\d{2})\b", text
        )
        summary = re.search(r"(?:Summary|Abstract)[:\s]*(.*)", text)
        fields = {
            "title": title.group(1).strip() if title else None,
            "date": date.group(0) if date else None,
            "summary": summary.group(1).strip() if summary else None
        }

    # ==============================================================
    # ❓ UNKNOWN
    # ==============================================================
    else:
        fields = {"note": "No structured fields found for this document type."}

    return fields
