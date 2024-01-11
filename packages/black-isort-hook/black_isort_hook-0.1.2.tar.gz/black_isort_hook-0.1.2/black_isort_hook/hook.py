import concurrent.futures
import os.path
import subprocess
import sys


def read_file(filename: str) -> bytes:
    """Read a file from the git index."""
    git = subprocess.run(
        ["git", "show", ":" + filename], check=True, capture_output=True
    )
    return git.stdout


def check_file(filename: str, code: bytes) -> tuple[str, list[str]]:
    """Check a file for formatting errors."""
    sys.stderr.write(f"checking {filename}\n")
    errors = []

    black = subprocess.run(
        ["black", "-q", "--check", "--stdin-filename", filename, "-"],
        input=code,
        capture_output=True,
    )
    if black.returncode:
        errors.append("black")

    isort = subprocess.run(
        ["isort", "-q", "--check", "-"], input=code, capture_output=True
    )
    if isort.returncode:
        errors.append("isort")

    return filename, errors


def main() -> int:
    """Check staged python files for formatting errors."""
    git = subprocess.run(
        ["git", "--no-pager", "diff", "--name-only", "--cached", "--", "*.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    staged_python_files = [x for x in git.stdout.split() if os.path.exists(x)]
    errors = {}

    with concurrent.futures.ThreadPoolExecutor() as executor:
        file_contents = executor.map(read_file, staged_python_files)
        for filename, file_errors in executor.map(
            check_file, staged_python_files, file_contents
        ):
            if file_errors:
                errors[filename] = file_errors

    if errors:
        sys.stderr.write("pre-commit check failed 😰\n")
        for filename, failures in errors.items():
            sys.stderr.write("  {}: {}\n".format(filename, ", ".join(failures)))
        return 1

    sys.stderr.write("pre-commit check passed 🎉\n")
    return 0
