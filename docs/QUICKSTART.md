# ⚡ DeepSeek OCR - Quick Start

## 🎯 What is this?

**DeepSeek OCR** is a complete optical character recognition (OCR) solution using state-of-the-art AI. This project includes:

- ✅ **DeepSeek-OCR Model** - 6.6GB open source AI optimized for OCR
- ✅ **REST API** - FastAPI backend for easy integration
- ✅ **Web Interface** - Modern frontend for code-free usage
- ✅ **Docker Compose** - Complete deployment in minutes

## 📋 Minimum Requirements

- **Docker** 20.10+
- **Docker Compose** 2.0+
- **8GB RAM**
- **10GB disk space**
- **(Optional) NVIDIA GPU** with CUDA 11.8+ for better performance

## 🚀 Installation in 3 Steps

### 1️⃣ Prepare Environment

```bash
# Copy configuration
cp .env.example .env

# (Optional) Edit configuration
# nano .env
```

### 2️⃣ Start Services

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f
```

### 3️⃣ Use it!

- **Web**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/health

## 📖 Basic Usage

### Web Interface

1. Open http://localhost:3000
2. Drag and drop an image
3. Select mode (recommended: "Markdown")
4. Click "Process OCR"
5. Copy or download the result

### API (cURL)

```bash
curl -X POST "http://localhost:8000/api/ocr" \
  -F "file=@document.jpg" \
  -F "mode=markdown"
```

### API (Python)

```python
import requests

files = {'file': open('image.jpg', 'rb')}
data = {'mode': 'markdown'}

response = requests.post(
    'http://localhost:8000/api/ocr',
    files=files,
    data=data
)

print(response.json()['text'])
```

## 🎨 Available Modes

| Mode | Speed | Best For |
|------|-------|----------|
| `free_ocr` | ⚡⚡⚡ | Fast simple text |
| `markdown` | ⚡⚡ | Structured documents |
| `grounding` | ⚡ | Text + coordinates |
| `parse_figure` | ⚡⚡ | Charts and tables |
| `detailed` | ⚡⚡⚡ | Image description |

## 📊 Usage Examples

### Digitize Invoice

```bash
curl -X POST "http://localhost:8000/api/ocr" \
  -F "file=@invoice.jpg" \
  -F "mode=markdown" \
  -F "custom_prompt=<image>\nExtract: number, date, total"
```

### Process Multiple Images

```python
from pathlib import Path
import requests

for img in Path('documents/').glob('*.jpg'):
    files = {'file': open(img, 'rb')}
    data = {'mode': 'markdown'}
    
    result = requests.post(
        'http://localhost:8000/api/ocr',
        files=files,
        data=data
    ).json()
    
    # Save result
    with open(f'output/{img.stem}.txt', 'w') as f:
        f.write(result['text'])
```

## 🔧 Useful Commands

```bash
# View real-time logs
docker-compose logs -f

# Restart services
docker-compose restart

# Stop everything
docker-compose down

# Check status
docker-compose ps

# Verify health
curl http://localhost:8000/health
```

## 🐛 Quick Troubleshooting

### API not loading model

```bash
# View logs
docker-compose logs deepseek-ocr-api

# Restart
docker-compose restart deepseek-ocr-api
```

### GPU not detected

```bash
# Verify NVIDIA Docker
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
```

### Very slow processing

**Solution**: Make sure to use GPU. If you don't have GPU, reduce resolution:

```yaml
# In docker-compose.yml
environment:
  - BASE_SIZE=640  # default: 1024
```

### Out of Memory

**Solution**: Reduce resolution or use smaller images:

```python
# Resize image before sending
from PIL import Image
img = Image.open('large.jpg')
img.thumbnail((1024, 1024))
img.save('small.jpg')
```

## 📈 Expected Performance

With **NVIDIA A100 GPU**:
- Free OCR: ~24s per image
- Markdown: ~39s per image
- Grounding: ~58s per image
- Detailed: ~9s per image

With **CPU**: 3-5x slower

## 🔒 Security

⚠️ **For local development only**

If you expose publicly:
- Add authentication
- Configure rate limiting
- Use HTTPS
- Validate files strictly

## 📚 Complete Documentation

- **../README.md** - Overview and features
- **USAGE_GUIDE.md** - Detailed usage guide
- **test_api.py** - Test script

## 🔗 Important Links

- [Original DeepSeek-OCR Repo](https://github.com/deepseek-ai/DeepSeek-OCR)
- [Model on HuggingFace](https://huggingface.co/deepseek-ai/DeepSeek-OCR)
- [FastAPI Docs](http://localhost:8000/docs) (when running)

## 💡 Tips

1. **First time**: Model downloads (~6.6GB), may take 10-20 min
2. **GPU vs CPU**: GPU is 3-5x faster
3. **Best quality**: Use 1024×1024 pixel images
4. **Best speed**: Use `free_ocr` mode
5. **Batch processing**: Process multiple images in parallel with Python

## 🆘 Help

1. Check logs: `docker-compose logs -f`
2. Verify health: `curl http://localhost:8000/health`
3. Read USAGE_GUIDE.md
4. Run test: `python test_api.py image.jpg`

## 🎉 All Set!

You now have a complete AI-powered OCR system.

**Next steps**:
- Test with your own images
- Experiment with different modes
- Integrate the API into your applications
- Read USAGE_GUIDE.md for advanced cases

---

**Happy OCR! 🚀**
