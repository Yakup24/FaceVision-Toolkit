# Usage

Run from the repository root.

## Default camera

```sh
python main.py --camera 0
```

## Video file

```sh
python main.py --source ./local-demo-video.mp4
```

The placeholder path shows the supported command shape. No real video file is committed.

## Resolution

```sh
python main.py --width 1280 --height 720
```

Resolution settings are applied to camera sources. Video files use their own encoded dimensions.

## Detection tuning

```sh
python main.py --scale-factor 1.2 --min-neighbors 6 --min-face-size 60
```

Higher `min-neighbors` can reduce false positives but may miss weak detections. `scale-factor` must be greater than `1.0`.

## Headless mode

```sh
python main.py --headless --max-frames 100
```

Headless mode is useful for SSH sessions, service-style runs and smoke testing. It prints frame-level counts instead of opening an OpenCV window.

## Keyboard controls

| Key | Action |
| --- | --- |
| `q` or `ESC` | Exit |
| `s` | Save screenshot |
| `e` | Toggle eye detection |
| `m` | Toggle mirror mode |
