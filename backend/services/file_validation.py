from fastapi import UploadFile

def validate_mime_type(file: UploadFile):
	if file.content_type != "application/pdf":
		print("[!] validate_mime_type")
		return False
	return True
def validate_extension(file: UploadFile):
	if not file.filename.endswith((".pdf")):
		print("[!] validate_extension")
		return False
	return True
def validate_magic_bytes(file: UploadFile):
	magic_bytes = file.file.read(5)
	file.file.seek(0)  # Reset file pointer after reading
	if magic_bytes != b"%PDF-" or len(magic_bytes) < 5:
		print("[!] validate_magic_bytes")
		return False
	return True

'''validate the uploaded file'''
def validate_document(file: UploadFile):
	if file.file is None:
		print("[!] file is None")
		return False
	if not validate_mime_type(file):
		return False
	if not validate_extension(file):
		return False
	if not validate_magic_bytes(file):
		return False
	return True