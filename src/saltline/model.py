"""Value records shared by repository analysis stages."""

from dataclasses import dataclass


@dataclass(frozen=True)
class InventoryFile:
    """One captured source file, identified by its root-relative POSIX path."""

    path: str
    language: str
    size_bytes: int
    sha256: str
    content: bytes


@dataclass(frozen=True)
class InventoryDiagnostic:
    """A file or ignore-policy problem that did not invalidate the inventory."""

    path: str
    reason: str


@dataclass(frozen=True)
class Inventory:
    """Canonical captured files and a root-independent content fingerprint."""

    files: tuple[InventoryFile, ...]
    fingerprint: str
    diagnostics: tuple[InventoryDiagnostic, ...]
