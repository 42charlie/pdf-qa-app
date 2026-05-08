import json

from services.prompt import FALLBACK_RESPONSE
from services.generation import craft_prompt, is_grounded_response, request_llm_response, parse_llm_json, relevant_chunks_to_json
from services.resource_manager import get_llm_client
from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from services.embedding import embed_question, get_relevant_chunks
from services.database import get_chunks_by_ids, update_document_activity

class ChatRequest(BaseModel):
	question: str
	uuid: str

route = APIRouter(prefix="/chat", tags=["Chat"])

@route.get("/ask")
async def ask():
	return HTMLResponse(content="""
					 <html><body>
					 <h1>Chat</h1>
					 <p>Welcome to the chat!</p>
					 <form action="/chat/ask" method="post">
					 <input type="text" name="uuid" value="3beb8f94b5c4e882cadba0459b759f53">
					 <input type="text" name="question" placeholder="Ask a question..." required>
					 <button type="submit">Send</button>
					 </form>
					 </body></html>
					 """)

@route.post("/ask")
async def ask_question(request: ChatRequest = Form(...)):
	question = embed_question(request.question)
	try:
		update_document_activity(request.uuid)
		chunks_ids, distances = get_relevant_chunks(question, request.uuid)
		if min(distances) > 0.85:  # Threshold for relevance, based on empirical testing
			return JSONResponse(content={"ok": True, "error": None, "data": json.loads(FALLBACK_RESPONSE), "relevant_chunks": []}, status_code=200)
		chunks = get_chunks_by_ids(chunks_ids)
	except Exception as e:
		print(f"Error retrieving chunks: {e}")
		return JSONResponse(content={"ok": False, "error": "Error retrieving relevant document chunks.", "data": None, "relevant_chunks": []}, status_code=500)
	prompt = craft_prompt(request.question, chunks)
	client = get_llm_client()
	response = request_llm_response(client, prompt)
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