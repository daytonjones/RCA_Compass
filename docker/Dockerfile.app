# docker/Dockerfile.app
FROM python:3.12-slim

# Install system dependencies (weasyprint might need some dependencies, plus we want to use pip).
RUN apt-get update && apt-get install -y \
    libffi-dev \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libpangoft2-1.0-0 \
    libssl-dev \
    build-essential \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY app/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app/ /app/

# Expose the port
EXPOSE 5000

# Create a non-root user for security
RUN useradd -m rcauser
USER rcauser

# By default, run Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]

