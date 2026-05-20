# Changelog

All notable changes to this project will be documented in this file.

## [1.1.0] - Unreleased

### Added

- Added root-level project structure for GitHub readability.
- Added headless mode and `--max-frames` for repeatable non-GUI runs.
- Added CLI argument validation for detection and runtime parameters.
- Added pytest tests for CLI parsing, camera failure behavior, cascade loading and runtime helpers.
- Added architecture, privacy, testing, usage and design documentation.
- Added examples for commands, service usage, console output and expected camera errors.
- Added GitHub Actions CI with pytest and ruff.

### Changed

- Reworked README into a technical portfolio-quality project overview.
- Replaced boilerplate security notes with project-specific privacy and data handling guidance.
- Improved screenshot error handling.

## [1.0.0] - Initial Public Release

### Added

- Real-time face detection with OpenCV Haar Cascade.
- Eye detection inside face regions.
- FPS, detection count and screenshot features.
- CLI arguments for camera/video source, resolution and detection settings.
