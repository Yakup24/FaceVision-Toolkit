import pytest

from facevision_tracker.camera import validate_video_source


def test_invalid_video_path_returns_clear_error(tmp_path):
    missing = tmp_path / "missing-video.mp4"

    with pytest.raises(RuntimeError, match="Video source does not exist"):
        validate_video_source(str(missing))


def test_existing_video_path_is_accepted(tmp_path):
    video = tmp_path / "demo.mp4"
    video.write_text("placeholder", encoding="utf-8")

    validate_video_source(str(video))


def test_integer_camera_source_does_not_require_path():
    validate_video_source(0)
