FROM python:3.12-alpine

ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache \
    postgresql-dev \
    gcc \
    python3-dev \
    musl-dev \
    postgresql-client \
    jpeg-dev \
    zlib-dev \
    linux-headers

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app
COPY . .

