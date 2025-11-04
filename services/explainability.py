"""
services/explainability.py
Generates explainability visualizations for extracted document fields.
- Supports both PDFs and image files.
- Returns a web-accessible path for the FastAPI frontend.
"""

from PIL import Image, ImageDraw, ImageFont
from pdf2image import convert_from_path
import os

# ✅ Poppler path for Windows (change if needed)
POPLER_PATH = r"C:\Users\Lakhan Pal\Downloads\Release-25.07.0-0\poppler-25.07.0\Library\bin"

def highlight_text_areas(image_path: str, extracted_fields: dict):
    """
    Highlights key fields detected in the document.
    Returns a relative web path (e.g. /outputs/file_highlighted.png)
    """
    try:
        # --- Step 1: Validate file ---
        if not os.path.exists(image_path):
            print(f"⚠️ File not found: {image_path}")
            return None

        # --- Step 2: Convert PDF → image if necessary ---
        if image_path.lower().endswith(".pdf"):
            pages = convert_from_path(image_path, dpi=200, poppler_path=POPLER_PATH)
            if not pages or len(pages) == 0:
                print("⚠️ No pages found in PDF.")
                return None

            pdf_img_path = image_path.replace(".pdf", "_page1.jpg")
            pages[0].save(pdf_img_path, "JPEG")
            image_path = pdf_img_path

        # --- Step 3: Open image ---
        img = Image.open(image_path).convert("RGB")
        draw = ImageDraw.Draw(img)

        # --- Step 4: Color mapping for different fields ---
        colors = {
            "name": "blue",
            "email": "green",
            "phone": "purple",
            "invoice_no": "orange",
            "total_amount": "red",
            "date": "yellow"
        }

        # --- Step 5: Draw highlights for each extracted field ---
        y = 30
        for field, value in extracted_fields.items():
            color = colors.get(field, "gray")
            draw.rectangle([(20, y), (500, y + 50)], outline=color, width=3)
            draw.text((30, y + 15), f"{field}: {value}", fill=color)
            y += 70

        # --- Step 6: Save the output image ---
        os.makedirs("outputs", exist_ok=True)
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        clean_name = f"{base_name}_highlighted.png"
        output_path = os.path.join("outputs", clean_name)
        img.save(output_path)

        abs_path = os.path.abspath(output_path)
        print(f"✅ Explainability image saved at: {abs_path}")

        # --- Step 7: Return a web-accessible path for frontend ---
        return f"/outputs/{clean_name}"

    except Exception as e:
        print(f"❌ Explainability generation failed: {e}")
        return None
