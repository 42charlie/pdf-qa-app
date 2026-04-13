from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent

# Directory to store uploaded files and FAISS index
UPLOAD_DIR = BASE_DIR / "uploads"
FAISS_DIR = BASE_DIR / "faiss_data"

# Database file path
DB_PATH = BASE_DIR / "database.db"

# Ensure necessary directories exist
UPLOAD_DIR.mkdir(exist_ok=True)
FAISS_DIR.mkdir(exist_ok=True)