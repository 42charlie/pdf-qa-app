from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse

# Import service functions
from services.file_validation import validate_document
from services.storage import save_file
from services.text_extraction import extract_pages_from_pdf, validate_text, clean_txt
from services.chunker import chunk_text
from services.embedding import generate_embeddings, save_embeddings

#database imports
from services.database import get_chunks_ids, insert_document, insert_chunks, get_document_chunks_by_uuid, get_document_by_uuid, document_exists

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
		insert_document(uuid, file.filename, validated_text, len(chunks))
		insert_chunks(chunks, uuid)
		chunk_ids = get_chunks_ids(uuid)
	except Exception as e:
		print(f"Database error: {e}")
		return JSONResponse(content={"success": False, "message": "Database error"}, status_code=500)

	#embed chunks and store embeddings in the vector database
	embeddings = generate_embeddings(chunks)
	save_embeddings(embeddings, chunk_ids, uuid)

	return JSONResponse(content={"success": True, "uuid": uuid, "message": "File uploaded successfully."})  # Return a preview of the extracted text

@route.get("/{uuid}")
async def get_document(uuid: str):
	# Placeholder for fetching document metadata and chunks from the database
	try:
		document = get_document_by_uuid(uuid)  # Implement this function to fetch document metadata
	except Exception as e:
		print(f"Database error: {e}")
		return JSONResponse(content={"success": False, "message": "Database error"}, status_code=500)

	if not document:
		return JSONResponse(content={"success": False, "message": "Document not found"}, status_code=404)

	return JSONResponse(content={"success": True, "document": document})

@route.get("/{uuid}/chunks")
async def get_document_chunks(uuid: str):
	# Placeholder for fetching document chunks from the database
	if not document_exists(uuid):
		return JSONResponse(content={"success": False, "message": "Document not found"}, status_code=404)
	try:
		chunks = get_document_chunks_by_uuid(uuid)  # Implement this function to fetch chunks based on document UUID
	except Exception as e:
		print(f"Database error: {e}")
		return JSONResponse(content={"success": False, "message": "Database error"}, status_code=500)

	return JSONResponse(content={"success": True, "chunks": chunks})