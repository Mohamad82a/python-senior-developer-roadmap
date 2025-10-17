# Simple Dockerfile
FROM python:3.11-slim


# --- Working Directory ---
WORKDIR /app


# --- Python Dependencies ---
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


# --- Application Code ---
COPY . .
RUN pip install fastapi uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
