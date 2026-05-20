"""Run a local benchmark against a camera or video source.

This script reports measurements from the current machine only. It does not
ship benchmark claims or compare hardware.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Benchmark FaceVision Toolkit on a local source.")
    parser.add_argument("--source", default="0", help="Camera index or video file path.")
    parser.add_argument("--frames", type=int, default=300, help="Maximum frames to process.")
    parser.add_argument("--width", type=int, default=640, help="Camera width for camera sources.")
    parser.add_argument("--height", type=int, default=480, help="Camera height for camera sources.")
    parser.add_argument("--no-eyes", action="store_true", help="Disable eye detection during benchmark.")
    return parser


def main() -> int:
    from facevision_toolkit.camera import open_capture
    from facevision_toolkit.cascades import default_cascade_dir
    from facevision_toolkit.config import DetectionSettings, RuntimeConfig, coerce_source
    from facevision_toolkit.detectors.haar_detector import HaarCascadeDetector

    args = build_parser().parse_args()
    source = coerce_source(args.source)
    config = RuntimeConfig(
        source=source,
        width=args.width,
        height=args.height,
        output_dir=ROOT / "output",
        headless=True,
        max_frames=args.frames,
    )
    settings = DetectionSettings(detect_eyes=not args.no_eyes)
    cascade_dir = default_cascade_dir()
    detector = HaarCascadeDetector(
        face_cascade_path=cascade_dir / "haarcascade_frontalface_default.xml",
        eye_cascade_path=cascade_dir / "haarcascade_eye.xml",
    )
    capture = open_capture(config)

    frames = 0
    started = time.perf_counter()
    try:
        while frames < args.frames:
            ok, frame = capture.read()
            if not ok:
                break
            detector.detect(frame, settings)
            frames += 1
    finally:
        capture.release()

    elapsed = time.perf_counter() - started
    average_fps = frames / elapsed if elapsed > 0 else 0.0
    print(f"Frames processed: {frames}")
    print(f"Elapsed seconds: {elapsed:.2f}")
    print(f"Average FPS: {average_fps:.2f}")
    print("Detector backend: haar")
    print(f"Resolution request: {args.width}x{args.height}")
    print("Note: results depend on hardware, lighting, source resolution and OpenCV backend.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
