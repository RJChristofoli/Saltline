# File inventory contract

`saltline.inventory.discover_files(repository, options)` captures the current
worktree under a supplied directory. It is an internal stage for later analysis;
the CLI does not expose an analysis command yet.

- File IDs are root-relative POSIX paths, sorted lexicographically with case
  preserved. The inventory includes `.py` and `.pyi` as Python files, including
  uncommitted and untracked files.
- Git applies `.gitignore` rules from the root and nested directories, including
  negation. The repository's `.git/info/exclude` also applies. The user's global
  Git excludes are disabled so machine configuration does not change results.
  Ignore rules apply to tracked files too, because this is an analysis exclusion
  policy rather than a listing of Git's untracked files.
- Directory symlinks are never traversed; file symlinks are skipped. Files are
  opened without following symlinks in any path component, so a symlink change
  during traversal cannot make Saltline read outside the selected root.
- `.git`, `.hg`, `.svn`, `.venv`, `venv`, `__pycache__`, `node_modules`, `vendor`,
  `dist`, and `build` directories are excluded by default at any depth.
  `InventoryOptions.excluded_directories` replaces this set, and
  `excluded_patterns` adds root-relative glob exclusions for generated files.
  Explicit exclusions take precedence over `.gitignore` negation.
- Files containing a NUL byte are treated as binary and skipped. Files over
  `max_file_bytes` (32 MiB by default) are skipped. Unreadable, changing,
  oversized, or binary files produce sorted diagnostics. Git failure also
  produces a diagnostic; capture continues without ignore filtering.
- Each included file has its language, byte size, SHA-256 content digest, and
  captured bytes for downstream analysis. The inventory fingerprint is SHA-256
  over sorted entries, each encoded as an eight-byte big-endian path length,
  UTF-8 path bytes (surrogate escape for non-UTF-8 names), and the 32-byte
  content digest. Absolute paths and timestamps do not enter the fingerprint.
  Capture is not an atomic worktree snapshot; a file changed while read is
  omitted with a diagnostic.
