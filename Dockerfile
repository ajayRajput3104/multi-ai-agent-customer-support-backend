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
# Install minimal system deps for building Python wheels (esp. langchain deps)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl \
    && rm -rf /var/lib/apt/lists/*

# =========================
# 4️⃣ Copy project files
# =========================
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend ./backend

# =========================
# 5️⃣ Environment variables
# =========================
# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# The key will be injected by Render or Docker CLI
ENV GROQ_API_KEY=""


# =========================
# 6️⃣ Expose port & run app
# =========================
EXPOSE 8000

# Run FastAPI app via Uvicorn
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
