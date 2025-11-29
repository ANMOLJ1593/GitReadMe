# Use Python slim image for lightweight container
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Avoid writing .pyc files and force stdout flush
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies (needed for GitPython)
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend application
COPY . .

# FastAPI will run at port 8000
EXPOSE 8000

# Render uses PORT env, so set default
ENV PORT=8000

# Health check (via curl)
RUN apt-get update && apt-get install -y curl

HEALTHCHECK CMD curl --fail http://localhost:8000/health || exit 1

# Use uvicorn to run FastAPI
CMD ["uvicorn", "fastapi_app:app", "--host", "0.0.0.0", "--port", "8000"]
