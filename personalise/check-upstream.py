#!/usr/bin/env python3
"""
Version drift detection for personalised framework forks.

Compares the current framework version to the version the fork was built from
and reports which files have changed, categorised by impact.

Usage:
    python personalise/check-upstream.py
"""

import hashlib
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
VERSION_FILE = REPO_ROOT / "personalise" / "output" / "site" / ".framework-version"

# Files that can be merged without re-personalisation.
SAFE_MERGE_PATTERNS = [
    "stages/",
    "worked-example/",
    "worked-example-ba/",
    "worked-example-se/",
    "getting-started/choose-a-platform.md",
]

# Files that require re-running the fork script.
REQUIRES_REPERSONALISATION = [
    "blank-templates/",
    "getting-started/quick-start.md",
    "getting-started/index.md",
    "reference/glossary.md",
    "reference/decision-trees.md",
    "reference/checklist.md",
]

# Files that may need config updates before re-personalisation.
REVIEW_RECOMMENDED = [
    "personalise/",
]


def compute_current_hash() -> str:
    """Compute the current framework docs hash."""
    h = hashlib.sha256()
    for p in sorted(DOCS_DIR.rglob("*.md")):
        h.update(p.read_bytes())
    return h.hexdigest()[:12]


def get_fork_hash() -> str | None:
    """Read the hash stored when the fork was built."""
    if not VERSION_FILE.exists():
        return None
    return VERSION_FILE.read_text().strip()


def compute_file_hashes() -> dict[str, str]:
    """Compute per-file hashes for change detection."""
    hashes = {}
    for p in sorted(DOCS_DIR.rglob("*.md")):
        rel = str(p.relative_to(DOCS_DIR))
        hashes[rel] = hashlib.sha256(p.read_bytes()).hexdigest()[:12]
    return hashes


def categorise_file(rel_path: str) -> str:
    """Categorise a changed file by its impact on the fork."""
    for pattern in REVIEW_RECOMMENDED:
        if rel_path.startswith(pattern):
            return "review"
    for pattern in REQUIRES_REPERSONALISATION:
        if rel_path.startswith(pattern):
            return "repersonalise"
    for pattern in SAFE_MERGE_PATTERNS:
        if rel_path.startswith(pattern):
            return "safe"
    return "safe"


def main():
    fork_hash = get_fork_hash()
    current_hash = compute_current_hash()

    if fork_hash is None:
        print("No fork version found at:", VERSION_FILE)
        print("Run personalise/fork.py first to create a personalised site.")
        sys.exit(1)

    if fork_hash == current_hash:
        print("Your fork is up to date with the current framework version.")
        print(f"  Version: {current_hash}")
        sys.exit(0)

    print("Framework has changed since your fork was built.")
    print(f"  Fork version:    {fork_hash}")
    print(f"  Current version: {current_hash}")
    print()

    # Detailed file-level analysis is only possible if we stored per-file
    # hashes. For now, categorise all customisable files as potentially changed.
    print("=== Safe Direct Merge ===")
    print("Changes to methodology text, typo fixes, new reference pages.")
    print("These can be pulled in without re-personalisation.")
    for pattern in SAFE_MERGE_PATTERNS:
        print(f"  - {pattern}")
    print()

    print("=== Requires Re-personalisation ===")
    print("Changes to templates, worked example structure, decision trees,")
    print("or personalisation prompts. Pull changes, then re-run fork.py.")
    for pattern in REQUIRES_REPERSONALISATION:
        print(f"  - {pattern}")
    print()

    print("=== Review Recommended ===")
    print("Changes to stage definitions or the config schema. May require")
    print("updates to your org config before re-personalisation.")
    for pattern in REVIEW_RECOMMENDED:
        print(f"  - {pattern}")
    print()

    print("To update your fork:")
    print("  1. git pull upstream main")
    print("  2. python personalise/fork.py --config personalise/org-config.yaml")


if __name__ == "__main__":
    main()
