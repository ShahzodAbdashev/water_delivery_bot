# Build stage
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gettext bash && \
    rm -rf /var/lib/apt/lists/*

# Copy Python dependencies
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Run shell script to setup and start the app
CMD ["bash", "start.sh"]
