from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from services.file_validation import validate_document
from services.storage import save_file
from services.text_extraction import extract_pages_from_pdf, validate_text, clean_txt
from services.chunker import chunk_text
#database imports
from services.database import insert_document, insert_chunks

route = APIRouter(prefix="/documents", tags=["Documents"])

@route.post("/upload")
async def upload(file: UploadFile = File(...)):
	#Check file type
	if not file or not validate_document(file):
		return JSONResponse(content={"success": False, "message": "Invalid or unsupported file"}, status_code=400)
	
	#save file to the uploads directory
	uuid = save_file(file)

	#extract text from the PDF (placeholder for actual extraction logic)
	pages = extract_pages_from_pdf(uuid)
	clean_text = clean_txt(pages)
	validated_text = validate_text(clean_text)

	chunks = chunk_text(validated_text)

	#store document metadata and chunks in the database
	try:
		insert_document(uuid, file.filename, uuid, validated_text)
		insert_chunks(chunks, uuid)
	except Exception as e:
		print(f"Database error: {e}")
		return JSONResponse(content={"success": False, "message": "Database error"}, status_code=500)

	return JSONResponse(content={"success": True, "uuid": uuid, "message": "File uploaded successfully."})  # Return a preview of the extracted text

#TODO : add endpoint to retrieve document metadata and text by UUID