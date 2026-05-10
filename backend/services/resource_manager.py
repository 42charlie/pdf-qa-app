import os
import asyncio
from groq import AsyncGroq
from functools import lru_cache
from sentence_transformers import SentenceTransformer
from db.qdrant import delete_document_chunks
from db.postgres import delete_inactive_documents

@lru_cache(maxsize=1)
def get_llm_client():
	''' Initialize and cache the Groq client '''
	print("Initializing Groq client...")
	return AsyncGroq(api_key=os.getenv("API_KEY"))

@lru_cache(maxsize=1)
def get_model():
	''' Load and cache the sentence transformer model '''
	print("Loading model...")
	return SentenceTransformer('BAAI/bge-small-en-v1.5')

async def clean_inactive_documents():
	''' clean up documents that haven't been accessed in a while '''
	while True:
		await asyncio.sleep(3600)  # Run cleanup every hour
		print("Running cleanup of inactive documents...")
		try:
			ids = await delete_inactive_documents()
			for doc_id in ids:
				await delete_document_chunks(doc_id)
			print(f"Deleted {len(ids)} inactive documents and their chunks.")
		except Exception as e:
			print(f"Error during cleanup: {e}")