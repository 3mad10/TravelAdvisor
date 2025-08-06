# Dockerfile.backend
FROM python:3.13

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r app/requirements.txt

CMD ["sh", "-c", "python3 -m app.init_db && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]
