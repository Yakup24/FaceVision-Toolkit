"""Camera and video source handling."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .config import RuntimeConfig
from .cv import require_cv2
from .errors import CameraOpenError, InvalidVideoSourceError


def validate_video_source(source: int | str) -> None:
    if isinstance(source, str):
        path = Path(source).expanduser()
        if not path.exists():
            raise InvalidVideoSourceError(f"Video source does not exist: {source}")


def open_capture(config: RuntimeConfig) -> Any:
    opencv = require_cv2()
    validate_video_source(config.source)
    capture = opencv.VideoCapture(config.source)
    if not capture.isOpened():
        raise CameraOpenError(
            f"Camera/video source could not be opened: {config.source!r}. "
            "Check webcam permissions or the source path."
        )
    if isinstance(config.source, int):
        capture.set(opencv.CAP_PROP_FRAME_WIDTH, config.width)
        capture.set(opencv.CAP_PROP_FRAME_HEIGHT, config.height)
    return capture
