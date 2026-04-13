import faiss
from sentence_transformers import SentenceTransformer
import numpy as np

from config import FAISS_DIR

def save_embeddings(embeddings, chunks_ids, uuid):
	np_chunks_ids = np.array(chunks_ids).astype('int64')
	index = faiss.IndexFlatL2(384)
	index_ids = faiss.IndexIDMap(index)
	index_ids.add_with_ids(embeddings, np_chunks_ids)
	faiss.write_index(index_ids, str(FAISS_DIR / f"{uuid}.faiss"))

def generate_embeddings(chunks):
	# Load the pre-trained model
	model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

	# Generate embeddings for each chunk of text
	embeddings = model.encode(chunks)

	return embeddings