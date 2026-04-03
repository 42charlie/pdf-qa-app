from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from api import chat
from api import documents

app = FastAPI()

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