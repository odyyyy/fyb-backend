FROM python:3.12-slim as base

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && apt-get install -y libpq-dev \
    gcc \
    python3-dev \
    postgresql-client


FROM base as dev
WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.6.6 /uv /uvx /bin/

COPY . .

RUN uv sync --frozen --no-cache

RUN useradd -u 8877 nonroot
USER nonroot