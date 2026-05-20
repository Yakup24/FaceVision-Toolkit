# Camera Setup

FaceVision Toolkit uses OpenCV `VideoCapture`, so camera behavior depends on the OS, camera driver and OpenCV backend.

## USB webcams

Most USB webcams use camera index `0` when no other camera is active:

```sh
python main.py --camera 0
```

If another device owns index `0`, try `1`.

## Video files

Use `--source` for local video files:

```sh
python main.py --source ./path/to/video.mp4
```

Do not commit private camera recordings to the repository.

## Camera unavailable checks

If the app reports that the source cannot be opened:

- confirm the camera is connected
- check OS camera permissions
- close other apps using the camera
- verify the camera index
- test a video file to isolate camera hardware issues

## Lighting and placement

Haar Cascade detection works best with front-facing, well-lit faces. Strong backlight, motion blur and extreme angles reduce reliability.
