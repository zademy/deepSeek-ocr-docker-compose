# 🚀 DeepSeek OCR - AI-Powered Text Recognition

> Complete OCR system using the **DeepSeek-OCR** model (Released Oct 2025) with modern web interface and production-ready REST API.

[![License: MIT](https://img.shields.io/badge/License-MIT%20(Dev%20Only)-yellow.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-green?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-teal?logo=fastapi)](https://fastapi.tiangolo.com/)
[![CUDA](https://img.shields.io/badge/CUDA-11.8+-76B900?logo=nvidia)](https://developer.nvidia.com/cuda-toolkit)
[![Code of Conduct](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](CODE_OF_CONDUCT.md)

⚠️ **IMPORTANT:** This project is for **DEVELOPMENT and TESTING ONLY**. Not intended for production use. See [LICENSE](LICENSE) for details.

## ✨ Features

- 🤖 **Latest AI Model** - DeepSeek-OCR optimized for text recognition
- 🌐 **Modern Web Interface** - Intuitive UI with drag-and-drop upload
- 📊 **Progress Tracking** - Real-time model download progress bar
- 🎮 **Demo Mode** - Test the interface without downloading the model
- 🔌 **Complete REST API** - Easy integration with FastAPI
- 🐳 **Docker Compose** - Deploy in minutes with one command
- ⚡ **GPU Accelerated** - NVIDIA CUDA support for maximum speed
- 📝 **Multiple Modes** - Free OCR, Markdown, Grounding, Parse Figure, Detailed
- 🔓 **100% Open Source** - MIT License for development/testing

## 📚 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Usage](#-usage)
  - [Web Interface](#web-interface)
  - [API Usage](#-api-usage)
- [Documentation](#-documentation)
- [Configuration](#-configuration)
- [Performance](#-performance)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [Security](#-security)
- [License](#-license)
- [Resources](#-resources)

---

## 📝 Requirements

- **Docker** 20.10+ and **Docker Compose** 2.0+
- **NVIDIA GPU** with CUDA 11.8+ (for GPU acceleration)
- At least **8GB VRAM** (recommended for optimal performance)
- **10GB** disk space (for model cache)
- **Windows 10/11**, **Linux**, or **macOS** (with Docker Desktop)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/deepseek-ocr.git
cd deepseek-ocr
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env if needed (optional)
```

### 3. Start Services
```bash
docker-compose up -d
```

### 4. Access the Application

- **Web Interface**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **API Health Check**: http://localhost:8000/health

### 5. Download Model (First Time)

When you first access the web interface, you'll see a button to download the DeepSeek-OCR model. Click it and wait for the download to complete (this may take several minutes depending on your internet connection).

Alternatively, use **Demo Mode** to test the interface without downloading the model.

### API Usage Example

```
curl -X POST "http://localhost:8000/api/ocr" \
  -F "file=@document.jpg" \
  -F "mode=markdown"
```

**API Documentation**: http://localhost:8000/docs

## 📚 Documentation

Detailed documentation is available in the `/docs` folder:

- **[QUICKSTART.md](docs/QUICKSTART.md)** - Quick setup guide
- **[USAGE_GUIDE.md](docs/USAGE_GUIDE.md)** - Complete usage manual
- **[WINDOWS_SETUP.md](docs/WINDOWS_SETUP.md)** - Windows-specific setup guide

### API Documentation

Interactive API documentation is available at http://localhost:8000/docs when the server is running.

---

## 🧰 Architecture

```
deepseek-ocr/
├── 📄 Configuration Files
│   ├── docker-compose.yml     # Docker orchestration
│   ├── .env.example           # Environment template
│   └── .gitignore             # Git ignore rules
│
├── 📖 Documentation
│   ├── README.md              # Main documentation
│   ├── LICENSE                # MIT License (Dev/Test)
│   ├── CONTRIBUTING.md        # Contribution guidelines
│   ├── CODE_OF_CONDUCT.md     # Code of conduct
│   ├── SECURITY.md            # Security policy
│   └── docs/                  # Additional documentation
│
├── 🐍 Backend (FastAPI)
│   ├── main.py                # API endpoints
│   ├── config.py              # Configuration
│   ├── Dockerfile             # Container image
│   └── requirements.txt       # Python dependencies
│
├── 🌐 Frontend (HTML/JS/CSS)
│   ├── index.html             # UI structure
│   ├── app.js                 # Application logic
│   ├── styles.css             # Styling
│   ├── nginx.conf             # Web server config
│   └── Dockerfile             # Container image
│
├── 💾 Data Directories
│   ├── uploads/               # Uploaded images
│   └── outputs/               # OCR results
│
└── 🧪 Testing
    └── test_api.py            # API test script
```

## 🔧 Configuration

### Environment Variables

Edit `docker-compose.yml` or create a `.env` file to customize:

```
environment:
  - CUDA_VISIBLE_DEVICES=0          # GPU a usar
  - MODEL_NAME=deepseek-ai/DeepSeek-OCR
  - MAX_IMAGE_SIZE=1024              # Resolución máxima
```

## 📖 Uso del API

### Endpoint: OCR de Imagen

```
curl -X POST "http://localhost:8000/api/ocr" \
  -F "file=@imagen.jpg" \
  -F "mode=markdown"
```

### Modos Disponibles

| Modo | Descripción | Uso Recomendado |
|------|-------------|-----------------|
| `free_ocr` | OCR rápido sin estructura | Texto general |
| `markdown` | Convierte a Markdown | Documentos |
| `grounding` | OCR + coordenadas | Análisis detallado |
| `detailed` | Descripción de imagen | Análisis visual |

### Ejemplo de Respuesta

```
{
  "text": "# Título del Documento\n\nContenido extraído...",
  "mode": "markdown",
  "processing_time": 2.5,
  "image_size": [1024, 768],
  "tokens": 2257
}
```

## 🎯 Ejemplos de Prompts

```
# Documento
"<image>\n<|grounding|>Convert the document to markdown."

# Imagen general
"<image>\n<|grounding|>OCR this image."

# Sin formato
"<image>\nFree OCR."

# Figuras
"<image>\nParse the figure."

# Descripción detallada
"<image>\nDescribe this image in detail."
```

## 🐳 Comandos Docker

```
# Iniciar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down

# Reiniciar
docker-compose restart

# Reconstruir imágenes
docker-compose build --no-cache
```

## 🔍 Monitoreo

### Health Check

```
curl http://localhost:8000/health
```

### Logs del API

```
docker-compose logs -f deepseek-ocr-api
```

## 📊 Performance

Benchmark results with 3503×1668 pixels image on NVIDIA A100 40GB:

| Modo | Tiempo | Calidad | Estructura |
|------|--------|---------|------------|
| Free OCR | ~24s | ⭐⭐⭐ | Básica |
| Markdown | ~39s | ⭐⭐⭐ | Completa |
| Grounding | ~58s | ⭐⭐ | + Coords |
| Detailed | ~9s | N/A | Descripción |

*Hardware: NVIDIA A100 40GB*

## 🛠️ Resoluciones Soportadas

- **Tiny**: 512×512 (64 tokens)
- **Small**: 640×640 (100 tokens)
- **Base**: 1024×1024 (256 tokens) - Recomendado
- **Large**: 1280×1280 (400 tokens)
- **Dynamic**: múltiples crops + base

## 🐛 Troubleshooting

### GPU Not Detected

```bash
# Verify NVIDIA runtime
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
```

### Model Not Downloading

- Check internet connection
- Verify disk space (need ~7GB free)
- Use the download button in the web interface
- Check logs: `docker-compose logs -f deepseek-ocr-api`

### Out of Memory

Reduce resolution in `backend/config.py`:
```python
BASE_SIZE = 640  # instead of 1024
```

### Port Already in Use

Change ports in `docker-compose.yml`:
```yaml
ports:
  - "3001:80"  # Frontend (change 3000 to 3001)
  - "8001:8000"  # Backend (change 8000 to 8001)
```

For more help, check the [documentation](docs/) or open an issue.

## 📜 Resources

- [DeepSeek-OCR Official Repository](https://github.com/deepseek-ai/DeepSeek-OCR)
- [Model on HuggingFace](https://huggingface.co/deepseek-ai/DeepSeek-OCR)
- [DeepSeek Research Paper](https://github.com/deepseek-ai/DeepSeek-OCR#paper)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)

---

## 📝 License

**MIT License - Development and Testing Only**

This software is licensed under the MIT License with specific restrictions for development and testing purposes only. It is **NOT intended for production use**.

⚠️ **Production Use Warning**: If you choose to use this software in production, you do so entirely at your own risk and responsibility. The authors provide no guarantees, support, or liability for production deployments.

See the [LICENSE](LICENSE) file for full terms and conditions.

### Third-Party Components

- **DeepSeek-OCR Model**: Subject to its own license terms
- **Other dependencies**: Check individual package licenses in `requirements.txt`

---

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting PRs.

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please follow our [Code of Conduct](CODE_OF_CONDUCT.md) in all interactions.

---

## 🔒 Security

⚠️ **This project is for development and testing only.** 

For security concerns, please review our [Security Policy](SECURITY.md).

**Key Security Notes:**
- No authentication implemented
- Not hardened for production use
- Use at your own risk in production environments
- Report vulnerabilities via GitHub issues with `security` label

---

## 🚀 Getting Help

- **Documentation**: Check the [docs](docs/) folder
- **Issues**: Open an issue on GitHub
- **Discussions**: Use GitHub Discussions for questions
- **API Docs**: Visit http://localhost:8000/docs when running

---

## 📌 Project Status

**Version**: 1.0.0  
**Status**: Active Development  
**Last Updated**: January 2025  
**Model**: DeepSeek-OCR (deepseek-ai)  
**Purpose**: Development and Testing Only

---

## ⭐ Show Your Support

If you find this project helpful, please consider:
- Giving it a ⭐ on GitHub
- Sharing it with others
- Contributing improvements
- Reporting bugs and suggestions

---

**Made with ❤️ for the AI community**
