# 1. Base image (Python installed)
FROM python:3.11-slim

# 2. Set working directory inside container
WORKDIR /app17

# 3. Copy dependency list first (for caching)
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip uninstall -y jwt PyJWT || true
RUN pip install --no-cache-dir PyJWT

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:9000/health || exit 1

# 5. Copy all project files
COPY . .

# 6. Expose Flask port
EXPOSE 9000

# 7. Start the webhook server (NOT Invoice.py)
CMD ["gunicorn", "-b", "0.0.0.0:9000", "app:app17"]