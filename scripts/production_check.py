#!/usr/bin/env python3
"""Production readiness verification script.

Automates the checks from docs/PRODUCTION_CHECKLIST.md that can be automated:
  - mkdocs build --strict (zero warnings)
  - Content gating (banned terms — empty in public build, see sync script)
  - docs/downloads/ files are non-empty
  - templates/check_sync.py passes
  - mkdocs.yml nav entries resolve to existing files

Usage:
    python scripts/production_check.py
"""

import os
import re
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
DOWNLOADS_DIR = DOCS_DIR / "downloads"
MKDOCS_YML = PROJECT_ROOT / "mkdocs.yml"
TEMPLATES_DIR = PROJECT_ROOT / "templates"

BANNED_TERMS: list[tuple[str, str]] = []  # public build: empty (see sync_to_public.sh)

# Directories to exclude from banned-term scanning
SCAN_DIRS = [DOCS_DIR, TEMPLATES_DIR]
SCAN_EXTENSIONS = {".md", ".yml", ".yaml", ".txt", ".html", ".csv", ".json", ".py"}


class CheckResult:
    def __init__(self, name: str):
        self.name = name
        self.passed = True
        self.details: list[str] = []

    def fail(self, detail: str = ""):
        self.passed = False
        if detail:
            self.details.append(detail)

    def info(self, detail: str):
        self.details.append(detail)


def check_mkdocs_build() -> CheckResult:
    """Run mkdocs build --strict and check for zero warnings."""
    result = CheckResult("mkdocs build --strict")
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "mkdocs", "build", "--strict"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=120,
        )
        if proc.returncode != 0:
            result.fail("Build failed or produced warnings")
            # Show up to 10 lines of stderr for context
            for line in proc.stderr.strip().splitlines()[:10]:
                result.fail(f"  {line}")
        else:
            result.info("Build completed with zero warnings")
    except FileNotFoundError:
        result.fail("mkdocs not installed — run: pip install mkdocs mkdocs-material")
    except subprocess.TimeoutExpired:
        result.fail("Build timed out after 120s")
    return result


def check_banned_terms() -> CheckResult:
    """Grep docs/ and templates/ for banned terms."""
    result = CheckResult("Content gating (banned terms)")
    hits = 0
    for scan_dir in SCAN_DIRS:
        if not scan_dir.exists():
            continue
        for path in scan_dir.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix.lower() not in SCAN_EXTENSIONS:
                continue
            try:
                content = path.read_text(errors="ignore")
            except Exception:
                continue
            rel = path.relative_to(PROJECT_ROOT)
            for pattern, label in BANNED_TERMS:
                for match in re.finditer(pattern, content, re.IGNORECASE):
                    line_num = content[:match.start()].count("\n") + 1
                    result.fail(f"  {rel}:{line_num} — found \"{label}\"")
                    hits += 1
    if hits == 0:
        result.info("No banned terms found")
    return result


def check_downloads() -> CheckResult:
    """Check that all files in docs/downloads/ exist and are non-empty."""
    result = CheckResult("Download files are non-empty")
    if not DOWNLOADS_DIR.exists():
        result.fail(f"Directory missing: {DOWNLOADS_DIR.relative_to(PROJECT_ROOT)}")
        return result

    files = [f for f in DOWNLOADS_DIR.iterdir() if f.is_file()]
    if not files:
        result.fail("No files found in docs/downloads/")
        return result

    empty = []
    for f in sorted(files):
        if f.stat().st_size == 0:
            empty.append(f.name)
    if empty:
        for name in empty:
            result.fail(f"  Empty file: docs/downloads/{name}")
    else:
        result.info(f"All {len(files)} download files are non-empty")
    return result


