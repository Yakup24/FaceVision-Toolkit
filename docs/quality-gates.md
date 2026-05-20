# Quality Gates

FaceVision Toolkit uses lightweight gates that work without a webcam or private media.

## Automated checks

Run these before merging:

```sh
python scripts/validate_project.py
python -m ruff check .
python -m pytest -q
```

The repository validation script checks required portfolio files, local Markdown links, tracked generated artifacts and tracked media files.

## CI policy

CI runs on pushes and pull requests to `main`.

Required gates:

- install the package in editable mode
- validate repository hygiene
- lint with ruff
- run pytest

CI must not require a physical camera, real faces, private screenshots or local video files.

## Manual checks

For camera-related changes, validate locally with a real camera or local non-private video:

```sh
python main.py --camera 0
python main.py --headless --max-frames 100
python benchmarks/benchmark_video_source.py --source 0 --frames 300
```

Do not commit the video source, screenshots or benchmark result as proof. Mention the local environment in the pull request instead.

## Review checklist

- Does the change preserve local-only processing?
- Are camera failures and missing files handled clearly?
- Do tests avoid real webcam access?
- Are docs updated for new commands, config or output behavior?
- Is any screenshot, video or media artifact excluded from Git?
- Are performance claims limited to locally measured, user-run commands?
