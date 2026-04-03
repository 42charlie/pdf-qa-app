import fitz  # PyMuPDF
import os
from config import UPLOAD_DIR

def extract_text_from_pdf(filename: str) -> dict:
	file_path = UPLOAD_DIR / filename
	try:
		document = fitz.open(file_path)
		pages = []
		for i, page in enumerate(document):
			pages.append(
				{
					"page": i + 1,
					"text": page.get_text()
				}
			)
		document.close()
	except Exception:
		raise ValueError(f"Failed to read PDF")
	full_text = "\n".join([page["text"] for page in pages])
	if not full_text or len(full_text.strip()) < 100:  # Arbitrary threshold for minimum text length
		raise ValueError("Extracted text is too short")
	full_text = "\n".join([line.strip() for line in full_text.splitlines() if line.strip()])

	os.remove(file_path)  # Clean up the uploaded file after extraction
	return {"text": full_text, "pages": pages}