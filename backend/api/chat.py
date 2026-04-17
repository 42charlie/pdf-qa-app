import json

from services.generation import craft_prompt, request_llm_response, parse_llm_json
from services.resource_manager import get_llm_client
from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from services.embedding import embed_question
from services.embedding import get_relevant_chunks_ids
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
					 <input type="text" name="uuid" value="618d8349bf09a632a3b93a89224010e9">
					 <input type="text" name="question" placeholder="Ask a question..." required>
					 <button type="submit">Send</button>
					 </form>
					 </body></html>
					 """)

@route.post("/ask")
async def ask_question(request: ChatRequest = Form(...)):
	question = embed_question(request.question)
	chunks_ids = get_relevant_chunks_ids(question, request.uuid)
	try:
		chunks = get_chunks_by_ids(chunks_ids)
	except Exception as e:
		print(f"Error retrieving chunks: {e}")
		return JSONResponse(content={"ok": False, "error": "Error retrieving relevant document chunks."})
	prompt = craft_prompt(request.question, chunks)
	client = get_llm_client()
	response = request_llm_response(client, prompt)
	if response["ok"]:
		response["content"] = parse_llm_json(response['content'])

	return JSONResponse(content=response)