# Build stage
FROM python:3.11-slim

WORKDIR /app

# Install OS-level dependencies including gettext
RUN apt-get update && \
    apt-get install -y --no-install-recommends gettext && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Run the FastAPI application
CMD ["alembic revision --autogenerate -m 'add:starting new models'","alembic upgrade heads","python3 bot.py"]