# services/decision_engine.py
"""
Rule-based decision engine for document understanding.
Later, replace this logic with a trained model for intelligent decisions.
"""

def make_decision(document_type: str, extracted_fields: dict):
    """
    Makes a rule-based decision given a document type and extracted fields.
    Returns (decision, confidence).
    """
    decision = "Needs Review"
    confidence = 0.75

    document_type = (document_type or "").lower()
    print(f"🧠 Evaluating document type: {document_type}")

    if document_type == "invoice":
        amount = extracted_fields.get("total_amount")
        if amount:
            try:
                numeric_amount = float(str(amount).replace(",", "").replace("₹", "").strip())
                if numeric_amount < 1000:
                    decision, confidence = "Approved", 0.95
                elif numeric_amount > 50000:
                    decision, confidence = "Rejected", 0.90
                else:
                    decision, confidence = "Needs Review", 0.85
            except ValueError:
                print(f"⚠️ Invalid amount: {amount}")

    elif document_type == "resume":
        skills = [s.upper() for s in extracted_fields.get("skills", [])]
        if "AI" in skills or "MACHINE LEARNING" in skills:
            decision, confidence = "Shortlisted", 0.92
        else:
            decision, confidence = "Needs Review", 0.70

    elif document_type == "report":
        decision, confidence = "Analyzed", 0.88

    else:
        print(f"⚠️ Unknown document type: {document_type}")

    print(f"✅ Decision: {decision}, Confidence: {confidence}")
    return decision, confidence
