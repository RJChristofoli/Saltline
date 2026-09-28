"""Inventory behavior on small, untrusted worktrees."""

import subprocess
from pathlib import Path

import pytest

from saltline.inventory import InventoryOptions, discover_files


def write(root: Path, relative: str, content: bytes = b"pass\n") -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return path


def repository(root: Path) -> None:
    subprocess.run(["git", "init", "-q", str(root)], check=True)


def test_ignore_rules_and_canonical_fingerprint(tmp_path: Path) -> None:
    repository(tmp_path)
    write(tmp_path, ".gitignore", b"*.py\n!keep.py\nignored/\n")
    write(tmp_path, "z.py")
    write(tmp_path, "keep.py", b"print(1)\n")
    write(tmp_path, "nested/.gitignore", b"!local.py\n")
    write(tmp_path, "nested/local.py")
    write(tmp_path, "nested/other.py")
    write(tmp_path, "ignored/hidden.py")
    write(tmp_path, "notes.txt")

    first = discover_files(tmp_path)
    second = discover_files(tmp_path)

    assert [file.path for file in first.files] == ["keep.py", "nested/local.py"]
    assert first == second
    assert first.files[0].language == "python"
    assert first.files[0].size_bytes == len(b"print(1)\n")
    assert len(first.files[0].sha256) == 64
    assert first.diagnostics == ()

    write(tmp_path, "keep.py", b"print(2)\n")
    assert discover_files(tmp_path).fingerprint != first.fingerprint


def test_exclusions_binary_symlinks_and_unsupported_files(tmp_path: Path) -> None:
    repository(tmp_path)
    write(tmp_path, "src/ok.py")
    write(tmp_path, "src/types.pyi")
    write(tmp_path, "src/generated_pb2.py")
    write(tmp_path, "vendor/lib.py")
    write(tmp_path, "src/binary.py", b"\x00\x01")
    write(tmp_path, "src/notes.md")
    outside = write(tmp_path.parent, "outside.py")
    (tmp_path / "src" / "external.py").symlink_to(outside)
    (tmp_path / "link_dir").symlink_to(tmp_path / "src", target_is_directory=True)

    result = discover_files(tmp_path, InventoryOptions(excluded_patterns=("*_pb2.py",)))

    assert [file.path for file in result.files] == ["src/ok.py", "src/types.pyi"]
    assert [(item.path, item.reason) for item in result.diagnostics] == [
        ("src/binary.py", "binary file")
    ]


def test_root_independence_and_size_limit(tmp_path: Path) -> None:
    left = tmp_path / "left"
    right = tmp_path / "right"
    left.mkdir()
    right.mkdir()
    for root in (left, right):
        repository(root)
        write(root, "package/app.py", b"hello\n")
    assert discover_files(left).fingerprint == discover_files(right).fingerprint
    limited = discover_files(left, InventoryOptions(max_file_bytes=2))
    assert limited.files == ()
    assert limited.diagnostics[0].path == "package/app.py"


def test_invalid_root(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        discover_files(tmp_path / "missing")
    with pytest.raises(NotADirectoryError):
        discover_files(write(tmp_path, "file.py"))


def test_git_unavailable_keeps_capture_with_diagnostic(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    write(tmp_path, "source.py")

    def missing_git(*args: object, **kwargs: object) -> None:
        raise FileNotFoundError("git")

    monkeypatch.setattr(subprocess, "run", missing_git)
    result = discover_files(tmp_path)
    assert [file.path for file in result.files] == ["source.py"]
    assert (
        result.diagnostics[0].reason == "Git is unavailable; .gitignore was not applied"
    )
