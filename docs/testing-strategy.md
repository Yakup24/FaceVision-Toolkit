# Testing Strategy

Tests should validate deterministic behavior without requiring a real camera or real face images.

## Goals

- CLI argument parsing and validation
- Camera unavailable behavior
- Cascade file loading errors
- Runtime toggle behavior
- Screenshot failure handling
- Detection summary formatting
- Repository hygiene and Markdown link integrity

## Test types

- Unit tests for argument parsing
- Unit tests for runtime helper functions
- Mock-based tests for OpenCV capture behavior
- File-existence tests for bundled cascade files
- Repository validation tests for portfolio-critical files and committed artifacts

## Not tested in CI

- Real webcam access
- Private video files
- Real face images
- FPS claims
- Detection accuracy claims

## Mocking strategy

Tests monkeypatch the module-level `cv2` object with lightweight fake objects. This lets CI run without camera hardware and without opening GUI windows.

## Quality gates

Before merging, run:

```sh
python scripts/validate_project.py
python -m ruff check .
python -m pytest -q
```

These gates intentionally avoid hardware-dependent checks. Real camera validation remains a manual local check.
