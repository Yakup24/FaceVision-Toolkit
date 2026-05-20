from scripts.validate_project import run_checks


def test_project_validation_passes():
    assert run_checks() == []
