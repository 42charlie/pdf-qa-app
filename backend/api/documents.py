from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse

# Import service functions
from services.file_validation import sanitize_for_display, validate_document
from services.storage import check_file_size, human_readable_size, save_file
from services.text_extraction import extract_pages_from_pdf, validate_text, clean_txt
from services.chunker import chunk_text
from services.embedding import generate_embeddings, save_embeddings

#database imports
from services.database import get_chunks_ids, get_document_text, insert_document, insert_chunks, get_document_chunks_by_uuid, get_document_by_uuid, document_exists, update_document_activity

route = APIRouter(prefix="/documents", tags=["Documents"])

@route.post("/upload")
async def upload(file: UploadFile = File(...)):

	file.filename = sanitize_for_display(file.filename)
	#Check file type
	if not file or not validate_document(file):
		return JSONResponse(content={"success": False, "error": "Invalid or unsupported file"}, status_code=400)
	
	#save file to the uploads directory
	content_size, content = check_file_size(file.file)
	if not content:
		return JSONResponse(content={"success": False, "error": "File size exceeds the limit of 10MB."}, status_code=400)
	uuid = save_file(content)

	#extract text from the PDF (placeholder for actual extraction logic)
	pages = extract_pages_from_pdf(uuid)
	clean_text = clean_txt(pages)
	validated_text = validate_text(clean_text)

	chunks = chunk_text(validated_text)

	#store document metadata and chunks in the database
	try:
		insert_document(uuid, file.filename, validated_text, len(chunks), pages[-1]['page'])
		insert_chunks(chunks, uuid)
		chunk_ids = get_chunks_ids(uuid)
	except Exception as e:
		print(f"Database error: {e}")
		return JSONResponse(content={"success": False, "error": "Database error, Please try again."}, status_code=500)

	#embed chunks and store embeddings in the vector database
	chunks = [chunk['content'] for chunk in chunks]  #extract just the text for embedding
	embeddings = generate_embeddings(chunks)
	save_embeddings(embeddings, chunk_ids, uuid)

	response = {
		"success": True,
		"metadata": {
			"id": uuid,
			"filename": file.filename,
			"chunk_count": len(chunks),
			"pages": pages[-1]['page'],
			"character_count": len(validated_text),
			"size": human_readable_size(content_size)
		}
	}

	return JSONResponse(content=response) 

@route.get("/{uuid}")
async def get_document(uuid: str):
	''' Placeholder for fetching document metadata and chunks from the database '''
	try:
		update_document_activity(uuid)
		document = get_document_by_uuid(uuid)  # Implement this function to fetch document metadata
	except Exception as e:
		print(f"Database error: {e}")
		return JSONResponse(content={"success": False, "message": "Database error"}, status_code=500)

	if not document:
		return JSONResponse(content={"success": False, "message": "Document not found"}, status_code=404)

	return JSONResponse(content={"success": True, "document": document})

@route.get("/{uuid}/preview")
async def get_document_chunks(uuid: str):
	''' Placeholder for fetching document chunks from the database '''
	try:
		if not document_exists(uuid):
			return JSONResponse(content={"success": False, "error": "Document not found. Please try again."}, status_code=404)
		update_document_activity(uuid)
		chunks = get_document_chunks_by_uuid(uuid)  # Implement this function to fetch chunks based on document UUID
		text_preview = get_document_text(uuid)
	except Exception as e:
		print(f"Database error: {e}")
		return JSONResponse(content={"success": False, "error": "Database error. Please try again."}, status_code=500)

	return JSONResponse(content={"success": True, "text": text_preview, "chunks": chunks})