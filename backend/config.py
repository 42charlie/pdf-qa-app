from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent

# Directory to store uploaded files
UPLOAD_DIR = BASE_DIR / "uploads"
DB_PATH = BASE_DIR / "database.db"
UPLOAD_DIR.mkdir(exist_ok=True)