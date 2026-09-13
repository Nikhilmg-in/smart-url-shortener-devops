from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
import secrets
import string


app = FastAPI(
    title="Smart URL Shortener",
    description="A simple URL shortener built for a DevOps project",
    version="1.0.0"
)


# Temporary in-memory storage
url_database = {}


class URLRequest(BaseModel):
    url: str


@app.get("/")
def home():
    return {
        "message": "Smart URL Shortener is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
@app.get("/info")
def info():
    return {
        "project": "Smart URL Shortener",
        "version": "1.0",
        "technology": "FastAPI"
    }

@app.post("/shorten")
def shorten_url(request: URLRequest):

    characters = string.ascii_letters + string.digits
    short_code = "".join(secrets.choice(characters) for _ in range(6))

    url_database[short_code] = request.url

    return {
        "original_url": request.url,
        "short_code": short_code,
        "short_url": f"/{short_code}"
    }


@app.get("/{short_code}")
def redirect_url(short_code: str):

    if short_code not in url_database:
        raise HTTPException(
            status_code=404,
            detail="Short URL not found"
        )

    return RedirectResponse(
        url=url_database[short_code]
    )