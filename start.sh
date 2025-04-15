#!/bin/bash

# Exit on any error
set -e

# Compile translation files (Babel)
echo "Compiling Babel translations..."
pybabel compile -d translations

# Apply Alembic migrations
echo "Running Alembic migrations..."
alembic upgrade heads

# Start your bot/app
echo "Starting bot.py..."
python3 bot.py
