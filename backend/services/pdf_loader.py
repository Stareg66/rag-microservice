from pypdf import PdfReader

class PDFLoader:
    
    def __init__(self):
        pass

    def load_pdf(self, pdf_path: str) -> str:
        try:
            reader = PdfReader(pdf_path)
            pages_text = []

            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    pages_text.append(page_text)

            return "\n".join(pages_text)

        except Exception as e:
            print(f"[PDFLoader] Error loading PDF: {e}")
            return None

def test_pdf_text_extract(pdf_path: str) -> str:
    loader = PDFLoader()
    return loader.load_pdf(pdf_path)