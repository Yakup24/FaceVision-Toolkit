# Detection Pipeline

## 1. Capture

`facevision_toolkit.camera.open_capture` opens a camera index or local video file through OpenCV `VideoCapture`.

## 2. Preprocessing

`facevision_toolkit.processing.preprocess_frame` converts each frame to grayscale and applies histogram equalization.

## 3. Face detection

The Haar backend runs the face cascade over the preprocessed frame.

## 4. Eye detection

If enabled, eye detection runs only inside each detected face ROI. This reduces the search area and keeps eye detection scoped to likely face regions.

## 5. Rendering

`facevision_toolkit.overlay.draw_detections` draws face boxes, eye boxes and runtime status text.

## 6. Runtime controls

`facevision_toolkit.runtime.handle_key` owns screenshot, eye-toggle, mirror-toggle and exit keys.
