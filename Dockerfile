# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY config.py .
COPY api.py .
COPY bot.py .
COPY storage.py .
COPY main.py .

# Create volume directory for persistent storage
RUN mkdir -p /app/data

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV LOG_FILE=/app/data/webetu_bot.log
ENV GRADES_FILE=/app/data/grades.json
ENV TOKEN_FILE=/app/data/token.json

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import os; exit(0 if os.path.exists('/tmp/bot_health') else 1)" || exit 1

# Run the bot
CMD ["python", "main.py"]
