"""Runtime configuration and optional config-file loading."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Mapping, Optional, Union

from .errors import ConfigError


CameraSource = Union[int, str]


@dataclass
class DetectionSettings:
    scale_factor: float = 1.2
    min_neighbors: int = 6
    min_face_size: tuple[int, int] = (60, 60)
    detect_eyes: bool = True
    mirror: bool = True


@dataclass(frozen=True)
class RuntimeConfig:
    source: CameraSource
    width: int
    height: int
    output_dir: Path
    headless: bool = False
    max_frames: Optional[int] = None
    debug: bool = False


DEFAULT_CAMERA = 0
DEFAULT_WIDTH = 1280
DEFAULT_HEIGHT = 720
DEFAULT_OUTPUT_DIR = "output"
DEFAULT_SCALE_FACTOR = 1.2
DEFAULT_MIN_NEIGHBORS = 6
DEFAULT_MIN_FACE_SIZE = 60


def load_config_file(path: Optional[str]) -> Mapping[str, Any]:
    if not path:
        return {}
    config_path = Path(path).expanduser()
    if not config_path.exists():
        raise ConfigError(f"Config file not found: {config_path}")
    try:
        with config_path.open("r", encoding="utf-8") as handle:
            if config_path.suffix.lower() in {".yaml", ".yml"}:
                try:
                    import yaml  # type: ignore[import-not-found]
                except ImportError as exc:
                    raise ConfigError("YAML config requires PyYAML.") from exc
                data = yaml.safe_load(handle) or {}
            else:
                data = json.load(handle)
    except OSError as exc:
        raise ConfigError(f"Could not read config file: {config_path}") from exc
    if not isinstance(data, Mapping):
        raise ConfigError("Config file must contain an object at the top level.")
    return data


def section(config: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    value = config.get(key, {})
    if value is None:
        return {}
    if not isinstance(value, Mapping):
        raise ConfigError(f"Config section '{key}' must be an object.")
    return value


def config_bool(value: Any, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"1", "true", "yes", "on"}:
            return True
        if lowered in {"0", "false", "no", "off"}:
            return False
    raise ConfigError(f"Expected boolean value, got: {value!r}")


def coerce_source(value: Any) -> CameraSource:
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if stripped.lstrip("-").isdigit():
            return int(stripped)
        if stripped:
            return stripped
    raise ConfigError("Camera source must be an integer camera index or a video file path.")


def validate_runtime_config(config: RuntimeConfig) -> None:
    if config.width < 1 or config.height < 1:
        raise ConfigError("Camera width and height must be positive.")
    if config.max_frames is not None and config.max_frames < 1:
        raise ConfigError("max_frames must be positive.")


def validate_detection_settings(settings: DetectionSettings) -> None:
    if settings.scale_factor <= 1.0:
        raise ConfigError("scale_factor must be greater than 1.0.")
    if settings.min_neighbors < 1:
        raise ConfigError("min_neighbors must be at least 1.")
    if settings.min_face_size[0] < 1 or settings.min_face_size[1] < 1:
        raise ConfigError("min_face_size must be positive.")
