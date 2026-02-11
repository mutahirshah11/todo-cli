# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user for Hugging Face (UID 1000 is standard)
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:${PATH}"

# Copy requirements file (ensure permissions)
COPY --chown=user:user requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --user -r requirements.txt

# Copy the rest of the application code
COPY --chown=user:user . .

# Set Python Path to include root and backend directory for imports
ENV PYTHONPATH=/app:/app/backend

# Hugging Face Spaces use port 7860 by default
EXPOSE 7860

# Run the application using the backend module
# We use backend.main:app because the structure is root/backend/main.py
# HF sets the PORT env var to 7860, so we respect that
CMD uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-7860}
