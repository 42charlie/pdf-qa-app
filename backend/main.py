import asyncio
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from contextlib import asynccontextmanager
from api import chat, documents
from db.qdrant import init_qdrant
from db.postgres import close_database, initialize_database
from services.resource_manager import clean_inactive_documents
from fastapi.middleware.cors import CORSMiddleware
from services.rate_limiter import limiter, custom_rate_limit_handler
from slowapi.errors import RateLimitExceeded

load_dotenv()

origins = [
    os.getenv("FRONTEND_URL")
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    try:
        await initialize_database(os.getenv("DATABASE_URL"))
        await init_qdrant()
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise

    asyncio.create_task(clean_inactive_documents())

    yield

    # SHUTDOWN
    try:
        await close_database()
    except Exception as e:
        print(f"Error closing database: {e}")

app = FastAPI(lifespan=lifespan)
# Attach the limiter to the app and set up the custom rate limit handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, custom_rate_limit_handler)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents.route)
app.include_router(chat.route)