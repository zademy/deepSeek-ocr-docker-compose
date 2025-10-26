# Use runtime image instead of devel to reduce size
FROM nvcr.io/nvidia/cuda:11.8.0-runtime-ubuntu22.04

# Evitar prompts interactivos
ENV DEBIAN_FRONTEND=noninteractive \
    TZ=UTC \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependencias del sistema en una sola capa
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 \
    python3-pip \
    curl \
    libgl1-mesa-glx \
    libglib2.0-0 \
    # Limpiar cache en la misma capa
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean \
    # Configurar Python
    && ln -sf /usr/bin/python3.10 /usr/bin/python \
    && ln -sf /usr/bin/pip3 /usr/bin/pip \
    # Actualizar pip en la misma capa
    && pip install --upgrade pip setuptools wheel

# Directorio de trabajo
WORKDIR /app

# Copiar solo requirements primero (mejor cache de layers)
COPY requirements.txt .

# Instalar todas las dependencias Python en una sola capa optimizada
RUN --mount=type=cache,target=/root/.cache/pip \
    # PyTorch primero (versión específica para CUDA 11.8)
    pip install --no-cache-dir \
    torch==2.0.1 \
    torchvision==0.15.2 \
    torchaudio==2.0.2 \
    --index-url https://download.pytorch.org/whl/cu118 \
    # Instalar otras dependencias en la misma capa
    && pip install --no-cache-dir -r requirements.txt \
    # Intentar flash-attention (puede fallar, no es crítico)
    && pip install --no-cache-dir flash-attn==2.7.3 --no-build-isolation || true \
    # Limpiar archivos temporales de pip
    && rm -rf /tmp/* /root/.cache/pip/*

# Copiar código de la aplicación (usar .dockerignore para excluir archivos innecesarios)
COPY . .

# Crear directorios y limpiar archivos innecesarios en una sola capa
RUN mkdir -p /app/uploads /app/outputs /root/.cache/huggingface \
    # Remover archivos innecesarios del código fuente
    && find /app -type f -name "*.pyc" -delete \
    && find /app -type d -name "__pycache__" -delete \
    && rm -rf /app/.git /app/.pytest_cache /app/.mypy_cache

# Exponer puerto
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5m --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Comando de inicio
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
