# tests/test_api.py
"""
Automated tests for FastAPI backend.
Covers root endpoint and /extract_text/ (with and without files).
"""

from fastapi.testclient import TestClient
from api.main import app
import io

client = TestClient(app)

def test_root():
    res = client.get("/")
    assert res.status_code == 200
    assert "Document Understanding" in res.json()["message"]

def test_extract_no_file():
    res = client.post("/extract_text/")
    assert res.status_code in [400, 422]

def test_extract_invalid_file_type():
    fake_file = io.BytesIO(b"not a pdf")
    res = client.post("/extract_text/", files={"file": ("fake.txt", fake_file, "text/plain")})
    assert res.status_code == 400
    assert "Only PDF" in res.json()["detail"]

def test_extract_with_pdf():
    # create a simple fake PDF in memory
    pdf_bytes = b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\ntrailer<</Root 1 0 R>>%%EOF"
    res = client.post("/extract_text/", files={"file": ("sample.pdf", io.BytesIO(pdf_bytes), "application/pdf")})
    assert res.status_code == 200
    data = res.json()
    assert "file_name" in data
    assert "extracted_text" in data
