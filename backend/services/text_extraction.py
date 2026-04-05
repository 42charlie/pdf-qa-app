import fitz  # PyMuPDF
import os
from config import UPLOAD_DIR

def clean_txt(pages: list) -> str:
    cleaned_pages = []

    for page in pages:
        text = page["text"]

        # Normalize line breaks
        text = text.replace("\r\n", "\n").replace("\r", "\n")

        # Fix ligatures
        text = (
            text.replace("ﬀ", "ff")
                .replace("ﬁ", "fi")
                .replace("ﬂ", "fl")
                .replace("ﬃ", "ffi")
                .replace("ﬄ", "ffl")
        )

        # Fix hyphenated line breaks (word-\nword → wordword)
        lines = text.split("\n")
        fixed_lines = []
        i = 0

        while i < len(lines):
            line = lines[i].strip()
			
            # Preserve blank lines: they may indicate paragraph boundaries
            if line == "":
                fixed_lines.append("")
                i += 1
                continue

            # Remove standalone noise lines (like "1", "2", etc.)
            if line.isdigit():
                prev_is_blank = (len(fixed_lines) == 0 or fixed_lines[-1] == "")
                next_is_blank = (i + 1 >= len(lines) or lines[i + 1].strip() == "" or lines[i + 1].strip().isdigit())
                if prev_is_blank or next_is_blank:
                    i += 1
                    continue

            # Fix hyphenated word at line break: "exam-\nple" -> "example"
            if line.endswith("-") and i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line:
                    line = line[:-1] + next_line
                    i += 1  # consume next line

            fixed_lines.append(line)
            i += 1

        # Remove repeated blank lines, but keep single blank lines
        normalized_lines = []
        previous_blank = False

        for line in fixed_lines:
            is_blank = (line == "")
            if is_blank:
                if not previous_blank:
                    normalized_lines.append("")
                previous_blank = True
            else:
                normalized_lines.append(line)
                previous_blank = False

        page_text = "\n".join(normalized_lines).strip()

        if page_text:
            cleaned_pages.append(page_text)

    # Preserve page separation with double newline
    full_text = "\n\n".join(cleaned_pages)

    return full_text.strip()

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