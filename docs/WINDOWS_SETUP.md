# 🪟 Configuración en Windows - DeepSeek OCR

## 📋 Requisitos Previos

### 1. Docker Desktop para Windows

**Descargar e instalar:**
- Descarga desde: https://www.docker.com/products/docker-desktop/
- Versión mínima: 4.0+
- Asegúrate de habilitar **WSL 2** durante la instalación

**Verificar instalación:**
```powershell
docker --version
docker-compose --version
```

### 2. (Opcional) GPU NVIDIA

**Si tienes tarjeta NVIDIA y quieres usar GPU:**

1. **Drivers NVIDIA actualizados**
   - Descarga desde: https://www.nvidia.com/download/index.aspx
   - Versión mínima: 525.60+

2. **CUDA Toolkit** (si usas WSL2)
   - Ya incluido en Docker, no necesitas instalar CUDA en Windows

3. **Habilitar GPU en Docker Desktop**
   - Abre Docker Desktop
   - Settings → Resources → WSL Integration
   - Habilita tu distribución WSL2
   - Settings → General → Use WSL 2 based engine ✓

**Verificar GPU:**
```powershell
# En PowerShell
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
```

## 🚀 Instalación Paso a Paso

### Opción 1: PowerShell (Recomendado)

```powershell
# 1. Navegar al directorio
cd C:\Users\Deep\Documents\workspace\deepseek-ocr

# 2. Copiar configuración
Copy-Item .env.example .env

# 3. Iniciar servicios
docker-compose up -d

# 4. Ver logs
docker-compose logs -f
```

### Opción 2: WSL2 (Linux en Windows)

```bash
# En WSL2 (Ubuntu, etc.)
cd /mnt/c/Users/Deep/Documents/workspace/deepseek-ocr

# Copiar configuración
cp .env.example .env

# Iniciar
docker-compose up -d

# Ver logs
docker-compose logs -f
```

### Opción 3: Git Bash

```bash
# Similar a Linux
cd /c/Users/Deep/Documents/workspace/deepseek-ocr
cp .env.example .env
docker-compose up -d
```

## ⚙️ Configuración Específica de Windows

### Ajustar Variables de Entorno

**Editar `.env`** (usa Notepad o VS Code):

```env
# Para GPU NVIDIA
CUDA_VISIBLE_DEVICES=0

# Para CPU (si no tienes GPU o hay problemas)
CUDA_VISIBLE_DEVICES=-1

# Otras configuraciones
MODEL_NAME=deepseek-ai/DeepSeek-OCR
BASE_SIZE=1024
IMAGE_SIZE=640
```

### Configurar Docker Desktop

1. **Aumentar memoria asignada**
   - Docker Desktop → Settings → Resources
   - Memory: Mínimo 8GB, recomendado 12GB+
   - CPU: Mínimo 4 cores, recomendado 8+
   - Swap: 2GB
   - Apply & Restart

2. **Configurar volúmenes**
   - Docker Desktop → Settings → Resources → File Sharing
   - Añadir: `C:\Users\Deep\Documents\workspace\deepseek-ocr`

## 🔧 Comandos en PowerShell

```powershell
# Iniciar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f

# Ver estado
docker-compose ps

# Detener servicios
docker-compose down

# Reiniciar
docker-compose restart

# Reconstruir imágenes
docker-compose build --no-cache

# Ver uso de recursos
docker stats

# Health check
curl http://localhost:8000/health

# Test con imagen
curl -X POST "http://localhost:8000/api/ocr" `
  -F "file=@C:\Users\Deep\Pictures\test.jpg" `
  -F "mode=markdown"
```

**Nota**: En PowerShell, usar backtick `` ` `` para continuar líneas

## 🐛 Problemas Comunes en Windows

### 1. "Docker daemon not running"

**Solución:**
- Abre Docker Desktop
- Espera a que inicie completamente (icono en la bandeja del sistema)

### 2. "Error response from daemon: Conflict"

**Causa**: Puertos 8000 o 3000 ya en uso

**Solución:**
```powershell
# Ver qué está usando el puerto
netstat -ano | findstr :8000
netstat -ano | findstr :3000

# Matar proceso (reemplaza <PID> con el número que encontraste)
taskkill /PID <PID> /F

# O cambiar puertos en docker-compose.yml:
# ports:
#   - "8001:8000"  # API
#   - "3001:80"    # Web
```

### 3. "Drive has not been shared"

**Solución:**
- Docker Desktop → Settings → Resources → File Sharing
- Añadir la unidad C:\ o el directorio específico
- Apply & Restart

### 4. GPU no detectada

**Verificar paso a paso:**

```powershell
# 1. Verificar drivers NVIDIA
nvidia-smi

# 2. Verificar Docker tiene acceso a GPU
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi

# 3. Si falla, asegurarse que Docker Desktop tiene GPU habilitada:
# Settings → General → Use the WSL 2 based engine ✓
# Settings → Resources → WSL Integration → Enable for your distro
```

**Si sigue fallando**, usa CPU:
```env
# En .env
CUDA_VISIBLE_DEVICES=-1
```

### 5. "path not found" o problemas con rutas

**Causa**: Diferencias Windows/Linux paths

**Solución en docker-compose.yml:**
```yaml
# En Windows, asegúrate de usar rutas relativas
volumes:
  - ./uploads:/app/uploads      # ✓ Correcto
  - ./outputs:/app/outputs      # ✓ Correcto
  
