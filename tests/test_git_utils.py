import pytest
from pytest_mock import MockerFixture

from synqit.git_utils import _trim, get_commits_since_main, get_staged_diff


def test_trim_short_text() -> None:
    text = "Short string"
    assert _trim(text, 100) == text


def test_trim_long_text() -> None:
    text = "Long string that needs to be truncated"
    trimmed = _trim(text, 10)
    assert len(trimmed) > 10
    assert "[... truncated ...]" in trimmed
    assert trimmed.startswith("Long strin")


def test_get_staged_diff_empty(mocker: MockerFixture) -> None:
    mock_repo = mocker.patch("synqit.git_utils.get_repo")
    mock_repo.return_value.git.diff.return_value = ""

    with pytest.raises(RuntimeError, match="No staged changes found"):
        get_staged_diff()


def test_get_commits_empty(mocker: MockerFixture) -> None:
    mock_repo = mocker.patch("synqit.git_utils.get_repo")
    # Simulate no branches to force fallback
    mock_repo.return_value.branches = []
    # Force git command to raise error or return empty log
    mock_repo.return_value.git.log.return_value = "  \n  "

    with pytest.raises(RuntimeError, match="No commits found"):
        get_commits_since_main()
