from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from services.file_validation import validate_document
from services.storage import save_file
from services.text_extraction import extract_text_from_pdf

route = APIRouter(prefix="/documents", tags=["Documents"])

@route.post("/upload")
async def upload(file: UploadFile = File(...)):
	#Check file type
	if not file or not validate_document(file):
		return JSONResponse(content={"success": False, "message": "Invalid or unsupported file"}, status_code=400)
	
	#save file to the uploads directory
	uuid = save_file(file)

	#extract text from the PDF (placeholder for actual extraction logic)
	text, pages = extract_text_from_pdf(uuid)

	# TODO: save to database

	return JSONResponse(content={"success": True, "uuid": uuid, "message": "File uploaded successfully."})  # Return a preview of the extracted text

#TODO : add endpoint to retrieve document metadata and text by UUID