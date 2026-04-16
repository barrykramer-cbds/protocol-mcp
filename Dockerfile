FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY . /app
WORKDIR /app

ENV PYTHONUNBUFFERED=1

RUN uv pip install --system fastmcp>=2.0.0 pydantic>=2.0.0 uvicorn>=0.30.0

EXPOSE 8080

CMD ["python", "server.py"]
