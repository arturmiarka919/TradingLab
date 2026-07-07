"""Tests for minimal procedural Dev Agent decisions."""

from tradinglab.dev_agent.procedural_decision import (
    DevAgentDecisionType,
    RepositoryState,
    evaluate_repository_state,
)


def test_clean_synced_repository_returns_next_step() -> None:
    decision = evaluate_repository_state(
        git_status=(
            "On branch main\n"
            "Your branch is up to date with 'origin/main'.\n"
            "\n"
            "nothing to commit, working tree clean\n"
        ),
        local_head="abc123",
        origin_main="abc123",
    )

    assert decision.decision_type == DevAgentDecisionType.NEXT_STEP
    assert decision.repository_state == RepositoryState.CLEAN_SYNCED
    assert decision.procedure == "PREFLIGHT_REPOSITORY_CHECK"
    assert decision.next_step == "continue_current_procedure"


def test_clean_repository_without_origin_hash_requests_missing_remote_hash() -> None:
    decision = evaluate_repository_state(
        git_status=(
            "On branch main\n"
            "Your branch is up to date with 'origin/main'.\n"
            "\n"
            "nothing to commit, working tree clean\n"
        ),
        local_head="abc123",
        origin_main=None,
    )

    assert decision.decision_type == DevAgentDecisionType.NEXT_STEP
    assert decision.repository_state == RepositoryState.CLEAN_UNKNOWN_REMOTE
    assert decision.procedure == "PREFLIGHT_REPOSITORY_CHECK"
    assert decision.next_step == "provide_origin_main_hash"


def test_clean_not_synced_repository_returns_stop() -> None:
    decision = evaluate_repository_state(
        git_status=(
            "On branch main\n"
            "Your branch is up to date with 'origin/main'.\n"
            "\n"
            "nothing to commit, working tree clean\n"
        ),
        local_head="local123",
        origin_main="remote456",
    )

    assert decision.decision_type == DevAgentDecisionType.STOP
    assert decision.repository_state == RepositoryState.CLEAN_NOT_SYNCED
    assert decision.procedure == "PREFLIGHT_REPOSITORY_CHECK"
    assert decision.reason == "local_head_differs_from_origin_main"


def test_untracked_file_with_empty_diff_is_not_treated_as_no_changes() -> None:
    decision = evaluate_repository_state(
        git_status=(
            "On branch main\n"
            "Your branch is up to date with 'origin/main'.\n"
            "\n"
            "Untracked files:\n"
            '  (use "git add <file>..." to include in what will be committed)\n'
            "        dokumentacja/procesy/DEV_AGENT_OBSERWACJE.md\n"
            "\n"
            "nothing added to commit but untracked files present "
            '(use "git add" to track)\n'
        ),
        local_head="abc123",
        origin_main="abc123",
        git_diff="",
    )

    assert decision.decision_type == DevAgentDecisionType.NEXT_STEP
    assert decision.repository_state == RepositoryState.UNTRACKED_FILES
    assert decision.procedure == "NEW_POLISH_DOCUMENTATION_FILE"
    assert decision.next_step == "stage_untracked_documentation_file"


def test_staged_changes_require_cached_diff_review() -> None:
    decision = evaluate_repository_state(
        git_status=(
            "On branch main\n"
            "Your branch is up to date with 'origin/main'.\n"
            "\n"
            "Changes to be committed:\n"
            '  (use "git restore --staged <file>..." to unstage)\n'
            "        new file:   dokumentacja/architektura/DEV_AGENT_CONTRACT.md\n"
        ),
        local_head="abc123",
        origin_main="abc123",
    )

    assert decision.decision_type == DevAgentDecisionType.NEXT_STEP
    assert decision.repository_state == RepositoryState.STAGED_CHANGES
    assert decision.procedure == "NEW_POLISH_DOCUMENTATION_FILE"
    assert decision.next_step == "review_cached_diff"


def test_staged_cached_diff_with_only_allowed_path_requests_diff_check() -> None:
    decision = evaluate_repository_state(
        git_status=(
            "On branch main\n"
            "Your branch is up to date with 'origin/main'.\n"
            "\n"
            "Changes to be committed:\n"
            '  (use "git restore --staged <file>..." to unstage)\n'
            "        new file:   dokumentacja/architektura/DEV_AGENT_CONTRACT.md\n"
        ),
        local_head="abc123",
        origin_main="abc123",
        git_diff_cached=(
            "diff --git a/dokumentacja/architektura/DEV_AGENT_CONTRACT.md "
            "b/dokumentacja/architektura/DEV_AGENT_CONTRACT.md\n"
            "new file mode 100644\n"
        ),
        allowed_paths=("dokumentacja/architektura/DEV_AGENT_CONTRACT.md",),
    )

    assert decision.decision_type == DevAgentDecisionType.NEXT_STEP
    assert decision.repository_state == RepositoryState.STAGED_CHANGES
    assert decision.procedure == "NEW_POLISH_DOCUMENTATION_FILE"
    assert decision.next_step == "run_diff_check"
    assert decision.reason == "staged_diff_matches_allowed_scope"


def test_staged_cached_diff_outside_allowed_scope_returns_stop() -> None:
    decision = evaluate_repository_state(
        git_status=(
            "On branch main\n"
            "Your branch is up to date with 'origin/main'.\n"
            "\n"
            "Changes to be committed:\n"
            '  (use "git restore --staged <file>..." to unstage)\n'
            "        new file:   dokumentacja/architektura/DEV_AGENT_CONTRACT.md\n"
            "        modified:   README.md\n"
        ),
        local_head="abc123",
        origin_main="abc123",
        git_diff_cached=(
            "diff --git a/dokumentacja/architektura/DEV_AGENT_CONTRACT.md "
            "b/dokumentacja/architektura/DEV_AGENT_CONTRACT.md\n"
            "new file mode 100644\n"
            "diff --git a/README.md b/README.md\n"
            "index 1111111..2222222 100644\n"
        ),
        allowed_paths=("dokumentacja/architektura/DEV_AGENT_CONTRACT.md",),
    )

    assert decision.decision_type == DevAgentDecisionType.STOP
    assert decision.repository_state == RepositoryState.STAGED_CHANGES
    assert decision.procedure == "NEW_POLISH_DOCUMENTATION_FILE"
    assert decision.reason == "staged_diff_outside_allowed_scope"


def test_unknown_repository_state_returns_stop() -> None:
    decision = evaluate_repository_state(
        git_status="fatal: not a git repository\n",
        local_head="abc123",
        origin_main="abc123",
    )

    assert decision.decision_type == DevAgentDecisionType.STOP
    assert decision.repository_state == RepositoryState.UNKNOWN_STATE
    assert decision.procedure == "UNKNOWN"
    assert decision.reason == "unknown_repository_state"
