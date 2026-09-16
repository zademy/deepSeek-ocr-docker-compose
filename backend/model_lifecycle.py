from __future__ import annotations

import asyncio
import logging
import time
from pathlib import Path
from typing import Callable, Literal, Optional, Protocol

import torch
from pydantic import BaseModel, Field
from transformers import AutoModel, AutoTokenizer

logger = logging.getLogger(__name__)


ProgressStatus = Literal["idle", "downloading", "completed", "error"]


class Progress(BaseModel):
    status: ProgressStatus = "idle"
    percent: int = Field(default=0, ge=0, le=100)
    message: str = ""


class ModelStatus(BaseModel):
    loaded: bool
    loading: bool
    error: Optional[str] = None
    progress: Progress = Field(default_factory=Progress)


class InferSettings(BaseModel):
    base_size: int = 1024
    image_size: int = 768
    crop_mode: bool = True
    save_results: bool = True


class OcrModel(Protocol):
    def infer(
        self,
        image_path: str,
        prompt: str,
        output_path: str,
        settings: InferSettings,
    ) -> str: ...


class LoadableModel(Protocol):
    def load(self, progress_callback: Callable[[int, str], None]) -> None: ...


class ModelLoadError(RuntimeError):
    pass


class ModelLifecycle:
    def __init__(self, model: LoadableModel, settings: InferSettings):
        self._model = model
        self._settings = settings
        self._loaded = False
        self._loading = False
        self._error: Optional[str] = None
        self._progress = Progress()
        self._lock = asyncio.Lock()

    def status(self) -> ModelStatus:
        return ModelStatus(
            loaded=self._loaded,
            loading=self._loading,
            error=self._error,
            progress=self._progress,
        )

    def settings(self) -> InferSettings:
        return self._settings

    async def ensure_loaded(self) -> None:
        async with self._lock:
            if self._loaded:
                return
            if self._error and not self._loading:
                raise ModelLoadError(self._error)
            self._loading = True
            self._progress = Progress(
                status="downloading", percent=0, message="Starting"
            )
            try:
                await asyncio.to_thread(self._model.load, self._report_progress)
                self._loaded = True
                self._loading = False
                self._progress = Progress(
                    status="completed", percent=100, message="Loaded"
                )
            except Exception as e:
                self._loading = False
                self._error = str(e)
                self._progress = Progress(status="error", percent=0, message=str(e))
                raise ModelLoadError(str(e)) from e

    def _report_progress(self, percent: int, message: str) -> None:
        self._progress = Progress(
            status="downloading" if percent < 100 else "completed",
            percent=percent,
            message=message,
        )


class DeepSeekModel:
    def __init__(self, model_name: str, device: str):
        self._model_name = model_name
        self._device = device
        self._model = None
        self._tokenizer = None

    def load(self, progress_callback) -> None:
        progress_callback(10, "Downloading tokenizer")
        self._tokenizer = AutoTokenizer.from_pretrained(
            self._model_name, trust_remote_code=True
        )

        progress_callback(30, "Tokenizer downloaded. Downloading model")

        try:
            progress_callback(40, "Loading with flash_attention_2")
            self._model = AutoModel.from_pretrained(
                self._model_name,
                _attn_implementation="flash_attention_2",
                trust_remote_code=True,
                use_safetensors=True,
            )
        except Exception as e:
            logger.warning(f"flash_attention_2 unavailable: {e}")
            progress_callback(50, "Loading with eager attention")
            self._model = AutoModel.from_pretrained(
                self._model_name,
                _attn_implementation="eager",
                trust_remote_code=True,
                use_safetensors=True,
            )

        progress_callback(80, "Configuring device")
        if self._device == "cuda" and torch.cuda.is_available():
            logger.info("Moving model to GPU")
            progress_callback(85, "Moving to GPU")
            self._model = self._model.eval().cuda().to(torch.bfloat16)
            logger.info(f"Model on GPU: {torch.cuda.get_device_name(0)}")
        else:
            progress_callback(85, "Using CPU")
            self._model = self._model.eval()

        progress_callback(100, "Model loaded")

    def infer(
        self,
        image_path: str,
        prompt: str,
        output_path: str,
        settings: InferSettings,
    ) -> str:
        if self._model is None or self._tokenizer is None:
            raise RuntimeError("Model not loaded")

        Path(output_path).mkdir(parents=True, exist_ok=True)

        result = self._model.infer(
            self._tokenizer,
            prompt=prompt,
            image_file=image_path,
            output_path=output_path,
            base_size=settings.base_size,
            image_size=settings.image_size,
            crop_mode=settings.crop_mode,
            save_results=settings.save_results,
        )
        return result or ""

    def device(self) -> str:
        return self._device


class CannedModel:
    def __init__(self, result_text: Optional[str] = None):
        default_text = (
            "# Documento de ejemplo\n\n"
            "Este texto proviene del adaptador de verificacion local.\n\n"
            "- Primer elemento\n- Segundo elemento\n"
        )
        self._result_text = default_text if result_text is None else result_text

    def load(self, progress_callback: Callable[[int, str], None]) -> None:
        for percent, message in [
            (10, "Preparando"),
            (40, "Cargando"),
            (80, "Configurando"),
        ]:
            progress_callback(percent, message)
            time.sleep(2.5)
        progress_callback(100, "Listo")

    def infer(
        self,
        image_path: str,
        prompt: str,
        output_path: str,
        settings: InferSettings,
    ) -> str:
        time.sleep(1.5)
        return self._result_text
