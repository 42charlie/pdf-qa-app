import sqlite3

from config import DB_PATH

INIT_QUERY = '''CREATE TABLE IF NOT EXISTS documents (
    id TEXT PRIMARY KEY,
    original_filename TEXT NOT NULL,
    full_text TEXT NOT NULL,
    text_length INTEGER NOT NULL,
    chunks_count INTEGER NOT NULL,
	pages_count INTEGER NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
	last_activity_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS chunks (
    id INTEGER PRIMARY KEY,
    document_id TEXT NOT NULL,
    chunk_index INTEGER NULL,
    text TEXT NOT NULL,
	chunk_length INTEGER NOT NULL,
	start_char INTEGER NULL,
	end_char INTEGER NULL,
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
	except sqlite3.Error:
		raise

def insert_document(document_id, original_filename, full_text, chunks_count, pages_count):
	try:
		with sqlite3.connect(DB_PATH) as conn:
			cursor = conn.cursor()
			cursor.execute('''
				INSERT INTO documents (id, original_filename, full_text, text_length, chunks_count, pages_count)
				VALUES (?, ?, ?, ?, ?, ?)
			''', (document_id, original_filename, full_text, len(full_text), chunks_count, pages_count))
			conn.commit()
			return cursor.lastrowid
	except sqlite3.Error:
		raise

def insert_chunks(chunks, document_id):
	formatted_chunks = [(document_id, chunk_index, text.get('content', ''), len(text.get('content', '')), text.get('start_char'), text.get('end_char')) for chunk_index, text in enumerate(chunks)]
	try:
		with sqlite3.connect(DB_PATH) as conn:
			cursor = conn.cursor()
			cursor.executemany('''
				INSERT INTO chunks (document_id, chunk_index, text, chunk_length, start_char, end_char)
				VALUES (?, ?, ?, ?, ?, ?)
			''', formatted_chunks)
			conn.commit()
	except sqlite3.Error:
		raise 

def get_chunks_ids(document_id):
	try:
		with sqlite3.connect(DB_PATH) as conn:
			cursor = conn.cursor()
			cursor.execute('SELECT id FROM chunks WHERE document_id = ?', (document_id,))
			#[(123,), (456,)] -> [123, 456]
			return [id[0] for id in cursor.fetchall()]
	except sqlite3.Error:
		raise

def get_chunks_by_ids(chunks_ids):
	try:
		with sqlite3.connect(DB_PATH) as conn:
			cursor = conn.cursor()
			placeholders = ','.join('?' for _ in chunks_ids)
			query = f'SELECT id, text FROM chunks WHERE id IN ({placeholders})'
			cursor.execute(query, chunks_ids)
			return [row for row in cursor.fetchall()]
	except sqlite3.Error:
		raise

def get_document_by_uuid(document_id):
	try:
		with sqlite3.connect(DB_PATH) as conn:
			cursor = conn.cursor()
			cursor.execute('SELECT id, original_filename, full_text, text_length, created_at FROM documents WHERE id = ?', (document_id,))
			row = cursor.fetchone()
			if row:
				return {
					"id": row[0],
					"original_filename": row[1],
					"full_text": row[2],
					"text_length": row[3],
					"created_at": row[4]
				}
			return None
	except sqlite3.Error:
		raise

def document_exists(document_id):
	try:
		with sqlite3.connect(DB_PATH) as conn:
			cursor = conn.cursor()
			cursor.execute('SELECT 1 FROM documents WHERE id = ?', (document_id,))
			return cursor.fetchone() is not None
	except sqlite3.Error as e:
		raise

def get_document_chunks_by_uuid(document_id):
	try:
		with sqlite3.connect(DB_PATH) as conn:
			cursor = conn.cursor()
			cursor.execute('SELECT id, chunk_index, text FROM chunks WHERE document_id = ? ORDER BY chunk_index', (document_id,))
			return [row for row in cursor.fetchall()]
	except sqlite3.Error:
		raise

def update_document_activity(document_id):
	try:
		with sqlite3.connect(DB_PATH) as conn:
			cursor = conn.cursor()
			cursor.execute('UPDATE documents SET last_activity_at = CURRENT_TIMESTAMP WHERE id = ?', (document_id,))
			conn.commit()
	except sqlite3.Error as e:
		raise

def delete_inactive_documents(inactivity_threshold_hours=24):
	try:
		with sqlite3.connect(DB_PATH) as conn:
			cursor = conn.cursor()
			cursor.execute('''
				DELETE FROM documents
				WHERE last_activity_at < datetime('now', ?)
			''', (f'-{inactivity_threshold_hours} hours',))
			conn.commit()
	except sqlite3.Error as e:
		raise