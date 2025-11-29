"""
FastAPI GitReadme Application (OpenAI Version)
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import logging
import datetime
import os

from app import ReadmeGeneratorApp    # ✅ FIXED IMPORT
from api_helper import (
    log_request_metrics, 
    validate_github_url, 
    sanitize_repo_name,
    format_error_response,
    log_generation_attempt,
    get_client_info,
    check_rate_limit,
    metrics
)

templates = Jinja2Templates(directory="templates")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="GitReadme - AI README Generator",
    description="OpenAI-powered README generator",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://gitreadme.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


try:
    readme_app = ReadmeGeneratorApp()
    logger.info("GitReadme initialized successfully")
except Exception as e:
    logger.error(f"Initialization failed: {e}")
    readme_app = None


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "home_page.html",
        {
            "request": request,
            "app_name": "GitReadme",
            "app_version": "1.0.0",
            "current_year": datetime.datetime.now().year
        }
    )


@app.post("/generate-readme", response_model=ReadmeResponse)
@log_request_metrics
async def generate_readme(request: ReadmeRequest, http_request: Request):

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
