import pdfplumber

def extract_text_from_pdf(pdf_file) -> str:
    """
    Uploaded PDF file থেকে সব টেক্সট এক্সট্র্যাক্ট করে রিটার্ন করে।
    """
    extracted_text = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"
        return extracted_text.strip()
    except Exception as e:
        return f"Error reading PDF: {str(e)}"