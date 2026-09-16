import asyncio
import logging
import os
import shutil
import time
from datetime import datetime
from pathlib import Path
from typing import Literal, Optional

import torch
from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config import settings
from model_lifecycle import (
    DeepSeekModel,
    InferSettings,
    ModelLifecycle,
    ModelLoadError,
)
from ocr_handler import OcrHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


infer_settings = InferSettings(
    base_size=settings.BASE_SIZE,
    image_size=settings.IMAGE_SIZE,
    crop_mode=settings.CROP_MODE,
    save_results=True,
)

model = DeepSeekModel(model_name=settings.MODEL_NAME, device=settings.DEVICE)
lifecycle = ModelLifecycle(model=model, settings=infer_settings)
ocr_handler = OcrHandler(
    model=model,
    upload_dir=settings.UPLOAD_DIR,
    output_dir=settings.OUTPUT_DIR,
    max_file_size=settings.MAX_FILE_SIZE,
    allowed_extensions=settings.ALLOWED_EXTENSIONS,
    device=settings.DEVICE,
)


async def ensure_loaded() -> None:
    try:
        await lifecycle.ensure_loaded()
    except ModelLoadError as e:
        raise HTTPException(status_code=503, detail=f"Model unavailable: {e}")


app = FastAPI(
    title="DeepSeek OCR API",
    description="API para reconocimiento óptico de caracteres usando DeepSeek-OCR",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
    logger.info("API ready. Model loads on first request.")


@app.get("/")
async def root():
    status = lifecycle.status()
    return {
        "message": "DeepSeek OCR API",
        "version": "1.0.0",
        "model": settings.MODEL_NAME,
        "model_loaded": status.loaded,
        "device": settings.DEVICE,
        "endpoints": {
            "health": "/health",
            "ocr": "/api/ocr",
            "docs": "/docs",
        },
    }


@app.get("/health")
async def health_check():
    status = lifecycle.status()
    return {
        "status": "healthy",
        "model_loaded": status.loaded,
        "model_loading": status.loading,
        "model_error": status.error,
        "download_progress": status.progress.model_dump(),
        "device": settings.DEVICE,
        "cuda_available": torch.cuda.is_available(),
        "timestamp": datetime.now().isoformat(),
    }


@app.post("/api/download-model")
async def download_model():
    status = lifecycle.status()
    if status.loaded:
        return {"status": "already_loaded", "message": "Model already loaded"}
    if status.loading:
        return {
            "status": "downloading",
            "message": "Download in progress",
            "progress": status.progress.model_dump(),
        }

    asyncio.create_task(lifecycle.ensure_loaded())
    return {"status": "started", "message": "Download started"}


@app.get("/api/download-progress")
async def get_download_progress():
    status = lifecycle.status()
    return {
        "model_loaded": status.loaded,
        "model_loading": status.loading,
        "progress": status.progress.model_dump(),
    }


@app.post("/api/ocr")
async def process_ocr(
    file: UploadFile = File(...),
    mode: Literal[
        "free_ocr", "markdown", "grounding", "parse_figure", "detailed"
    ] = Form("markdown"),
    custom_prompt: Optional[str] = Form(None),
    _: None = Depends(ensure_loaded),
):
    result = await ocr_handler.handle(
        file.file, file.filename or "upload", mode, custom_prompt
    )
    return JSONResponse(content=result.model_dump())


@app.get("/api/modes")
async def get_modes():
    return {
        "modes": {
            "free_ocr": {
                "description": "Fast OCR without structure",
                "speed": "⚡⚡⚡ Fast",
                "use_case": "General text extraction",
            },
            "markdown": {
                "description": "Convert document to Markdown with structure",
                "speed": "⚡⚡ Medium",
                "use_case": "Formatted documents",
            },
            "grounding": {
                "description": "OCR with bounding box coordinates",
                "speed": "⚡ Slow",
                "use_case": "Detailed analysis with locations",
            },
            "parse_figure": {
                "description": "Extract information from figures and diagrams",
                "speed": "⚡⚡ Medium",
                "use_case": "Charts, tables, diagrams",
            },
            "detailed": {
                "description": "Detailed description of the image",
                "speed": "⚡⚡⚡ Very fast",
                "use_case": "Visual content analysis",
            },
        }
    }


@app.delete("/api/cleanup")
async def cleanup_old_files(days: int = 7):
    try:
        current_time = time.time()
        days_in_seconds = days * 24 * 60 * 60

        cleaned = {"uploads": 0, "outputs": 0}

        for f in Path(settings.UPLOAD_DIR).iterdir():
            if current_time - f.stat().st_mtime > days_in_seconds:
                f.unlink()
                cleaned["uploads"] += 1

        for folder in Path(settings.OUTPUT_DIR).iterdir():
            if (
                folder.is_dir()
                and current_time - folder.stat().st_mtime > days_in_seconds
            ):
                shutil.rmtree(folder)
                cleaned["outputs"] += 1

        return {
            "success": True,
            "cleaned": cleaned,
            "days": days,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
