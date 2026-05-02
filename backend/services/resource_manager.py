
import os
import asyncio
from groq import Groq
from sentence_transformers import SentenceTransformer

_model = None
client = None

def get_llm_client():
	global client
	if client is None:
		client = Groq(api_key=os.getenv("API_KEY"))
	return client

def get_model():
	global _model
	if _model is None:
		_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
	return _model

async def clean_inactive_documents():
	''' clean up documents that haven't been accessed in a while '''
	while True:
		await asyncio.sleep(3600)  # Run cleanup every hour
		try:
			cleanup_inactive_documents()
		except Exception as e:
			print(f"Error during cleanup: {e}")