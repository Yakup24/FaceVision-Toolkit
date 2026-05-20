# Benchmarks

FaceVision Toolkit does not ship fixed FPS claims. Benchmark results depend on CPU, camera backend, video resolution, lighting, detector settings and whether eye detection is enabled.

Run a local benchmark:

```sh
python benchmarks/benchmark_video_source.py --source 0 --frames 300 --width 640 --height 480
```

Run against a local video file:

```sh
python benchmarks/benchmark_video_source.py --source ./examples/demo-video-placeholder.mp4 --frames 300
```

Do not publish benchmark numbers without the hardware model, OS, Python version, OpenCV version, input resolution and detector settings.
