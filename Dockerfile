# Use Python 3.12 slim from Docker Hub
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt /app/

# Install Python dependencies with increased timeout
RUN --mount=type=cache,target=/root/.cache pip install -r requirements.txt

# Copy project files
COPY src /app/
COPY deploy/docker/app/entrypoint.sh /app/

# Create a non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
