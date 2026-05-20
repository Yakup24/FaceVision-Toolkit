# Component Boundaries

- `cli.py`: argument parsing, optional config loading and application wiring.
- `config.py`: dataclasses and validation rules.
- `camera.py`: source validation and `VideoCapture` setup.
- `cascades.py`: Haar cascade path and load checks.
- `processing.py`: frame transformations.
- `detectors/`: detector backend contract and Haar implementation.
- `overlay.py`: drawing and detection summaries.
- `screenshot.py`: screenshot path generation and writes.
- `runtime.py`: main loop and keyboard state changes.
- `errors.py`: project-specific exception types.

These boundaries make it possible to test most behavior without a real webcam.
