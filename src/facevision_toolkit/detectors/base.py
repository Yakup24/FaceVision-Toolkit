"""Detector backend protocol."""

from __future__ import annotations

from typing import Any, Protocol

from ..config import DetectionSettings


class Detector(Protocol):
    def detect(self, frame: Any, settings: DetectionSettings) -> list[tuple[int, int, int, int, Any]]:
        """Return face boxes and nested eye detections for a frame."""
