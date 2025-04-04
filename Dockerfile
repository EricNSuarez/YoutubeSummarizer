FROM python:3.10-slim

# Install system dependencies and clean up
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .

# Explicitly install gunicorn
RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir gunicorn && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# Verify gunicorn installation in final image
RUN which gunicorn

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]