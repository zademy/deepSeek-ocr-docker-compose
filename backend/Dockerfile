# Use runtime image instead of devel to reduce size
FROM nvcr.io/nvidia/cuda:11.8.0-runtime-ubuntu22.04

# Evitar prompts interactivos
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# Instalar solo dependencias necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 \
    python3-pip \
    curl \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Configurar Python
RUN ln -sf /usr/bin/python3.10 /usr/bin/python && \
    ln -sf /usr/bin/pip3 /usr/bin/pip

# Directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar PyTorch primero (versión específica para CUDA 11.8)
# Usar pip cache para acelerar rebuilds
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir \
    torch==2.6.0 \
    torchvision==0.21.0 \
    torchaudio==2.6.0 \
    --index-url https://download.pytorch.org/whl/cu118

# Instalar otras dependencias
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt

# Instalar flash-attention (puede fallar, no es crítico)
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir flash-attn==2.7.3 --no-build-isolation || true

# Copiar código de la aplicación
COPY . .

# Crear directorios necesarios
RUN mkdir -p /app/uploads /app/outputs /root/.cache/huggingface

# Exponer puerto
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5m --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Comando de inicio
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
