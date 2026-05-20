"""OpenCV dependency boundary."""

from __future__ import annotations

from typing import Any

try:
    import cv2  # type: ignore[import-not-found]
except ImportError:
    cv2 = None  # type: ignore[assignment]


def require_cv2() -> Any:
    if cv2 is None:
        raise RuntimeError("OpenCV is not installed. Run: python -m pip install -r requirements.txt")
    return cv2
