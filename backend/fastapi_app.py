"""
FastAPI GitReadme Application (OpenAI Version)
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from pydantic import BaseModel
import logging
import datetime

# Your local imports
from app import ReadmeGeneratorApp
from api_helper import (
    log_request_metrics,
    validate_github_url,
    sanitize_repo_name,
    format_error_response,
    metrics
)

# ------------------------------------------------------------------------------
# Logging
# ------------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------------------
# FastAPI App
# ------------------------------------------------------------------------------
app = FastAPI(
    title="GitReadme - AI README Generator",
    version="1.0.0",
    docs_url="/docs",       # <-- IMPORTANT FIX
    redoc_url="/redoc"
)

# ------------------------------------------------------------------------------
# CORS
# ------------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------------------
# Request/Response Models
# ------------------------------------------------------------------------------
class ReadmeRequest(BaseModel):
    repo_url: str
    generation_method: str = "Standard README"

class ReadmeResponse(BaseModel):
    success: bool
    readme_content: str = ""
    error_message: str = ""
    generation_timestamp: str
    repo_url: str
    generation_method: str

# ------------------------------------------------------------------------------
# Initialize AI App
# ------------------------------------------------------------------------------
try:
    readme_app = ReadmeGeneratorApp()
    logger.info("GitReadme initialized successfully.")
except Exception as e:
    logger.error(f"Initialization failed: {e}")
    readme_app = None

# ------------------------------------------------------------------------------
# HEALTH CHECK  ✔ REQUIRED FOR RENDER
# ------------------------------------------------------------------------------
@app.get("/health", response_class=PlainTextResponse)
async def health():
    return "OK"

# ------------------------------------------------------------------------------
# ROOT ROUTE
# ------------------------------------------------------------------------------
@app.get("/", response_class=PlainTextResponse)
async def root():
    return "GitReadme Backend Running"

# ------------------------------------------------------------------------------
# README GENERATION ROUTE
# ------------------------------------------------------------------------------
@app.post("/generate-readme", response_model=ReadmeResponse)
@log_request_metrics
async def generate_readme(request: ReadmeRequest):

    if not validate_github_url(request.repo_url):
        raise HTTPException(400, "Invalid GitHub URL")

    if not readme_app:
        raise HTTPException(503, "Service unavailable")

    try:
        content = readme_app.generate_readme_from_repo_url(
            request.repo_url,
            request.generation_method
        )

        return ReadmeResponse(
            success=True,
            readme_content=content,
            generation_timestamp=datetime.datetime.now().isoformat(),
            repo_url=request.repo_url,
            generation_method=request.generation_method
        )

    except Exception as e:
        logger.error(str(e))
        return ReadmeResponse(
            success=False,
            error_message=str(e),
            generation_timestamp=datetime.datetime.now().isoformat(),
            repo_url=request.repo_url,
            generation_method=request.generation_method
        )
