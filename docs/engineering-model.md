# Engineering Model

This document describes how FaceVision Toolkit is structured as a maintainable local computer vision tool rather than a one-file OpenCV demo.

## System boundary

FaceVision Toolkit owns the local runtime pipeline:

```text
video source -> frame capture -> preprocessing -> detector backend -> overlay -> runtime controls -> optional screenshot
```

It does not own identity recognition, access control, cloud processing, storage policy outside the local filesystem, or camera driver behavior.

## Runtime contracts

- `RuntimeConfig` owns source selection, resolution, output path, headless mode and frame limit.
- `DetectionSettings` owns cascade tuning and runtime toggles.
- `Detector` is the backend boundary; new detectors should implement `detect(frame, settings)`.
- `run_tracker` owns resource cleanup and returns the number of processed frames.
- `open_capture` is the only place that opens OpenCV `VideoCapture`.

These contracts keep camera access, detection logic, rendering and CLI parsing separate enough to test without real hardware.

## Failure model

Expected failures should exit with clear messages:

- missing config file -> `ConfigError`
- invalid detection settings -> CLI parser error
- missing video path -> `InvalidVideoSourceError`
- unavailable camera or unreadable source -> `CameraOpenError`
- missing or invalid cascade XML -> `CascadeLoadError`
- screenshot write failure -> `ScreenshotSaveError`
- missing OpenCV installation -> runtime error from `require_cv2`

Unexpected failures are not hidden by fake success output. The tool should fail fast enough for CI and local debugging to reveal the issue.

## Extension points

- Detector backend: add a new implementation under `src/facevision_toolkit/detectors/`.
- Runtime output: extend `overlay.py` or add structured event logging behind a small output boundary.
- Configuration: extend `RuntimeConfig` and `DetectionSettings`, then update CLI, config example and tests together.
- Benchmarking: add new benchmark modes only when they report locally measured data.

## Operational posture

The project is designed for local execution, SSH/headless smoke tests and CI without camera access. It avoids claiming fixed FPS, accuracy or model quality because those depend on hardware, lighting, camera backend and source media.

## Change policy

Behavior changes should update:

- tests for deterministic logic
- `README.md` or `docs/usage.md` for user-facing commands
- `docs/privacy.md` when screenshot, media or logging behavior changes
- `docs/quality-gates.md` when CI expectations change
- `CHANGELOG.md` for release-visible changes
