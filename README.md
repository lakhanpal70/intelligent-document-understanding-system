🧠 End-to-End AI System for Intelligent Document Understanding and Automated Decision-Making
🚀 Overview

This project implements an AI-powered document understanding system capable of reading, extracting, and interpreting data from unstructured business documents such as resumes, invoices, and reports.

The system combines OCR, NLP, and machine learning models to automate document classification, field extraction, and decision-making — reducing manual review time and improving data accuracy.

📂 Project Structure
📦 intelligent-document-understanding-system/
├── api/                 # FastAPI backend for ML model serving
├── frontend/            # Web interface (HTML/CSS/JS)
├── services/            # Utility and processing services
├── training/            # Model training and evaluation scripts
├── tests/               # Unit and integration tests
├── outputs/             # Model outputs and results
├── requirements.txt     # Python dependencies
├── .gitignore           # Ignored files and directories
└── README.md            # Project documentation

⚙️ Features

✅ Intelligent document parsing and text extraction
✅ Named Entity Recognition (NER) for field detection
✅ Resume and invoice understanding
✅ Decision-making pipeline (accept/reject logic)
✅ REST API with FastAPI
✅ Interactive web frontend for document upload and result visualization
✅ Dockerized deployment





                +-------------------------+
                |   Web Interface (UI)    |
                +-----------+-------------+
                            |
                            ▼
                +-------------------------+
                |     REST API (FastAPI)  |
                +-----------+-------------+
                            |
                            ▼
            +---------------------------------------+
            |     ML Model: Document Understanding   |
            |  - OCR Text Extraction                 |
            |  - NLP Field Extraction (NER)          |
            |  - Decision Model                      |
            +---------------------------------------+
                            |
                            ▼
                +-------------------------+
                |    Database / Storage   |
                +-------------------------+





🧠 Model Pipeline

Preprocessing – Text extraction from PDFs/images

Feature Extraction – NLP-based entity tagging and vectorization

Model Training – Using Transformer-based architecture (BERT / LayoutLM)

Evaluation – Accuracy, Precision, Recall, and F1 Score

Inference API – Serve model via FastAPI



🧪 Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/lakhanpal70/intelligent-document-understanding-system.git
cd intelligent-document-understanding-system

2️⃣ Create Virtual Environment
python -m venv .venv
source .venv/bin/activate   # (Linux/Mac)
.venv\Scripts\activate      # (Windows)

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run the Backend (FastAPI)
uvicorn api.main:app --reload


Open in browser → http://127.0.0.1:8000/docs

5️⃣ Run the Frontend

Open frontend/index.html in your browser.

🐳 Docker Deployment

Build and run using Docker:

docker build -t intelligent-doc-ai .
docker run -p 8000:8000 intelligent-doc-ai

📘 Dataset Description

Used a combination of synthetic and publicly available datasets (resumes, invoices, ID cards) to train and evaluate models for text extraction and structured field understanding.

📈 Results & Future Improvements

✅ Achieved high accuracy in field extraction and classification
✅ Scalable API for production use

🔮 Future Enhancements:

Fine-tune transformer models with more diverse data

Add support for multilingual document processing

Integrate advanced OCR (Tesseract + LayoutLMv3)

Deploy on cloud (AWS / Render / HuggingFace Spaces)

👨‍💻 Author

Lakhan Pal
AI Developer | Machine Learning Engineer
📧 lakhanpal7400@gmail.com

🪪 License

This project is licensed under the MIT License
.
