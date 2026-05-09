from datetime import timedelta

import asyncpg
from click import UUID
from services.storage import human_readable_size
from config import DB_PATH, PREVIEW_LENGTH

# The global connection pool
pool = None

INIT_QUERY = '''
CREATE TABLE IF NOT EXISTS documents (
    id TEXT PRIMARY KEY,
    original_filename TEXT NOT NULL,
    full_text TEXT NOT NULL,
    text_length INTEGER NOT NULL,
    chunks_count INTEGER NOT NULL,
    pages_count INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_activity_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS chunks (
    id SERIAL PRIMARY KEY,
    document_id TEXT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    chunk_index INTEGER NULL,
    text TEXT NOT NULL,
    chunk_length INTEGER NOT NULL,
    start_char INTEGER NULL,
    end_char INTEGER NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_chunks_document_id ON chunks(document_id);
CREATE INDEX IF NOT EXISTS idx_chunks_document_id_chunk_index ON chunks(document_id, chunk_index);
'''

async def initialize_database(db_url: str):
    """Initialize the database connection pool and create tables if they don't exist."""
    global pool
    try:
        # Create a connection pool
        pool = await asyncpg.create_pool(db_url, min_size=2, max_size=10)
        async with pool.acquire() as conn:
            await conn.execute(INIT_QUERY)
    except Exception as e:
        print(f"Database initialization failed: {e}")
        raise

async def close_database():
    """Close the database connection pool."""
    global pool
    if pool:
        await pool.close()

async def insert_document(document_id, original_filename, full_text, chunks_count, pages_count):
    ''' Insert a new document into the database and return its ID '''
    query = '''
        INSERT INTO documents (id, original_filename, full_text, text_length, chunks_count, pages_count)
        VALUES ($1, $2, $3, $4, $5, $6)
    '''
    async with pool.acquire() as conn:
        await conn.execute(query, document_id, original_filename, full_text, len(full_text), chunks_count, pages_count)
        return document_id

async def insert_chunks(chunks, document_id):
    ''' Insert chunks into the database with their metadata '''
    formatted_chunks = [
        (document_id, chunk_index, text.get('content', ''), len(text.get('content', '')), text.get('start_char'), text.get('end_char')) 
        for chunk_index, text in enumerate(chunks)
    ]
    query = '''
        INSERT INTO chunks (document_id, chunk_index, text, chunk_length, start_char, end_char)
        VALUES ($1, $2, $3, $4, $5, $6)
    '''
    async with pool.acquire() as conn:
        await conn.executemany(query, formatted_chunks)

async def get_chunks_ids(document_id):
    ''' Retrieve chunk IDs for a given document ID '''
    async with pool.acquire() as conn:
        records = await conn.fetch('SELECT id FROM chunks WHERE document_id = $1', document_id)
        return [record['id'] for record in records]

async def get_chunks_by_ids(chunks_ids):
    ''' Retrieve chunk metadata for a list of chunk IDs '''
    async with pool.acquire() as conn:
        query = 'SELECT chunk_index, text, start_char, end_char FROM chunks WHERE id = ANY($1::int[])'
        records = await conn.fetch(query, chunks_ids)
        return [dict(record) for record in records]

async def get_document_by_uuid(document_id):
    ''' Retrieve document metadata by its UUID '''
    async with pool.acquire() as conn:
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

async def document_exists(document_id):
    ''' Check if a document with the given ID exists in the database '''
    async with pool.acquire() as conn:
        row = await conn.fetchval('SELECT 1 FROM documents WHERE id = $1', document_id)
        return row is not None

async def get_document_chunks_by_uuid(document_id):
    ''' Retrieve chunk metadata for a document, ordered by chunk index '''
    async with pool.acquire() as conn:
        query = '''
            SELECT chunk_index, chunk_length, start_char, end_char 
            FROM chunks 
            WHERE document_id = $1 AND end_char <= $2 
            ORDER BY chunk_index
        '''
        records = await conn.fetch(query, document_id, PREVIEW_LENGTH + 1000)
        return [
            {
                "index": row['chunk_index'],
                "length": row['chunk_length'],
                "start": row['start_char'],
                "end": row['end_char']
            }
            for row in records
        ]

async def get_document_text(document_id, start_char=0, length=PREVIEW_LENGTH):
    ''' Retrieve a substring of the document's full text based on character offsets '''
    async with pool.acquire() as conn:
        query = 'SELECT SUBSTR(full_text, $1, $2) FROM documents WHERE id = $3'
        text = await conn.fetchval(query, start_char + 1, length, document_id)
        return text

async def get_chunk_context_by_index(document_id, chunk_index):
    ''' Retrieve the character offsets for a chunk and its immediate neighbors to provide context '''
    async with pool.acquire() as conn:
        query = '''
            SELECT start_char, end_char 
            FROM chunks 
            WHERE document_id = $1 AND chunk_index = ANY($2::int[])
        '''
        records = await conn.fetch(query, document_id, [chunk_index, chunk_index - 1, chunk_index + 1])
        return [index for row in records for index in (row['start_char'], row['end_char'])]

async def update_document_activity(document_id):
    ''' Update the last activity timestamp for a document '''
    async with pool.acquire() as conn:
        await conn.execute('UPDATE documents SET last_activity_at = CURRENT_TIMESTAMP WHERE id = $1', document_id)

async def delete_inactive_documents(inactivity_threshold_hours=48):
    ''' Delete documents that haven't been accessed within the specified inactivity threshold '''
    async with pool.acquire() as conn:
        # Pass a standard Python timedelta, and asyncpg translates it to a Postgres INTERVAL
        threshold = timedelta(hours=inactivity_threshold_hours)
        query = '''
            DELETE FROM documents
            WHERE last_activity_at < CURRENT_TIMESTAMP - $1::interval
        '''
        await conn.execute(query, threshold)