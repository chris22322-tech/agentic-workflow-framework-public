#!/usr/bin/env python3
"""Template-methodology sync checker.

Reads manifest.json, re-hashes each methodology source file, and reports
whether any methodology has changed since the templates were last verified.

Usage:
    python templates/check_sync.py              # summary report
    python templates/check_sync.py --details    # include change context
"""

import hashlib
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
MANIFEST_PATH = SCRIPT_DIR / "manifest.json"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def load_manifest() -> dict:
    with open(MANIFEST_PATH) as f:
        return json.load(f)


def check_sync(details: bool = False) -> int:
    manifest = load_manifest()
    templates = manifest["templates"]

    drifted = []
    missing_source = []
    missing_template = []
    in_sync = []

    # Track methodology files already checked to avoid duplicate work
    methodology_status: dict[str, dict] = {}

    for entry in templates:
        template_path = SCRIPT_DIR / entry["file"]
        source_path = PROJECT_ROOT / entry["methodology_source"]

        # Check template file exists
        if not template_path.exists():
            missing_template.append(entry)
            continue

        # Check methodology source exists
        if not source_path.exists():
            missing_source.append(entry)
            continue

        # Hash methodology source (cache results)
        source_key = entry["methodology_source"]
        if source_key not in methodology_status:
            current_hash = sha256_file(source_path)
            methodology_status[source_key] = {
                "current_hash": current_hash,
                "changed": current_hash != entry["methodology_hash"],
            }

        if methodology_status[source_key]["changed"]:
            drifted.append({
                "entry": entry,
                "current_hash": methodology_status[source_key]["current_hash"],
            })
        else:
            in_sync.append(entry)

    # Print report
    print()
    print("Template Sync Check")
    print("=" * 60)
    print()

    max_name = max(len(e["file"]) for e in templates) if templates else 30

    for entry in in_sync:
        print(f"  {entry['file']:<{max_name}}  \u2713 In sync")

    for item in drifted:
        entry = item["entry"]
        print(f"  {entry['file']:<{max_name}}  \u26a0 Methodology changed ({entry['methodology_source']})")

    for entry in missing_source:
        print(f"  {entry['file']:<{max_name}}  \u2717 Methodology source missing ({entry['methodology_source']})")

    for entry in missing_template:
        print(f"  {entry['file']:<{max_name}}  \u2717 Template file missing")

    print()

    # Summary
    total = len(templates)
    ok = len(in_sync)
    drift_count = len(drifted)
    miss_src = len(missing_source)
    miss_tpl = len(missing_template)

    if drift_count == 0 and miss_src == 0 and miss_tpl == 0:
        print(f"All {total} templates are in sync with their methodology sources.")
    else:
        parts = []
        if drift_count:
            parts.append(f"{drift_count} template(s) may need updating")
        if miss_src:
            parts.append(f"{miss_src} methodology source(s) missing")
        if miss_tpl:
            parts.append(f"{miss_tpl} template file(s) missing")
        print(f"{ok}/{total} in sync. " + ". ".join(parts) + ".")

    # Details
    if details and drifted:
        print()
        print("-" * 60)
        print("Change Details")
        print("-" * 60)
        for item in drifted:
            entry = item["entry"]
            print()
            print(f"  Template:    {entry['file']}")
            print(f"  Source:      {entry['methodology_source']}")
            print(f"  Stored hash: {entry['methodology_hash'][:16]}...")
            print(f"  Current:     {item['current_hash'][:16]}...")
            print(f"  Last verified: {entry['last_verified']}")
            print()
            print("  Action: Review template columns against current methodology,")
            print("          update template if needed, then re-run with --update.")

    if not details and drift_count > 0:
        print()
        print("Run with --details for change summary.")

    print()
    return 1 if (drift_count > 0 or miss_src > 0 or miss_tpl > 0) else 0


def update_manifest():
    """Re-hash all methodology sources and update manifest in place."""
    manifest = load_manifest()
    from datetime import datetime, timezone

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    updated = 0

    for entry in manifest["templates"]:
        source_path = PROJECT_ROOT / entry["methodology_source"]
        template_path = SCRIPT_DIR / entry["file"]

        if source_path.exists():
            new_hash = sha256_file(source_path)
            if new_hash != entry["methodology_hash"]:
                entry["methodology_hash"] = new_hash
                entry["last_verified"] = now
                updated += 1

        if template_path.exists():
            new_hash = sha256_file(template_path)
            if new_hash != entry["template_hash"]:
                entry["template_hash"] = new_hash
                entry["last_verified"] = now

    manifest["generated"] = now

    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")

    print(f"Manifest updated. {updated} methodology hash(es) refreshed.")


if __name__ == "__main__":
    args = sys.argv[1:]

    if "--update" in args:
        update_manifest()
        sys.exit(0)

    details = "--details" in args
    sys.exit(check_sync(details))
