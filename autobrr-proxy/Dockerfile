FROM python:3.11-slim AS builder

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /build
COPY requirements.txt .

# ✅ Instalar no diretório customizado
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ============================================
# Stage final
# ============================================
FROM python:3.11-slim

RUN groupadd -r autobrr && \
    useradd -r -g autobrr -u 1000 autobrr

WORKDIR /app

# ✅ Copiar para /usr/local (padrão do Python)
COPY --from=builder /install /usr/local

COPY --chown=autobrr:autobrr autobrr-proxy-unified.py .

EXPOSE 8888
USER autobrr

CMD ["python", "-u", "autobrr-proxy-unified.py"]