# Troubleshooting

## Webcam does not open

Check camera index, OS permissions and whether another app is using the camera.

## External camera is missing

Try another index such as `--camera 1` and confirm the device appears in the OS.

## Video file does not read

Confirm the file path exists and OpenCV supports the codec.

## Haar cascade file missing

Confirm `cascades/haarcascade_frontalface_default.xml` and `cascades/haarcascade_eye.xml` exist.

## OpenCV import error

Run `python -m pip install -r requirements.txt`.

## FPS is low

Lower resolution, disable eye detection or test a shorter video source.

## Window does not open

Use `--headless` on SSH or environments without a GUI display.

## Screenshot is not saved

Check output directory permissions and available disk space.
