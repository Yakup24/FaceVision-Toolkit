# Deployment

FaceVision Tracker is primarily a local CLI tool.

## Local

```sh
python -m pip install -e .
facevision-tracker --camera 0
```

## Headless

```sh
facevision-tracker --camera 0 --headless
```

## systemd

Use `examples/systemd/facevision-tracker.service` as a starting point. Adjust user, working directory and virtual environment path before installing.
