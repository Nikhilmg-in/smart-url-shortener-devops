# ---------- Stage 1: build the wheel artifact ----------
FROM python:3.11-slim AS builder

WORKDIR /build
RUN pip install --no-cache-dir build
COPY pyproject.toml main.py ./
RUN python -m build --wheel

# ---------- Stage 2: slim runtime image ----------
FROM python:3.11-slim AS runtime

ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY --from=builder /build/dist/*.whl /tmp/
RUN pip install --no-cache-dir /tmp/*.whl && rm -f /tmp/*.whl

# Run as a non-root user
RUN useradd --create-home appuser
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
