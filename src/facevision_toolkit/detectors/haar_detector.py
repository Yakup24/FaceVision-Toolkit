"""Haar Cascade detector backend."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..cascades import load_cascade
from ..config import DetectionSettings
from ..cv import require_cv2
from ..processing import preprocess_frame


class HaarCascadeDetector:
    """OpenCV Haar Cascade based face and eye detector."""

    def __init__(self, face_cascade_path: Path, eye_cascade_path: Path) -> None:
        self.face_cascade = load_cascade(face_cascade_path, "face")
        self.eye_cascade = load_cascade(eye_cascade_path, "eye")

    def detect(self, frame: Any, settings: DetectionSettings) -> list[tuple[int, int, int, int, Any]]:
        opencv = require_cv2()
        gray = preprocess_frame(frame)

        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=settings.scale_factor,
            minNeighbors=settings.min_neighbors,
            minSize=settings.min_face_size,
            flags=opencv.CASCADE_SCALE_IMAGE,
        )

        results = []
        for x, y, width, height in faces:
            eyes = []
            if settings.detect_eyes:
                roi_gray = gray[y : y + height, x : x + width]
                eyes = self.eye_cascade.detectMultiScale(
                    roi_gray,
                    scaleFactor=1.1,
                    minNeighbors=8,
                    minSize=(18, 18),
                    flags=opencv.CASCADE_SCALE_IMAGE,
                )
            results.append((int(x), int(y), int(width), int(height), eyes))

        return results


FaceEyeDetector = HaarCascadeDetector
