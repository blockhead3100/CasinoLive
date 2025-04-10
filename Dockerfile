# syntax=docker/dockerfile:1

# Use a slim Python base image
FROM python:3.9-slim AS base

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY Requirements.txt ./

# Install Python dependencies in a virtual environment
RUN python -m venv /app/.venv \
    && . /app/.venv/bin/activate \
    && pip install --no-cache-dir -r Requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV FLASK_APP=app.py

# Expose the application port
EXPOSE 5000

# Run the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]