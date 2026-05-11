import json
from services.prompt import FALLBACK_RESPONSE
from services.generation import craft_prompt, is_grounded_response, request_llm_response, parse_llm_json, relevant_chunks_to_json
from services.resource_manager import get_llm_client
from fastapi import APIRouter, Form, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from db.qdrant import get_relevant_chunks
from services.embedding import embed_question
from db.postgres import update_document_activity
from services.rate_limiter import limiter

class ChatRequest(BaseModel):
	question: str
	uuid: str

route = APIRouter(prefix="/chat", tags=["Chat"])

@route.post("/ask")
@limiter.limit("5/minute")
async def ask_question(request: Request, body: ChatRequest = Form(...)):
	question = embed_question(body.question)
	try:
		await update_document_activity(body.uuid)
		chunks, distances = await get_relevant_chunks(question, body.uuid)
		if max(distances) < 0.52:  # Threshold for relevance, based on empirical testing
			return JSONResponse(content={"ok": True, "error": None, "data": json.loads(FALLBACK_RESPONSE), "relevant_chunks": []}, status_code=200)
	except Exception as e:
		print(f"Error retrieving chunks: {e}")
		return JSONResponse(content={"ok": False, "error": "Error retrieving relevant document chunks.", "data": None, "relevant_chunks": []}, status_code=500)
	prompt = craft_prompt(body.question, chunks)
	client = get_llm_client()
	response = await request_llm_response(client, prompt)
	if not response.get("ok"):
		return JSONResponse(content={"ok": False, "error": response.get("error", "LLM generation failed."), "data": None, "relevant_chunks": []}, status_code=500)
	parsed_data = parse_llm_json(response['data'])
	if not is_grounded_response(parsed_data):
		# If it's ungrounded, malicious, or failed parsing, trigger the fallback
		parsed_data = json.loads(FALLBACK_RESPONSE)
		retrieved_chunks = []  # Don't include chunks if the response isn't grounded
	else:
		# If it's grounded, include the relevant chunks in the response for transparency
		retrieved_chunks = relevant_chunks_to_json(chunks, distances)
	
	final_response = {
		"ok": True,
		"error": None,
		"data": parsed_data,
		"retrieved_chunks": retrieved_chunks
	}

	return JSONResponse(content=final_response)