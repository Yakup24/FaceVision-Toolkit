"""Runtime loop and keyboard state handling."""

from __future__ import annotations

from pathlib import Path
import time
from typing import Any

from .config import DetectionSettings, RuntimeConfig
from .cv import require_cv2
from .detectors.base import Detector
from .overlay import draw_detections
from .processing import mirror_frame
from .screenshot import save_screenshot


class FPSCounter:
    def __init__(self) -> None:
        self.previous_time = time.time()
        self.fps = 0.0

    def update(self) -> float:
        current_time = time.time()
        delta = current_time - self.previous_time
        self.previous_time = current_time
        if delta > 0:
            self.fps = 1.0 / delta
        return self.fps


def handle_key(key: int, settings: DetectionSettings, frame: Any, output_dir: Path) -> bool:
    if key in (ord("q"), 27):
        return False
    if key == ord("s"):
        screenshot_path = save_screenshot(frame, output_dir)
        print(f"Screenshot saved: {screenshot_path}")
    if key == ord("e"):
        settings.detect_eyes = not settings.detect_eyes
        print(f"Eye detection: {'ON' if settings.detect_eyes else 'OFF'}")
    if key == ord("m"):
        settings.mirror = not settings.mirror
        print(f"Mirror mode: {'ON' if settings.mirror else 'OFF'}")
    return True


def run_tracker(detector: Detector, capture: Any, settings: DetectionSettings, config: RuntimeConfig) -> int:
    opencv = require_cv2()
    fps_counter = FPSCounter()
    window_name = "FaceVision Tracker"
    frames_processed = 0

    if not config.headless:
        opencv.namedWindow(window_name, opencv.WINDOW_NORMAL)

    print("Application started.")
    print("Controls: q/ESC=exit, s=screenshot, e=toggle eyes, m=toggle mirror")

    try:
        while True:
            success, frame = capture.read()
            if not success:
                print("Frame could not be read. Exiting...")
                break

            frames_processed += 1
            if settings.mirror:
                frame = mirror_frame(frame)

            detections = detector.detect(frame, settings)
            fps = fps_counter.update()
            summary = draw_detections(frame, detections, fps, settings)

            if config.headless:
                print(f"frame={frames_processed} faces={summary.faces} eyes={summary.eyes} fps={fps:.1f}")
            else:
                opencv.imshow(window_name, frame)
                key = opencv.waitKey(1) & 0xFF
                if not handle_key(key, settings, frame, config.output_dir):
                    break

            if config.max_frames is not None and frames_processed >= config.max_frames:
                break
    finally:
        capture.release()
        if not config.headless:
            opencv.destroyAllWindows()

    return frames_processed
