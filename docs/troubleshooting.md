# Troubleshooting

## Webcam does not open

Check the camera index, operating system permissions and whether another application is using the camera.

## External camera is not visible

Try `--camera 1` or `--camera 2` and confirm the device appears in the operating system.

## Video file is not read

Confirm the file exists and the codec is supported by your OpenCV installation.

## Haar cascade file is missing

Confirm the `cascades/` directory contains both XML files.

## OpenCV import error

Run `python -m pip install -r requirements.txt`.

## FPS is too low

Lower the resolution, disable eye detection or test on a shorter video source.

## Display window does not open

Use `--headless` in SSH, CI or environments without a desktop display.

## Screenshot is not saved

Check output directory permissions and available disk space.