# NO usar rutas absolutas de Windows:
# - C:\Users\...:              # ✗ Incorrecto
```

### 6. Permisos en carpetas

**Solución:**
```powershell
# Dar permisos completos a las carpetas
icacls uploads /grant Everyone:F
icacls outputs /grant Everyone:F
```

### 7. "EOF" o error al construir imagen

**Causa**: Archivos con CRLF (Windows line endings)

**Solución:**
```powershell
# Convertir a LF (usar Git Bash o WSL)
dos2unix backend/Dockerfile
dos2unix docker-compose.yml

# O configurar Git:
git config --global core.autocrlf input
```

## 🖥️ Usar con WSL2 (Recomendado)

**Ventajas**:
- Mejor rendimiento
- Más compatible con scripts Linux
- Menos problemas de paths

**Setup**:

1. **Instalar WSL2**
   ```powershell
   # En PowerShell como Administrador
   wsl --install
   ```

2. **Instalar Ubuntu**
   ```powershell
   wsl --install -d Ubuntu-22.04
   ```

3. **Trabajar desde WSL**
   ```bash
   # En WSL
   cd /mnt/c/Users/Deep/Documents/workspace/deepseek-ocr
   
   # Copiar configuración
   cp .env.example .env
   
   # Iniciar
   docker-compose up -d
   ```

4. **Acceder desde Windows**
   - Navegador: http://localhost:3000
   - Todo funciona igual, Docker Desktop maneja la integración

## 📁 Estructura de Archivos en Windows

```
C:\Users\Deep\Documents\workspace\deepseek-ocr\
├── .env.example
├── .gitignore
├── README.md
├── QUICKSTART.md
├── USAGE_GUIDE.md
├── COMANDOS_UTILES.md
├── NOTAS_IMPORTANTE.md
├── WINDOWS_SETUP.md (este archivo)
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

## 🧪 Testing en Windows

### Con PowerShell

```powershell
# Test básico
Invoke-WebRequest -Uri "http://localhost:8000/health" | Select-Object -Expand Content

# Test OCR con cURL (si está instalado)
curl -X POST "http://localhost:8000/api/ocr" `
  -F "file=@C:\Users\Deep\Pictures\test.jpg" `
  -F "mode=markdown"

# Con Python
python test_api.py C:\Users\Deep\Pictures\test.jpg
```

### Con Python Script

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

Ejecutar:
```powershell
python test_windows.py
```

## 🎯 Accesos Directos

### Crear script de inicio (start.bat)

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

### Crear script de detención (stop.bat)

```bat
@echo off
echo Stopping DeepSeek OCR...
cd /d "%~dp0"
docker-compose down
echo Services stopped!
pause
```

### Crear script de logs (logs.bat)

```bat
@echo off
cd /d "%~dp0"
docker-compose logs -f
```

## 🌐 Acceder desde Otros Dispositivos

Si quieres acceder desde otro PC en tu red local:

1. **Obtener tu IP local**
   ```powershell
   ipconfig
   # Buscar "IPv4 Address" (ej: 192.168.1.100)
   ```

2. **Configurar firewall**
   ```powershell
   # En PowerShell como Administrador
   New-NetFirewallRule -DisplayName "DeepSeek OCR Web" -Direction Inbound -LocalPort 3000 -Protocol TCP -Action Allow
   New-NetFirewallRule -DisplayName "DeepSeek OCR API" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
   ```

3. **Acceder desde otro dispositivo**
   - Web: http://192.168.1.100:3000
   - API: http://192.168.1.100:8000

## 💡 Tips para Windows

1. **Usar VS Code**
   - Abre el proyecto en VS Code
   - Instala extensión "Docker"
   - Fácil manejo de containers y logs

2. **Windows Terminal**
   - Mejor que PowerShell/CMD clásico
   - Descarga desde Microsoft Store
   - Soporte para pestañas y WSL

3. **Docker Desktop Dashboard**
   - Ver containers en ejecución
   - Logs con GUI
   - Fácil start/stop

4. **Antivirus**
   - Añade excepciones para Docker Desktop
   - Excluye carpeta del proyecto si hay lentitud

## 🔄 Actualización

```powershell
# Detener servicios
docker-compose down

# Actualizar código (si usas Git)
git pull

# Reconstruir imágenes
docker-compose build --no-cache

# Iniciar de nuevo
docker-compose up -d
```

## 🆘 Soporte Específico de Windows

### Recursos Útiles
- [Docker Desktop for Windows Docs](https://docs.docker.com/desktop/windows/)
- [WSL2 Documentation](https://docs.microsoft.com/en-us/windows/wsl/)
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)

### Comunidades
- Docker Community Forums
- Stack Overflow (tag: docker-desktop)
- Reddit: r/docker

---

**¡Listo para usar en Windows!** 🎉

Si tienes problemas, revisa primero:
1. Docker Desktop está corriendo
2. Puertos no están ocupados
3. Tienes suficiente RAM asignada a Docker
4. Firewall/Antivirus no está bloqueando
