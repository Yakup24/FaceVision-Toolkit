# FaceVision Toolkit

[![CI](https://github.com/Yakup24/FaceVision-Toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/Yakup24/FaceVision-Toolkit/actions/workflows/ci.yml)

FaceVision Toolkit is a Python and OpenCV real-time face and eye detection toolkit. It reads frames from a webcam or video file, runs a Haar Cascade based detection pipeline, renders face/eye overlays, displays FPS and detection metrics, and can save local screenshots.

## Overview

FaceVision Toolkit is a local computer vision utility, not a face recognition system. It detects face and eye regions; it does not identify people, match identities, perform biometric authentication, upload frames, or make security decisions.

The project is useful for learning OpenCV pipelines, testing camera/video input handling, and demonstrating a clean real-time detection loop with CLI controls, tests, CI, docs and privacy-aware packaging.

## Problem

Simple webcam scripts often skip the engineering details that make a project maintainable:

- camera and video inputs fail in different ways
- detection settings need repeatable controls
- GUI loops are hard to test in CI
- cascade files need clear load errors
- screenshots can contain private data
- FPS or accuracy claims are misleading without hardware-specific measurement

## Solution

FaceVision Toolkit provides:

- OpenCV Haar Cascade face and eye detection
- webcam or video-file input
- runtime keyboard controls
- FPS and detection counters
- local screenshot output
- CLI parameters and optional JSON/YAML config
- controlled error types for camera, cascade, config and screenshot failures
- modular `src/facevision_toolkit` architecture
- camera-independent pytest suite and GitHub Actions CI
- local benchmark script that reports only measurements from the user's machine

## Architecture

```text
Video Source
  -> Frame Capture
  -> Preprocessing
  -> Face Detection
  -> Eye Detection
  -> Overlay Rendering
  -> Keyboard Handler
  -> Screenshot Output
```

Key modules:

- `facevision_toolkit.cli`: CLI parsing, config loading and application wiring
- `facevision_toolkit.camera`: `VideoCapture` opening and source validation
- `facevision_toolkit.cascades`: Haar cascade loading
- `facevision_toolkit.processing`: grayscale conversion, histogram equalization and mirror transform
- `facevision_toolkit.detectors`: detector backend boundary and Haar implementation
- `facevision_toolkit.overlay`: overlay drawing and detection summaries
- `facevision_toolkit.screenshot`: screenshot naming and write handling
- `facevision_toolkit.runtime`: frame loop and keyboard controls
- `facevision_toolkit.errors`: project-specific exceptions

## Design Philosophy

FaceVision Toolkit is designed around four principles:

1. Simple real-time vision pipeline
   The project keeps the detection flow understandable: capture frame, preprocess, detect faces, detect eyes and render overlays.

2. Runtime usability
   Keyboard shortcuts, FPS display, screenshot output and CLI arguments make the tool usable beyond a minimal demo script.

3. Local processing
   Camera frames are processed locally. The project does not require cloud processing or remote upload.

4. Honest limitations
   Haar Cascade detection is lightweight and fast, but it is not as robust as modern deep learning-based detectors in difficult lighting, pose or occlusion scenarios.

## Core Features

- Real-time face detection
- Eye detection inside face ROI
- FPS display
- Face and eye counter
- Screenshot saving
- Webcam input
- Video file input
- Camera index selection
- Width/height configuration
- Mirror mode toggle
- Eye detection toggle
- Keyboard shortcuts
- Headless mode
- Optional config file
- Basic benchmark script
- Camera-independent tests
- GitHub Actions CI

## Tech Stack

- Python 3.10+
- OpenCV
- NumPy
- PyYAML
- Haar Cascade classifiers
- pytest
- ruff
- GitHub Actions

## Project Structure

```text
.github/                     CI workflow, issue templates and PR template
benchmarks/                  Local benchmark runner and notes
cascades/                    Haar Cascade XML files
config/                      Example YAML config
docs/                        Single-level technical documentation
examples/                    Placeholder commands, output, errors and service file
src/facevision_toolkit/      Modular application package
tests/                       Camera-independent pytest suite
main.py                      Backward-compatible script entrypoint
pyproject.toml               Package metadata and console scripts
requirements.txt             Runtime dependencies for quick setup
requirements-dev.txt         Development dependency entrypoint
README.md                    Project overview
SECURITY.md                  Security and privacy policy
CONTRIBUTING.md              Contribution guide
CODE_OF_CONDUCT.md           Community expectations
CHANGELOG.md                 Release history
LICENSE                      MIT license
```

## Getting Started

```sh
git clone https://github.com/Yakup24/FaceVision-Toolkit.git
cd FaceVision-Toolkit
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
```

Install as an editable local package:

```sh
python -m pip install -e .
facevision-toolkit --help
```

The legacy `facevision-tracker` command is kept as an alias for compatibility.

## Usage

Default camera:

```sh
python main.py --camera 0
```

External camera:

```sh
python main.py --camera 1
```

Resolution:

```sh
python main.py --camera 0 --width 1280 --height 720
```

Video file:

```sh
python main.py --source ./examples/demo-video-placeholder.mp4
```

Eye detection disabled:

```sh
python main.py --no-eyes
```

Mirror mode disabled:

```sh
python main.py --no-mirror
```

Headless smoke run:

```sh
python main.py --headless --max-frames 100
```

Config file:

```sh
python main.py --config config/config.example.yaml
```

## CLI Reference

```text
--config PATH          Optional JSON/YAML config file
--camera INDEX         Camera index
--source PATH          Video file path instead of webcam
--width PIXELS         Camera frame width
--height PIXELS        Camera frame height
--scale-factor FLOAT   Haar cascade scale factor
--min-neighbors INT    Haar cascade minNeighbors value
--min-face-size INT    Minimum face width/height
--no-eyes              Start with eye detection disabled
--no-mirror            Start with mirror mode disabled
--output-dir PATH      Screenshot output directory
--headless             Run without opening a GUI window
--max-frames INT       Stop after N frames
--debug                Print extra runtime context
```

## Keyboard Shortcuts

| Key | Action |
| --- | --- |
| `q` or `ESC` | Quit |
| `s` | Save screenshot |
| `e` | Toggle eye detection |
| `m` | Toggle mirror mode |

## Output

Screenshots are saved to the configured output directory. By default:

```text
output/
  screenshot_YYYYMMDD_HHMMSS.png
```

The output directory is created when needed and ignored by Git because screenshots can contain personal data.

## Testing

```sh
python -m pytest -q
python -m ruff check .
```

Tests cover CLI parsing, config defaults, cascade loading, invalid video paths, camera-open errors, frame preprocessing, screenshot path generation, screenshot failure handling and runtime state toggles.

Tests do not use a real webcam, real face images or private videos.

## Benchmarking

Run a local benchmark:

```sh
python benchmarks/benchmark_video_source.py --source 0 --frames 300 --width 640 --height 480
```

No benchmark result is committed or claimed. Results depend on hardware, camera backend, source resolution, lighting and detector settings.

## Documentation

- [Architecture](docs/architecture.md)
- [OpenCV pipeline](docs/opencv-pipeline.md)
- [Camera flow](docs/camera-flow.md)
- [Usage](docs/usage.md)
- [Testing strategy](docs/testing-strategy.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Privacy](docs/privacy.md)
- [Roadmap](docs/roadmap.md)
- [Design decisions](docs/design-decisions.md)

## Security and Privacy

- Frames are processed locally.
- The project does not upload images, videos or detection output.
- Screenshots and local videos may contain personal data.
- Real face images, private videos and screenshots must not be committed.
- This project is not designed for identity verification, surveillance or security-grade authentication.

## Limitations

- Haar Cascade is not as robust as modern deep learning detectors.
- Low light, blur, occlusion and side profiles can reduce detection quality.
- Camera quality and OpenCV backend affect results.
- The project detects regions; it does not identify people.
- FPS depends on the local machine and should be measured locally.

## Roadmap

- DNN detector backend
- MediaPipe detector backend experiment
- Persistent tracking IDs across frames
- Detection metrics export
- Structured event logging
- Docker/devcontainer support
- Simple GUI mode
- Local API endpoint
- Release packaging workflow

## My Contributions

This project includes the OpenCV detection loop, modular detector pipeline, CLI options, FPS/detection counter overlay, screenshot handling, runtime keyboard controls, headless execution, config support, benchmark runner, pytest suite, CI workflow, README/docs packaging and privacy/security notes.

## License

This project is licensed under the MIT License. Haar Cascade XML files include their original OpenCV/Intel license notices.
