from __future__ import annotations

from typing import Callable, Optional

from model_lifecycle import InferSettings, OcrModel


class FakeOcr:
    def __init__(
        self,
        infer_return: str = "CANNED OCR RESULT",
        load_error: Optional[Exception] = None,
    ):
        self.infer_return = infer_return
        self.load_error = load_error
        self.load_called = False
        self.infer_calls: list[tuple[str, str, str, InferSettings]] = []
        self._load_callback: Optional[Callable[[int, str], None]] = None

    def load(self, progress_callback: Callable[[int, str], None]) -> None:
        self.load_called = True
        self._load_callback = progress_callback
        if self.load_error:
            raise self.load_error

    def infer(
        self,
        image_path: str,
        prompt: str,
        output_path: str,
        settings: InferSettings,
    ) -> str:
        self.infer_calls.append((image_path, prompt, output_path, settings))
        return self.infer_return
