"""Repository hygiene checks for FaceVision Toolkit.

The checks are intentionally lightweight so they can run in CI without camera
hardware, OpenCV windows or private test media.
"""

from __future__ import annotations

from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    "README.md",
    "LICENSE",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "pyproject.toml",
    ".github/workflows/ci.yml",
    ".github/dependabot.yml",
    "config/config.example.yaml",
    "docs/architecture.md",
    "docs/engineering-model.md",
    "docs/quality-gates.md",
    "docs/privacy.md",
    "examples/sample-console-output.txt",
    "src/facevision_toolkit/cli.py",
    "tests/test_cli.py",
]

FORBIDDEN_TRACKED_PREFIXES = (
    "facevision-tracker/",
    "__pycache__/",
    ".pytest_cache/",
    ".ruff_cache/",
)

FORBIDDEN_TRACKED_PARTS = (
    "/__pycache__/",
    "/.pytest_cache/",
    "/.ruff_cache/",
    ".egg-info/",
)

FORBIDDEN_MEDIA_EXTENSIONS = {
    ".avi",
    ".jpeg",
    ".jpg",
    ".mkv",
    ".mov",
    ".mp4",
    ".png",
}

MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]+\]\(([^)]+)\)")


def tracked_files() -> list[str]:
    """Return files tracked by Git, or a filesystem fallback outside Git."""
    try:
        result = subprocess.run(
            ["git", "ls-files"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return [
            path.relative_to(ROOT).as_posix()
            for path in ROOT.rglob("*")
            if path.is_file() and ".git" not in path.parts
        ]

    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def validate_required_paths(errors: list[str]) -> None:
    for relative_path in REQUIRED_PATHS:
        if not (ROOT / relative_path).exists():
            errors.append(f"required path is missing: {relative_path}")


def validate_tracked_files(errors: list[str]) -> None:
    for relative_path in tracked_files():
        normalized = relative_path.replace("\\", "/")
        path = Path(normalized)

        if normalized.startswith(FORBIDDEN_TRACKED_PREFIXES):
            errors.append(f"legacy or generated path is tracked: {relative_path}")

        if any(part in normalized for part in FORBIDDEN_TRACKED_PARTS):
            errors.append(f"generated artifact is tracked: {relative_path}")

        if path.suffix.lower() in FORBIDDEN_MEDIA_EXTENSIONS:
            errors.append(f"media file must not be committed: {relative_path}")


def iter_markdown_files() -> list[Path]:
    tracked = [ROOT / item for item in tracked_files()]
    return [path for path in tracked if path.suffix.lower() == ".md" and path.exists()]


def local_markdown_target(markdown_file: Path, raw_target: str) -> Path | None:
    target = raw_target.strip().strip("<>")
    if not target or target.startswith(("#", "http://", "https://", "mailto:")):
        return None

    path_part = target.split("#", 1)[0].strip()
    if not path_part:
        return None

    return (markdown_file.parent / path_part).resolve()


def validate_markdown_links(errors: list[str]) -> None:
    for markdown_file in iter_markdown_files():
        text = markdown_file.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK_RE.finditer(text):
            target = local_markdown_target(markdown_file, match.group(1))
            if target is None:
                continue
            try:
                target.relative_to(ROOT)
            except ValueError:
                errors.append(f"markdown link escapes repository: {markdown_file}: {match.group(1)}")
                continue
            if not target.exists():
                relative_markdown = markdown_file.relative_to(ROOT).as_posix()
                errors.append(f"broken markdown link in {relative_markdown}: {match.group(1)}")


def run_checks() -> list[str]:
    errors: list[str] = []
    validate_required_paths(errors)
    validate_tracked_files(errors)
    validate_markdown_links(errors)
    return errors


def main() -> int:
    errors = run_checks()
    if errors:
        print("Repository validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
