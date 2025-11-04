# services/reasoning.py
import re

def _parse_amount(amount_str):
    try:
        if not amount_str:
            return None
        cleaned = re.sub(r'[^\d.]', '', amount_str.replace(",", ""))
        return float(cleaned) if cleaned else None
    except:
        return None

def validate_invoice(fields: dict) -> dict:
    """
    Example validator: checks the total_amount is numeric and returns confidence.
    This is a placeholder: a real system would parse line items and sum them.
    """
    total = _parse_amount(fields.get("total_amount"))
    if total is None:
        return {"decision": "Invalid", "confidence": 0.0, "reason": "no_total"}
    # Placeholder: we don't have line-items to compute; return Unchecked with confidence
    return {"decision": "Unchecked", "confidence": 0.5, "reason": "no_line_items_to_verify"}

def rank_resume(fields: dict, full_text: str) -> dict:
    """
    Simple resume scoring:
    - presence of email and phone
    - keywords: experience, python, machine learning, ai, leadership
    """
    score = 0.0
    if fields.get("email"):
        score += 0.3
    if fields.get("phone"):
        score += 0.2

    text = (full_text or "").lower()
    keywords = ["experience", "python", "machine learning", "deep learning", "nlp", "ai", "leadership"]
    found = sum(1 for k in keywords if k in text)
    score += min(found * 0.08, 0.4)  # up to 0.4

    decision = "Recommended" if score >= 0.6 else "Consider" if score >= 0.3 else "Reject"
    return {"decision": decision, "score": round(score, 2)}
