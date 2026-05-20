# CI Quality Gates

The GitHub Actions workflow runs:

1. checkout
2. Python 3.11 setup
3. system dependency install for OpenCV wheels
4. package install
5. `ruff check .`
6. `pytest -q`

The test suite is camera-independent. Failures in lint or tests should block merge.
