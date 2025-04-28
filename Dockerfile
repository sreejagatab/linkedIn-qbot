# Use Python 3.9 as base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    python -m spacy download en_core_web_sm

# Copy application code
COPY . .

# Create profiles directory
RUN mkdir -p profiles

# Expose port for API
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Start the API server by default
CMD ["python", "api_server.py"]