# Deploy from THIS directory (billing_api) — uploads only files here.
#   gcloud run deploy nextbase-billing --source . --region asia-northeast1
# (Use a dedicated service name; do not reuse nextbase-api unless you intend to replace that image.)
#
# Build context must include ./canonical (sync: cp -r ../canonical ./canonical).
FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
  && apt-get install -y --no-install-recommends ca-certificates \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Single copy: whole module tree; .dockerignore strips only local junk (not canonical/).
COPY . .

RUN pip install --no-cache-dir -r requirements-billing.txt

RUN set -eux; \
  ls -la; \
  ls -la canonical/; \
  test -f canonical/ORE_LAYER_SYNC.json; \
  test -f canonical/ORE_LAYER_LOCK.json

ENV CANONICAL_PATH=/app/canonical
ENV PYTHONPATH=/app
ENV PORT=8080
EXPOSE 8080

CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT}
