import pytest

from facevision_toolkit.cli import parse_arguments, runtime_config_from_args, settings_from_args


def test_parse_default_arguments():
    args = parse_arguments([])

    assert args.camera == 0
    assert args.source is None
    assert args.width == 1280
    assert args.height == 720
    assert args.no_eyes is False
    assert args.no_mirror is False


def test_parse_video_source_and_headless_mode(tmp_path):
    args = parse_arguments(["--source", "demo.mp4", "--headless", "--max-frames", "3"])
    runtime = runtime_config_from_args(args, tmp_path)

    assert runtime.source == "demo.mp4"
    assert runtime.headless is True
    assert runtime.max_frames == 3


def test_parse_config_file_defaults(tmp_path):
    config_path = tmp_path / "config.json"
    config_path.write_text(
        """
        {
          "camera": {"source": 1, "width": 640, "height": 480},
          "detector": {"enable_eye_detection": false, "min_neighbors": 4},
          "runtime": {"mirror": false, "headless": true, "max_frames": 5},
          "output": {"screenshots_dir": "captures"}
        }
        """,
        encoding="utf-8",
    )

    args = parse_arguments(["--config", str(config_path)])
    runtime = runtime_config_from_args(args, tmp_path)
    settings = settings_from_args(args)

    assert args.camera == 1
    assert runtime.width == 640
    assert runtime.height == 480
    assert runtime.headless is True
    assert runtime.max_frames == 5
    assert runtime.output_dir == tmp_path / "captures"
    assert settings.detect_eyes is False
    assert settings.mirror is False
    assert settings.min_neighbors == 4


def test_settings_from_args_disables_eyes_and_mirror():
    args = parse_arguments(["--no-eyes", "--no-mirror", "--min-face-size", "80"])
    settings = settings_from_args(args)

    assert settings.detect_eyes is False
    assert settings.mirror is False
    assert settings.min_face_size == (80, 80)


@pytest.mark.parametrize(
    "argv",
    [
        ["--scale-factor", "1.0"],
        ["--min-neighbors", "0"],
        ["--width", "0"],
        ["--height", "-1"],
        ["--max-frames", "0"],
    ],
)
def test_invalid_arguments_exit_cleanly(argv):
    with pytest.raises(SystemExit):
        parse_arguments(argv)
