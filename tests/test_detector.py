from pathlib import Path
from types import SimpleNamespace

import pytest

from facevision_toolkit import cv
from facevision_toolkit.cascades import load_cascade


class FakeCascade:
    def __init__(self, empty=False):
        self._empty = empty

    def empty(self):
        return self._empty


def test_load_cascade_reports_missing_file(tmp_path, monkeypatch):
    fake_cv2 = SimpleNamespace(CascadeClassifier=lambda path: FakeCascade())
    monkeypatch.setattr(cv, "cv2", fake_cv2)

    with pytest.raises(RuntimeError, match="Face cascade file not found"):
        load_cascade(tmp_path / "missing.xml", "face")


def test_load_cascade_reports_empty_classifier(tmp_path, monkeypatch):
    cascade_path = tmp_path / "cascade.xml"
    cascade_path.write_text("<xml />", encoding="utf-8")
    fake_cv2 = SimpleNamespace(CascadeClassifier=lambda path: FakeCascade(empty=True))
    monkeypatch.setattr(cv, "cv2", fake_cv2)

    with pytest.raises(RuntimeError, match="could not be loaded"):
        load_cascade(cascade_path, "face")


def test_repository_cascade_files_exist():
    root = Path(__file__).resolve().parents[1]

    assert (root / "cascades" / "haarcascade_frontalface_default.xml").exists()
    assert (root / "cascades" / "haarcascade_eye.xml").exists()
