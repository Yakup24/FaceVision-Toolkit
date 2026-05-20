# Contributing

## Local Setup

```sh
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m ruff check .
```

## Branch Naming

- `feature/headless-video-mode`
- `fix/camera-open-error`
- `docs/update-privacy-notes`
- `test/add-cli-validation`
- `chore/update-release-notes`

## Commit Style

- `feat: add detector backend option`
- `fix: handle missing cascade file`
- `docs: update camera setup`
- `test: add runtime helper tests`
- `chore: update ci`

## Pull Request Checklist

- Tests pass locally.
- No real face photos or screenshots are included.
- No private videos or secrets are committed.
- README/docs are updated when behavior changes.
- Camera-dependent behavior is mocked or documented.
- Privacy impact is considered for screenshots, videos and logs.
