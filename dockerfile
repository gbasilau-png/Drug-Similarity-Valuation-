# Use official slim Python 3.11 image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for pandas, kaleido, etc.
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements first for caching
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create a non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose Dash default port
EXPOSE 8050

# Gunicorn configuration optimized for Dash
# Make sure `server` exists in app.py: `server = app.server`
CMD ["gunicorn", "--bind", "0.0.0.0:8050", "--workers", "2", "--threads", "2", "--timeout", "60", "app:server"]
