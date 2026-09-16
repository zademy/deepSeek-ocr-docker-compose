# 🚀 DeepSeek OCR - AI-Powered Text Recognition

> Complete OCR system using the **DeepSeek-OCR-2** model (Released Jan 2026) with modern web interface and production-ready REST API.

[![License: MIT](https://img.shields.io/badge/License-MIT%20(Dev%20Only)-yellow.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.12+-green?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-teal?logo=fastapi)](https://fastapi.tiangolo.com/)
[![CUDA](https://img.shields.io/badge/CUDA-11.8+-76B900?logo=nvidia)](https://developer.nvidia.com/cuda-toolkit)
[![Code of Conduct](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](CODE_OF_CONDUCT.md)

⚠️ **IMPORTANT:** This project is for **DEVELOPMENT and TESTING ONLY**. Not intended for production use. See [LICENSE](LICENSE) for details.

## ✨ Features

- 🤖 **Latest AI Model** - DeepSeek-OCR-2 optimized for text recognition
- 🌐 **Interfaz clara** - Flujo de tres pasos pensado para personas no técnicas
- 📊 **Progress Tracking** - Real-time model download progress bar
- 🎮 **Demo Mode** - Test the interface without downloading the model
- 🔌 **Complete REST API** - Easy integration with FastAPI
- 🐳 **Docker Compose** - Deploy in minutes with one command
- ⚡ **GPU Accelerated** - NVIDIA CUDA support for maximum speed
- ♿ **Accesible** - Keyboard navigation, WCAG AA contrast, responsive from 320px
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
- [CPU-Only / Apple Silicon](#-cpu-only--apple-silicon)
- [Contributing](#-contributing)
- [Security](#-security)
- [License](#-license)
- [Resources](#-resources)

---

## 📝 Requirements

- **Docker** 20.10+ and **Docker Compose** 2.0+
- **NVIDIA GPU** with CUDA 11.8+ (for GPU acceleration, optional — see [CPU-only mode](#-cpu-only--apple-silicon))
- At least **8GB VRAM** (recommended for optimal performance)
- **10GB** disk space (for model cache)
- **Windows 10/11**, **Linux**, or **macOS** (with Docker Desktop)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/zademy/deepSeek-ocr-docker-compose
cd deepSeek-ocr-docker-compose
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env if needed (optional)
```

### 3. Start Services

```bash
# Standard (no GPU reservation — works on any Docker host)
docker compose up -d

# With NVIDIA GPU acceleration
docker compose -f docker-compose.yml -f docker-compose.gpu.yml up -d
```

### 4. Access the Application

- **Web Interface**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **API Health Check**: http://localhost:8000/health

### 5. Download Model (First Time)

When you first access the web interface, you'll see a "Preparar modelo" panel. Click it and wait for the download to complete (this may take several minutes depending on your internet connection).

Alternatively, use **Demo Mode** ("Probar sin modelo") to test the interface without downloading the model. Results in demo mode are clearly marked as simulated.

### Web interface formats

The web interface accepts **JPG, PNG and WEBP** up to 10 MB. PDF is not supported by the interface pipeline.

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
│   ├── main.py                # API endpoints (thin shells)
│   ├── model_lifecycle.py     # Model loading state machine + DeepSeek adapter
│   ├── ocr_handler.py         # OCR request pipeline
│   ├── config.py              # Configuration
│   ├── Dockerfile             # Container image
│   ├── requirements.txt       # Python dependencies
│   └── tests/                 # Unit tests (pytest, no GPU needed)
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
  - CUDA_VISIBLE_DEVICES=0              # GPU to use
  - MODEL_NAME=deepseek-ai/DeepSeek-OCR-2
  - BASE_SIZE=1024                       # Base resolution
  - IMAGE_SIZE=768                       # Crop size (OCR-2 default)
```

## 📖 API Usage

### Image OCR Endpoint

```
curl -X POST "http://localhost:8000/api/ocr" \
  -F "file=@image.jpg" \
  -F "mode=markdown"
```

### Available Modes

| Mode | Interface label (Spanish) | Recommended Use |
|------|---------------------------|-----------------|
| `markdown` | Documento con formato | Documents (default) |
| `free_ocr` | Texto sin formato | General text |
| `grounding` | Texto con posiciones | Detailed analysis |
| `parse_figure` | Figuras y gráficos | Charts, tables |
| `detailed` | Descripción de la imagen | Visual analysis |

The web interface shows these as "Opciones avanzadas" (collapsed by default); the API accepts the raw values.

### Response Example

```
{
  "text": "# Document Title\n\nExtracted content...",
  "mode": "markdown",
  "processing_time": 2.5,
  "image_size": [1024, 768],
  "tokens": 2257
}
```

## 🎯 Prompt Examples

```
# Document
"<image>\n<|grounding|>Convert the document to markdown."

# General image
"<image>\n<|grounding|>OCR this image."

# No format
"<image>\nFree OCR."

# Figures
"<image>\nParse the figure."

# Detailed description
"<image>\nDescribe this image in detail."
```

## 🐳 Docker Commands

```
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart
docker-compose restart

# Rebuild images
docker-compose build --no-cache
```

## 🔍 Monitoring

### Health Check

```
curl http://localhost:8000/health
```

### API Logs

```
docker-compose logs -f deepseek-ocr-api
```

## 📊 Performance

Benchmark results with 3503×1668 pixels image on NVIDIA A100 40GB:

| Mode | Time | Quality | Structure |
|------|--------|---------|------------|
| Free OCR | ~24s | ⭐⭐⭐ | Basic |
| Markdown | ~39s | ⭐⭐⭐ | Complete |
| Grounding | ~58s | ⭐⭐ | + Coords |
| Detailed | ~9s | N/A | Description |

*Hardware: NVIDIA A100 40GB*

## 🛠️ Supported Resolutions (DeepSeek-OCR-2)

- **Dynamic resolution** (default): (0-6)×768×768 + 1×1024×1024 — (0-6)×144 + 256 visual tokens

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

Reduce resolution in `.env`:
```
BASE_SIZE=640
IMAGE_SIZE=512
```

### Port Already in Use

Change ports in `docker-compose.yml`:
```yaml
ports:
  - "3001:80"  # Frontend (change 3000 to 3001)
  - "8001:8000"  # Backend (change 8000 to 8001)
```

For more help, check the [documentation](docs/) or open an issue.

## 💻 CPU-Only / Apple Silicon

The stack runs on hosts without an NVIDIA GPU (model loads on CPU, slower):

```bash
docker compose up -d
```

On Apple Silicon Macs, the backend forces `platform: linux/amd64` because PyTorch cu118 wheels are x86_64-only. Note that loading the 3B-parameter model on CPU needs ~8GB RAM — increase Docker Desktop's VM memory accordingly. Use **Demo Mode** in the web UI to validate the interface without loading the model.

## 📜 Resources

- [DeepSeek-OCR-2 Official Repository](https://github.com/deepseek-ai/DeepSeek-OCR-2)
- [Model on HuggingFace](https://huggingface.co/deepseek-ai/DeepSeek-OCR-2)
- [DeepSeek-OCR-2 Research Paper](https://arxiv.org/abs/2601.20552)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)

---

## 📝 License

**MIT License - Development and Testing Only**

This software is licensed under the MIT License with specific restrictions for development and testing purposes only. It is **NOT intended for production use**.

⚠️ **Production Use Warning**: If you choose to use this software in production, you do so entirely at your own risk and responsibility. The authors provide no guarantees, support, or liability for production deployments.

See the [LICENSE](LICENSE) file for full terms and conditions.

### Third-Party Components

- **DeepSeek-OCR-2 Model**: Subject to its own license terms
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

**Version**: 2.0.0  
**Status**: Active Development  
**Last Updated**: September 2026
**Model**: DeepSeek-OCR-2 (deepseek-ai)  
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
