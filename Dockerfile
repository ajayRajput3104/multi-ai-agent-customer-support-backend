# =========================
# 1️⃣ Base image
# =========================
FROM python:3.11-slim

# =========================
# 2️⃣ Set working directory
# =========================
WORKDIR /app

# =========================
# 3️⃣ Install system dependencies
# =========================
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl \
    && rm -rf /var/lib/apt/lists/*

# =========================
# 4️⃣ Copy requirements and install Python packages
# =========================
COPY requirements.txt .
RUN pip install --upgrade --no-cache-dir pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# =========================
# 5️⃣ Copy project code
# =========================
COPY backend ./backend

# =========================
# 6️⃣ Environment variables
# =========================
ENV PYTHONUNBUFFERED=1
ENV GROQ_API_KEY=""

# =========================
# 7️⃣ Expose port & run app
# =========================
EXPOSE 8000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
