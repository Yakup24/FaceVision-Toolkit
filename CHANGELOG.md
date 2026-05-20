# Changelog

All notable changes to this project will be documented in this file.

## [0.3.0] - Planned

### Planned

- Detector backend selection for DNN or MediaPipe experiments.
- Structured detection metrics export.
- Optional local API endpoint.
- Release packaging workflow.

## [0.2.0] - Unreleased

### Added

- Added root-level project documentation.
- Added modular `src/facevision_toolkit` package structure.
- Added CLI, camera, cascade, processing, detector, overlay, screenshot, runtime and errors modules.
- Added optional JSON/YAML config file support.
- Added benchmark script for local FPS measurement without committed results.
- Added architecture, OpenCV pipeline, ADR, security, testing, operations and product documentation.
- Added sample console outputs, command examples and troubleshooting notes.
- Added CI workflow for camera-independent test execution.
- Added project-specific security, privacy, contribution and conduct notes.
- Added MIT license.

### Changed

- Improved README structure for technical review and portfolio presentation.
- Cleaned placeholder clone commands and setup instructions.
- Reworked `main.py` into a backward-compatible entrypoint over the package.

## [0.1.0] - Initial Public Release

### Added

- Initial OpenCV-based face and eye detection workflow.
- Webcam and video file input support.
- FPS and detection counter display.
- Screenshot saving and keyboard controls.
