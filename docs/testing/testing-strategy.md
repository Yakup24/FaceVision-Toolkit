# Testing Strategy

## Goals

- CLI argument validation
- Config defaults and overrides
- Cascade loading failures
- Camera unavailable behavior
- Video source path validation
- Screenshot path and failure handling
- Frame preprocessing behavior
- Runtime state toggles

## CI Boundaries

CI should not access a real webcam, real face images, private videos or hardware-specific FPS checks.

## Mocking

Tests monkeypatch the OpenCV dependency boundary in `facevision_toolkit.cv`. This keeps camera and GUI behavior out of CI.
