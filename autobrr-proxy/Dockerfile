FROM python:3.11-slim AS builder

# Instala dependências de build
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Copia requirements e instala
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ============================================
# Stage final (imagem mínima)
# ============================================
FROM python:3.11-slim

# Metadata
LABEL maintainer="Marcos <your-email@example.com>"
LABEL description="Autobrr Proxy for Brazilian Trackers"
LABEL version="2.0.0"

# Cria user não-root
RUN groupadd -r autobrr && \
    useradd -r -g autobrr -u 1000 autobrr

WORKDIR /app

# Copia dependências do builder
COPY --from=builder /root/.local /root/.local

# Copia aplicação
COPY --chown=autobrr:autobrr autobrr-proxy-unified.py .

# Adiciona PATH do pip user
ENV PATH=/root/.local/bin:$PATH

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8888/health').read()"

# Expõe porta
EXPOSE 8888

# Roda como usuário não-root
USER autobrr

# Comando
CMD ["python", "-u", "autobrr-proxy-unified.py"]