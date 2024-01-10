"""Git operations for cloning and validating repositories."""

import os
import platform
import shutil
from pathlib import Path
from typing import Optional

import git

from readmeai.exceptions import GitCloneError


async def clone_repo_to_temp_dir(repo_source: str, temp_dir: str) -> str:
    """Clone the repository to a temporary directory."""
    try:
        repo_path = Path(repo_source)

        if repo_path.is_file():
            raise GitCloneError(repo_source, "Path is a file, not directory.")

        if repo_path.is_dir():
            shutil.copytree(repo_path, temp_dir, dirs_exist_ok=True)
        else:
            git.Repo.clone_from(
                repo_source, temp_dir, depth=1, single_branch=True
            )
        return temp_dir

    except (
        git.GitCommandError,
        git.InvalidGitRepositoryError,
        OSError,
    ) as exc:
        raise GitCloneError(repo_source, exc) from exc


def find_git_executable() -> Optional[Path]:
    """Find the path to the git executable, if available."""
    git_exec_path = os.environ.get("GIT_PYTHON_GIT_EXECUTABLE")
    if git_exec_path:
        return Path(git_exec_path)

    # For Windows, set default location of git executable.
    if platform.system() == "Windows":
        default_windows_path = Path("C:\\Program Files\\Git\\cmd\\git.EXE")
        if default_windows_path.exists():
            return default_windows_path

    # For other OS, set executable path from PATH environment variable.
    paths = os.environ["PATH"].split(os.pathsep)
    for path in paths:
        git_path = Path(path) / "git"
        if git_path.exists():
            return git_path

    return None


def validate_file_permissions(temp_dir: Path) -> None:
    """Validates file permissions of the cloned repository."""
    if platform.system() != "Windows":
        if isinstance(temp_dir, str):
            temp_dir = Path(temp_dir)
        permissions = temp_dir.stat().st_mode & 0o777
        if permissions != 0o700:
            raise SystemExit(
                f"Invalid file permissions for {temp_dir}.\n"
                f"Expected 0o700, but found {oct(permissions)}."
            )


def validate_git_executable(git_exec_path: Optional[str]) -> None:
    """Validate the path to the git executable."""
    if not git_exec_path or not Path(git_exec_path).exists():
        raise ValueError(f"Git executable not found at {git_exec_path}")
