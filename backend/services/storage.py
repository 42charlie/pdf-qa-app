from fastapi import UploadFile, HTTPException
from config import UPLOAD_DIR
import os

'''save the uploaded file to the uploads directory'''
def save_file(file: UploadFile):
	uuid = os.urandom(16).hex()
	with open(UPLOAD_DIR / uuid, "wb") as f:
		content = file.file.read()
		if len(content) > 1024 * 1024 * 10:  # Limit file size to 10MB
			raise HTTPException(status_code=400, detail={"success": False, "uuid": None, "message": "File size exceeds the limit of 10MB."})
		f.write(content)
	return uuid