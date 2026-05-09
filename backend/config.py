from pathlib import Path

PREVIEW_LENGTH = 10000

#chunler configuration
CHUNK_SIZE = 1200
OVERLAP_SIZE = 200
MIN_CHUNK_SIZE = 100

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent

# Directory to store uploaded files
UPLOAD_DIR = BASE_DIR / "uploads"

# Database file path
DB_PATH = BASE_DIR / "database.db"

# Ensure necessary directories exist
UPLOAD_DIR.mkdir(exist_ok=True)
