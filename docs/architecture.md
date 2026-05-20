# Architecture

FaceVision Toolkit is a local OpenCV application with a small, testable runtime loop.

## High-level flow

```text
Camera / Video Source
  -> Frame Capture
  -> Grayscale Conversion
  -> Histogram Equalization
  -> Face Cascade Detection
  -> Optional Eye Cascade Detection
  -> Overlay Renderer
  -> GUI Window or Headless Console Output
  -> Optional Screenshot Output
```

## Components

- `DetectionSettings`: cascade tuning and runtime toggles.
- `RuntimeConfig`: source, output directory, resolution, headless mode and frame limit.
- `FaceEyeDetector`: loads Haar Cascade XML files and detects faces/eyes.
- `FPSCounter`: computes simple per-frame FPS.
- `draw_detections`: draws boxes and text overlays.
- `handle_key`: handles screenshot, toggle and exit keys.
- `run_tracker`: owns the capture loop and cleanup.

## Input sources

The app supports:

- camera index through `--camera`
- video file path through `--source`

OpenCV `VideoCapture` is responsible for backend-specific behavior.

## Error handling

Expected errors are surfaced clearly:

- OpenCV missing
- cascade XML missing
- cascade classifier failed to load
- camera/video source unavailable
- screenshot write failure
- invalid CLI arguments

## Logging approach

The app currently writes human-readable status lines to stdout and errors to stderr. Structured event logging is planned but not implemented.
