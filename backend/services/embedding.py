from services.resource_manager import get_model

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