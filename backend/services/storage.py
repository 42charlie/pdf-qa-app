from fastapi import UploadFile, HTTPException
from config import UPLOAD_DIR
import os

def human_readable_size(size):
    """Convert bytes to human readable format"""
    for unit in ['B', 'KB', 'MB']:
        if size < 1024.0:
            break
        size /= 1024.0
    return f"{size:.2f} {unit}"

'''save the uploaded file to the uploads directory'''
def save_file(file: UploadFile):
	uuid = os.urandom(16).hex()
	with open(UPLOAD_DIR / uuid, "wb") as f:
		content = file.file.read()
		if len(content) > 1024 * 1024 * 10:  # Limit file size to 10MB
			raise HTTPException(status_code=400, detail={"success": False, "uuid": None, "message": "File size exceeds the limit of 10MB."})
		f.write(content)
	return uuid