def check_template_sync() -> CheckResult:
    """Run templates/check_sync.py and report pass/fail."""
    result = CheckResult("Template-methodology sync")
    check_script = TEMPLATES_DIR / "check_sync.py"
    if not check_script.exists():
        result.fail("templates/check_sync.py not found")
        return result

    try:
        proc = subprocess.run(
            [sys.executable, str(check_script)],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if proc.returncode != 0:
            result.fail("Templates are out of sync with methodology")
            for line in proc.stdout.strip().splitlines():
                if "\u26a0" in line or "\u2717" in line:
                    result.fail(f"  {line.strip()}")
        else:
            result.info("All templates in sync")
    except subprocess.TimeoutExpired:
        result.fail("check_sync.py timed out after 30s")
    return result


# Forbidden platform terms: the framework is platform-neutral and must not name
# specific agent frameworks, SDKs, or vendor products in user-facing docs. These
# are allowed only on the Choose a Platform page (which is where platform names
# belong) and in files explicitly listed in PLATFORM_ALLOW.
PLATFORM_FORBIDDEN = [
    r"LangGraph\b",
    r"langgraph\b",
    r"langchain\b",
    r"Gemini Agent Builder",
    r"Agent Designer",
    r"\bADK\b",
    r"Vertex AI Agent Builder",
    r"Dialogflow CX",
    r"\bMCP\b",
    r"McpToolset",
    r"OpenAPIToolset",
    r"FunctionTool",
    r"MultiServerMCPClient",
    r"TypedDict",
    r"StateGraph",
    r"interrupt\(\)",
    r"MemorySaver",
    r"LangSmith",
    r"Gemini \(",
    r"Playbook \(",
]

PLATFORM_ALLOW = {
    # The platform-choice page is the one place platform names are allowed.
    "docs/getting-started/choose-a-platform.md",
    # The cheat-sheet appendix (added as part of Proposal 4) lists platforms by name.
    "docs/reference/platform-cheatsheet.md",
}


def check_platform_neutrality() -> CheckResult:
    """Fail if any user-facing doc references a specific agent framework, SDK,
    or vendor product outside the explicit allowlist.

    This enforces the framework's platform-neutral claim. If you genuinely need
    to reference a specific platform, either add the file to PLATFORM_ALLOW
    (for framework-level pages that intentionally name platforms) or rewrite
    the content in platform-neutral language.
    """
    result = CheckResult("Platform-neutral content")
    pattern = re.compile("|".join(PLATFORM_FORBIDDEN))
    scan_extensions = {".md", ".html"}

    hits: list[tuple[str, int, str]] = []
    for path in DOCS_DIR.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in scan_extensions:
            continue

        rel = str(path.relative_to(PROJECT_ROOT))
        if rel in PLATFORM_ALLOW:
            continue

        try:
            text = path.read_text(errors="ignore")
        except Exception:
            continue

        for match in pattern.finditer(text):
            line_num = text[: match.start()].count("\n") + 1
            hits.append((rel, line_num, match.group()))

    if hits:
        # Group by file for readability
        by_file: dict[str, list[tuple[int, str]]] = {}
        for rel, line_num, term in hits:
            by_file.setdefault(rel, []).append((line_num, term))
        total = len(hits)
        result.fail(f"Found {total} platform reference(s) in {len(by_file)} file(s) outside the allowlist")
        for rel in sorted(by_file.keys())[:10]:  # cap output
            for line_num, term in by_file[rel][:3]:
                result.fail(f"  {rel}:{line_num} — {term}")
            if len(by_file[rel]) > 3:
                result.fail(f"  {rel}: ... and {len(by_file[rel]) - 3} more")
        if len(by_file) > 10:
            result.fail(f"  ... and {len(by_file) - 10} more files")
    else:
        result.info("No platform-specific references found outside the allowlist")
    return result


def check_cheatsheet_freshness() -> CheckResult:
    """Fail if the platform cheat sheet is more than 180 days stale.

    The cheat sheet names specific vendor products and links to their current
    docs. Unlike the rest of the framework, this page is allowed to name
    platforms because it is explicitly a maintainer's current reference — but
    that only holds as long as the reference is actually current. This check
    reads the `last_verified` frontmatter field and fails if it's older than
    180 days.
    """
    result = CheckResult("Platform cheat sheet freshness")
    cheatsheet = DOCS_DIR / "reference" / "platform-cheatsheet.md"
    if not cheatsheet.exists():
        result.info("Platform cheat sheet not present — skipping")
        return result

    from datetime import date, datetime
    text = cheatsheet.read_text()
    m = re.search(r"^last_verified:\s*(\d{4}-\d{2}-\d{2})", text, re.MULTILINE)
    if not m:
        result.fail("No `last_verified` frontmatter field found")
        return result

    try:
        verified = datetime.strptime(m.group(1), "%Y-%m-%d").date()
    except ValueError:
        result.fail(f"Invalid last_verified date format: {m.group(1)}")
        return result

    today = date.today()
    age_days = (today - verified).days
    if age_days > 180:
        result.fail(
            f"Platform cheat sheet is {age_days} days old (last verified {verified}). "
            f"Re-verify the cells and update the frontmatter date."
        )
    else:
        result.info(f"Last verified {verified} ({age_days} days ago)")
    return result


def check_personalise_smoke() -> CheckResult:
    """Static smoke test of the personalisation engine.

    Verifies that fork.py's declared inputs (COPY_AS_IS and CUSTOMISATIONS)
    all resolve to existing files in docs/, and that every CUSTOMISATIONS
    entry has a matching prompt file in personalise/prompts/customise/.
    Also verifies that the personalisation prompts are free of references
    to files that have been deleted from docs/.

    This catches the most common personalisation-engine breakage: a
    methodology-level rewrite that removes or renames files the fork script
    depends on, or leaves prompts referencing content that no longer exists.
    """
    result = CheckResult("Personalisation engine smoke test")

    fork_py = PROJECT_ROOT / "personalise" / "fork.py"
    if not fork_py.exists():
        result.info("personalise/fork.py not present — skipping")
        return result

    # Extract COPY_AS_IS and CUSTOMISATIONS by importing fork.py.
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("fork", str(fork_py))
        fork_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(fork_module)
    except Exception as e:
        result.fail(f"Could not import personalise/fork.py: {e}")
        return result

    copy_as_is = getattr(fork_module, "COPY_AS_IS", [])
    customisations = getattr(fork_module, "CUSTOMISATIONS", {})
    prompts_dir = PROJECT_ROOT / "personalise" / "prompts" / "customise"

    missing = []

    for p in copy_as_is:
        if not (DOCS_DIR / p).exists():
            missing.append(f"COPY_AS_IS path not found: docs/{p}")

    for source, prompt in customisations.items():
        source_path = DOCS_DIR / source
        if not source_path.exists():
            missing.append(f"CUSTOMISATIONS source not found: docs/{source}")
        prompt_path = prompts_dir / prompt
        if not prompt_path.exists():
            missing.append(f"CUSTOMISATIONS prompt not found: personalise/prompts/customise/{prompt}")

    # Scan prompts for references to deleted platform-specific files.
    deleted_refs = re.compile(
        r"04-design-langgraph|04-design-gemini|05-build-langgraph|05-build-gemini"
        r"|design-document-gemini|langgraph-patterns|worked-example/design-gemini"
        r"|worked-example/build-gemini"
    )
    prompts_root = PROJECT_ROOT / "personalise" / "prompts"
    if prompts_root.exists():
        for path in prompts_root.rglob("*.md"):
            try:
                text = path.read_text(errors="ignore")
            except Exception:
                continue
            if deleted_refs.search(text):
                rel = path.relative_to(PROJECT_ROOT)
                missing.append(f"Prompt references deleted file: {rel}")

    if missing:
        for m in missing:
            result.fail(f"  {m}")
    else:
        total_paths = len(copy_as_is) + len(customisations)
        result.info(f"All {total_paths} fork.py inputs resolve; no stale prompt references")
    return result


def check_nav_entries() -> CheckResult:
    """Check that every nav entry in mkdocs.yml resolves to an existing file."""
    result = CheckResult("mkdocs.yml nav entries resolve")
    if not MKDOCS_YML.exists():
        result.fail("mkdocs.yml not found")
        return result

    content = MKDOCS_YML.read_text()

    # Extract all .md references from nav section
    # Match patterns like: path/to/file.md
    md_refs = re.findall(r":\s*([^\s#]+\.md)\s*$", content, re.MULTILINE)
    # Also match bare entries like: - path/to/file.md
    md_refs += re.findall(r"^\s*-\s+([^\s:]+\.md)\s*$", content, re.MULTILINE)

    missing = []
    for ref in md_refs:
        full_path = DOCS_DIR / ref
        if not full_path.exists():
            missing.append(ref)

    if missing:
        for m in missing:
            result.fail(f"  Missing: docs/{m}")
    else:
        result.info(f"All {len(md_refs)} nav entries resolve")
    return result


def main():
    print()
    print("=" * 60)
    print("  Production Readiness Check")
    print("=" * 60)
    print()

    checks = [
        check_mkdocs_build,
        check_banned_terms,
        check_platform_neutrality,
        check_cheatsheet_freshness,
        check_downloads,
        check_template_sync,
        check_personalise_smoke,
        check_nav_entries,
    ]

    results: list[CheckResult] = []
    for check_fn in checks:
        r = check_fn()
        results.append(r)

        status = "\u2705 PASS" if r.passed else "\u274c FAIL"
        print(f"  {status}  {r.name}")
        for detail in r.details:
            print(f"         {detail}")
        print()

    # Summary
    passed = sum(1 for r in results if r.passed)
    total = len(results)
    print("-" * 60)
    print(f"  Result: {passed}/{total} checks passed")
    if passed == total:
        print("  Status: READY FOR PRODUCTION")
    else:
        print("  Status: NOT READY — fix failures above")
    print("-" * 60)
    print()

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
