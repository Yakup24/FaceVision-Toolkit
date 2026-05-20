# ADR-002: Start With Haar Cascade Detection

## Status

Accepted

## Context

The current project is a lightweight face/eye detection tool, not a recognition system or deep learning benchmark.

## Decision

Use OpenCV Haar Cascade classifiers as the initial detector backend.

## Consequences

Haar Cascades are simple and fast, but they are less robust than modern DNN, MediaPipe or YOLO-based approaches in difficult lighting, pose and occlusion scenarios.
