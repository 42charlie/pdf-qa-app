import faiss
import numpy as np
from services.model_loader import get_model
from config import FAISS_DIR

def save_embeddings(embeddings, chunks_ids, uuid):
	np_chunks_ids = np.array(chunks_ids).astype('int64')
	index = faiss.IndexFlatL2(384)
	index_ids = faiss.IndexIDMap(index)
	index_ids.add_with_ids(embeddings, np_chunks_ids)
	faiss.write_index(index_ids, str(FAISS_DIR / f"{uuid}.faiss"))

def generate_embeddings(chunks):
	# Load the pre-trained model
	model = get_model()

	# Generate embeddings for each chunk of text
	embeddings = model.encode(chunks)

	return embeddings

def embed_question(question):
	model = get_model()
	embedding = model.encode([question])
	return embedding

def get_relevant_chunks(question_embedding, uuid, top_k=5):
	index = faiss.read_index(str(FAISS_DIR / f"{uuid}.faiss"))
	distances, indices = index.search(question_embedding, top_k)
	return indices[0].tolist()  # Return the list of relevant chunk IDs