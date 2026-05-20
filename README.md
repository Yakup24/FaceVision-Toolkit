# FaceVision Tracker

[![CI](https://github.com/Yakup24/facevision-tracker/actions/workflows/ci.yml/badge.svg)](https://github.com/Yakup24/facevision-tracker/actions/workflows/ci.yml)

FaceVision Tracker is a local OpenCV application for real-time face and eye detection from a webcam or video source. It uses Haar Cascade classifiers, overlays detection boxes and runtime metrics, supports screenshots, and can run in GUI or headless mode for repeatable testing.

## Overview

This project demonstrates a practical local computer vision workflow rather than a single throwaway webcam script. The application opens a camera or video file, detects faces, optionally detects eyes inside each face region, draws overlays, reports FPS, and lets the operator toggle runtime behavior from the keyboard.

It does not perform face recognition, identity matching, biometric authentication, cloud upload, or persistent person tracking. Those are listed as limitations or roadmap items when relevant.

## Problem

Small OpenCV demos often hide operational concerns:

- Camera/video sources may be unavailable or permission-limited.
- Detection parameters need repeatable CLI controls.
- GUI-only loops are hard to test in CI.
- Screenshots can contain personal data.
- Cascade files and runtime output need clear project boundaries.
- Claims about accuracy or FPS should not be made without hardware-specific measurements.

## Solution

FaceVision Tracker keeps the workflow local and explicit:

- Webcam and video-file input through OpenCV `VideoCapture`
- Face detection with `haarcascade_frontalface_default.xml`
- Optional eye detection with `haarcascade_eye.xml`
- Runtime overlays for face count, eye count, FPS and mode state
- Keyboard controls for screenshot, eye detection and mirror mode
- Headless mode and `--max-frames` for non-GUI execution
- Camera-independent pytest coverage with mocked OpenCV objects

## Architecture

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

Core responsibilities:

- `DetectionSettings`: runtime detection and display toggles
- `RuntimeConfig`: source, resolution, output directory and headless options
- `FaceEyeDetector`: cascade loading and face/eye detection
- `FPSCounter`: frame timing
- `draw_detections`: visual overlay and summary generation
- `run_tracker`: main capture loop

## Design Philosophy

FaceVision Tracker is designed around four principles:

1. Local-first processing
   Frames are processed on the machine running the app.

2. Operational clarity
   Camera source, resolution and detection parameters are controlled through CLI flags.

3. Testable vision loop
   Runtime helpers are structured so behavior can be tested without real cameras or real face images.

4. Privacy-aware usage
   Screenshots and video sources may contain personal data and should not be committed.

## Core Features

- Real-time face detection
- Eye detection inside face regions
- Webcam or video-file input
- FPS, face count and eye count overlay
- Screenshot capture to a local output directory
- Runtime keyboard controls
- Mirror mode
- Headless mode for non-GUI runs
- CLI argument validation
- Camera-independent pytest test suite
- GitHub Actions CI with pytest and ruff

## Tech Stack

- Python 3.10+
- OpenCV
- NumPy
- pytest
- ruff
- GitHub Actions

## Project Structure

```text
cascades/                   Haar Cascade XML files used by OpenCV
docs/                       Architecture, usage, testing, privacy and design notes
examples/                   Placeholder commands, output and service examples
tests/                      Unit tests with mocked OpenCV/camera behavior
main.py                     Application entry point and runtime loop
requirements.txt            Runtime and development dependencies
pyproject.toml              Project metadata, script entry point and pytest config
SECURITY.md                 Data and responsible-use policy
CONTRIBUTING.md             Contribution workflow
CHANGELOG.md                Project history
LICENSE                     GPLv3 license
```

## Getting Started

Clone the repository:

```sh
git clone https://github.com/Yakup24/facevision-tracker.git
cd facevision-tracker
```

Create and activate a virtual environment:

```sh
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```sh
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Run the app:

```sh
python main.py
```

Or install the local console script:

```sh
python -m pip install -e .
facevision-tracker --help
```

## Usage

Run with the default camera:

```sh
python main.py --camera 0
```

Choose camera resolution:

```sh
python main.py --camera 0 --width 1280 --height 720
```

Use a video file:

```sh
python main.py --source ./examples/demo-video-placeholder.mp4
```

Disable eye detection on startup:

```sh
python main.py --no-eyes
```

Run without a GUI window:

```sh
python main.py --headless --max-frames 100
```

Tune detection parameters:

```sh
python main.py --scale-factor 1.2 --min-neighbors 6 --min-face-size 60
```

## Keyboard Controls

| Key | Action |
| --- | --- |
| `q` or `ESC` | Exit |
| `s` | Save screenshot |
| `e` | Toggle eye detection |
| `m` | Toggle mirror mode |

## Testing

Run the camera-independent test suite:

```sh
python -m pytest -q
```

Current tests cover:

- CLI parsing and invalid argument handling
- Runtime config creation
- Camera unavailable behavior with fake capture objects
- Cascade file loading errors
- Detection summary counting
- Keyboard toggle behavior
- Screenshot write failure handling

CI does not use a real camera, real face photos, real videos or hardware-specific FPS assertions.

## Privacy and Safety

- Frames are processed locally.
- The project does not upload images, videos or detections to a remote service.
- Screenshots can contain faces or private environments and should stay out of Git.
- Example files use placeholders only.
- This project is a face/eye detection demo and local vision utility, not an identity verification or security authentication system.

## Limitations

- Haar Cascade detection is sensitive to lighting, angle and blur.
- Eye detection can produce false positives in low-quality frames.
- FPS depends on camera, resolution, CPU and OpenCV backend.
- The app does not identify people.
- The app does not implement persistent multi-object tracking IDs.
- The app does not provide liveness detection or security-grade verification.

## Roadmap

- Optional YAML/JSON config file
- Structured event logging
- OpenCV DNN or MediaPipe detector backend
- Detection-zone metrics
- Real tracking IDs across frames
- Benchmark script with hardware metadata
- Docker/devcontainer setup for non-camera tests
- Optional local web dashboard

## My Contributions

This repository contains the local OpenCV face/eye detection loop, cascade loading checks, CLI controls, screenshot workflow, headless execution support, testable runtime helpers, privacy-aware documentation, examples and CI configuration.

## License

This project is licensed under GPLv3. The Haar Cascade XML files include their original OpenCV/Intel license notices.
