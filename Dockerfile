FROM python:3.12.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TAREFAS_DATABASE_URL=sqlite:////data/tarefas.db

COPY pyproject.toml ./
COPY app ./app
COPY tests ./tests
COPY scripts ./scripts

RUN python -m pip install --no-cache-dir ".[test]" && mkdir -p /data

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
