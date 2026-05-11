from fastapi import APIRouter, Request, UploadFile, File, BackgroundTasks
from fastapi.responses import JSONResponse

# Import service functions
from services.file_validation import sanitize_for_display, validate_document
from services.storage import check_file_size, human_readable_size, save_file
from services.text_extraction import extract_pages_from_pdf, validate_text, clean_txt
from services.chunker import chunk_text
from services.embedding import process_embeddings_background
from db.qdrant import get_chunk_context_by_index, get_document_chunks_by_uuid
from services.rate_limiter import limiter

#database imports
from db.postgres import get_document_text, insert_document, get_document_by_uuid, document_exists, update_document_activity

route = APIRouter(prefix="/documents", tags=["Documents"])

@route.post("/upload")
@limiter.limit("3/minute")
async def upload(request: Request, file: UploadFile = File(...), background_tasks: BackgroundTasks = None):

	file.filename = sanitize_for_display(file.filename)
	#Check file type
	if not file or not validate_document(file):
		return JSONResponse(content={"success": False, "error": "Invalid or unsupported file"}, status_code=400)
	
	#save file to the uploads directory
	content_size, content = check_file_size(file.file)
	if not content:
		return JSONResponse(content={"success": False, "error": "File size exceeds the limit of 10MB."}, status_code=400)
	document_id = save_file(content)

	#extract text from the PDF (placeholder for actual extraction logic)
	pages = extract_pages_from_pdf(document_id)
	clean_text = clean_txt(pages)
	validated_text = validate_text(clean_text)

	chunks = chunk_text(validated_text)

	#store document metadata and chunks in the database
	try:
		await insert_document(document_id, file.filename, validated_text, len(chunks), pages[-1]['page'])
	except Exception as e:
		print(f"Database error: {e}")
		return JSONResponse(content={"success": False, "error": "Database error, Please try again."}, status_code=500)

	#embed chunks and store embeddings in the vector database
	background_tasks.add_task(process_embeddings_background, chunks, document_id)

	response = {
		"success": True,
		"metadata": {
			"id": document_id,
			"filename": file.filename,
			"chunk_count": len(chunks),
			"pages": pages[-1]['page'],
			"character_count": len(validated_text),
			"size": human_readable_size(content_size)
		}
	}

	return JSONResponse(content=response)

@route.get("/{uuid}/status")
@limiter.limit("20/minute")
async def check_processing_status(request: Request, uuid: str):
    """Checks if Qdrant has finished saving the chunks"""
    try:
        chunks = await get_document_chunks_by_uuid(uuid)
        is_ready = len(chunks) > 0
        return JSONResponse(content={"success": True, "ready": is_ready})
    except Exception:
        return JSONResponse(content={"success": True, "ready": False})

@route.get("/{uuid}")
@limiter.limit("30/minute")
async def get_document(request: Request, uuid: str):
	''' Placeholder for fetching document metadata and chunks from the database '''
	try:
		await update_document_activity(uuid)
		document = await get_document_by_uuid(uuid)  # Implement this function to fetch document metadata
	except Exception as e:
		print(f"Database error: {e}")
		return JSONResponse(content={"success": False, "message": "Database error"}, status_code=500)

	if not document:
		return JSONResponse(content={"success": False, "message": "Document not found"}, status_code=404)

	return JSONResponse(content={"success": True, "document": document})

@route.get("/{uuid}/info")
@limiter.limit("30/minute")
async def get_document_info(request: Request, uuid: str):
	''' Placeholder for fetching document metadata and chunks from the database '''
	try:
		await update_document_activity(uuid)
		document = await get_document_by_uuid(uuid)  # Implement this function to fetch document metadata
	except Exception as e:
		print(f"Database error: {e}")
		return JSONResponse(content={"success": False, "error": "Database error"}, status_code=500)

	if not document:
		return JSONResponse(content={"success": False, "error": "Document not found"}, status_code=404)

	return JSONResponse(content={"success": True, "metadata": document})

@route.get("/{uuid}/preview")
@limiter.limit("30/minute")
async def get_document_chunks(request: Request, uuid: str):
	''' Placeholder for fetching document chunks from the database '''
	try:
		if not await document_exists(uuid):
			return JSONResponse(content={"success": False, "error": "Document not found. Please try again."}, status_code=404)
		await update_document_activity(uuid)
		chunks = await get_document_chunks_by_uuid(uuid)
		text_preview = await get_document_text(uuid)
	except Exception as e:
		print(f"Database error: {e}")
		return JSONResponse(content={"success": False, "error": "Database error. Please try again."}, status_code=500)

	return JSONResponse(content={"success": True, "text": text_preview, "chunks": chunks})

@route.get("/{uuid}/{chunk_index}/context")
@limiter.limit("30/minute")
async def get_chunk_context(request: Request, uuid: str, chunk_index: int):
	''' Placeholder for fetching document chunks from the database '''
	try:
		if not await document_exists(uuid):
			return JSONResponse(content={"success": False, "error": "Document not found. Please try again."}, status_code=404)
		await update_document_activity(uuid)
		index_pool = await get_chunk_context_by_index(uuid, chunk_index)
		if not index_pool:
			return JSONResponse(content={"success": False, "error": "Chunk context not found. Please try again."}, status_code=404)
		context = await get_document_text(uuid, min(index_pool), max(index_pool) - min(index_pool))
		if not context:
			return JSONResponse(content={"success": False, "error": "Chunk context not found. Please try again."}, status_code=404)
	except Exception as e:
		print(f"Database error: {e}")
		return JSONResponse(content={"success": False, "error": "Database error. Please try again."}, status_code=500)

	return JSONResponse(content={"success": True, "context": {"text": context, "start_char": min(index_pool), "end_char": max(index_pool)}})