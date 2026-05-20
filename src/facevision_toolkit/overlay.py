"""Overlay rendering and detection summary helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from .config import DetectionSettings
from .cv import require_cv2


@dataclass(frozen=True)
class DetectionSummary:
    faces: int
    eyes: int


def count_detections(detections: Iterable[tuple[int, int, int, int, Iterable[Any]]]) -> DetectionSummary:
    faces = 0
    eyes = 0
    for _, _, _, _, face_eyes in detections:
        faces += 1
        eyes += len(list(face_eyes))
    return DetectionSummary(faces=faces, eyes=eyes)


def draw_detections(frame: Any, detections: Iterable, fps: float, settings: DetectionSettings) -> DetectionSummary:
    opencv = require_cv2()
    detections = list(detections)
    summary = count_detections(detections)

    for x, y, width, height, eyes in detections:
        opencv.rectangle(frame, (x, y), (x + width, y + height), (40, 220, 40), 2)
        opencv.putText(
            frame,
            "Face",
            (x, max(y - 10, 20)),
            opencv.FONT_HERSHEY_SIMPLEX,
            0.7,
            (40, 220, 40),
            2,
        )

        for ex, ey, eye_width, eye_height in eyes:
            opencv.rectangle(
                frame,
                (x + ex, y + ey),
                (x + ex + eye_width, y + ey + eye_height),
                (40, 40, 240),
                2,
            )

    status_line = (
        f"Faces: {summary.faces} | Eyes: {summary.eyes} | FPS: {fps:.1f} | "
        f"Eye Detection: {'ON' if settings.detect_eyes else 'OFF'} | Mirror: {'ON' if settings.mirror else 'OFF'}"
    )
    help_line = "q/ESC: Exit | s: Screenshot | e: Eye ON/OFF | m: Mirror ON/OFF"

    opencv.rectangle(frame, (0, 0), (frame.shape[1], 64), (0, 0, 0), -1)
    opencv.putText(frame, status_line, (12, 24), opencv.FONT_HERSHEY_SIMPLEX, 0.58, (255, 255, 255), 2)
    opencv.putText(frame, help_line, (12, 52), opencv.FONT_HERSHEY_SIMPLEX, 0.55, (210, 210, 210), 1)
    return summary
