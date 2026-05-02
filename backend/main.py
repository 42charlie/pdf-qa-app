import asyncio
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from api import chat, documents
from services.database import initialize_database
from services.resource_manager import clean_inactive_documents
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

load_dotenv()
origins = [
    os.getenv("FRONTEND_URL")
]

# add the CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # allows all methods
    allow_headers=["*"],  # allows all headers
)

@app.on_event("startup")
async def startup_event():
	''' Initialize resources on startup, such as the database and background tasks '''
	try:
		initialize_database()
	except Exception as e:
		print(f"Error initializing database: {e}")
		raise

	asyncio.create_task(clean_inactive_documents())

# Include the routers for documents and chat endpoints
app.include_router(documents.route)
app.include_router(chat.route)

'''Serve a simple HTML form for testing the endpoint'''
@app.get("/")
def upload_form():
	return HTMLResponse(content="""<html>
	<head>
		<title>PDF Upload</title>
	</head>
	<body>
		<h1>Upload PDF File</h1>
		<form action="/documents/upload" method="post" enctype="multipart/form-data">
			<input type="file" name="file" accept=".pdf" required>
			<button type="submit">Upload</button>
		</form>
	</body>
</html>""")