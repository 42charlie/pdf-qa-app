import json

from config import FALLBACK_RESPONSE
from services.generation import craft_prompt, request_llm_response, parse_llm_json, relevant_chunks_to_json
from services.resource_manager import get_llm_client
from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from services.embedding import embed_question, get_relevant_chunks
from services.database import get_chunks_by_ids

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
		chunks_ids, distances = get_relevant_chunks(question, request.uuid)
		if min(distances) > 1.3:  # Threshold for relevance, based on empirical testing
			return JSONResponse(content={"ok": True, "error": None, "data": json.loads(FALLBACK_RESPONSE), "relevant_chunks": None}, status_code=200)
		chunks = get_chunks_by_ids(chunks_ids)
	except Exception as e:
		print(f"Error retrieving chunks: {e}")
		return JSONResponse(content={"ok": False, "error": "Error retrieving relevant document chunks.", "data": None, "relevant_chunks": None}, status_code=500)
	prompt = craft_prompt(request.question, chunks)
	client = get_llm_client()
	response = request_llm_response(client, prompt)
	if response["ok"]:
		response["data"] = parse_llm_json(response['data'])
		response["retrieved_chunks"] = relevant_chunks_to_json(chunks_ids, distances)
	else:
		response["retrieved_chunks"] = None

	return JSONResponse(content=response)