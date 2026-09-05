FROM python:3.12-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY services/ai/requirements.lock.txt ./requirements.lock.txt
RUN pip install --no-cache-dir -r requirements.lock.txt
COPY services ./services
EXPOSE 8000
CMD ["uvicorn", "services.ai.app:app", "--host", "0.0.0.0", "--port", "8000"]
