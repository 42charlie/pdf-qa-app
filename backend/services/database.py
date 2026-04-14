import sqlite3

from config import DB_PATH

INIT_QUERY = '''CREATE TABLE IF NOT EXISTS documents (
    id TEXT PRIMARY KEY,
    original_filename TEXT NOT NULL,
    stored_filename TEXT NOT NULL,
    full_text TEXT NOT NULL,
    text_length INTEGER NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS chunks (
    id INTEGER PRIMARY KEY,
    document_id TEXT NOT NULL,
    chunk_index INTEGER NULL,
    text TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_chunks_document_id ON chunks(document_id);
CREATE INDEX IF NOT EXISTS idx_chunks_document_id_chunk_index ON chunks(document_id, chunk_index);'''


def initialize_database():
	try:
		with sqlite3.connect(DB_PATH) as conn:
			cursor = conn.cursor()
			cursor.executescript(INIT_QUERY)
	except sqlite3.Error as e:
		print(f"Error initializing database: {e}")
		raise

def insert_document(document_id, original_filename, stored_filename, full_text):
	try:
		with sqlite3.connect(DB_PATH) as conn:
			cursor = conn.cursor()
			cursor.execute('''
				INSERT INTO documents (id, original_filename, stored_filename, full_text, text_length)
				VALUES (?, ?, ?, ?, ?)
			''', (document_id, original_filename, stored_filename, full_text, len(full_text)))
			conn.commit()
			return cursor.lastrowid
	except sqlite3.Error as e:
		print(f"Error inserting document: {e}")
		raise

def insert_chunks(chunks, document_id):
	formatted_chunks = [(document_id, chunk_index, text) for chunk_index, text in enumerate(chunks)]
	try:
		with sqlite3.connect(DB_PATH) as conn:
			cursor = conn.cursor()
			cursor.executemany('''
				INSERT INTO chunks (document_id, chunk_index, text)
				VALUES (?, ?, ?)
			''', formatted_chunks)
			conn.commit()
	except sqlite3.Error as e:
		print(f"Error inserting chunks: {e}")
		raise 

def get_chunks_ids(document_id):
	try:
		with sqlite3.connect(DB_PATH) as conn:
			cursor = conn.cursor()
			cursor.execute('SELECT id FROM chunks WHERE document_id = ?', (document_id,))
			#[(123,), (456,)] -> [123, 456]
			return [id[0] for id in cursor.fetchall()]
	except sqlite3.Error as e:
		print(f"Error initializing database: {e}")
		raise

def get_chunks_by_ids(chunks_ids):
	try:
		with sqlite3.connect(DB_PATH) as conn:
			cursor = conn.cursor()
			placeholders = ','.join('?' for _ in chunks_ids)
			query = f'SELECT text FROM chunks WHERE id IN ({placeholders})'
			cursor.execute(query, chunks_ids)
			return [row[0] for row in cursor.fetchall()]
	except sqlite3.Error as e:
		print(f"Error retrieving chunks: {e}")
		raise