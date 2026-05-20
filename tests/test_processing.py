from types import SimpleNamespace

from facevision_toolkit import cv
from facevision_toolkit.processing import mirror_frame, preprocess_frame


def test_preprocess_frame_runs_grayscale_and_equalization(monkeypatch):
    calls = []

    def fake_cvt_color(frame, mode):
        calls.append(("cvtColor", frame, mode))
        return "gray"

    def fake_equalize_hist(frame):
        calls.append(("equalizeHist", frame))
        return "equalized"

    fake_cv2 = SimpleNamespace(COLOR_BGR2GRAY=6, cvtColor=fake_cvt_color, equalizeHist=fake_equalize_hist)
    monkeypatch.setattr(cv, "cv2", fake_cv2)

    result = preprocess_frame("frame")

    assert result == "equalized"
    assert calls == [("cvtColor", "frame", 6), ("equalizeHist", "gray")]


def test_mirror_frame_uses_horizontal_flip(monkeypatch):
    fake_cv2 = SimpleNamespace(flip=lambda frame, axis: (frame, axis))
    monkeypatch.setattr(cv, "cv2", fake_cv2)

    assert mirror_frame("frame") == ("frame", 1)
