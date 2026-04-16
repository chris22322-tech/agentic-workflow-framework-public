# Template Sync Guide

This guide explains how to keep the CSV/XLSX/DOCX templates in sync with the methodology documentation they derive from.

## How It Works

Each template is linked to a methodology source file (e.g., `docs/stages/01-decompose.md`). The `manifest.json` records a SHA-256 hash of each methodology file at the time the templates were last verified. When a methodology file changes, the hash no longer matches, and `check_sync.py` flags it.

## When to Run the Sync Check

Run the check whenever you:

- **Change a methodology page** (`docs/stages/*.md`) — to see which templates reference it
- **Before a release or handoff** — to confirm nothing drifted
- **After an automated edit session** — Claude agents may update methodology without updating templates

```bash
python templates/check_sync.py
```

## Reading the Report

```
stage1-workflow-inventory.csv    ✓ In sync
stage2-scoring-matrix.csv       ⚠ Methodology changed (docs/stages/02-select.md)
```

- **✓ In sync** — the methodology file hasn't changed since the template was last verified
- **⚠ Methodology changed** — the methodology file has been modified; the template may need updating
- **✗ Missing** — a file referenced in the manifest doesn't exist

## How to Fix Drift

When a template is flagged:

### 1. Check what changed

```bash
python templates/check_sync.py --details
```

This shows which methodology file changed and when the template was last verified.

### 2. Decide if the template needs updating

- **Structural change** (columns added/removed/renamed in the methodology's table definitions) → update the CSV template headers and example rows
- **Content-only change** (wording tweaks, expanded explanations, additional examples) → templates are probably fine, just update the manifest hash

### 3. Update the template (if needed)

1. Open the flagged CSV in a text editor or spreadsheet
2. Compare its columns against the methodology page's table definitions
3. Add, remove, or rename columns as needed
4. Update any example rows that reference changed concepts

### 4. Rebuild XLSX workbooks (if CSVs changed)

```bash
python templates/build_xlsx.py
```

### 5. Update the manifest

After verifying (and optionally updating) templates, refresh the manifest hashes:

```bash
python templates/check_sync.py --update
```

This re-hashes all methodology sources and templates, recording the current state as "verified."

## Manifest Structure

`manifest.json` contains:

| Field | Purpose |
|---|---|
| `file` | Template filename |
| `stage` | Which methodology stage (1-6) |
| `format` | csv, xlsx, or docx |
| `methodology_source` | Path to the methodology doc this template derives from |
| `worked_example_source` | Path to the worked example that demonstrates this template |
| `columns` | CSV column headers (for CSV templates only) |
| `methodology_hash` | SHA-256 of the methodology file at last verification |
| `template_hash` | SHA-256 of the template file at last verification |
| `last_verified` | Timestamp of last verification |

## Quick Reference

| Task | Command |
|---|---|
| Check sync status | `python templates/check_sync.py` |
| Check with details | `python templates/check_sync.py --details` |
| Update manifest after review | `python templates/check_sync.py --update` |
| Rebuild XLSX from CSVs | `python templates/build_xlsx.py` |
