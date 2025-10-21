import os
from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # Modelo
    MODEL_NAME: str = os.getenv("MODEL_NAME", "deepseek-ai/DeepSeek-OCR")
    
    # Rutas
    UPLOAD_DIR: str = "/app/uploads"
    OUTPUT_DIR: str = "/app/outputs"
    
    # Configuración de imagen
    BASE_SIZE: int = int(os.getenv("BASE_SIZE", "1024"))
    IMAGE_SIZE: int = int(os.getenv("IMAGE_SIZE", "640"))
    CROP_MODE: bool = True
    
    # Límites
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: set = {".jpg", ".jpeg", ".png", ".pdf", ".webp"}
    
    # Device
    DEVICE: str = "cuda" if os.getenv("CUDA_VISIBLE_DEVICES") else "cpu"
    
    class Config:
        env_file = ".env"


# Prompts predefinidos
PROMPTS = {
    "free_ocr": "<image>\nFree OCR. ",
    "markdown": "<image>\n<|grounding|>Convert the document to markdown. ",
    "grounding": "<image>\n<|grounding|>OCR this image. ",
    "parse_figure": "<image>\nParse the figure. ",
    "detailed": "<image>\nDescribe this image in detail. ",
}


settings = Settings()
