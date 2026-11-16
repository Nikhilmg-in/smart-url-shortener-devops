import os
import secrets
import string
import time

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl

# Configuration (can be injected via a Kubernetes ConfigMap / environment)
APP_NAME = os.getenv("APP_NAME", "Smart URL Shortener")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
APP_ENV = os.getenv("APP_ENV", "development")
PORT = int(os.getenv("PORT", "8000"))

START_TIME = time.time()

app = FastAPI(
    title=APP_NAME,
    description="A simple URL shortener built for a DevOps project",
    version=APP_VERSION,
)

# Temporary in-memory storage (acceptable for this project)
url_database = {}

ALPHABET = string.ascii_letters + string.digits


class URLRequest(BaseModel):
    url: HttpUrl


def generate_code(length: int = 6) -> str:
    """Generate a random short code that is not already in use."""
    while True:
        code = "".join(secrets.choice(ALPHABET) for _ in range(length))
        if code not in url_database:
            return code


@app.get("/")
def home():
    return {"message": "Smart URL Shortener is running"}


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "ready": True,
        "uptime_seconds": round(time.time() - START_TIME, 2),
    }


@app.get("/info")
def info():
    return {
        "project": APP_NAME,
        "version": APP_VERSION,
        "environment": APP_ENV,
        "technology": "FastAPI",
        "links_stored": len(url_database),
    }


@app.post("/shorten")
def shorten_url(request: URLRequest):
    original = str(request.url)
    short_code = generate_code()
    url_database[short_code] = original

    return {
        "original_url": original,
        "short_code": short_code,
        "short_url": f"/{short_code}",
    }


# NOTE: keep this catch-all route LAST so it never shadows fixed routes.
@app.get("/{short_code}")
def redirect_url(short_code: str):
    if short_code not in url_database:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return RedirectResponse(url=url_database[short_code])


def run():
    """Console entry point: `url-shortener`."""
    uvicorn.run(app, host="0.0.0.0", port=PORT)


if __name__ == "__main__":
    run()
