"""Frame preprocessing helpers."""

from __future__ import annotations

from typing import Any

from .cv import require_cv2


def preprocess_frame(frame: Any) -> Any:
    opencv = require_cv2()
    gray = opencv.cvtColor(frame, opencv.COLOR_BGR2GRAY)
    return opencv.equalizeHist(gray)


def mirror_frame(frame: Any) -> Any:
    opencv = require_cv2()
    return opencv.flip(frame, 1)
