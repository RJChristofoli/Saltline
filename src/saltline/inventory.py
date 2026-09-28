"""Deterministic capture of current Python files in a local repository.

Git applies nested ``.gitignore`` rules, including negation and directory
precedence. If Git is unavailable, capture still proceeds and records that the
ignore policy could not be applied. No repository source is executed.
"""

import fnmatch
import hashlib
import os
import stat
import subprocess
from dataclasses import dataclass
from pathlib import Path

from saltline.model import Inventory, InventoryDiagnostic, InventoryFile

_LANGUAGES = {".py": "python", ".pyi": "python"}
_DEFAULT_EXCLUDED_DIRS = frozenset(
    {
        ".git",
        ".hg",
        ".svn",
        ".venv",
        "venv",
        "__pycache__",
        "node_modules",
        "vendor",
        "dist",
        "build",
    }
)


@dataclass(frozen=True)
class InventoryOptions:
    """Additional exclusions; directory names apply at every depth."""

    excluded_directories: frozenset[str] = _DEFAULT_EXCLUDED_DIRS
    excluded_patterns: tuple[str, ...] = ()
    max_file_bytes: int = 32 * 1024 * 1024


def _ignored_paths(root: Path, paths: list[str]) -> set[str]:
    if not paths:
        return set()
    data = b"\0".join(os.fsencode(path) for path in paths) + b"\0"
    try:
        result = subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "-c",
                "core.excludesFile=/dev/null",
                "check-ignore",
                "--no-index",
                "--stdin",
                "-z",
            ],
            input=data,
            capture_output=True,
            check=False,
        )
    except OSError as exc:
        raise RuntimeError("Git is unavailable; .gitignore was not applied") from exc
    if result.returncode not in (0, 1):
        raise RuntimeError("Git could not apply .gitignore rules")
    return {os.fsdecode(path) for path in result.stdout.split(b"\0") if path}


def _capture(root: Path, relative: str, max_file_bytes: int) -> InventoryFile:
    parts = relative.split("/")
    directory = os.open(root, os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in parts[:-1]:
            next_directory = os.open(
                part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory
            )
            os.close(directory)
            directory = next_directory
        descriptor = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW, dir_fd=directory)
    finally:
        os.close(directory)
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise ValueError("not a regular file")
        if before.st_size > max_file_bytes:
            raise ValueError("file exceeds size limit")
        with os.fdopen(descriptor, "rb", closefd=False) as stream:
            content = stream.read(max_file_bytes + 1)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    if len(content) > max_file_bytes:
        raise ValueError("file exceeds size limit")
    if (before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (
        after.st_size,
        after.st_mtime_ns,
        after.st_ctime_ns,
    ):
        raise ValueError("file changed during capture")
    if b"\0" in content:
        raise ValueError("binary file")
    return InventoryFile(
        path=relative,
        language=_LANGUAGES[Path(relative).suffix],
        size_bytes=len(content),
        sha256=hashlib.sha256(content).hexdigest(),
        content=content,
    )


def discover_files(
    repository: str | Path, options: InventoryOptions | None = None
) -> Inventory:
    """Capture supported files with sorted paths and a stable SHA-256 fingerprint.

    Directory symlinks are never traversed and file symlinks are not captured.
    Paths use root-relative POSIX spelling and retain case. Capture failures are
    diagnostics; a missing or unreadable root is an execution error.
    """
    root = Path(repository).resolve(strict=True)
    if not root.is_dir():
        raise NotADirectoryError(root)
    options = options or InventoryOptions()
    if options.max_file_bytes < 0:
        raise ValueError("max_file_bytes must be nonnegative")

    candidates: list[str] = []
    diagnostics: list[InventoryDiagnostic] = []

    def on_walk_error(error: OSError) -> None:
        diagnostics.append(
            InventoryDiagnostic(".", f"directory unreadable: {error.strerror}")
        )

    for current, directories, filenames in os.walk(
        root, followlinks=False, onerror=on_walk_error
    ):
        base = Path(current)
        directories[:] = sorted(
            name
            for name in directories
            if name not in options.excluded_directories
            and not (base / name).is_symlink()
            and (base / name).resolve().is_relative_to(root)
        )
        for name in sorted(filenames):
            path = base / name
            if path.is_symlink() or path.suffix not in _LANGUAGES:
                continue
            relative = path.relative_to(root).as_posix()
            if any(
                fnmatch.fnmatchcase(relative, pattern)
                for pattern in options.excluded_patterns
            ):
                continue
            candidates.append(relative)

    candidates.sort()
    try:
        ignored = _ignored_paths(root, candidates)
    except RuntimeError as exc:
        diagnostics.append(InventoryDiagnostic(".", str(exc)))
        ignored = set()

    files: list[InventoryFile] = []
    fingerprint = hashlib.sha256()
    for relative in candidates:
        if relative in ignored:
            continue
        try:
            captured = _capture(root, relative, options.max_file_bytes)
        except (OSError, ValueError) as exc:
            diagnostics.append(InventoryDiagnostic(relative, str(exc)))
            continue
        files.append(captured)
        path_bytes = relative.encode("utf-8", errors="surrogateescape")
        fingerprint.update(len(path_bytes).to_bytes(8, "big"))
        fingerprint.update(path_bytes)
        fingerprint.update(bytes.fromhex(captured.sha256))

    return Inventory(
        tuple(files),
        fingerprint.hexdigest(),
        tuple(sorted(diagnostics, key=lambda item: (item.path, item.reason))),
    )
