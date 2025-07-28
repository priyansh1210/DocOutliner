FROM python:3.9-slim

# Set environment variables for multilingual support
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=UTF-8
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PYTHONPATH=/app

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libicu-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and data (preserve directory structure)
COPY src/ ./src/
COPY data/ ./data/
COPY main.py .

# Create directories
RUN mkdir -p /app/input /app/output

# Verify package structure
RUN find /app -name "*.py" -type f

# Make main.py executable
RUN chmod +x main.py

# Default command
CMD ["python", "main.py"]
