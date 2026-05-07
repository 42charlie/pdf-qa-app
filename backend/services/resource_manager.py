import os
import asyncio
from groq import Groq
from functools import lru_cache
from sentence_transformers import SentenceTransformer

@lru_cache(maxsize=1)
def get_llm_client():
	print("Initializing Groq client...")
	return Groq(api_key=os.getenv("API_KEY"))

@lru_cache(maxsize=1)
def get_model():
	print("Loading model...")
	return SentenceTransformer('BAAI/bge-small-en-v1.5')

async def clean_inactive_documents():
	''' clean up documents that haven't been accessed in a while '''
	while True:
		await asyncio.sleep(3600)  # Run cleanup every hour
		try:
			cleanup_inactive_documents()
		except Exception as e:
			print(f"Error during cleanup: {e}")