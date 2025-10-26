# 🪟 Windows Setup - DeepSeek OCR

## 📋 Prerequisites

### 1. Docker Desktop for Windows

**Download and install:**
- Download from: https://www.docker.com/products/docker-desktop/
- Minimum version: 4.0+
- Make sure to enable **WSL 2** during installation

**Verify installation:**
```powershell
docker --version
docker-compose --version
```

### 2. (Optional) NVIDIA GPU

**If you have NVIDIA card and want to use GPU:**

1. **Updated NVIDIA drivers**
   - Download from: https://www.nvidia.com/download/index.aspx
   - Minimum version: 525.60+

2. **CUDA Toolkit** (if using WSL2)
   - Already included in Docker, no need to install CUDA on Windows

3. **Enable GPU in Docker Desktop**
   - Open Docker Desktop
   - Settings → Resources → WSL Integration
   - Enable your WSL2 distribution
   - Settings → General → Use WSL 2 based engine ✓

**Verify GPU:**
```powershell
# In PowerShell
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
```

## 🚀 Step-by-Step Installation

### Option 1: PowerShell (Recommended)

```powershell
# 1. Navigate to directory
cd C:\Users\Deep\Documents\workspace\deepseek-ocr

# 2. Copy configuration
Copy-Item .env.example .env

# 3. Start services
docker-compose up -d

# 4. View logs
docker-compose logs -f
```

### Option 2: WSL2 (Linux on Windows)

```bash
# In WSL2 (Ubuntu, etc.)
cd /mnt/c/Users/Deep/Documents/workspace/deepseek-ocr

# Copy configuration
cp .env.example .env

# Start
docker-compose up -d

# View logs
docker-compose logs -f
```

### Option 3: Git Bash

```bash
# Similar to Linux
cd /c/Users/Deep/Documents/workspace/deepseek-ocr
cp .env.example .env
docker-compose up -d
```

## ⚙️ Windows-Specific Configuration

### Adjust Environment Variables

**Edit `.env`** (use Notepad or VS Code):

```env
# For NVIDIA GPU
CUDA_VISIBLE_DEVICES=0

# For CPU (if you don't have GPU or have problems)
CUDA_VISIBLE_DEVICES=-1

# Other configurations
MODEL_NAME=deepseek-ai/DeepSeek-OCR
BASE_SIZE=1024
IMAGE_SIZE=640
```

### Configure Docker Desktop

1. **Increase allocated memory**
   - Docker Desktop → Settings → Resources
   - Memory: Minimum 8GB, recommended 12GB+
   - CPU: Minimum 4 cores, recommended 8+
   - Swap: 2GB
   - Apply & Restart

2. **Configure volumes**
   - Docker Desktop → Settings → Resources → File Sharing
   - Add: `C:\Users\Deep\Documents\workspace\deepseek-ocr`

## 🔧 PowerShell Commands

```powershell
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Check status
docker-compose ps

# Stop services
docker-compose down

# Restart
docker-compose restart

# Rebuild images
docker-compose build --no-cache

# View resource usage
docker stats

# Health check
curl http://localhost:8000/health

# Test with image
curl -X POST "http://localhost:8000/api/ocr" `
  -F "file=@C:\Users\Deep\Pictures\test.jpg" `
  -F "mode=markdown"
```

**Note**: In PowerShell, use backtick `` ` `` to continue lines

## 🐛 Common Windows Problems

### 1. "Docker daemon not running"

**Solution:**
- Open Docker Desktop
- Wait for it to start completely (icon in system tray)

### 2. "Error response from daemon: Conflict"

**Cause**: Ports 8000 or 3000 already in use

**Solution:**
```powershell
# See what's using the port
netstat -ano | findstr :8000
netstat -ano | findstr :3000

# Kill process (replace <PID> with the number you found)
taskkill /PID <PID> /F

# Or change ports in docker-compose.yml:
# ports:
#   - "8001:8000"  # API
#   - "3001:80"    # Web
```

### 3. "Drive has not been shared"

**Solution:**
- Docker Desktop → Settings → Resources → File Sharing
- Add C:\ drive or specific directory
- Apply & Restart

### 4. GPU not detected

**Step-by-step verification:**

```powershell
# 1. Verify NVIDIA drivers
nvidia-smi

# 2. Verify Docker has GPU access
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi

# 3. If it fails, make sure Docker Desktop has GPU enabled:
# Settings → General → Use WSL 2 based engine ✓
# Settings → Resources → WSL Integration → Enable for your distro
```

**If it still fails**, use CPU:
```env
# In .env
CUDA_VISIBLE_DEVICES=-1
```

### 5. "path not found" or path problems

**Cause**: Windows/Linux path differences

**Solution in docker-compose.yml:**
```yaml
# On Windows, make sure to use relative paths
volumes:
  - ./uploads:/app/uploads      # ✓ Correct
  - ./outputs:/app/outputs      # ✓ Correct
  
# DO NOT use absolute Windows paths:
# - C:\Users\...:              # ✗ Incorrect
```

### 6. Folder permissions

**Solution:**
```powershell
# Give full permissions to folders
icacls uploads /grant Everyone:F
icacls outputs /grant Everyone:F
```

### 7. "EOF" or error building image

**Cause**: Files with CRLF (Windows line endings)

**Solution:**
```powershell
# Convert to LF (use Git Bash or WSL)
dos2unix backend/Dockerfile
dos2unix docker-compose.yml

