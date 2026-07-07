"""Minimal procedural decision engine for the Dev Agent."""

from dataclasses import dataclass
from enum import Enum


class DevAgentDecisionType(str, Enum):
    """Known procedural decision types returned by the Dev Agent."""

    NEXT_STEP = "NEXT_STEP"
    STOP = "STOP"
    READY_FOR_HUMAN_APPROVAL = "READY_FOR_HUMAN_APPROVAL"
    DONE = "DONE"


class RepositoryState(str, Enum):
    """Known repository states recognized by the Dev Agent."""

    CLEAN_SYNCED = "CLEAN_SYNCED"
    CLEAN_UNKNOWN_REMOTE = "CLEAN_UNKNOWN_REMOTE"
    CLEAN_NOT_SYNCED = "CLEAN_NOT_SYNCED"
    UNTRACKED_FILES = "UNTRACKED_FILES"
    STAGED_CHANGES = "STAGED_CHANGES"
    UNSTAGED_CHANGES = "UNSTAGED_CHANGES"
    UNKNOWN_STATE = "UNKNOWN_STATE"


@dataclass(frozen=True)
class DevAgentDecision:
    """A procedural decision produced from supplied repository state data."""

    decision_type: DevAgentDecisionType
    repository_state: RepositoryState
    procedure: str
    next_step: str | None = None
    reason: str | None = None


def evaluate_repository_state(
    *,
    git_status: str,
    local_head: str | None,
    origin_main: str | None,
    git_diff: str | None = None,
    git_diff_cached: str | None = None,
    allowed_paths: tuple[str, ...] | None = None,
) -> DevAgentDecision:
    """Evaluate supplied Git state and return the next procedural decision."""
    normalized_status = git_status.strip()
    normalized_status_lower = normalized_status.lower()

    if _is_unknown_git_status(normalized_status_lower):
        return _stop_unknown_state("unknown_repository_state")

    has_clean_worktree = "nothing to commit, working tree clean" in normalized_status
    has_untracked_files = "Untracked files:" in normalized_status
    has_staged_changes = "Changes to be committed:" in normalized_status
    has_unstaged_changes = "Changes not staged for commit:" in normalized_status

    change_state_count = sum(
        [
            has_untracked_files,
            has_staged_changes,
            has_unstaged_changes,
        ]
    )

    if change_state_count > 1:
        return _stop_unknown_state("ambiguous_repository_state")

    if has_clean_worktree:
        return _evaluate_clean_repository_state(
            local_head=local_head,
            origin_main=origin_main,
        )

    if has_untracked_files:
        return _evaluate_untracked_files(git_diff=git_diff)

    if has_staged_changes:
        return _evaluate_staged_changes(
            git_diff_cached=git_diff_cached,
            allowed_paths=allowed_paths,
        )

    if has_unstaged_changes:
        return DevAgentDecision(
            decision_type=DevAgentDecisionType.NEXT_STEP,
            repository_state=RepositoryState.UNSTAGED_CHANGES,
            procedure="UNKNOWN",
            next_step="review_worktree_diff",
            reason="unstaged_changes_require_worktree_diff_review",
        )

    return _stop_unknown_state("unknown_repository_state")


def _evaluate_clean_repository_state(
    *,
    local_head: str | None,
    origin_main: str | None,
) -> DevAgentDecision:
    if local_head is None and origin_main is None:
        return DevAgentDecision(
            decision_type=DevAgentDecisionType.NEXT_STEP,
            repository_state=RepositoryState.CLEAN_UNKNOWN_REMOTE,
            procedure="PREFLIGHT_REPOSITORY_CHECK",
            next_step="provide_local_and_origin_hashes",
            reason="missing_local_head_and_origin_main_hashes",
        )

    if local_head is None:
        return DevAgentDecision(
            decision_type=DevAgentDecisionType.NEXT_STEP,
            repository_state=RepositoryState.CLEAN_UNKNOWN_REMOTE,
            procedure="PREFLIGHT_REPOSITORY_CHECK",
            next_step="provide_local_head_hash",
            reason="missing_local_head_hash",
        )

    if origin_main is None:
        return DevAgentDecision(
            decision_type=DevAgentDecisionType.NEXT_STEP,
            repository_state=RepositoryState.CLEAN_UNKNOWN_REMOTE,
            procedure="PREFLIGHT_REPOSITORY_CHECK",
            next_step="provide_origin_main_hash",
            reason="missing_origin_main_hash",
        )

    if local_head != origin_main:
        return DevAgentDecision(
            decision_type=DevAgentDecisionType.STOP,
            repository_state=RepositoryState.CLEAN_NOT_SYNCED,
            procedure="PREFLIGHT_REPOSITORY_CHECK",
            reason="local_head_differs_from_origin_main",
        )

    return DevAgentDecision(
        decision_type=DevAgentDecisionType.NEXT_STEP,
        repository_state=RepositoryState.CLEAN_SYNCED,
        procedure="PREFLIGHT_REPOSITORY_CHECK",
        next_step="continue_current_procedure",
        reason="repository_clean_and_synced",
    )


