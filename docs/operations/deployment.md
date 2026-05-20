# Deployment

FaceVision Toolkit is primarily a local CLI tool.

## Local

```sh
python -m pip install -e .
facevision-toolkit --camera 0
```

## Headless

```sh
facevision-toolkit --camera 0 --headless
```

## systemd

Use `examples/systemd/facevision-toolkit.service` as a starting point. Adjust user, working directory and virtual environment path before installing.
