# Build from repository root, e.g.:
#   docker build -f nextbase-api/Dockerfile .
FROM python:3.11-slim
WORKDIR /app
COPY nextbase-api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY nextbase-api/main.py .
COPY nextbase-api/rooms_firestore.py .
COPY nextbase-api/session_firestore.py .
COPY nextbase-api/agent_tasks.py .
COPY docs/NEXTBASE_SYSTEM_CANONICAL.md docs/
COPY docs/SYSTEM_INVENTORY.md docs/
ENV PYTHONUNBUFFERED=1
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
