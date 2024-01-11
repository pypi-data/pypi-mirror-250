import os
import pathlib
import shutil
import subprocess
import sys


def find_git_root() -> pathlib.Path:
    """Find the root of the current git repository."""
    git = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=True,
        capture_output=True,
        text=True,
    )
    return pathlib.Path(git.stdout.strip())


def main() -> int:
    """Install the pre-commit hook."""
    root = find_git_root()
    hook_path = root / ".git" / "hooks" / "pre-commit"
    if hook_path.exists():
        sys.stderr.write(
            f"removing existing hook `{os.path.relpath(hook_path)}`\n"
        )
        confirm = input("are you sure? [y/N] ")
        if confirm.lower() not in ("y", "yes"):
            return 1
        hook_path.unlink(missing_ok=True)
    script_path = shutil.which("black-isort-hook")
    if script_path is None:
        sys.stderr.write(
            "black-isort-hook not found in PATH, please install it first 😰\n"
        )
        return 1
    hook_path.symlink_to(script_path)
    sys.stderr.write(
        f"added symlink `{os.path.relpath(hook_path)}` to"
        f" `{os.path.relpath(script_path)}` 🎉\n"
    )
    return 0
