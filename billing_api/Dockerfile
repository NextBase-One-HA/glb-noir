# Build with context = this directory (billing_api), e.g.
#   cd billing_api && gcloud run deploy SERVICE --source . --region asia-northeast1
FROM python:3.12-slim
WORKDIR /app

COPY requirements-billing.txt .
RUN pip install --no-cache-dir -r requirements-billing.txt

COPY main.py .
COPY canonical ./canonical

# Fail the image build if the law files are not in the context
RUN test -f canonical/ORE_LAYER_SYNC.json && test -f canonical/ORE_LAYER_LOCK.json

ENV CANONICAL_PATH=/app/canonical
ENV PYTHONPATH=/app
ENV PORT=8080
EXPOSE 8080

CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT}
