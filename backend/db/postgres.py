from datetime import timedelta

from fastapi import Request
from services.storage import human_readable_size
from config import PREVIEW_LENGTH

#CREATE TABLE IF NOT EXISTS documents (
#     id TEXT PRIMARY KEY,
#     original_filename TEXT NOT NULL,
#     full_text TEXT NOT NULL,
#     text_length INTEGER NOT NULL,
#     file_hash TEXT UNIQUE NOT NULL,
#     chunks_count INTEGER NOT NULL,
#     pages_count INTEGER NOT NULL,
#     created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
#     last_activity_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
# );

async def get_pg_pool(request: Request):
    return request.app.state.pg_pool

async def insert_document(document_id, original_filename, full_text, chunks_count, pages_count, file_hash, pg_pool):
    ''' Insert a new document into the database and return its ID '''
    query = '''
        INSERT INTO documents (id, original_filename, full_text, text_length, chunks_count, pages_count, file_hash)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
    '''
    async with pg_pool.acquire() as conn:
        await conn.execute(query, document_id, original_filename, full_text, len(full_text), chunks_count, pages_count, file_hash)
        return document_id

async def get_document_by_uuid(document_id, pg_pool):
    ''' Retrieve document metadata by its UUID '''
    async with pg_pool.acquire() as conn:
        query = 'SELECT id, original_filename, chunks_count, pages_count, text_length, created_at FROM documents WHERE id = $1'
        row = await conn.fetchrow(query, document_id)
        if row:
            return {
                "id": row['id'],
                "filename": row['original_filename'],
                "chunk_count": row['chunks_count'],
                "pages": row['pages_count'],
                "character_count": row['text_length'],
                "size": human_readable_size(row['text_length']),
                "created_at": row['created_at'].isoformat() # Convert Postgres datetime to string
            }
        return None

async def document_exists(document_id, pg_pool):
    ''' Check if a document with the given ID exists in the database '''
    async with pg_pool.acquire() as conn:
        row = await conn.fetchval('SELECT 1 FROM documents WHERE id = $1', document_id)
        return row is not None

async def get_document_text(document_id, pg_pool, start_char=0, length=PREVIEW_LENGTH):
    ''' Retrieve a substring of the document's full text based on character offsets '''
    async with pg_pool.acquire() as conn:
        query = 'SELECT SUBSTR(full_text, $1, $2) FROM documents WHERE id = $3'
        text = await conn.fetchval(query, start_char + 1, length, document_id)
        return text

async def update_document_activity(document_id, pg_pool):
    ''' Update the last activity timestamp for a document '''
    async with pg_pool.acquire() as conn:
        await conn.execute('UPDATE documents SET last_activity_at = CURRENT_TIMESTAMP WHERE id = $1', document_id)

async def delete_inactive_documents(pg_pool, inactivity_threshold_hours=48):
    ''' Delete documents that haven't been accessed within the specified inactivity threshold '''
    async with pg_pool.acquire() as conn:
        # Pass a standard Python timedelta, and asyncpg translates it to a Postgres INTERVAL
        threshold = timedelta(seconds=inactivity_threshold_hours)
        query = '''
            DELETE FROM documents
            WHERE last_activity_at < CURRENT_TIMESTAMP - $1::interval
            RETURNING id
        '''
        records = await conn.fetch(query, threshold)

        return [record['id'] for record in records]
    
async def get_document_by_hash(file_hash, pg_pool):
    ''' Retrieve document metadata by its file hash '''
    async with pg_pool.acquire() as conn:
        query = 'SELECT id, original_filename, chunks_count, pages_count, text_length, created_at FROM documents WHERE file_hash = $1'
        row = await conn.fetchrow(query, file_hash)
        if row:
            return {
                "id": row['id'],
                "filename": row['original_filename'],
                "chunk_count": row['chunks_count'],
                "pages": row['pages_count'],
                "character_count": row['text_length'],
                "size": human_readable_size(row['text_length']),
            }
        return None