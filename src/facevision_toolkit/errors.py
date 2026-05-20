"""Project-specific exceptions."""


class FaceVisionError(RuntimeError):
    """Base error for expected FaceVision failures."""


class CameraOpenError(FaceVisionError):
    """Raised when a camera or video source cannot be opened."""


class CascadeLoadError(FaceVisionError):
    """Raised when a Haar cascade cannot be loaded."""


class InvalidVideoSourceError(FaceVisionError):
    """Raised when a video source path is invalid."""


class ScreenshotSaveError(FaceVisionError):
    """Raised when a screenshot cannot be written."""


class ConfigError(FaceVisionError):
    """Raised when configuration cannot be parsed or validated."""
