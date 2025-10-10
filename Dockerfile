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
# 4️⃣ Upgrade pip
# =========================
RUN pip install --upgrade pip

# =========================
# 5️⃣ Copy and install Python dependencies
# =========================
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# =========================
# 6️⃣ Copy project code
# =========================
COPY backend ./backend

# =========================
# 7️⃣ Environment variables
# =========================
ENV PYTHONUNBUFFERED=1
ENV GROQ_API_KEY=""

# =========================
# 8️⃣ Expose port & run app
# =========================
EXPOSE 8000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
