import asyncio
import os
import asyncpg
from dotenv import load_dotenv
from fastapi import FastAPI
from contextlib import asynccontextmanager

from qdrant_client import AsyncQdrantClient
from api import chat, documents
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
    print("Connecting to databases...")
    
    # Initialize PostgreSQL Connection Pool
    app.state.pg_pool = await asyncpg.create_pool(os.getenv("POSTGRES_URI"))
    
    # Initialize Qdrant Client
    app.state.qdrant = AsyncQdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY")
    )

    asyncio.create_task(clean_inactive_documents(app.state.pg_pool, app.state.qdrant))

    yield

    print("Closing database connections...")
    await app.state.pg_pool.close()
    await app.state.qdrant.close()

app = FastAPI(docs_url=None,
              redoc_url=None,
              openapi_url=None,
              lifespan=lifespan)
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