# Or configure Git:
git config --global core.autocrlf input
```

## 🖥️ Using with WSL2 (Recommended)

**Advantages**:
- Better performance
- More compatible with Linux scripts
- Fewer path problems

**Setup**:

1. **Install WSL2**
   ```powershell
   # In PowerShell as Administrator
   wsl --install
   ```

2. **Install Ubuntu**
   ```powershell
   wsl --install -d Ubuntu-22.04
   ```

3. **Work from WSL**
   ```bash
   # In WSL
   cd /mnt/c/Users/Deep/Documents/workspace/deepseek-ocr
   
   # Copy configuration
   cp .env.example .env
   
   # Start
   docker-compose up -d
   ```

4. **Access from Windows**
   - Browser: http://localhost:3000
   - Everything works the same, Docker Desktop handles integration

## 📁 File Structure on Windows

```
C:\Users\Deep\Documents\workspace\deepseek-ocr\
├── .env.example
├── .gitignore
├── README.md
├── QUICKSTART.md
├── USAGE_GUIDE.md
├── WINDOWS_SETUP.md (this file)
├── docker-compose.yml
├── start.sh
├── test_api.py
├── backend\
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── config.py
│   └── main.py
├── frontend\
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── uploads\
└── outputs\
```

## 🧪 Testing on Windows

### With PowerShell

```powershell
# Basic test
Invoke-WebRequest -Uri "http://localhost:8000/health" | Select-Object -Expand Content

# Test OCR with cURL (if installed)
curl -X POST "http://localhost:8000/api/ocr" `
  -F "file=@C:\Users\Deep\Pictures\test.jpg" `
  -F "mode=markdown"

# With Python
python test_api.py C:\Users\Deep\Pictures\test.jpg
```

### With Python Script

```python
# test_windows.py
import requests
from pathlib import Path

# Test health
print("Testing health...")
response = requests.get('http://localhost:8000/health')
print(response.json())

# Test OCR
print("\nTesting OCR...")
image_path = r"C:\Users\Deep\Pictures\test.jpg"
if Path(image_path).exists():
    files = {'file': open(image_path, 'rb')}
    data = {'mode': 'markdown'}
    
    response = requests.post(
        'http://localhost:8000/api/ocr',
        files=files,
        data=data
    )
    
    if response.ok:
        result = response.json()
        print(f"Success! Processing time: {result['processing_time']}s")
        print(f"Text: {result['text'][:200]}...")
    else:
        print(f"Error: {response.status_code}")
else:
    print(f"Image not found: {image_path}")
```

Run:
```powershell
python test_windows.py
```

## 🎯 Shortcuts

### Create startup script (start.bat)

```bat
@echo off
echo Starting DeepSeek OCR...
cd /d "%~dp0"
docker-compose up -d
echo.
echo Services started!
echo Web UI: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
pause
```

### Create stop script (stop.bat)

```bat
@echo off
echo Stopping DeepSeek OCR...
cd /d "%~dp0"
docker-compose down
echo Services stopped!
pause
```

### Create logs script (logs.bat)

```bat
@echo off
cd /d "%~dp0"
docker-compose logs -f
```

## 🌐 Access from Other Devices

If you want to access from another PC on your local network:

1. **Get your local IP**
   ```powershell
   ipconfig
   # Look for "IPv4 Address" (e.g., 192.168.1.100)
   ```

2. **Configure firewall**
   ```powershell
   # In PowerShell as Administrator
   New-NetFirewallRule -DisplayName "DeepSeek OCR Web" -Direction Inbound -LocalPort 3000 -Protocol TCP -Action Allow
   New-NetFirewallRule -DisplayName "DeepSeek OCR API" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
   ```

3. **Access from another device**
   - Web: http://192.168.1.100:3000
   - API: http://192.168.1.100:8000

## 💡 Windows Tips

1. **Use VS Code**
   - Open project in VS Code
   - Install "Docker" extension
   - Easy container and log management

2. **Windows Terminal**
   - Better than classic PowerShell/CMD
   - Download from Microsoft Store
   - Tab support and WSL

3. **Docker Desktop Dashboard**
   - View running containers
   - Logs with GUI
   - Easy start/stop

4. **Antivirus**
   - Add exceptions for Docker Desktop
   - Exclude project folder if there's slowness

## 🔄 Updates

```powershell
# Stop services
docker-compose down

# Update code (if using Git)
git pull

# Rebuild images
docker-compose build --no-cache

# Start again
docker-compose up -d
```

## 🆘 Windows-Specific Support

### Useful Resources
- [Docker Desktop for Windows Docs](https://docs.docker.com/desktop/windows/)
- [WSL2 Documentation](https://docs.microsoft.com/en-us/windows/wsl/)
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)

### Communities
- Docker Community Forums
- Stack Overflow (tag: docker-desktop)
- Reddit: r/docker

---

**Ready to use on Windows!** 🎉

If you have problems, check first:
1. Docker Desktop is running
2. Ports are not occupied
3. You have enough RAM assigned to Docker
4. Firewall/Antivirus is not blocking
