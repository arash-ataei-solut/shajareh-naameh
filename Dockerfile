# Use Python 3.12 slim from Docker Hub
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DEFAULT_TIMEOUT=100
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_NO_CACHE_DIR=1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Configure pip to use a more reliable mirror
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn

# Copy requirements file
COPY requirements.txt /app/

# Install Python dependencies with increased timeout
RUN pip install --no-cache-dir -r requirements.txt --timeout 100

# Copy project files
COPY src /app/

# Create a non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
