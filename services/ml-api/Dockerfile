FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN useradd --create-home --uid 10001 appuser

COPY services/ml-api/requirements.txt ./api-requirements.txt
COPY services/ml-api/ml-requirements.txt ./ml-requirements.txt
RUN pip install --no-cache-dir -r api-requirements.txt \
    && pip install --no-cache-dir torch==2.9.0 --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir -r ml-requirements.txt \
    && python -m nltk.downloader -d /usr/local/share/nltk_data punkt punkt_tab

RUN mkdir -p /home/appuser/.cache/huggingface \
    && chown -R appuser:appuser /home/appuser/.cache

COPY services/ml-api/app ./app
COPY ML ./ML

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=15s --timeout=5s --start-period=15s --retries=5 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=3)"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
