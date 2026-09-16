from __future__ import annotations

import asyncio
import io
from pathlib import Path

import pytest
from fastapi import HTTPException
from PIL import Image

from model_lifecycle import (
    CannedModel,
    InferSettings,
    ModelLifecycle,
    ModelLoadError,
)
from ocr_handler import OcrHandler
from tests.fakes import FakeOcr


def _png_bytes() -> bytes:
    buf = io.BytesIO()
    Image.new("RGB", (4, 4), color="white").save(buf, format="PNG")
    return buf.getvalue()


@pytest.fixture
def fake_ocr() -> FakeOcr:
    return FakeOcr(infer_return="CANNED OCR TEXT")


@pytest.fixture
def handler(fake_ocr: FakeOcr, tmp_path: Path) -> OcrHandler:
    return OcrHandler(
        model=fake_ocr,
        upload_dir=str(tmp_path / "uploads"),
        output_dir=str(tmp_path / "outputs"),
        max_file_size=10 * 1024 * 1024,
        allowed_extensions={".png", ".jpg", ".jpeg"},
        device="cpu",
    )


@pytest.mark.asyncio
async def test_handler_runs_pipeline_without_gpu(
    fake_ocr: FakeOcr, handler: OcrHandler
):
    file_obj = io.BytesIO(_png_bytes())
    result = await handler.handle(file_obj, "test.png", "markdown")

    assert result.text == "CANNED OCR TEXT"
    assert result.mode == "markdown"
    assert result.image_size == (4, 4)
    assert fake_ocr.infer_calls, "infer should have been called"
    called_image, called_prompt, called_output, called_settings = fake_ocr.infer_calls[
        0
    ]
    assert called_image.endswith(".png")
    assert "<image>" in called_prompt
    assert called_settings.image_size == 768


@pytest.mark.asyncio
async def test_handler_rejects_disallowed_extension(handler: OcrHandler):
    file_obj = io.BytesIO(_png_bytes())
    with pytest.raises(HTTPException) as exc:
        await handler.handle(file_obj, "test.gif", "markdown")
    assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_handler_rejects_oversized_file(handler: OcrHandler, tmp_path: Path):
    big = b"\x00" * (11 * 1024 * 1024)
    file_obj = io.BytesIO(big)
    with pytest.raises(HTTPException) as exc:
        await handler.handle(file_obj, "big.png", "markdown")
    assert exc.value.status_code == 400
    assert not list((tmp_path / "uploads").glob("*.png"))


@pytest.mark.asyncio
async def test_handler_rejects_corrupt_image(handler: OcrHandler):
    file_obj = io.BytesIO(b"not a real image")
    with pytest.raises(HTTPException) as exc:
        await handler.handle(file_obj, "bad.png", "markdown")
    assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_handler_uses_custom_prompt_when_provided(
    fake_ocr: FakeOcr, handler: OcrHandler
):
    file_obj = io.BytesIO(_png_bytes())
    await handler.handle(
        file_obj, "test.png", "markdown", custom_prompt="<image>\nCustom."
    )
    _, called_prompt, _, _ = fake_ocr.infer_calls[0]
    assert called_prompt == "<image>\nCustom."


@pytest.mark.asyncio
async def test_lifecycle_idempotent_under_concurrent_calls():
    fake = FakeOcr()
    lc = ModelLifecycle(model=fake, settings=InferSettings())
    await asyncio.gather(lc.ensure_loaded(), lc.ensure_loaded(), lc.ensure_loaded())
    assert fake.load_called


@pytest.mark.asyncio
async def test_lifecycle_load_error_surfaces_as_model_load_error():
    fake = FakeOcr(load_error=RuntimeError("boom"))
    lc = ModelLifecycle(model=fake, settings=InferSettings())

    with pytest.raises(ModelLoadError):
        await lc.ensure_loaded()

    status = lc.status()
    assert status.error == "boom"
    assert status.progress.status == "error"


@pytest.mark.asyncio
async def test_canned_model_loads_and_infers():
    canned = CannedModel(result_text="TEXTO ENLATADO")
    lc = ModelLifecycle(model=canned, settings=InferSettings())
    await lc.ensure_loaded()

    assert lc.status().loaded
    assert lc.status().progress.percent == 100

    out = canned.infer("/tmp/x.png", "<image>\nFree OCR. ", "/tmp/out", InferSettings())
    assert out == "TEXTO ENLATADO"


@pytest.mark.asyncio
async def test_canned_model_can_return_empty_result():
    canned = CannedModel(result_text="")
    out = canned.infer("/tmp/x.png", "<image>\nFree OCR. ", "/tmp/out", InferSettings())
    assert out == ""
