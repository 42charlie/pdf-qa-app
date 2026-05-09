from config import UPLOAD_DIR
import uuid

def human_readable_size(size):
    """Convert bytes to human readable format"""
    for unit in ['B', 'KB', 'MB']:
        if size < 1024.0:
            break
        size /= 1024.0
    return f"{size:.2f} {unit}"

'''save the uploaded file to the uploads directory'''
def save_file(content: bytes) -> str:
	document_id = str(uuid.uuid4())
	with open(UPLOAD_DIR / document_id, "wb") as f:
		f.write(content)
	return document_id

def check_file_size(file) -> bytes:
	'''Check if the file size is within the allowed limit (10MB)'''
	content = bytearray()
	while chunk := file.read(1024 * 1024):  # Read in 1MB chunks
		content.extend(chunk)
		if len(content) > 10 * 1024 * 1024:  # Check if size exceeds 10MB
			return None
	return len(content), bytes(content)