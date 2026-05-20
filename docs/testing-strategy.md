# Testing Strategy

Tests should validate deterministic behavior without requiring a real camera or real face images.

## Goals

- CLI argument parsing and validation
- Camera unavailable behavior
- Cascade file loading errors
- Runtime toggle behavior
- Screenshot failure handling
- Detection summary formatting

## Test types

- Unit tests for argument parsing
- Unit tests for runtime helper functions
- Mock-based tests for OpenCV capture behavior
- File-existence tests for bundled cascade files

## Not tested in CI

- Real webcam access
- Private video files
- Real face images
- FPS claims
- Detection accuracy claims

## Mocking strategy

Tests monkeypatch the module-level `cv2` object with lightweight fake objects. This lets CI run without camera hardware and without opening GUI windows.
