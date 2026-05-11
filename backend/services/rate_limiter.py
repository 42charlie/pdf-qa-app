from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

# Initialize the limiter
limiter = Limiter(key_func=get_remote_address)

async def custom_rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """Intercepts the 429 error and returns clean JSON matching your API style"""
    return JSONResponse(
        status_code=429,
        content={
            "ok": False,
            "error": "You're moving too fast! Please wait a moment before trying again.",
            "limit_details": str(exc.detail) # Tells the frontend the exact limit hit
        }
    )