# OpenCV Pipeline

## 1. Haar Cascade

Haar Cascades are lightweight classical object detectors available through OpenCV.

## 2. Face cascade

The face cascade runs on the preprocessed grayscale frame and returns bounding boxes for likely face regions.

## 3. Eye cascade inside face ROI

Eye detection runs only inside face regions. This reduces false search area and keeps the pipeline faster than scanning the full frame for eyes.

## 4. Grayscale conversion

Cascade classifiers operate on grayscale images, so each frame is converted before detection.

## 5. Histogram equalization

Histogram equalization improves contrast in the grayscale frame and can help detection under uneven lighting.

## 6. FPS calculation

`FPSCounter` measures time between frames and reports a simple instantaneous FPS estimate.

## 7. Detection parameters

- `scale_factor` controls image pyramid scaling.
- `min_neighbors` controls detection grouping strictness.
- `min_face_size` filters small detections.

## 8. Limitations

Haar Cascades are fast and understandable, but less robust than modern deep learning detectors for difficult pose, lighting and occlusion.
