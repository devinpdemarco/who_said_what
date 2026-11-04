FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN useradd --create-home --uid 10002 appuser

COPY services/data-api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY services/data-api/app ./app
COPY data_pipeline ./data_pipeline
COPY supabase_client.py ./supabase_client.py

USER appuser

EXPOSE 8001

HEALTHCHECK --interval=15s --timeout=5s --start-period=15s --retries=5 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8001/health', timeout=3)"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
