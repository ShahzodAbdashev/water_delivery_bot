# Build stage
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY src/ src/


# Run the FastAPI application
CMD ["python3", "bot.py"]