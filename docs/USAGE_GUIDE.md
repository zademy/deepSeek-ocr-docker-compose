# 📖 Guía de Uso - DeepSeek OCR

## 🎯 Índice

1. [Inicio Rápido](#inicio-rápido)
2. [Uso de la Interfaz Web](#uso-de-la-interfaz-web)
3. [Uso del API](#uso-del-api)
4. [Modos de OCR](#modos-de-ocr)
5. [Ejemplos Prácticos](#ejemplos-prácticos)
6. [Tips y Mejores Prácticas](#tips-y-mejores-prácticas)
7. [Troubleshooting](#troubleshooting)

---

## 🚀 Inicio Rápido

### Requisitos Previos

- **Docker** y **Docker Compose** instalados
- **GPU NVIDIA** con CUDA 11.8+ (recomendado, no obligatorio)
- Al menos **8GB RAM** y **10GB espacio en disco**

### Instalación en 3 Pasos

```bash
# 1. Clonar o navegar al directorio
cd deepseek-ocr

# 2. Copiar configuración
cp .env.example .env

# 3. Iniciar servicios
docker-compose up -d
```

**En Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

### Verificar que Funciona

```bash
# Ver logs
docker-compose logs -f

# Verificar salud del API
curl http://localhost:8000/health
```

Accede a: **http://localhost:3000**

---

## 🖥️ Uso de la Interfaz Web

### 1. Subir Imagen

- **Arrastra y suelta** una imagen en el área de carga
- O **haz clic** para seleccionar desde tu computadora
- Formatos soportados: JPG, PNG, WEBP, PDF
- Tamaño máximo: 10MB

### 2. Seleccionar Modo

| Modo | Cuándo Usar | Velocidad |
|------|-------------|-----------|
| **Markdown** | Documentos con estructura | Media ⚡⚡ |
| **Free OCR** | Texto simple y rápido | Rápida ⚡⚡⚡ |
| **Grounding** | Necesitas coordenadas del texto | Lenta ⚡ |
| **Parse Figure** | Gráficos, tablas, diagramas | Media ⚡⚡ |
| **Detailed** | Descripción de la imagen | Muy Rápida ⚡⚡⚡ |

### 3. Procesar

- Click en **"Procesar OCR"**
- Espera 10-60 segundos (dependiendo del modo y GPU)
- Revisa los resultados

### 4. Usar Resultados

- **Copiar** al portapapeles
- **Descargar** como archivo TXT
- **Nuevo OCR** para procesar otra imagen

---

## 🔌 Uso del API

### Documentación Interactiva

Accede a la documentación Swagger:
```
http://localhost:8000/docs
```

### Ejemplo Básico con cURL

```bash
curl -X POST "http://localhost:8000/api/ocr" \
  -F "file=@mi_documento.jpg" \
  -F "mode=markdown"
```

### Ejemplo con Python

```python
import requests

url = "http://localhost:8000/api/ocr"

# Cargar imagen
files = {"file": open("documento.jpg", "rb")}
data = {"mode": "markdown"}

# Enviar request
response = requests.post(url, files=files, data=data)
result = response.json()

# Usar resultado
print(result["text"])
print(f"Procesado en {result['processing_time']}s")
```

### Ejemplo con JavaScript/Node.js

```javascript
const FormData = require('form-data');
const fs = require('fs');
const axios = require('axios');

const form = new FormData();
form.append('file', fs.createReadStream('documento.jpg'));
form.append('mode', 'markdown');

axios.post('http://localhost:8000/api/ocr', form, {
  headers: form.getHeaders()
})
.then(response => {
  console.log('Texto:', response.data.text);
  console.log('Tiempo:', response.data.processing_time);
})
.catch(error => console.error('Error:', error));
```

### Prompt Personalizado

```bash
curl -X POST "http://localhost:8000/api/ocr" \
  -F "file=@factura.jpg" \
  -F "mode=markdown" \
  -F "custom_prompt=<image>\nExtrae: número de factura, fecha, total y cliente"
```

---

## 🎨 Modos de OCR

### 1. **Free OCR** (Rápido y Simple)

**Cuándo usar:**
- Necesitas solo el texto, sin formato
- Prioridad en velocidad
- Texto simple sin estructura compleja

**Ejemplo:**
```bash
curl -X POST "http://localhost:8000/api/ocr" \
  -F "file=@nota.jpg" \
  -F "mode=free_ocr"
```

**Salida típica:**
```
Esto es un texto simple
extraído de la imagen
sin formato especial
```

---

### 2. **Markdown** (Documentos Estructurados)

**Cuándo usar:**
- Documentos con títulos, párrafos, listas
- Necesitas mantener la estructura
- Quieres formato Markdown

**Ejemplo:**
```bash
curl -X POST "http://localhost:8000/api/ocr" \
  -F "file=@articulo.jpg" \
  -F "mode=markdown"
```

**Salida típica:**
```markdown
# Título Principal

## Subtítulo

- Elemento de lista 1
- Elemento de lista 2

Párrafo de texto con **negritas** y *cursivas*.
```

---

### 3. **Grounding** (Con Coordenadas)

**Cuándo usar:**
- Necesitas saber DÓNDE está cada texto
- Análisis de layout
- Detección de regiones

**Ejemplo:**
```bash
curl -X POST "http://localhost:8000/api/ocr" \
  -F "file=@formulario.jpg" \
  -F "mode=grounding"
```

**Salida típica:**
```
<|ref|>Nombre:<|/ref|><|det|>[[120, 50, 200, 80]]<|/det|>
<|ref|>Juan Pérez<|/ref|><|det|>[[220, 50, 350, 80]]<|/det|>
```

---

### 4. **Parse Figure** (Gráficos y Tablas)

**Cuándo usar:**
- Imágenes con gráficos de barras, líneas, pie
- Tablas complejas
- Diagramas técnicos

**Ejemplo:**
```bash
curl -X POST "http://localhost:8000/api/ocr" \
  -F "file=@grafico.jpg" \
  -F "mode=parse_figure"
```

---

### 5. **Detailed** (Descripción Visual)

**Cuándo usar:**
- Quieres una descripción de la imagen
- No solo texto, sino contexto visual
- Análisis de contenido

**Ejemplo:**
```bash
curl -X POST "http://localhost:8000/api/ocr" \
  -F "file=@foto.jpg" \
  -F "mode=detailed"
```

**Salida típica:**
```
The image shows a business presentation slide with a 
blue header containing the title "Q4 Results". Below 
are three bullet points describing financial metrics...
```

---

## 💡 Ejemplos Prácticos

### Caso 1: Digitalizar Facturas

```python
import requests

def procesar_factura(archivo_factura):
    url = "http://localhost:8000/api/ocr"
    
    files = {"file": open(archivo_factura, "rb")}
    data = {
        "mode": "markdown",
        "custom_prompt": "<image>\nExtrae: número, fecha, total, cliente"
    }
    
    response = requests.post(url, files=files, data=data)
    return response.json()

# Usar
resultado = procesar_factura("factura_001.jpg")
print(resultado["text"])
```

### Caso 2: Batch Processing (Múltiples Imágenes)

```python
import os
import requests
from pathlib import Path

def procesar_lote(carpeta_imagenes, modo="markdown"):
    resultados = []
    
    for archivo in Path(carpeta_imagenes).glob("*.jpg"):
        print(f"Procesando {archivo.name}...")
        
        files = {"file": open(archivo, "rb")}
        data = {"mode": modo}
        
        response = requests.post(
            "http://localhost:8000/api/ocr",
            files=files,
            data=data
        )
        
        if response.ok:
            result = response.json()
            resultados.append({
                "archivo": archivo.name,
                "texto": result["text"],
                "tiempo": result["processing_time"]
            })
    
    return resultados

# Procesar carpeta completa
resultados = procesar_lote("./documentos")

# Guardar resultados
for r in resultados:
    with open(f"output/{r['archivo']}.txt", "w") as f:
        f.write(r["texto"])
```

### Caso 3: Extraer Tablas de PDFs

```bash
# Convertir PDF a imágenes primero (usando ImageMagick)
convert -density 300 documento.pdf pagina_%d.jpg

# Procesar cada página
for img in pagina_*.jpg; do
  curl -X POST "http://localhost:8000/api/ocr" \
    -F "file=@$img" \
    -F "mode=parse_figure" \
    -o "resultado_$img.json"
done
```

---

## 🎯 Tips y Mejores Prácticas

### Para Mejor Calidad

1. **Resolución óptima**: 1024×1024 píxeles
2. **Formato**: JPG o PNG (evitar compresión excesiva)
3. **Iluminación**: Imágenes bien iluminadas, sin sombras
4. **Orientación**: Asegúrate que el texto esté derecho

### Para Mejor Velocidad

1. **Usa GPU**: Mucho más rápido que CPU
2. **Modo adecuado**: `free_ocr` es el más rápido
3. **Resolución menor**: Reduce si no necesitas máxima calidad
4. **Batch async**: Procesa múltiples imágenes en paralelo

### Configuración de Rendimiento

Edita `docker-compose.yml`:

```yaml
environment:
  - BASE_SIZE=640    # Menor = más rápido (default: 1024)
  - IMAGE_SIZE=512   # Menor = más rápido (default: 640)
```

### Ajustes de Memoria

Si tienes problemas de memoria GPU:

```yaml
# En docker-compose.yml, limitar memoria
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

### Problema: "Model not loaded"

**Solución:**
```bash
# Ver logs del contenedor
docker-compose logs deepseek-ocr-api

# Reiniciar servicios
docker-compose restart
```

### Problema: GPU no detectada

**Verificar NVIDIA Docker:**
```bash
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
```

**Si falla, instalar NVIDIA Container Toolkit:**
```bash
# Ubuntu/Debian
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

### Problema: Out of Memory (OOM)

**Soluciones:**

1. Reduce resolución:
```python
# En backend/config.py
BASE_SIZE = 640  # en lugar de 1024
```

2. Usa CPU si GPU falla:
```yaml
# En docker-compose.yml, comentar la sección GPU:
# deploy:
#   resources:
#     reservations:
#       devices:
#         - driver: nvidia
```

3. Procesa imágenes más pequeñas

### Problema: Procesamiento muy lento

**Diagnóstico:**
```bash
# Verificar uso de GPU
nvidia-smi

# Ver logs en tiempo real
docker-compose logs -f deepseek-ocr-api
```

**Si usa CPU en vez de GPU:**
- Verifica NVIDIA Docker Toolkit
- Revisa `CUDA_VISIBLE_DEVICES` en `.env`

### Problema: Errores de conexión

**Verificar servicios:**
```bash
docker-compose ps
curl http://localhost:8000/health
```

**Reiniciar:**
```bash
docker-compose down
docker-compose up -d
```

### Problema: Resultados vacíos

**Posibles causas:**
- Imagen de baja calidad
- Texto muy pequeño
- Modo incorrecto

**Soluciones:**
- Aumenta resolución de imagen
- Usa modo `grounding` en vez de `free_ocr`
- Prueba con `detailed` para ver qué detecta

---

## 📊 Monitoreo

### Logs en tiempo real

```bash
# Todos los servicios
docker-compose logs -f

# Solo API
docker-compose logs -f deepseek-ocr-api

# Solo web
docker-compose logs -f deepseek-ocr-web
```

### Uso de recursos

```bash
# Docker stats
docker stats

# GPU usage (si NVIDIA)
watch -n 1 nvidia-smi
```

### Limpiar archivos antiguos

```bash
# Via API
curl -X DELETE "http://localhost:8000/api/cleanup?days=7"

# Manual
rm -rf uploads/* outputs/*
```

---

## 🔐 Seguridad

### Producción

Si expones el API públicamente:

1. **Añade autenticación**
2. **Limita rate limiting**
3. **Valida archivos estrictamente**
4. **Usa HTTPS**
5. **Configura firewall**

### Límites recomendados

```python
# En backend/config.py
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
RATE_LIMIT = "10/minute"  # Requiere middleware
```

---

## 📚 Recursos Adicionales

- [Repositorio DeepSeek-OCR](https://github.com/deepseek-ai/DeepSeek-OCR)
- [Modelo en HuggingFace](https://huggingface.co/deepseek-ai/DeepSeek-OCR)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Docker Compose Docs](https://docs.docker.com/compose/)

---

**¿Preguntas o problemas?** Abre un issue en el repositorio.