def _evaluate_untracked_files(*, git_diff: str | None) -> DevAgentDecision:
    reason = "untracked_files_require_staging"

    if git_diff == "":
        reason = "untracked_files_not_visible_in_worktree_diff"

    return DevAgentDecision(
        decision_type=DevAgentDecisionType.NEXT_STEP,
        repository_state=RepositoryState.UNTRACKED_FILES,
        procedure="NEW_POLISH_DOCUMENTATION_FILE",
        next_step="stage_untracked_documentation_file",
        reason=reason,
    )


def _evaluate_staged_changes(
    *,
    git_diff_cached: str | None,
    allowed_paths: tuple[str, ...] | None,
) -> DevAgentDecision:
    if git_diff_cached is None or allowed_paths is None:
        return DevAgentDecision(
            decision_type=DevAgentDecisionType.NEXT_STEP,
            repository_state=RepositoryState.STAGED_CHANGES,
            procedure="NEW_POLISH_DOCUMENTATION_FILE",
            next_step="review_cached_diff",
            reason="staged_changes_require_cached_diff_review",
        )

    diff_paths = _extract_cached_diff_paths(git_diff_cached=git_diff_cached)
    normalized_allowed_paths = {
        _normalize_repo_path(path)
        for path in allowed_paths
    }

    if not diff_paths:
        return DevAgentDecision(
            decision_type=DevAgentDecisionType.STOP,
            repository_state=RepositoryState.STAGED_CHANGES,
            procedure="NEW_POLISH_DOCUMENTATION_FILE",
            reason="staged_diff_has_no_paths",
        )

    if not diff_paths.issubset(normalized_allowed_paths):
        return DevAgentDecision(
            decision_type=DevAgentDecisionType.STOP,
            repository_state=RepositoryState.STAGED_CHANGES,
            procedure="NEW_POLISH_DOCUMENTATION_FILE",
            reason="staged_diff_outside_allowed_scope",
        )

    return DevAgentDecision(
        decision_type=DevAgentDecisionType.NEXT_STEP,
        repository_state=RepositoryState.STAGED_CHANGES,
        procedure="NEW_POLISH_DOCUMENTATION_FILE",
        next_step="run_diff_check",
        reason="staged_diff_matches_allowed_scope",
    )


def _extract_cached_diff_paths(*, git_diff_cached: str) -> set[str]:
    paths: set[str] = set()

    for line in git_diff_cached.splitlines():
        if not line.startswith("diff --git "):
            continue

        parts = line.split()
        if len(parts) < 4:
            continue

        new_path = parts[3]
        paths.add(_strip_diff_prefix(new_path))

    return paths


def _strip_diff_prefix(path: str) -> str:
    normalized_path = _normalize_repo_path(path)

    if normalized_path.startswith("b/"):
        return normalized_path[2:]

    if normalized_path.startswith("a/"):
        return normalized_path[2:]

    return normalized_path


def _normalize_repo_path(path: str) -> str:
    return path.replace("\\", "/").strip()


def _is_unknown_git_status(normalized_status_lower: str) -> bool:
    return (
        not normalized_status_lower
        or normalized_status_lower.startswith("fatal:")
        or "not a git repository" in normalized_status_lower
    )


def _stop_unknown_state(reason: str) -> DevAgentDecision:
    return DevAgentDecision(
        decision_type=DevAgentDecisionType.STOP,
        repository_state=RepositoryState.UNKNOWN_STATE,
        procedure="UNKNOWN",
        reason=reason,
    )
