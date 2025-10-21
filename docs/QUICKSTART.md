# ⚡ DeepSeek OCR - Quick Start

## 🎯 ¿Qué es esto?

**DeepSeek OCR** es una solución completa de reconocimiento óptico de caracteres (OCR) usando IA de última generación. Este proyecto incluye:

- ✅ **Modelo DeepSeek-OCR** - IA open source de 6.6GB optimizada para OCR
- ✅ **API REST** - Backend con FastAPI para integración fácil
- ✅ **Interfaz Web** - Frontend moderno para usar sin código
- ✅ **Docker Compose** - Deploy completo en minutos

## 📋 Requisitos Mínimos

- **Docker** 20.10+
- **Docker Compose** 2.0+
- **8GB RAM**
- **10GB espacio disco**
- **(Opcional) GPU NVIDIA** con CUDA 11.8+ para mejor rendimiento

## 🚀 Instalación en 3 Pasos

### 1️⃣ Preparar el entorno

```bash
# Copiar configuración
cp .env.example .env

# (Opcional) Editar configuración
# nano .env
```

### 2️⃣ Iniciar servicios

```bash
# Construir e iniciar
docker-compose up -d

# Ver logs
docker-compose logs -f
```

### 3️⃣ Usar!

- **Web**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/health

## 📖 Uso Básico

### Interfaz Web

1. Abre http://localhost:3000
2. Arrastra una imagen
3. Selecciona el modo (recomendado: "Markdown")
4. Click en "Procesar OCR"
5. Copia o descarga el resultado

### API (cURL)

```bash
curl -X POST "http://localhost:8000/api/ocr" \
  -F "file=@documento.jpg" \
  -F "mode=markdown"
```

### API (Python)

```python
import requests

files = {'file': open('imagen.jpg', 'rb')}
data = {'mode': 'markdown'}

response = requests.post(
    'http://localhost:8000/api/ocr',
    files=files,
    data=data
)

print(response.json()['text'])
```

## 🎨 Modos Disponibles

| Modo | Velocidad | Mejor Para |
|------|-----------|------------|
| `free_ocr` | ⚡⚡⚡ | Texto simple rápido |
| `markdown` | ⚡⚡ | Documentos estructurados |
| `grounding` | ⚡ | Texto + coordenadas |
| `parse_figure` | ⚡⚡ | Gráficos y tablas |
| `detailed` | ⚡⚡⚡ | Descripción de imagen |

## 📊 Ejemplos de Uso

### Digitalizar Factura

```bash
curl -X POST "http://localhost:8000/api/ocr" \
  -F "file=@factura.jpg" \
  -F "mode=markdown" \
  -F "custom_prompt=<image>\nExtrae: número, fecha, total"
```

### Procesar Múltiples Imágenes

```python
from pathlib import Path
import requests

for img in Path('documentos/').glob('*.jpg'):
    files = {'file': open(img, 'rb')}
    data = {'mode': 'markdown'}
    
    result = requests.post(
        'http://localhost:8000/api/ocr',
        files=files,
        data=data
    ).json()
    
    # Guardar resultado
    with open(f'output/{img.stem}.txt', 'w') as f:
        f.write(result['text'])
```

## 🔧 Comandos Útiles

```bash
# Ver logs en tiempo real
docker-compose logs -f

# Reiniciar servicios
docker-compose restart

# Detener todo
docker-compose down

# Ver estado
docker-compose ps

# Verificar salud
curl http://localhost:8000/health
```

## 🐛 Solución Rápida de Problemas

### API no carga el modelo

```bash
# Ver logs
docker-compose logs deepseek-ocr-api

# Reiniciar
docker-compose restart deepseek-ocr-api
```

### GPU no detectada

```bash
# Verificar NVIDIA Docker
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
```

### Procesamiento muy lento

**Solución**: Asegúrate de usar GPU. Si no tienes GPU, reduce la resolución:

```yaml
# En docker-compose.yml
environment:
  - BASE_SIZE=640  # default: 1024
```

### Out of Memory

**Solución**: Reduce resolución o usa imágenes más pequeñas:

```python
# Redimensionar imagen antes de enviar
from PIL import Image
img = Image.open('grande.jpg')
img.thumbnail((1024, 1024))
img.save('pequena.jpg')
```

## 📈 Rendimiento Esperado

Con **GPU NVIDIA A100**:
- Free OCR: ~24s por imagen
- Markdown: ~39s por imagen
- Grounding: ~58s por imagen
- Detailed: ~9s por imagen

Con **CPU**: 3-5x más lento

## 🔒 Seguridad

⚠️ **Para desarrollo local solamente**

Si expones públicamente:
- Añade autenticación
- Configura rate limiting
- Usa HTTPS
- Valida archivos estrictamente

## 📚 Documentación Completa

- **README.md** - Visión general y features
- **USAGE_GUIDE.md** - Guía detallada de uso
- **COMANDOS_UTILES.md** - Referencia de comandos
- **test_api.py** - Script de pruebas

## 🔗 Links Importantes

- [Repo Original DeepSeek-OCR](https://github.com/deepseek-ai/DeepSeek-OCR)
- [Modelo en HuggingFace](https://huggingface.co/deepseek-ai/DeepSeek-OCR)
- [FastAPI Docs](http://localhost:8000/docs) (cuando esté corriendo)

## 💡 Tips

1. **Primera vez**: El modelo se descarga (~6.6GB), puede tardar 10-20 min
2. **GPU vs CPU**: GPU es 3-5x más rápida
3. **Mejor calidad**: Usa imágenes de 1024×1024 píxeles
4. **Mejor velocidad**: Usa modo `free_ocr`
5. **Batch processing**: Procesa múltiples imágenes en paralelo con Python

## 🆘 Ayuda

1. Revisa logs: `docker-compose logs -f`
2. Verifica salud: `curl http://localhost:8000/health`
3. Lee USAGE_GUIDE.md
4. Ejecuta test: `python test_api.py imagen.jpg`

## 🎉 ¡Listo!

Ahora tienes un sistema completo de OCR con IA. 

**Próximos pasos**:
- Prueba con tus propias imágenes
- Experimenta con diferentes modos
- Integra el API en tus aplicaciones
- Lee USAGE_GUIDE.md para casos avanzados

---

**Happy OCR! 🚀**
