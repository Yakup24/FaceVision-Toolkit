# Camera Flow

## 1. Default camera index

The default source is camera index `0`.

```sh
python main.py --camera 0
```

## 2. External camera selection

External webcams commonly appear as index `1` or higher.

```sh
python main.py --camera 1
```

## 3. Video file input

Use `--source` for a local video file.

```sh
python main.py --source ./local-demo-video.mp4
```

## 4. Width and height

Width and height are applied to integer camera sources through OpenCV capture properties.

## 5. Camera open failure

`open_capture` raises `CameraOpenError` when `VideoCapture` cannot open the source.

## 6. Frame read failure

If a frame cannot be read, the runtime loop prints a message and exits cleanly.

## 7. Resource cleanup

`run_tracker` releases the capture object in a `finally` block.

## 8. Window cleanup

For GUI mode, `cv2.destroyAllWindows` is called after the loop exits.
