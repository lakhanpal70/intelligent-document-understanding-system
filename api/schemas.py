# api/schemas.py
from pydantic import BaseModel
from typing import Dict, Any

class InferenceResponse(BaseModel):
    document_type: str
    fields_extracted: Dict[str, Any]
    decision: str
    confidence_score: float
    explainability_map: str
