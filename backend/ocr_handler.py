from __future__ import annotations

import logging
import os
import shutil
import time
from datetime import datetime
from pathlib import Path
from typing import BinaryIO, Literal, Optional

from fastapi import HTTPException
from PIL import Image
from pydantic import BaseModel

from config import PROMPTS
from model_lifecycle import InferSettings, OcrModel

logger = logging.getLogger(__name__)

OcrMode = Literal["free_ocr", "markdown", "grounding", "parse_figure", "detailed"]


class OcrResult(BaseModel):
    text: str
    mode: str
    prompt: str
    processing_time: float
    image_size: tuple[int, int]
    file_size: int
    timestamp: str
    output_dir: str
    metadata: dict


class OcrHandler:
    def __init__(
        self,
        model: OcrModel,
        upload_dir: str,
        output_dir: str,
        max_file_size: int,
        allowed_extensions: set[str],
        device: str,
    ):
        self._model = model
        self._upload_dir = upload_dir
        self._output_dir = output_dir
        self._max_file_size = max_file_size
        self._allowed_extensions = allowed_extensions
        self._device = device

        Path(self._upload_dir).mkdir(parents=True, exist_ok=True)
        Path(self._output_dir).mkdir(parents=True, exist_ok=True)

    async def handle(
        self,
        file_obj: BinaryIO,
        filename: str,
        mode: OcrMode = "markdown",
        custom_prompt: Optional[str] = None,
    ) -> OcrResult:
        file_ext = Path(filename).suffix.lower()
        if file_ext not in self._allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"File type not allowed. Use: {self._allowed_extensions}",
            )

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = f"{timestamp}_{filename}"
        upload_path = os.path.join(self._upload_dir, unique_id)
        output_dir = os.path.join(self._output_dir, timestamp)

        try:
            with open(upload_path, "wb") as buffer:
                shutil.copyfileobj(file_obj, buffer)

            file_size = os.path.getsize(upload_path)
            if file_size > self._max_file_size:
                os.remove(upload_path)
                raise HTTPException(
                    status_code=400,
                    detail=f"File too large. Max: {self._max_file_size / 1024 / 1024}MB",
                )

            try:
                with Image.open(upload_path) as img:
                    img_size = img.size
            except Exception as e:
                os.remove(upload_path)
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid image: {e}",
                )

            prompt = (
                custom_prompt
                if custom_prompt
                else PROMPTS.get(mode, PROMPTS["markdown"])
            )

            os.makedirs(output_dir, exist_ok=True)
            logger.info(f"Processing {unique_id} mode={mode}")
            start = time.time()

            settings = InferSettings()
            result_text = self._model.infer(upload_path, prompt, output_dir, settings)
            elapsed = time.time() - start

            result_file = os.path.join(output_dir, "result.mmd")
            text_content = ""
            if os.path.exists(result_file):
                with open(result_file, "r", encoding="utf-8") as f:
                    text_content = f.read()

            return OcrResult(
                text=text_content or result_text,
                mode=mode,
                prompt=prompt,
                processing_time=round(elapsed, 2),
                image_size=img_size,
                file_size=file_size,
                timestamp=timestamp,
                output_dir=output_dir,
                metadata={
                    "filename": filename,
                    "unique_id": unique_id,
                    "device": self._device,
                },
            )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"OCR error: {e}")
            if os.path.exists(upload_path):
                os.remove(upload_path)
            raise HTTPException(status_code=500, detail=f"OCR error: {e}")
