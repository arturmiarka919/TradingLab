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
        git_status=_staged_documentation_status(),
        local_head="abc123",
        origin_main="abc123",
    )

    assert decision.decision_type == DevAgentDecisionType.NEXT_STEP
    assert decision.repository_state == RepositoryState.STAGED_CHANGES
    assert decision.procedure == "NEW_POLISH_DOCUMENTATION_FILE"
    assert decision.next_step == "review_cached_diff"


def test_staged_cached_diff_with_only_allowed_path_requests_diff_check() -> None:
    decision = evaluate_repository_state(
        git_status=_staged_documentation_status(),
        local_head="abc123",
        origin_main="abc123",
        git_diff_cached=_allowed_documentation_cached_diff(),
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


def test_valid_staged_diff_with_clean_diff_check_requests_ruff_result() -> None:
    decision = evaluate_repository_state(
        git_status=_staged_documentation_status(),
        local_head="abc123",
        origin_main="abc123",
        git_diff_cached=_allowed_documentation_cached_diff(),
        allowed_paths=("dokumentacja/architektura/DEV_AGENT_CONTRACT.md",),
        git_diff_check="",
    )

    assert decision.decision_type == DevAgentDecisionType.NEXT_STEP
    assert decision.repository_state == RepositoryState.STAGED_CHANGES
    assert decision.procedure == "NEW_POLISH_DOCUMENTATION_FILE"
    assert decision.next_step == "provide_ruff_result"
    assert decision.reason == "diff_check_passed"


def test_diff_check_error_returns_stop() -> None:
    decision = evaluate_repository_state(
        git_status=_staged_documentation_status(),
        local_head="abc123",
        origin_main="abc123",
        git_diff_cached=_allowed_documentation_cached_diff(),
        allowed_paths=("dokumentacja/architektura/DEV_AGENT_CONTRACT.md",),
        git_diff_check="dokumentacja/file.md: trailing whitespace.\n",
    )

    assert decision.decision_type == DevAgentDecisionType.STOP
    assert decision.repository_state == RepositoryState.STAGED_CHANGES
    assert decision.procedure == "NEW_POLISH_DOCUMENTATION_FILE"
    assert decision.reason == "diff_check_failed"


def test_clean_diff_check_and_missing_ruff_result_requests_ruff_result() -> None:
    decision = evaluate_repository_state(
        git_status=_staged_documentation_status(),
        local_head="abc123",
        origin_main="abc123",
        git_diff_cached=_allowed_documentation_cached_diff(),
        allowed_paths=("dokumentacja/architektura/DEV_AGENT_CONTRACT.md",),
        git_diff_check="",
        ruff_result=None,
    )

    assert decision.decision_type == DevAgentDecisionType.NEXT_STEP
    assert decision.repository_state == RepositoryState.STAGED_CHANGES
    assert decision.procedure == "NEW_POLISH_DOCUMENTATION_FILE"
    assert decision.next_step == "provide_ruff_result"
    assert decision.reason == "diff_check_passed"


def test_ruff_error_returns_stop() -> None:
    decision = evaluate_repository_state(
        git_status=_staged_documentation_status(),
        local_head="abc123",
        origin_main="abc123",
        git_diff_cached=_allowed_documentation_cached_diff(),
        allowed_paths=("dokumentacja/architektura/DEV_AGENT_CONTRACT.md",),
        git_diff_check="",
        ruff_result="Found 1 error.\n",
    )

    assert decision.decision_type == DevAgentDecisionType.STOP
    assert decision.repository_state == RepositoryState.STAGED_CHANGES
    assert decision.procedure == "NEW_POLISH_DOCUMENTATION_FILE"
    assert decision.reason == "ruff_failed"


def test_clean_diff_check_and_clean_ruff_requests_pytest_result() -> None:
    decision = evaluate_repository_state(
        git_status=_staged_documentation_status(),
        local_head="abc123",
        origin_main="abc123",
        git_diff_cached=_allowed_documentation_cached_diff(),
        allowed_paths=("dokumentacja/architektura/DEV_AGENT_CONTRACT.md",),
        git_diff_check="",
        ruff_result="All checks passed!\n",
    )

    assert decision.decision_type == DevAgentDecisionType.NEXT_STEP
    assert decision.repository_state == RepositoryState.STAGED_CHANGES
    assert decision.procedure == "NEW_POLISH_DOCUMENTATION_FILE"
    assert decision.next_step == "provide_pytest_result"
    assert decision.reason == "ruff_passed"


def test_pytest_error_returns_stop() -> None:
    decision = evaluate_repository_state(
        git_status=_staged_documentation_status(),
        local_head="abc123",
        origin_main="abc123",
        git_diff_cached=_allowed_documentation_cached_diff(),
        allowed_paths=("dokumentacja/architektura/DEV_AGENT_CONTRACT.md",),
        git_diff_check="",
        ruff_result="All checks passed!\n",
        pytest_result="FAILED tests/dev_agent/test_procedural_decision.py\n",
    )

    assert decision.decision_type == DevAgentDecisionType.STOP
    assert decision.repository_state == RepositoryState.STAGED_CHANGES
    assert decision.procedure == "NEW_POLISH_DOCUMENTATION_FILE"
    assert decision.reason == "pytest_failed"


def test_all_checks_passed_returns_ready_for_human_approval() -> None:
    decision = evaluate_repository_state(
        git_status=_staged_documentation_status(),
        local_head="abc123",
        origin_main="abc123",
        git_diff_cached=_allowed_documentation_cached_diff(),
        allowed_paths=("dokumentacja/architektura/DEV_AGENT_CONTRACT.md",),
        git_diff_check="",
        ruff_result="All checks passed!\n",
        pytest_result="157 passed in 1.05s\n",
    )

    assert decision.decision_type == DevAgentDecisionType.READY_FOR_HUMAN_APPROVAL
    assert decision.repository_state == RepositoryState.STAGED_CHANGES
    assert decision.procedure == "NEW_POLISH_DOCUMENTATION_FILE"
    assert decision.next_step == "request_commit_approval"
    assert decision.reason == "all_required_checks_passed"


def test_rejected_commit_approval_returns_stop() -> None:
    decision = evaluate_repository_state(
        git_status=_staged_documentation_status(),
        local_head="abc123",
        origin_main="abc123",
        git_diff_cached=_allowed_documentation_cached_diff(),
        allowed_paths=("dokumentacja/architektura/DEV_AGENT_CONTRACT.md",),
        git_diff_check="",
        ruff_result="All checks passed!\n",
        pytest_result="157 passed in 1.05s\n",
        approval_decision="rejected",
    )

    assert decision.decision_type == DevAgentDecisionType.STOP
    assert decision.repository_state == RepositoryState.STAGED_CHANGES
    assert decision.procedure == "NEW_POLISH_DOCUMENTATION_FILE"
    assert decision.reason == "commit_rejected_by_human"


def test_approved_commit_without_commit_result_requests_run_commit() -> None:
    decision = evaluate_repository_state(
        git_status=_staged_documentation_status(),
        local_head="abc123",
        origin_main="abc123",
        git_diff_cached=_allowed_documentation_cached_diff(),
        allowed_paths=("dokumentacja/architektura/DEV_AGENT_CONTRACT.md",),
        git_diff_check="",
        ruff_result="All checks passed!\n",
        pytest_result="157 passed in 1.05s\n",
        approval_decision="approved",
    )

    assert decision.decision_type == DevAgentDecisionType.NEXT_STEP
    assert decision.repository_state == RepositoryState.STAGED_CHANGES
    assert decision.procedure == "NEW_POLISH_DOCUMENTATION_FILE"
    assert decision.next_step == "run_commit"
    assert decision.reason == "commit_approved"


def test_completed_commit_without_push_result_requests_run_push() -> None:
    decision = evaluate_repository_state(
        git_status=_staged_documentation_status(),
        local_head="abc123",
        origin_main="abc123",
        git_diff_cached=_allowed_documentation_cached_diff(),
        allowed_paths=("dokumentacja/architektura/DEV_AGENT_CONTRACT.md",),
        git_diff_check="",
        ruff_result="All checks passed!\n",
        pytest_result="157 passed in 1.05s\n",
        approval_decision="approved",
        commit_result="[main abc123] Add documentation\n",
    )

    assert decision.decision_type == DevAgentDecisionType.NEXT_STEP
    assert decision.repository_state == RepositoryState.STAGED_CHANGES
    assert decision.procedure == "NEW_POLISH_DOCUMENTATION_FILE"
    assert decision.next_step == "run_push"
    assert decision.reason == "commit_completed"


def test_completed_push_without_final_state_requests_final_repository_state() -> None:
    decision = evaluate_repository_state(
        git_status=_staged_documentation_status(),
        local_head="abc123",
        origin_main="abc123",
        git_diff_cached=_allowed_documentation_cached_diff(),
        allowed_paths=("dokumentacja/architektura/DEV_AGENT_CONTRACT.md",),
        git_diff_check="",
        ruff_result="All checks passed!\n",
        pytest_result="157 passed in 1.05s\n",
        approval_decision="approved",
        commit_result="[main abc123] Add documentation\n",
        push_result="main -> main\n",
    )

    assert decision.decision_type == DevAgentDecisionType.NEXT_STEP
    assert decision.repository_state == RepositoryState.STAGED_CHANGES
    assert decision.procedure == "NEW_POLISH_DOCUMENTATION_FILE"
    assert decision.next_step == "provide_final_repository_state"
    assert decision.reason == "missing_final_repository_state"


def test_final_dirty_working_tree_after_push_returns_stop() -> None:
    decision = evaluate_repository_state(
        git_status=_staged_documentation_status(),
        local_head="abc123",
        origin_main="abc123",
        git_diff_cached=_allowed_documentation_cached_diff(),
        allowed_paths=("dokumentacja/architektura/DEV_AGENT_CONTRACT.md",),
        git_diff_check="",
        ruff_result="All checks passed!\n",
        pytest_result="157 passed in 1.05s\n",
        approval_decision="approved",
        commit_result="[main abc123] Add documentation\n",
        push_result="main -> main\n",
        final_git_status=_dirty_final_status(),
        final_local_head="abc123",
        final_origin_main="abc123",
    )

    assert decision.decision_type == DevAgentDecisionType.STOP
    assert decision.repository_state == RepositoryState.STAGED_CHANGES
    assert decision.procedure == "NEW_POLISH_DOCUMENTATION_FILE"
    assert decision.reason == "final_working_tree_not_clean"


def test_final_head_difference_after_push_returns_stop() -> None:
    decision = evaluate_repository_state(
        git_status=_staged_documentation_status(),
        local_head="abc123",
        origin_main="abc123",
        git_diff_cached=_allowed_documentation_cached_diff(),
        allowed_paths=("dokumentacja/architektura/DEV_AGENT_CONTRACT.md",),
        git_diff_check="",
        ruff_result="All checks passed!\n",
        pytest_result="157 passed in 1.05s\n",
        approval_decision="approved",
        commit_result="[main abc123] Add documentation\n",
        push_result="main -> main\n",
        final_git_status=_clean_final_status(),
        final_local_head="local123",
        final_origin_main="remote456",
    )

    assert decision.decision_type == DevAgentDecisionType.STOP
    assert decision.repository_state == RepositoryState.STAGED_CHANGES
    assert decision.procedure == "NEW_POLISH_DOCUMENTATION_FILE"
    assert decision.reason == "final_head_differs_from_origin_main"


def test_final_clean_synced_state_after_push_returns_done() -> None:
    decision = evaluate_repository_state(
        git_status=_staged_documentation_status(),
        local_head="abc123",
        origin_main="abc123",
        git_diff_cached=_allowed_documentation_cached_diff(),
        allowed_paths=("dokumentacja/architektura/DEV_AGENT_CONTRACT.md",),
        git_diff_check="",
        ruff_result="All checks passed!\n",
        pytest_result="157 passed in 1.05s\n",
        approval_decision="approved",
        commit_result="[main abc123] Add documentation\n",
        push_result="main -> main\n",
        final_git_status=_clean_final_status(),
        final_local_head="abc123",
        final_origin_main="abc123",
    )

    assert decision.decision_type == DevAgentDecisionType.DONE
    assert decision.repository_state == RepositoryState.CLEAN_SYNCED
    assert decision.procedure == "NEW_POLISH_DOCUMENTATION_FILE"
    assert decision.reason == "procedure_completed_and_synced"


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


def _staged_documentation_status() -> str:
    return (
        "On branch main\n"
        "Your branch is up to date with 'origin/main'.\n"
        "\n"
        "Changes to be committed:\n"
        '  (use "git restore --staged <file>..." to unstage)\n'
        "        new file:   dokumentacja/architektura/DEV_AGENT_CONTRACT.md\n"
    )


def _allowed_documentation_cached_diff() -> str:
    return (
        "diff --git a/dokumentacja/architektura/DEV_AGENT_CONTRACT.md "
        "b/dokumentacja/architektura/DEV_AGENT_CONTRACT.md\n"
        "new file mode 100644\n"
    )


def _clean_final_status() -> str:
    return (
        "On branch main\n"
        "Your branch is up to date with 'origin/main'.\n"
        "\n"
        "nothing to commit, working tree clean\n"
    )


def _dirty_final_status() -> str:
    return (
        "On branch main\n"
        "Your branch is up to date with 'origin/main'.\n"
        "\n"
        "Changes not staged for commit:\n"
        '  (use "git add <file>..." to update what will be committed)\n'
        "        modified:   README.md\n"
    )
