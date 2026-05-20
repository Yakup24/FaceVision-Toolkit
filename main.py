"""
FaceVision Tracker
------------------
Real-time face and eye detection with OpenCV Haar Cascade classifiers.

Controls:
    q / ESC  : Exit
    s        : Save screenshot to output folder
    e        : Toggle eye detection on/off
    m        : Toggle mirror mode on/off
"""

from __future__ import annotations

import argparse
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Optional, Sequence

try:
    import cv2
except ImportError:
    cv2 = None  # type: ignore[assignment]


@dataclass
class DetectionSettings:
    scale_factor: float = 1.2
    min_neighbors: int = 6
    min_face_size: tuple[int, int] = (60, 60)
    detect_eyes: bool = True
    mirror: bool = True


@dataclass(frozen=True)
class RuntimeConfig:
    source: int | str
    width: int
    height: int
    output_dir: Path
    headless: bool = False
    max_frames: Optional[int] = None


@dataclass(frozen=True)
class DetectionSummary:
    faces: int
    eyes: int


def require_cv2() -> Any:
    if cv2 is None:
        raise RuntimeError("OpenCV is not installed. Run: python -m pip install -r requirements.txt")
    return cv2


class FaceEyeDetector:
    """OpenCV Haar Cascade based face and eye detector."""

    def __init__(self, face_cascade_path: Path, eye_cascade_path: Path) -> None:
        self.face_cascade = self._load_cascade(face_cascade_path, "face")
        self.eye_cascade = self._load_cascade(eye_cascade_path, "eye")

    @staticmethod
    def _load_cascade(path: Path, name: str) -> cv2.CascadeClassifier:
        opencv = require_cv2()
        if not path.exists():
            raise FileNotFoundError(f"{name.capitalize()} cascade file not found: {path}")

        cascade = opencv.CascadeClassifier(str(path))
        if cascade.empty():
            raise RuntimeError(f"{name.capitalize()} cascade could not be loaded: {path}")

        return cascade

    def detect(self, frame: Any, settings: DetectionSettings) -> list[tuple[int, int, int, int, Any]]:
        opencv = require_cv2()
        gray = opencv.cvtColor(frame, opencv.COLOR_BGR2GRAY)
        gray = opencv.equalizeHist(gray)

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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Real-time face and eye tracking with OpenCV Haar Cascade classifiers."
    )
    parser.add_argument("--camera", type=int, default=0, help="Camera index. Default: 0")
    parser.add_argument("--source", type=str, default=None, help="Optional video file path instead of webcam.")
    parser.add_argument("--scale-factor", type=float, default=1.2, help="Detection scale factor. Default: 1.2")
    parser.add_argument("--min-neighbors", type=int, default=6, help="Detection minNeighbors value. Default: 6")
    parser.add_argument("--min-face-size", type=int, default=60, help="Minimum face width/height in pixels.")
    parser.add_argument("--no-eyes", action="store_true", help="Start with eye detection disabled.")
    parser.add_argument("--no-mirror", action="store_true", help="Start with mirror mode disabled.")
    parser.add_argument("--width", type=int, default=1280, help="Camera frame width. Default: 1280")
    parser.add_argument("--height", type=int, default=720, help="Camera frame height. Default: 720")
    parser.add_argument("--output-dir", type=str, default="output", help="Screenshot output directory.")
    parser.add_argument("--headless", action="store_true", help="Run without opening an OpenCV preview window.")
    parser.add_argument("--max-frames", type=int, default=None, help="Stop after N frames, useful for video tests.")
    return parser


def parse_arguments(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = build_parser()
    args = parser.parse_args(argv)
    validate_arguments(args, parser)
    return args


def validate_arguments(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    if args.scale_factor <= 1.0:
        parser.error("--scale-factor must be greater than 1.0")
    if args.min_neighbors < 1:
        parser.error("--min-neighbors must be at least 1")
    if args.min_face_size < 1:
        parser.error("--min-face-size must be at least 1")
    if args.width < 1 or args.height < 1:
        parser.error("--width and --height must be positive")
    if args.max_frames is not None and args.max_frames < 1:
        parser.error("--max-frames must be positive")


def settings_from_args(args: argparse.Namespace) -> DetectionSettings:
    return DetectionSettings(
        scale_factor=args.scale_factor,
        min_neighbors=args.min_neighbors,
        min_face_size=(args.min_face_size, args.min_face_size),
        detect_eyes=not args.no_eyes,
        mirror=not args.no_mirror,
    )


def runtime_config_from_args(args: argparse.Namespace, project_dir: Path) -> RuntimeConfig:
    source: int | str = args.source if args.source else args.camera
    return RuntimeConfig(
        source=source,
        width=args.width,
        height=args.height,
        output_dir=(project_dir / args.output_dir).resolve(),
        headless=args.headless,
        max_frames=args.max_frames,
    )


def open_capture(config: RuntimeConfig) -> Any:
    opencv = require_cv2()
    capture = opencv.VideoCapture(config.source)
    if not capture.isOpened():
        raise RuntimeError(
            f"Camera/video source could not be opened: {config.source!r}. "
            "Check webcam permissions or the source path."
        )
    if isinstance(config.source, int):
        capture.set(opencv.CAP_PROP_FRAME_WIDTH, config.width)
        capture.set(opencv.CAP_PROP_FRAME_HEIGHT, config.height)
    return capture


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


def save_screenshot(frame: Any, output_dir: Path) -> Path:
    opencv = require_cv2()
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"detection_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    output_path = output_dir / filename
    if not opencv.imwrite(str(output_path), frame):
        raise RuntimeError(f"Screenshot could not be written: {output_path}")
    return output_path


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


def run_tracker(detector: FaceEyeDetector, capture: Any, settings: DetectionSettings, config: RuntimeConfig) -> int:
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
                frame = opencv.flip(frame, 1)

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


def main(argv: Optional[Sequence[str]] = None) -> int:
    try:
        args = parse_arguments(argv)
        project_dir = Path(__file__).resolve().parent
        cascade_dir = project_dir / "cascades"
        settings = settings_from_args(args)
        runtime_config = runtime_config_from_args(args, project_dir)
        detector = FaceEyeDetector(
            face_cascade_path=cascade_dir / "haarcascade_frontalface_default.xml",
            eye_cascade_path=cascade_dir / "haarcascade_eye.xml",
        )
        capture = open_capture(runtime_config)
        run_tracker(detector, capture, settings, runtime_config)
        return 0
    except (FileNotFoundError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
