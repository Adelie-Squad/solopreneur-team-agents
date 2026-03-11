FROM python:3.12-slim

WORKDIR /app

# Claude Code CLI 설치 (Node.js 필요)
RUN apt-get update && apt-get install -y \
    curl git nodejs npm \
    && npm install -g @anthropic-ai/claude-code \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY core/ ./core/
COPY routines/ ./routines/

ENV PYTHONUNBUFFERED=1
