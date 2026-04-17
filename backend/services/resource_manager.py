
import os
from groq import Groq
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

_model = None
client = None

def get_llm_client():
	global client
	if client is None:
		load_dotenv()
		client = Groq(api_key=os.getenv("API_KEY"))
	return client

def get_model():
	global _model
	if _model is None:
		_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
	return _model