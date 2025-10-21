from fastapi import FastAPI, File, UploadFile, HTTPException, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from transformers import AutoModel, AutoTokenizer
import torch
import os
from pathlib import Path
import time
from datetime import datetime
from typing import Optional, Literal
import shutil
from PIL import Image
import logging
import asyncio
import json
from huggingface_hub import snapshot_download

from config import settings, PROMPTS

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear app FastAPI
app = FastAPI(
    title="DeepSeek OCR API",
    description="API para reconocimiento óptico de caracteres usando DeepSeek-OCR",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Variables globales para el modelo
model = None
tokenizer = None
model_loaded = False
model_loading = False
model_error = None
download_progress = {"status": "idle", "progress": 0, "message": ""}


def load_model():
    """Carga el modelo DeepSeek-OCR"""
    global model, tokenizer, model_loaded, model_loading, model_error, download_progress
    
    if model_loaded:
        return
    
    if model_loading:
        return
    
    model_loading = True
    model_error = None
    download_progress["status"] = "downloading"
    download_progress["progress"] = 0
    download_progress["message"] = "Iniciando descarga del modelo..."
    
    try:
        logger.info(f"Cargando modelo {settings.MODEL_NAME}...")
        
        download_progress["progress"] = 10
        download_progress["message"] = "Descargando tokenizer..."
        
        tokenizer = AutoTokenizer.from_pretrained(
            settings.MODEL_NAME,
            trust_remote_code=True
        )
        
        download_progress["progress"] = 30
        download_progress["message"] = "Tokenizer descargado. Descargando modelo..."
        
        # Intentar primero con flash_attention_2, sino usar eager
        try:
            logger.info("Intentando cargar con flash_attention_2...")
            download_progress["message"] = "Cargando modelo con flash_attention_2..."
            model = AutoModel.from_pretrained(
                settings.MODEL_NAME,
                _attn_implementation='flash_attention_2',
                trust_remote_code=True,
                use_safetensors=True
            )
            logger.info("✓ Modelo cargado con flash_attention_2")
        except Exception as e:
            logger.warning(f"Flash attention no disponible: {e}")
            logger.info("Cargando modelo con eager attention...")
            download_progress["message"] = "Cargando modelo con eager attention..."
            model = AutoModel.from_pretrained(
                settings.MODEL_NAME,
                _attn_implementation='eager',
                trust_remote_code=True,
                use_safetensors=True
            )
            logger.info("✓ Modelo cargado con eager attention")
        
        download_progress["progress"] = 80
        download_progress["message"] = "Modelo descargado. Configurando..."
        
        # Mover a GPU si está disponible
        if settings.DEVICE == "cuda" and torch.cuda.is_available():
            logger.info("Moviendo modelo a GPU...")
            download_progress["message"] = "Moviendo modelo a GPU..."
            model = model.eval().cuda().to(torch.bfloat16)
            logger.info(f"✓ Modelo cargado en GPU: {torch.cuda.get_device_name(0)}")
        else:
            model = model.eval()
            logger.info("✓ Modelo cargado en CPU")
        
        download_progress["progress"] = 100
        download_progress["status"] = "completed"
        download_progress["message"] = "✓ Modelo completamente cargado y listo"
        
        model_loaded = True
        model_loading = False
        logger.info("✓ Modelo completamente cargado y listo")
        
    except Exception as e:
        model_loading = False
        model_error = str(e)
        download_progress["status"] = "error"
        download_progress["progress"] = 0
        download_progress["message"] = f"Error: {str(e)}"
        logger.error(f"Error al cargar modelo: {str(e)}")
        raise


@app.on_event("startup")
async def startup_event():
    """Inicialización al arrancar la aplicación"""
    logger.info("Iniciando DeepSeek OCR API...")
    
    # Crear directorios
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
    
    # NO cargar modelo en startup - se cargará en la primera petición
    logger.info("✓ API lista. El modelo se cargará en la primera petición.")


@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": "DeepSeek OCR API",
        "version": "1.0.0",
        "model": settings.MODEL_NAME,
        "model_loaded": model_loaded,
        "device": settings.DEVICE,
        "endpoints": {
            "health": "/health",
            "ocr": "/api/ocr",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model_loaded,
        "model_loading": model_loading,
        "model_error": model_error,
        "download_progress": download_progress,
        "device": settings.DEVICE,
        "cuda_available": torch.cuda.is_available(),
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/download-model")
async def download_model(background_tasks: BackgroundTasks):
    """Inicia la descarga del modelo en background"""
    global model_loading, download_progress
    
    if model_loaded:
        return {"status": "already_loaded", "message": "Modelo ya cargado"}
    
    if model_loading:
        return {"status": "downloading", "message": "Descarga en progreso", "progress": download_progress}
    
    # Iniciar carga en background
    background_tasks.add_task(load_model)
    
    return {"status": "started", "message": "Descarga iniciada"}


@app.get("/api/download-progress")
async def get_download_progress():
    """Obtiene el progreso de descarga del modelo"""
    return {
        "model_loaded": model_loaded,
        "model_loading": model_loading,
        "progress": download_progress
    }


@app.post("/api/ocr")
async def process_ocr(
    file: UploadFile = File(...),
    mode: Literal["free_ocr", "markdown", "grounding", "parse_figure", "detailed"] = Form("markdown"),
    custom_prompt: Optional[str] = Form(None)
):
    """
    Procesa una imagen y extrae texto usando OCR
    
    Args:
        file: Imagen a procesar (JPG, PNG, PDF, WEBP)
        mode: Modo de procesamiento predefinido
        custom_prompt: Prompt personalizado (opcional, sobrescribe mode)
    
    Returns:
        JSON con el texto extraído y metadata
    """
    
    # Verificar que el modelo esté cargado
    if not model_loaded:
        try:
            load_model()
        except Exception as e:
            raise HTTPException(
                status_code=503,
                detail=f"Modelo no disponible: {str(e)}"
            )
    
    # Validar archivo
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de archivo no permitido. Usar: {settings.ALLOWED_EXTENSIONS}"
        )
    
    # Generar nombres únicos
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = f"{timestamp}_{file.filename}"
    upload_path = os.path.join(settings.UPLOAD_DIR, unique_id)
    
    try:
        # Guardar archivo subido
        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Validar tamaño
        file_size = os.path.getsize(upload_path)
        if file_size > settings.MAX_FILE_SIZE:
            os.remove(upload_path)
            raise HTTPException(
                status_code=400,
                detail=f"Archivo muy grande. Máximo: {settings.MAX_FILE_SIZE / 1024 / 1024}MB"
            )
        
        # Validar que sea imagen válida
        try:
            img = Image.open(upload_path)
            img_size = img.size
            img.close()
        except Exception as e:
            os.remove(upload_path)
            raise HTTPException(
                status_code=400,
                detail=f"Archivo no es una imagen válida: {str(e)}"
            )
        
        # Determinar prompt
        prompt = custom_prompt if custom_prompt else PROMPTS.get(mode, PROMPTS["markdown"])
        
        # Crear directorio de salida único
        output_dir = os.path.join(settings.OUTPUT_DIR, timestamp)
        os.makedirs(output_dir, exist_ok=True)
        
        # Procesar imagen con el modelo
        logger.info(f"Procesando {unique_id} con modo '{mode}'")
        start_time = time.time()
        
        # Verificar que el modelo esté cargado correctamente
        if model is None or tokenizer is None:
            raise HTTPException(
                status_code=503,
                detail="Modelo no inicializado correctamente"
            )
        
        result = model.infer(
            tokenizer,
            prompt=prompt,
            image_file=upload_path,
            output_path=output_dir,
            base_size=settings.BASE_SIZE,
            image_size=settings.IMAGE_SIZE,
            crop_mode=settings.CROP_MODE,
            save_results=True,
            test_compress=True
        )
        
        processing_time = time.time() - start_time
        logger.info(f"✓ Procesado en {processing_time:.2f}s")
        
        # Leer resultado
        result_file = os.path.join(output_dir, "result.mmd")
        text_content = ""
        
        if os.path.exists(result_file):
            with open(result_file, 'r', encoding='utf-8') as f:
                text_content = f.read()
        
        # Respuesta
        response = {
            "success": True,
            "text": text_content or result,
            "mode": mode,
            "prompt": prompt,
            "processing_time": round(processing_time, 2),
            "image_size": img_size,
            "file_size": file_size,
            "timestamp": timestamp,
            "output_dir": output_dir,
            "metadata": {
                "filename": file.filename,
                "unique_id": unique_id,
                "device": settings.DEVICE
            }
        }
        
        return JSONResponse(content=response)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error procesando imagen: {str(e)}")
        # Limpiar archivos en caso de error
        if os.path.exists(upload_path):
            os.remove(upload_path)
        raise HTTPException(
            status_code=500,
            detail=f"Error procesando imagen: {str(e)}"
        )


@app.get("/api/modes")
async def get_modes():
    """Retorna los modos de OCR disponibles"""
    return {
        "modes": {
            "free_ocr": {
                "description": "OCR rápido sin estructura",
                "speed": "⚡⚡⚡ Rápido",
                "use_case": "Extracción de texto general"
            },
            "markdown": {
                "description": "Convierte documento a Markdown con estructura",
                "speed": "⚡⚡ Medio",
                "use_case": "Documentos con formato"
            },
            "grounding": {
                "description": "OCR con coordenadas de bounding boxes",
                "speed": "⚡ Lento",
                "use_case": "Análisis detallado con ubicaciones"
            },
            "parse_figure": {
                "description": "Extrae información de figuras y diagramas",
                "speed": "⚡⚡ Medio",
                "use_case": "Gráficos, tablas, diagramas"
            },
            "detailed": {
                "description": "Descripción detallada de la imagen",
                "speed": "⚡⚡⚡ Muy rápido",
                "use_case": "Análisis de contenido visual"
            }
        }
    }


@app.delete("/api/cleanup")
async def cleanup_old_files(days: int = 7):
    """Limpia archivos antiguos"""
    try:
        import time
        current_time = time.time()
        days_in_seconds = days * 24 * 60 * 60
        
        cleaned = {"uploads": 0, "outputs": 0}
        
        # Limpiar uploads
        for file in Path(settings.UPLOAD_DIR).iterdir():
            if current_time - file.stat().st_mtime > days_in_seconds:
                file.unlink()
                cleaned["uploads"] += 1
        
        # Limpiar outputs
        for folder in Path(settings.OUTPUT_DIR).iterdir():
            if folder.is_dir() and current_time - folder.stat().st_mtime > days_in_seconds:
                shutil.rmtree(folder)
                cleaned["outputs"] += 1
        
        return {
            "success": True,
            "cleaned": cleaned,
            "days": days
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
