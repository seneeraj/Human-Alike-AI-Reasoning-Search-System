from pypdf import PdfReader
import os

def extract_text_from_pdf(uploaded_file):
    text = ""
    file_bytes = uploaded_file.read()

    # ---------------- DETECT ENV ----------------
    is_cloud = os.environ.get("STREAMLIT_SERVER_PORT") is not None

    # ---------------- OCR BLOCK (LOCAL ONLY) ----------------
    if not is_cloud:
        try:
            from pdf2image import convert_from_bytes
            import pytesseract

            # 👉 set local paths ONLY here
            pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

            images = convert_from_bytes(
                file_bytes,
                poppler_path=r"C:\Users\senee\Downloads\Release-25.12.0-0\poppler-25.12.0\Library\bin"
            )

            for img in images[:50]:
                text += pytesseract.image_to_string(img)

            if text.strip():
                return text

        except Exception as e:
            print("OCR failed:", e)

    # ---------------- FALLBACK (CLOUD SAFE) ----------------
    try:
        import io
        reader = PdfReader(io.BytesIO(file_bytes))

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

        if text.strip():
            return text

        return "ERROR: No readable text found"

    except Exception as e:
        return f"ERROR: Unable to read PDF - {str(e)}"