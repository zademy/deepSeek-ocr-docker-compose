# 📖 DeepSeek OCR - Usage Guide

## 🎯 Table of Contents

1. [Quick Start](#quick-start)
2. [Using the Web Interface](#using-the-web-interface)
3. [Using the API](#using-the-api)
4. [OCR Modes](#ocr-modes)
5. [Practical Examples](#practical-examples)
6. [Tips and Best Practices](#tips-and-best-practices)
7. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### Prerequisites

- **Docker** and **Docker Compose** installed
- **NVIDIA GPU** with CUDA 11.8+ (recommended, not required)
- At least **8GB RAM** and **10GB disk space**

### Installation in 3 Steps

```bash
# 1. Clone or navigate to directory
cd deepseek-ocr

# 2. Copy configuration
cp .env.example .env

# 3. Start services
docker-compose up -d
```

**On Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

### Verify It's Working

```bash
# View logs
docker-compose logs -f

# Check API health
curl http://localhost:8000/health
```

Access: **http://localhost:3000**

---

## 🖥️ Using the Web Interface

### 1. Upload Image

- **Drag and drop** an image in the upload area
- Or **click** to select from your computer
- Supported formats: JPG, PNG, WEBP, PDF
- Maximum size: 10MB

### 2. Select Mode

| Mode | When to Use | Speed |
|------|-------------|-------|
| **Markdown** | Structured documents | Medium ⚡⚡ |
| **Free OCR** | Simple and fast text | Fast ⚡⚡⚡ |
| **Grounding** | Need text coordinates | Slow ⚡ |
| **Parse Figure** | Charts, tables, diagrams | Medium ⚡⚡ |
| **Detailed** | Image description | Very Fast ⚡⚡⚡ |

### 3. Process

- Click **"Process OCR"**
- Wait 10-60 seconds (depending on mode and GPU)
- Review the results

### 4. Use Results

- **Copy** to clipboard
- **Download** as TXT file
- **New OCR** to process another image

---

## 🔌 Using the API

### Interactive Documentation

Access Swagger documentation:
```
http://localhost:8000/docs
```

### Basic cURL Example

```bash
curl -X POST "http://localhost:8000/api/ocr" \
  -F "file=@my_document.jpg" \
  -F "mode=markdown"
```

### Python Example

```python
import requests

url = "http://localhost:8000/api/ocr"

# Load image
files = {"file": open("document.jpg", "rb")}
data = {"mode": "markdown"}

# Send request
response = requests.post(url, files=files, data=data)
result = response.json()

# Use result
print(result["text"])
print(f"Processed in {result['processing_time']}s")
```

### JavaScript/Node.js Example

```javascript
const FormData = require('form-data');
const fs = require('fs');
const axios = require('axios');

const form = new FormData();
form.append('file', fs.createReadStream('document.jpg'));
form.append('mode', 'markdown');

axios.post('http://localhost:8000/api/ocr', form, {
  headers: form.getHeaders()
})
.then(response => {
  console.log('Text:', response.data.text);
  console.log('Time:', response.data.processing_time);
})
.catch(error => console.error('Error:', error));
```

### Custom Prompt

```bash
curl -X POST "http://localhost:8000/api/ocr" \
  -F "file=@invoice.jpg" \
  -F "mode=markdown" \
  -F "custom_prompt=<image>\nExtract: invoice number, date, total and customer"
```

---

## 🎨 OCR Modes

### 1. **Free OCR** (Fast and Simple)

**When to use:**
- You need only text, without formatting
- Priority in speed
- Simple text without complex structure

**Example:**
```bash
curl -X POST "http://localhost:8000/api/ocr" \
  -F "file=@note.jpg" \
  -F "mode=free_ocr"
```

**Typical output:**
```
This is a simple text
extracted from the image
without special formatting
```

---

### 2. **Markdown** (Structured Documents)

**When to use:**
- Documents with titles, paragraphs, lists
- You need to maintain structure
- You want Markdown format

**Example:**
```bash
curl -X POST "http://localhost:8000/api/ocr" \
  -F "file=@article.jpg" \
  -F "mode=markdown"
```

**Typical output:**
```markdown
# Main Title

## Subtitle

- List item 1
- List item 2

Paragraph with **bold** and *italic* text.
```

---

### 3. **Grounding** (With Coordinates)

**When to use:**
- You need to know WHERE each text is
- Layout analysis
- Region detection

**Example:**
```bash
curl -X POST "http://localhost:8000/api/ocr" \
  -F "file=@form.jpg" \
  -F "mode=grounding"
```

**Typical output:**
```
<|ref|>Name:<|/ref|><|det|>[[120, 50, 200, 80]]<|/det|>
<|ref|>John Pérez<|/ref|><|det|>[[220, 50, 350, 80]]<|/det|>
```

---

### 4. **Parse Figure** (Charts and Tables)

**When to use:**
- Images with bar charts, line charts, pie charts
- Complex tables
- Technical diagrams

**Example:**
```bash
curl -X POST "http://localhost:8000/api/ocr" \
  -F "file=@chart.jpg" \
  -F "mode=parse_figure"
```

---

### 5. **Detailed** (Visual Description)

**When to use:**
- You want an image description
- Not just text, but visual context
- Content analysis

**Example:**
```bash
curl -X POST "http://localhost:8000/api/ocr" \
  -F "file=@photo.jpg" \
  -F "mode=detailed"
```

**Typical output:**
```
The image shows a business presentation slide with a 
blue header containing the title "Q4 Results". Below 
are three bullet points describing financial metrics...
```

---

## 💡 Practical Examples

### Case 1: Digitizing Invoices

```python
import requests

def process_invoice(invoice_file):
    url = "http://localhost:8000/api/ocr"
    
    files = {"file": open(invoice_file, "rb")}
    data = {
        "mode": "markdown",
        "custom_prompt": "<image>\nExtract: number, date, total, customer"
    }
    
    response = requests.post(url, files=files, data=data)
    return response.json()

# Use
result = process_invoice("invoice_001.jpg")
print(result["text"])
```

### Case 2: Batch Processing (Multiple Images)

```python
import os
import requests
from pathlib import Path

def process_batch(image_folder, mode="markdown"):
    results = []
    
    for file in Path(image_folder).glob("*.jpg"):
        print(f"Processing {file.name}...")
        
        files = {"file": open(file, "rb")}
        data = {"mode": mode}
        
        response = requests.post(
            "http://localhost:8000/api/ocr",
            files=files,
            data=data
        )
        
        if response.ok:
            result = response.json()
            results.append({
                "file": file.name,
                "text": result["text"],
                "time": result["processing_time"]
            })
    
    return results

# Process complete folder
results = process_batch("./documents")

# Save results
for r in results:
    with open(f"output/{r['file']}.txt", "w") as f:
        f.write(r["text"])
```

### Case 3: Extract Tables from PDFs

```bash
# Convert PDF to images first (using ImageMagick)
convert -density 300 document.pdf page_%d.jpg

# Process each page
for img in page_*.jpg; do
  curl -X POST "http://localhost:8000/api/ocr" \
    -F "file=@$img" \
    -F "mode=parse_figure" \
    -o "result_$img.json"
done
```

---

## 🎯 Tips and Best Practices

### For Better Quality

1. **Optimal resolution**: 1024×1024 pixels
2. **Format**: JPG or PNG (avoid excessive compression)
3. **Lighting**: Well-lit images, without shadows
4. **Orientation**: Make sure text is upright

### For Better Speed

1. **Use GPU**: Much faster than CPU
2. **Appropriate mode**: `free_ocr` is the fastest
3. **Lower resolution**: Reduce if you don't need maximum quality
4. **Async batch**: Process multiple images in parallel

### Performance Configuration

Edit `docker-compose.yml`:

```yaml
environment:
  - BASE_SIZE=640    # Lower = faster (default: 1024)
  - IMAGE_SIZE=512   # Lower = faster (default: 640)
```

### Memory Adjustments

If you have GPU memory problems:

```yaml
# In docker-compose.yml, limit memory
deploy:
  resources:
    limits:
      memory: 8G
    reservations:
      devices:
        - capabilities: [gpu]
          device_ids: ['0']
```

---

## 🔧 Troubleshooting

### Problem: "Model not loaded"

**Solution:**
```bash
# View container logs
docker-compose logs deepseek-ocr-api

# Restart services
docker-compose restart
```

### Problem: GPU not detected

**Verify NVIDIA Docker:**
```bash
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
```

**If it fails, install NVIDIA Container Toolkit:**
```bash
# Ubuntu/Debian
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

### Problem: Out of Memory (OOM)

**Solutions:**

1. Reduce resolution:
```python
# In backend/config.py
BASE_SIZE = 640  # instead of 1024
```

2. Use CPU if GPU fails:
```yaml
# In docker-compose.yml, comment GPU section:
# deploy:
#   resources:
#     reservations:
#       devices:
#         - driver: nvidia
```

3. Process smaller images

### Problem: Very Slow Processing

**Diagnosis:**
```bash
# Check GPU usage
nvidia-smi

# View real-time logs
docker-compose logs -f deepseek-ocr-api
```

**If using CPU instead of GPU:**
- Verify NVIDIA Docker Toolkit
- Check `CUDA_VISIBLE_DEVICES` in `.env`

### Problem: Connection Errors

**Check services:**
```bash
docker-compose ps
curl http://localhost:8000/health
```

**Restart:**
```bash
docker-compose down
docker-compose up -d
```

### Problem: Empty Results

**Possible causes:**
- Low quality image
- Very small text
- Incorrect mode

**Solutions:**
- Increase image resolution
- Use `grounding` mode instead of `free_ocr`
- Try with `detailed` to see what it detects

---

## 📊 Monitoring

### Real-time Logs

```bash
# All services
docker-compose logs -f

# Only API
docker-compose logs -f deepseek-ocr-api

# Only web
docker-compose logs -f deepseek-ocr-web
```

### Resource Usage

```bash
# Docker stats
docker stats

# GPU usage (if NVIDIA)
watch -n 1 nvidia-smi
```

### Clean Old Files

```bash
# Via API
curl -X DELETE "http://localhost:8000/api/cleanup?days=7"

# Manual
rm -rf uploads/* outputs/*
```

---

## 🔐 Security

### Production

If you expose the API publicly:

1. **Add authentication**
2. **Limit rate limiting**
3. **Validate files strictly**
4. **Use HTTPS**
5. **Configure firewall**

### Recommended Limits

```python
# In backend/config.py
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
RATE_LIMIT = "10/minute"  # Requires middleware
```

---

## 📚 Additional Resources

- [DeepSeek-OCR Repository](https://github.com/deepseek-ai/DeepSeek-OCR)
- [Model on HuggingFace](https://huggingface.co/deepseek-ai/DeepSeek-OCR)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Docker Compose Docs](https://docs.docker.com/compose/)

---

**Questions or problems?** Open an issue in the repository.
