from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from services.embedding import embed_question
from services.embedding import get_relevant_chunks
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
					 <input type="hidden" name="uuid" value="3fff2a461be5e01615f8893012730408">
					 <input type="text" name="question" placeholder="Ask a question..." required>
					 <button type="submit">Send</button>
					 </form>
					 </body></html>
					 """)

@route.post("/ask")
async def ask_question(request: ChatRequest = Form(...)):
	question = embed_question(request.question)
	chunks_ids = get_relevant_chunks(question, request.uuid)
	try:
		chunks = get_chunks_by_ids(chunks_ids)
	except Exception as e:
		print(f"Error retrieving chunks: {e}")
		raise
	debug = f"Question: {request.question}\nRelevant Chunks:\n" + "<br><br>".join(chunks)

	return HTMLResponse(content=f"<html><body><h1>Chat</h1><p>{debug}</p><a href='/chat/ask'>Ask another question</a></body></html>")