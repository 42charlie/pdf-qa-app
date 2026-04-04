import fitz  # PyMuPDF
import os
from config import UPLOAD_DIR

def clean_txt(pages: list) -> str:
    cleaned_pages = []

    for page in pages:
        text = page["text"]

        # Normalize line breaks
        text = text.replace("\r", "\n")

        # Fix ligatures
        text = text.replace("ﬀ", "ff").replace("ﬁ", "fi").replace("ﬂ", "fl")

        # Fix hyphenated line breaks (word-\nword → wordword)
        lines = text.split("\n")
        fixed_lines = []
        i = 0

        while i < len(lines):
            line = lines[i].strip()

            # Remove standalone noise lines (like "1", "2", etc.)
            if line.isdigit():
                i += 1
                continue

            # Handle hyphenation
            if line.endswith("-") and i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                line = line[:-1] + next_line
                i += 1  # skip next line

            fixed_lines.append(line)
            i += 1

        text = "\n".join(fixed_lines)

        cleaned_pages.append(text.strip())

    # Combine pages
    full_text = "\n".join(cleaned_pages)

    # Final cleanup
    full_text = "\n".join(line.strip() for line in full_text.splitlines() if line.strip())

    return full_text

def validate_text(clean_text: str) -> str:
	if not clean_text or len(clean_text.strip()) < 100:  # Arbitrary threshold for minimum text length
		raise ValueError("Extracted text is too short")
	return clean_text

def extract_pages_from_pdf(filename: str) -> dict:
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
	os.remove(file_path)  # Clean up the uploaded file after extraction
	return pages