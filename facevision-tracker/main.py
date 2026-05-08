"""
Yakup Face & Eye Detector
--------------------------------
Real-time face and eye detection with OpenCV Haar Cascade classifiers.

Controls:
    q / ESC  : Exit
    s        : Save screenshot to output folder
    e        : Toggle eye detection on/off
    m        : Toggle mirror mode on/off
"""

from __future__ import annotations

import argparse
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

import cv2


@dataclass
class DetectionSettings:
    scale_factor: float = 1.2
    min_neighbors: int = 6
    min_face_size: tuple[int, int] = (60, 60)
    detect_eyes: bool = True
    mirror: bool = True


class FaceEyeDetector:
    """OpenCV Haar Cascade based face and eye detector."""

    def __init__(self, face_cascade_path: Path, eye_cascade_path: Path) -> None:
        self.face_cascade = self._load_cascade(face_cascade_path, "face")
        self.eye_cascade = self._load_cascade(eye_cascade_path, "eye")

    @staticmethod
    def _load_cascade(path: Path, name: str) -> cv2.CascadeClassifier:
        if not path.exists():
            raise FileNotFoundError(f"{name.capitalize()} cascade file not found: {path}")

        cascade = cv2.CascadeClassifier(str(path))
        if cascade.empty():
            raise RuntimeError(f"{name.capitalize()} cascade could not be loaded: {path}")

        return cascade

    def detect(self, frame, settings: DetectionSettings):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=settings.scale_factor,
            minNeighbors=settings.min_neighbors,
            minSize=settings.min_face_size,
            flags=cv2.CASCADE_SCALE_IMAGE,
        )

        results = []
        for (x, y, w, h) in faces:
            eyes = []
            if settings.detect_eyes:
                roi_gray = gray[y : y + h, x : x + w]
                eyes = self.eye_cascade.detectMultiScale(
                    roi_gray,
                    scaleFactor=1.1,
                    minNeighbors=8,
                    minSize=(18, 18),
                    flags=cv2.CASCADE_SCALE_IMAGE,
                )
            results.append((x, y, w, h, eyes))

        return results


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


def draw_detections(frame, detections: Iterable, fps: float, settings: DetectionSettings) -> None:
    face_count = 0
    eye_count = 0

    for (x, y, w, h, eyes) in detections:
        face_count += 1
        cv2.rectangle(frame, (x, y), (x + w, y + h), (40, 220, 40), 2)
        cv2.putText(
            frame,
            "Face",
            (x, max(y - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (40, 220, 40),
            2,
        )

        for (ex, ey, ew, eh) in eyes:
            eye_count += 1
            cv2.rectangle(
                frame,
                (x + ex, y + ey),
                (x + ex + ew, y + ey + eh),
                (40, 40, 240),
                2,
            )

    status_line = (
        f"Faces: {face_count} | Eyes: {eye_count} | FPS: {fps:.1f} | "
        f"Eye Detection: {'ON' if settings.detect_eyes else 'OFF'} | Mirror: {'ON' if settings.mirror else 'OFF'}"
    )
    help_line = "q/ESC: Exit | s: Screenshot | e: Eye ON/OFF | m: Mirror ON/OFF"

    cv2.rectangle(frame, (0, 0), (frame.shape[1], 64), (0, 0, 0), -1)
    cv2.putText(frame, status_line, (12, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.58, (255, 255, 255), 2)
    cv2.putText(frame, help_line, (12, 52), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (210, 210, 210), 1)


def save_screenshot(frame, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"detection_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    output_path = output_dir / filename
    cv2.imwrite(str(output_path), frame)
    return output_path


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Advanced real-time face and eye detection with OpenCV."
    )
    parser.add_argument("--camera", type=int, default=0, help="Camera index. Default: 0")
    parser.add_argument("--source", type=str, default=None, help="Optional video file path instead of webcam.")
    parser.add_argument("--scale-factor", type=float, default=1.2, help="Detection scale factor. Default: 1.2")
    parser.add_argument("--min-neighbors", type=int, default=6, help="Detection minNeighbors value. Default: 6")
    parser.add_argument("--no-eyes", action="store_true", help="Start with eye detection disabled.")
    parser.add_argument("--no-mirror", action="store_true", help="Start with mirror mode disabled.")
    parser.add_argument("--width", type=int, default=1280, help="Camera frame width. Default: 1280")
    parser.add_argument("--height", type=int, default=720, help="Camera frame height. Default: 720")
    parser.add_argument("--output-dir", type=str, default="output", help="Screenshot output directory.")
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    project_dir = Path(__file__).resolve().parent
    cascade_dir = project_dir / "cascades"

    settings = DetectionSettings(
        scale_factor=args.scale_factor,
        min_neighbors=args.min_neighbors,
        detect_eyes=not args.no_eyes,
        mirror=not args.no_mirror,
    )

    detector = FaceEyeDetector(
        face_cascade_path=cascade_dir / "haarcascade_frontalface_default.xml",
        eye_cascade_path=cascade_dir / "haarcascade_eye.xml",
    )

    source = args.source if args.source else args.camera
    capture = cv2.VideoCapture(source)

    if not capture.isOpened():
        raise RuntimeError("Camera/video source could not be opened. Check your webcam permissions or source path.")

    if args.source is None:
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)

    fps_counter = FPSCounter()
    output_dir = project_dir / args.output_dir
    window_name = "Advanced Face & Eye Detection"

    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    print("Application started.")
    print("Controls: q/ESC=exit, s=screenshot, e=toggle eyes, m=toggle mirror")

    while True:
        success, frame = capture.read()
        if not success:
            print("Frame could not be read. Exiting...")
            break

        if settings.mirror:
            frame = cv2.flip(frame, 1)

        detections = detector.detect(frame, settings)
        fps = fps_counter.update()
        draw_detections(frame, detections, fps, settings)

        cv2.imshow(window_name, frame)
        key = cv2.waitKey(1) & 0xFF

        if key in (ord("q"), 27):
            break
        if key == ord("s"):
            screenshot_path = save_screenshot(frame, output_dir)
            print(f"Screenshot saved: {screenshot_path}")
        if key == ord("e"):
            settings.detect_eyes = not settings.detect_eyes
            print(f"Eye detection: {'ON' if settings.detect_eyes else 'OFF'}")
        if key == ord("m"):
            settings.mirror = not settings.mirror
            print(f"Mirror mode: {'ON' if settings.mirror else 'OFF'}")

    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
