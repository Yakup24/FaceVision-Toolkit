# Privacy

FaceVision Toolkit detects faces and eyes locally. Even without identity recognition, camera frames and screenshots can contain personal data.

## Local processing

Frames are processed on the local machine with OpenCV. The project does not upload frames, screenshots, videos or detection output.

## Screenshots

The `s` key saves screenshots to the configured output directory. Screenshots may contain faces, rooms, screens or other private context.

## Repository rules

Do not commit:

- real face photos
- private screenshots
- camera recordings
- logs containing sensitive locations or personal context
- credentials or local environment files

## Consent

Use the app only in environments where people are informed and authorized.

## Security warning

This project is not an authentication system, surveillance product or identity verification tool. It has no liveness detection, access policy, identity model or risk assessment.
