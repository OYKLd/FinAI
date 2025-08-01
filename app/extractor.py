# app/extractor.py
import pandas as pd
import pdfplumber
import pytesseract
from PIL import Image
import docx
from io import BytesIO

async def extract_data(files):
    result = []
    for file in files:
        name = file.filename.lower()
        content = None
        raw = await file.read()
        stream = BytesIO(raw)
        if name.endswith(".xlsx") or name.endswith(".xls"):
            df = pd.read_excel(stream)
            content = {"type": "table", "data": df}
        elif name.endswith(".csv"):
            df = pd.read_csv(stream)
            content = {"type": "table", "data": df}
        elif name.endswith(".docx"):
            doc = docx.Document(stream)
            text = "\n".join([p.text for p in doc.paragraphs])
            content = {"type": "text", "data": text}
        elif name.endswith(".pdf"):
            text_pages = []
            tables = []
            with pdfplumber.open(stream) as pdf:
                for page in pdf.pages:
                    t = page.extract_text()
                    if t:
                        text_pages.append(t)
                    for tbl in page.extract_tables():
                        df = pd.DataFrame(tbl[1:], columns=tbl[0])
                        tables.append(df)
                if not text_pages:
                    for page in pdf.pages:
                        img = page.to_image(resolution=300).original
                        ocr_text = pytesseract.image_to_string(img)
                        text_pages.append(ocr_text)
            content = {"type": "pdf", "text": "\n".join(text_pages), "tables": tables}
        if content:
            result.append(content)
    return result