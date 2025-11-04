# api/main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import shutil, os

# Import core services
from services.ocr import extract_text_from_image, detect_document_type, extract_key_fields
from services.decision_engine import make_decision
from services.explainability import highlight_text_areas
from api.schemas import InferenceResponse

# -------------------------------------------------------
# 🌟 FastAPI App Initialization
# -------------------------------------------------------
app = FastAPI(title="🌟 Intelligent Document Understanding and Automated Decision-Making API")

# Allow frontend (HTML) to connect to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict later to ["http://127.0.0.1:5500"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Serve explainability images (output visualization)
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")


# -------------------------------------------------------
# 🏠 Root Endpoint
# -------------------------------------------------------
@app.get("/")
def root():
    return {"message": "🚀 API is running successfully!"}


# -------------------------------------------------------
# 🧠 Main AI Endpoint
# -------------------------------------------------------
@app.post("/analyze_document/", response_model=InferenceResponse)
async def analyze_document(file: UploadFile = File(...)):
    """
    Full AI pipeline:
    1️⃣ Save uploaded file
    2️⃣ OCR text extraction
    3️⃣ Document type detection
    4️⃣ Key field extraction
    5️⃣ Automated decision-making
    6️⃣ Explainability visualization
    """
    # --- Step 1: Save uploaded file temporarily
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # --- Step 2: OCR / Text extraction
    text = extract_text_from_image(temp_path)

    # --- Step 3: Document type & key field extraction
    doc_type = detect_document_type(text)
    key_fields = extract_key_fields(doc_type, text)

    # --- Step 4: Decision logic
    decision, confidence = make_decision(doc_type, key_fields)

    # --- Step 5: Explainability (highlight)
    explain_map = highlight_text_areas(temp_path, key_fields)

    # --- Step 6: Build consistent response (match schema + frontend)
    response = {
        "document_type": doc_type,
        "fields_extracted": key_fields,
        "decision": decision,
        "confidence_score": confidence,
        "explainability_map": explain_map or "N/A"
    }

    # Optional cleanup
    # os.remove(temp_path)

    return JSONResponse(response)
