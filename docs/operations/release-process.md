# Release Process

1. Update `CHANGELOG.md`.
2. Confirm version in `pyproject.toml` and `src/facevision_tracker/__init__.py`.
3. Run `python -m pytest -q`.
4. Run `python -m ruff check .`.
5. Create a GitHub release tag.
6. Include notes about limitations and any privacy-impacting changes.
