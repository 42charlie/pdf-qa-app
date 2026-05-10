import os
import uuid
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Distance, Range, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from config import PREVIEW_LENGTH

# Connect to your local Qdrant Docker container
qdrant = AsyncQdrantClient(url=os.getenv("QDRANT_URL"))
COLLECTION_NAME = "1337_documents"

async def init_qdrant():
	"""Call this in your FastAPI lifespan alongside your Postgres init"""
	if not await qdrant.collection_exists(COLLECTION_NAME):
		await qdrant.create_collection(
			collection_name=COLLECTION_NAME,
			vectors_config=VectorParams(size=384, distance=Distance.COSINE),
		)

async def save_embeddings(embeddings, chunks, document_id):
	"""Saves both the vector AND the text payload into Qdrant"""
	points = []
	
	#loop through the text chunks and their matching vectors
	for i, (chunk_dict, vector) in enumerate(zip(chunks, embeddings)):
		points.append(
			PointStruct(
				id=str(uuid.uuid4()),
				vector=vector.tolist(),
				payload={
					"document_id": document_id,
					"chunk_index": i,
					"text": chunk_dict.get('content', ''),
					"start_char": chunk_dict.get('start_char', 0),
					"end_char": chunk_dict.get('end_char', 0)
				}
			)
		)
		
	# Upsert the batch into Qdrant
	await qdrant.upsert(
		collection_name=COLLECTION_NAME,
		points=points
	)

async def get_relevant_chunks(question_embedding, document_id, top_k=3):
	"""Searches Qdrant and filters ONLY for the active document"""
	
	search_results = await qdrant.query_points(
		collection_name=COLLECTION_NAME,
		query=question_embedding[0].tolist(),
		query_filter=Filter(
			must=[
				FieldCondition(
					key="document_id",
					match=MatchValue(value=document_id)
				)
			]
		),
		limit=top_k
	)
	
	#extract the payloads and the similarity scores
	retrieved_chunks = [hit.payload for hit in search_results.points]
	scores = [hit.score for hit in search_results.points]
	
	return retrieved_chunks, scores

async def get_chunk_context_by_index(document_id: str, target_index: int):
	"""Fetches ONLY the start and end characters for a chunk and its neighbors"""
	
	records, _ = await qdrant.scroll(
		collection_name=COLLECTION_NAME,
		scroll_filter=Filter(
			must=[
				FieldCondition(
					key="document_id",
					match=MatchValue(value=document_id)
				)
			],
			should=[
				FieldCondition(key="chunk_index", match=MatchValue(value=target_index - 1)),
				FieldCondition(key="chunk_index", match=MatchValue(value=target_index)),
				FieldCondition(key="chunk_index", match=MatchValue(value=target_index + 1))
			]
		),
		limit=3,
		with_payload=["chunk_index", "start_char", "end_char"],
		with_vectors=False
	)
	
	# Sort chunks by chunk_index
	records.sort(key=lambda x: x.payload['chunk_index'])
	
	# flatten into a single list of integers
	return [
		index 
		for record in records 
		for index in (record.payload['start_char'], record.payload['end_char'])
	]

async def get_document_chunks_by_uuid(document_id: str):
	"""Fetches clean, contiguous preview chunks with exactly the keys needed"""
	
	records, _ = await qdrant.scroll(
		collection_name=COLLECTION_NAME,
		scroll_filter=Filter(
			must=[
				FieldCondition(
					key="document_id",
					match=MatchValue(value=document_id)
				),
				FieldCondition(
					key="end_char",
					range=Range(lte=PREVIEW_LENGTH + 1000)
				)
			]
		),
		limit=30,
		with_payload=["chunk_index", "start_char", "end_char"],
		with_vectors=False
	)

	records.sort(key=lambda x: x.payload['chunk_index'])
	return [
		{
			"index": record.payload['chunk_index'],
			"length": record.payload['end_char'] - record.payload['start_char'], # Calculated instantly!
			"start": record.payload['start_char'],
			"end": record.payload['end_char']
		}
		for record in records
	]

async def delete_document_chunks(document_id: str):
	"""Deletes all chunks and vectors belonging to a specific document"""

	await qdrant.delete(
		collection_name=COLLECTION_NAME,
		points_selector=Filter(
			must=[
				FieldCondition(
					key="document_id",
					match=MatchValue(value=document_id)
				)
			]
		)
	)