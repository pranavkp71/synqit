from synqit.prompts import COMMIT_SYSTEM, PR_SYSTEM, commit_user_prompt, pr_user_prompt


def test_commit_user_prompt_without_context() -> None:
    diff = "diff --git a/test.py b/test.py"
    prompt = commit_user_prompt(diff)
    assert diff in prompt
    assert "Developer's intent:" not in prompt


def test_commit_user_prompt_with_context() -> None:
    diff = "diff --git a/test.py b/test.py"
    context = "Fix the tests"
    prompt = commit_user_prompt(diff, context)
    assert diff in prompt
    assert "Developer's intent: Fix the tests" in prompt


def test_pr_user_prompt() -> None:
    commits = "a1b2c3d Fix bug\ne4f5g6h Add feature"
    prompt = pr_user_prompt(commits)
    assert commits in prompt


def test_system_prompts_contain_conventions() -> None:
    assert "Conventional Commits" in COMMIT_SYSTEM
    assert "PR description" in PR_SYSTEM
