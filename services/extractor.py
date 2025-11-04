# services/extractor.py
import re

def detect_document_type(text: str) -> str:
    """Robust detection of invoice/resume/report from extracted text."""
    if not text:
        return "unknown"
    t = text.lower()
    if any(x in t for x in ["invoice", "amount", "bill", "gst", "invoice no", "tax"]):
        return "invoice"
    if any(x in t for x in ["resume", "curriculum vitae", "cv", "experience", "education", "skills"]):
        return "resume"
    if any(x in t for x in ["report", "summary", "findings", "conclusion", "analysis"]):
        return "report"
    return "unknown"


def extract_key_fields(doc_type: str, text: str) -> dict:
    """Extract fields for invoice/resume/report."""
    fields = {}
    if not text:
        return fields

    if doc_type == "invoice":
        # invoice number
        invoice_no = re.search(r"(?:invoice[:\s]*|inv[-\s:]*)?([A-Z0-9\-]{4,20})", text, re.IGNORECASE)
        # amount (try multiple patterns)
        total = re.search(r"(?:total\s*[:\-\s]|amount\s*[:\-\s]|grand total[:\-\s]|amount payable[:\-\s])?₹?\s*([0-9\.,]+)", text, re.IGNORECASE)
        vendor = re.search(r"([A-Z][A-Za-z&\-\s]{3,50}(?:Pvt|Ltd|LLP|Solutions|Technologies|Corporation|Inc)?)", text)
        fields["invoice_no"] = invoice_no.group(1) if invoice_no else None
        fields["total_amount"] = total.group(1) if total else None
        fields["vendor"] = vendor.group(1) if vendor else None

    elif doc_type == "resume":
        name = re.search(r"^(?:name[:\s]*)?([A-Z][a-zA-Z]{2,}(?:\s+[A-Z][a-zA-Z]{2,}){0,3})", text)
        email = re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", text)
        phone = re.search(r"\b(?:\+91|0)?\s*([6-9]\d{9})\b", text)
        # try to be flexible: if no Name pattern, search for lines with capitalized words + common resume headers
        fields["name"] = name.group(1).strip() if name else None
        fields["email"] = email.group(0) if email else None
        fields["phone"] = phone.group(1) if phone else None

    elif doc_type == "report":
        title = re.search(r"(?:title[:\s]*)?(.{5,120})", text, re.IGNORECASE)
        date = re.search(r"\b(\d{1,2}[\/\-\.\s]\d{1,2}[\/\-\.\s]\d{2,4})\b", text)
        fields["title"] = title.group(1).strip() if title else None
        fields["date"] = date.group(1) if date else None

    return fields
