# Design Decisions

## Why Python?

Python keeps OpenCV experiments readable and fast to iterate on. It is also accessible for portfolio review and local scripting.

## Why OpenCV?

OpenCV provides camera capture, Haar Cascade detection, image operations and drawing utilities in a single mature toolkit.

## Why Haar Cascades?

Haar Cascades are lightweight, local and easy to understand. They are not the most accurate modern detector, but they are appropriate for a compact real-time demo.

## Why local-first?

Local processing avoids unnecessary camera-frame upload and keeps privacy boundaries easier to inspect.

## Why headless mode?

GUI loops are hard to run in SSH, CI and service contexts. Headless mode makes the app more operationally realistic and easier to smoke test.

## Alternatives

- OpenCV DNN detector: likely better accuracy, more setup and heavier runtime.
- MediaPipe: strong real-time face pipeline, additional dependency and different runtime model.
- Cloud vision API: simpler remote inference, higher privacy and network dependency risk.
- Full desktop UI: richer controls, more maintenance overhead.

## Trade-offs

- Haar Cascade is simple but sensitive to lighting and angle.
- Local processing improves privacy but still requires responsible screenshot handling.
- Headless mode helps operations but does not replace visual QA.
