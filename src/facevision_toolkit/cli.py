"""Command-line interface for FaceVision Toolkit."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import Any, Mapping, Optional, Sequence

from .camera import open_capture
from .cascades import default_cascade_dir
from .config import (
    DEFAULT_CAMERA,
    DEFAULT_HEIGHT,
    DEFAULT_MIN_FACE_SIZE,
    DEFAULT_MIN_NEIGHBORS,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_SCALE_FACTOR,
    DEFAULT_WIDTH,
    DetectionSettings,
    RuntimeConfig,
    coerce_source,
    config_bool,
    load_config_file,
    section,
    validate_detection_settings,
    validate_runtime_config,
)
from .detectors.haar_detector import HaarCascadeDetector
from .errors import ConfigError, FaceVisionError
from .runtime import run_tracker


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Real-time face and eye tracking with OpenCV Haar Cascade classifiers."
    )
    parser.add_argument("--config", type=str, default=None, help="Optional JSON/YAML config file.")
    parser.add_argument("--camera", type=int, default=None, help="Camera index. Default: 0")
    parser.add_argument("--source", type=str, default=None, help="Optional video file path instead of webcam.")
    parser.add_argument("--scale-factor", type=float, default=None, help="Detection scale factor. Default: 1.2")
    parser.add_argument("--min-neighbors", type=int, default=None, help="Detection minNeighbors value. Default: 6")
    parser.add_argument("--min-face-size", type=int, default=None, help="Minimum face width/height in pixels.")
    parser.add_argument("--no-eyes", action="store_true", default=None, help="Start with eye detection disabled.")
    parser.add_argument("--no-mirror", action="store_true", default=None, help="Start with mirror mode disabled.")
    parser.add_argument("--width", type=int, default=None, help="Camera frame width. Default: 1280")
    parser.add_argument("--height", type=int, default=None, help="Camera frame height. Default: 720")
    parser.add_argument("--output-dir", type=str, default=None, help="Screenshot output directory.")
    parser.add_argument("--headless", action="store_true", default=None, help="Run without an OpenCV preview window.")
    parser.add_argument("--max-frames", type=int, default=None, help="Stop after N frames, useful for video tests.")
    parser.add_argument("--debug", action="store_true", default=None, help="Print extra runtime context.")
    return parser


def parse_arguments(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = build_parser()
    args = parser.parse_args(argv)
    config = load_config_file(args.config)
    apply_argument_defaults(args, config)
    validate_args(args, parser)
    return args


def apply_argument_defaults(args: argparse.Namespace, config: Mapping[str, Any]) -> None:
    camera = section(config, "camera")
    detector = section(config, "detector")
    runtime = section(config, "runtime")
    output = section(config, "output")

    configured_source = camera.get("source", camera.get("camera", DEFAULT_CAMERA))
    if args.source is None and args.camera is None:
        source = coerce_source(configured_source)
        if isinstance(source, int):
            args.camera = source
        else:
            args.source = source

    args.camera = DEFAULT_CAMERA if args.camera is None else args.camera
    args.width = int(camera.get("width", DEFAULT_WIDTH) if args.width is None else args.width)
    args.height = int(camera.get("height", DEFAULT_HEIGHT) if args.height is None else args.height)
    args.scale_factor = float(
        detector.get("face_scale_factor", detector.get("scale_factor", DEFAULT_SCALE_FACTOR))
        if args.scale_factor is None
        else args.scale_factor
    )
    args.min_neighbors = int(
        detector.get("min_neighbors", DEFAULT_MIN_NEIGHBORS)
        if args.min_neighbors is None
        else args.min_neighbors
    )
    args.min_face_size = int(
        detector.get("min_face_size", DEFAULT_MIN_FACE_SIZE)
        if args.min_face_size is None
        else args.min_face_size
    )

    detect_eyes = config_bool(detector.get("enable_eye_detection", True), True)
    mirror = config_bool(runtime.get("mirror", True), True)
    headless = config_bool(runtime.get("headless", False), False)
    debug = config_bool(runtime.get("debug", False), False)

    args.no_eyes = (not detect_eyes) if args.no_eyes is None else args.no_eyes
    args.no_mirror = (not mirror) if args.no_mirror is None else args.no_mirror
    args.headless = headless if args.headless is None else args.headless
    args.debug = debug if args.debug is None else args.debug
    args.max_frames = runtime.get("max_frames") if args.max_frames is None else args.max_frames
    if args.max_frames is not None:
        args.max_frames = int(args.max_frames)
    args.output_dir = str(output.get("screenshots_dir", DEFAULT_OUTPUT_DIR) if args.output_dir is None else args.output_dir)


def validate_args(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    try:
        validate_detection_settings(settings_from_args(args))
        validate_runtime_config(runtime_config_from_args(args, Path.cwd()))
    except ConfigError as exc:
        parser.error(str(exc))


def settings_from_args(args: argparse.Namespace) -> DetectionSettings:
    settings = DetectionSettings(
        scale_factor=args.scale_factor,
        min_neighbors=args.min_neighbors,
        min_face_size=(args.min_face_size, args.min_face_size),
        detect_eyes=not args.no_eyes,
        mirror=not args.no_mirror,
    )
    validate_detection_settings(settings)
    return settings


def runtime_config_from_args(args: argparse.Namespace, project_dir: Path) -> RuntimeConfig:
    source = args.source if args.source else args.camera
    config = RuntimeConfig(
        source=source,
        width=args.width,
        height=args.height,
        output_dir=(project_dir / args.output_dir).resolve(),
        headless=args.headless,
        max_frames=args.max_frames,
        debug=args.debug,
    )
    validate_runtime_config(config)
    return config


def main(argv: Optional[Sequence[str]] = None) -> int:
    try:
        args = parse_arguments(argv)
        project_dir = Path(__file__).resolve().parents[2]
        cascade_dir = default_cascade_dir()
        settings = settings_from_args(args)
        runtime_config = runtime_config_from_args(args, project_dir)
        detector = HaarCascadeDetector(
            face_cascade_path=cascade_dir / "haarcascade_frontalface_default.xml",
            eye_cascade_path=cascade_dir / "haarcascade_eye.xml",
        )
        if runtime_config.debug:
            print(f"source={runtime_config.source!r} output_dir={runtime_config.output_dir}")
        capture = open_capture(runtime_config)
        run_tracker(detector, capture, settings, runtime_config)
        return 0
    except (FaceVisionError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
