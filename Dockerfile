# Use Python 3.12 slim from Docker Hub
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app
VOLUME /app

# Copy requirements file
COPY requirements.txt /app/

# Install Python dependencies with increased timeout
RUN --mount=type=cache,target=/root/.cache pip install -r requirements.txt

# Copy project files
COPY deploy/docker/app/entrypoint.sh /entrypoint/

CMD ["sh", "/entrypoint/entrypoint.sh"]
