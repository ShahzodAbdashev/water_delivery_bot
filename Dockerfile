# Build stage
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .


# Run the FastAPI application
CMD ["alembic revision --autogenerate -m 'add:starting new models'","alembic upgrade heads","python3 bot.py"]