# ═══════════════════════════════════════════════════════════════════════════════
# DevSecOps Hardened Container: Autonomous AI Ads -> Voice -> Revenue Engine
# Principle #3: Zero-CVE Distroless / Hardened Slim Base
# Principle #4: Non-root execution (UID 65532) & Read-Only Root Filesystem
# ═══════════════════════════════════════════════════════════════════════════════

# Stage 1: Dependency Builder
FROM python:3.12-slim AS builder

WORKDIR /build

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --prefix=/install --no-warn-script-location -r requirements.txt

# Stage 2: Hardened Non-Root Production Runtime
FROM python:3.12-slim AS runner

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/install/bin:${PATH}" \
    PYTHONPATH="/install/lib/python3.12/site-packages:${PYTHONPATH}"

# Create non-root user UID 65532 (compatible with distroless/K8s securityContext)
RUN groupadd -g 65532 appgroup && \
    useradd -u 65532 -g appgroup -s /sbin/nologin -M appuser && \
    mkdir -p /app/data /tmp/runtime && \
    chown -R appuser:appgroup /app /tmp/runtime

# Copy installed Python packages from builder
COPY --from=builder /install /install

# Copy application source code
COPY --chown=appuser:appgroup src/ ./src/

# Enforce non-root execution
USER 65532:65532

EXPOSE 8000

# Health check probe
HEALTHCHECK --interval=15s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health').read()" || exit 1

ENTRYPOINT ["uvicorn", "src.webhook_server:app", "--host", "0.0.0.0", "--port", "8000"]
