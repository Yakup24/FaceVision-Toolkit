"""Screenshot path and write helpers."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from .cv import require_cv2
from .errors import ScreenshotSaveError


def build_screenshot_path(output_dir: Path, timestamp: datetime | None = None) -> Path:
    moment = timestamp or datetime.now()
    filename = f"screenshot_{moment.strftime('%Y%m%d_%H%M%S')}.png"
    return output_dir / filename


def save_screenshot(frame: Any, output_dir: Path) -> Path:
    opencv = require_cv2()
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = build_screenshot_path(output_dir)
    if not opencv.imwrite(str(output_path), frame):
        raise ScreenshotSaveError(f"Screenshot could not be written: {output_path}")
    return output_path
