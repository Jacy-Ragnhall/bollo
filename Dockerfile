FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install OS deps required by some Python packages (e.g. psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy project files
COPY . .

# Ensure the entrypoint is executable
RUN chmod +x /app/entrypoint.sh

ENV PORT 8000

EXPOSE 8000

CMD ["/app/entrypoint.sh"]
