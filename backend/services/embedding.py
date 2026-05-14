from db.qdrant import save_embeddings
from services.resource_manager import get_model
import asyncio

def generate_embeddings(chunks):
	chunks_text = [chunk['content'] for chunk in chunks]
	# Load the pre-trained model
	model = get_model()

	# Generate embeddings for each chunk of text
	embeddings = model.encode(chunks_text)

	return embeddings

def embed_question(question):
	model = get_model()
	bge_query = "Represent this sentence for searching relevant passages: " + question
	embedding = model.encode([bge_query])
	return embedding

async def process_embeddings_background(chunks, document_id, qdrant):
    print(f"Starting background embedding for {document_id}...", flush=True)
    try:
        embeddings = await asyncio.to_thread(generate_embeddings, chunks)
        await save_embeddings(embeddings, chunks, document_id, qdrant)
        print(f"Background embedding complete for {document_id}", flush=True)
    except Exception as e:
        print(f"Background embedding failed: {e}", flush=True)