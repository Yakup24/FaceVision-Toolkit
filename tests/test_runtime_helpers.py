from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from facevision_toolkit import cv
from facevision_toolkit.camera import open_capture
from facevision_toolkit.config import DetectionSettings, RuntimeConfig
from facevision_toolkit.overlay import count_detections
from facevision_toolkit.runtime import handle_key
from facevision_toolkit.screenshot import build_screenshot_path, save_screenshot


class FakeCapture:
    def __init__(self, opened=True):
        self.opened = opened
        self.settings = []

    def isOpened(self):
        return self.opened

    def set(self, prop, value):
        self.settings.append((prop, value))


def test_require_cv2_reports_missing_dependency(monkeypatch):
    monkeypatch.setattr(cv, "cv2", None)

    with pytest.raises(RuntimeError, match="OpenCV is not installed"):
        cv.require_cv2()


def test_open_capture_reports_unavailable_source(monkeypatch):
    fake_cv2 = SimpleNamespace(VideoCapture=lambda source: FakeCapture(opened=False))
    monkeypatch.setattr(cv, "cv2", fake_cv2)
    config = RuntimeConfig(source=99, width=640, height=480, output_dir=Mock())

    with pytest.raises(RuntimeError, match="could not be opened"):
        open_capture(config)


def test_open_capture_applies_camera_dimensions(monkeypatch, tmp_path):
    capture = FakeCapture(opened=True)
    fake_cv2 = SimpleNamespace(
        VideoCapture=lambda source: capture,
        CAP_PROP_FRAME_WIDTH=3,
        CAP_PROP_FRAME_HEIGHT=4,
    )
    monkeypatch.setattr(cv, "cv2", fake_cv2)
    config = RuntimeConfig(source=0, width=640, height=480, output_dir=tmp_path)

    opened = open_capture(config)

    assert opened is capture
    assert capture.settings == [(3, 640), (4, 480)]


def test_count_detections_returns_faces_and_eyes():
    detections = [
        (0, 0, 100, 100, [(1, 1, 20, 20), (30, 1, 20, 20)]),
        (120, 0, 100, 100, []),
    ]

    summary = count_detections(detections)

    assert summary.faces == 2
    assert summary.eyes == 2


def test_handle_key_toggles_runtime_settings(tmp_path, monkeypatch):
    settings = DetectionSettings(detect_eyes=True, mirror=True)
    monkeypatch.setattr("facevision_toolkit.runtime.save_screenshot", lambda frame, output_dir: tmp_path / "shot.png")

    assert handle_key(ord("e"), settings, object(), tmp_path) is True
    assert settings.detect_eyes is False

    assert handle_key(ord("m"), settings, object(), tmp_path) is True
    assert settings.mirror is False

    assert handle_key(ord("q"), settings, object(), tmp_path) is False


def test_save_screenshot_raises_when_write_fails(tmp_path, monkeypatch):
    fake_cv2 = SimpleNamespace(imwrite=Mock(return_value=False))
    monkeypatch.setattr(cv, "cv2", fake_cv2)

    with pytest.raises(RuntimeError, match="Screenshot could not be written"):
        save_screenshot(object(), tmp_path)


def test_screenshot_filename_has_png_extension(tmp_path):
    path = build_screenshot_path(tmp_path)

    assert path.suffix == ".png"
    assert path.parent == tmp_path
