# System Overview

FaceVision Tracker is now organized as a small local computer vision toolkit.

```text
Video Source
  -> Frame Capture
  -> Preprocessing
  -> Face Detection
  -> Eye Detection
  -> Overlay Rendering
  -> Keyboard Handler
  -> Screenshot Output
```

The CLI builds runtime configuration, the camera module owns `VideoCapture`, the detector backend owns Haar Cascade calls and the runtime module owns the frame loop.

No cloud processing or remote upload is part of the default architecture.
