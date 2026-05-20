"""Haar cascade loading helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .cv import require_cv2
from .errors import CascadeLoadError


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def default_cascade_dir() -> Path:
    return project_root() / "cascades"


def load_cascade(path: Path, name: str) -> Any:
    opencv = require_cv2()
    if not path.exists():
        raise CascadeLoadError(f"{name.capitalize()} cascade file not found: {path}")

    cascade = opencv.CascadeClassifier(str(path))
    if cascade.empty():
        raise CascadeLoadError(f"{name.capitalize()} cascade could not be loaded: {path}")

    return cascade
