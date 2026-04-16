#!/usr/bin/env python3
"""
Fork script for Layer 3: Framework Personalisation.

Reads org-config.yaml and produces a personalised version of the entire
framework site — with org-specific worked examples, pre-filled templates,
extended glossary, and customised decision trees.

Usage:
    python personalise/fork.py --config personalise/org-config.yaml
"""

import argparse
import hashlib
import logging
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)


class _PreservedYamlTag:
    """Wrapper that round-trips ``!!python/name:...`` tags through load→dump.

    mkdocs.yml uses these tags for pymdownx/material emoji and fence
    extensions. ``yaml.SafeLoader`` refuses them by default, so we register
    a pass-through constructor and a matching representer so they survive
    load→modify→dump unchanged.
    """
    __slots__ = ("tag_suffix",)

    def __init__(self, tag_suffix: str):
        self.tag_suffix = tag_suffix


def _construct_python_name_tag(loader, tag_suffix, node):  # noqa: ARG001
    return _PreservedYamlTag(tag_suffix)


def _represent_python_name_tag(dumper, data):
    return dumper.represent_scalar(
        f"tag:yaml.org,2002:python/name:{data.tag_suffix}", ""
    )


yaml.SafeLoader.add_multi_constructor(
    "tag:yaml.org,2002:python/name:", _construct_python_name_tag
)
yaml.SafeDumper.add_representer(_PreservedYamlTag, _represent_python_name_tag)
# Also register on the full Dumper so plain yaml.dump() round-trips correctly.
yaml.Dumper.add_representer(_PreservedYamlTag, _represent_python_name_tag)


REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
PROMPTS_DIR = REPO_ROOT / "personalise" / "prompts" / "customise"
OUTPUT_DIR = REPO_ROOT / "personalise" / "output" / "site"
APP_GUIDE = REPO_ROOT / "personalise" / "output" / "APPLICATION-GUIDE.md"

# Pages that are copied unchanged (methodology is universal).
COPY_AS_IS = [
    "stages",
    "worked-example",
    "worked-example-ba",
    "worked-example-se",
]

# Sections that get personalised, mapped to their prompt file.
CUSTOMISATIONS = {
    "getting-started/index.md": "getting-started.md",
    "getting-started/quick-start.md": "quick-start.md",
    "reference/glossary.md": "glossary.md",
    "reference/decision-trees.md": "decision-trees.md",
    "reference/checklist.md": "checklist.md",
    "blank-templates": "templates.md",
}


def load_config(config_path: Path) -> dict:
    """Load and validate the org config."""
    with open(config_path) as f:
        config = yaml.safe_load(f)
    if not config or "organisation" not in config:
        log.error("Invalid org config: missing 'organisation' key.")
        sys.exit(1)
    return config


def framework_version_hash() -> str:
    """Compute a hash of the framework docs directory for version tracking."""
    h = hashlib.sha256()
    for p in sorted(DOCS_DIR.rglob("*.md")):
        h.update(p.read_bytes())
    return h.hexdigest()[:12]


def _verify_repo_layout() -> None:
    """Exit early with a clear error if REPO_ROOT does not look like a framework repo.

    Guards against fork.py being copied out of its expected location, where
    ``Path(__file__).resolve().parent.parent`` would resolve to an unrelated
    directory and produce confusing downstream errors.
    """
    missing = [
        marker for marker in ("docs", "personalise", "mkdocs.yml")
        if not (REPO_ROOT / marker).exists()
    ]
    if missing:
        log.error(
            "fork.py cannot locate the framework repo at %s. "
            "Missing expected entries: %s. "
            "Run fork.py from personalise/fork.py in the framework repo root, "
            "not from a copied location.",
            REPO_ROOT, ", ".join(missing),
        )
        sys.exit(1)


def _check_cli_available(cli: str) -> None:
    """Exit early if the chosen CLI binary is not installed.

    Called before any filesystem mutation so a missing CLI does not leave a
    half-built output directory behind (MISSING-4 from the empirical audit).
    """
    binary = "gemini" if cli == "gemini" else "claude"
    if shutil.which(binary) is None:
        cli_name = "Gemini CLI" if cli == "gemini" else "Claude CLI"
        log.error(
            "%s not found on PATH. Install %s before running fork.py, "
            "or re-run with --cli <alternative>. No files have been written.",
            cli_name, binary,
        )
        sys.exit(1)


def _build_cli_command(cli: str, instruction: str) -> list[str]:
    """Build the subprocess command for the chosen CLI.

    Gemini CLI v0.38.0+ uses ``-y`` for YOLO (auto-approve tool calls) and
    ``-p`` for non-interactive prompt mode. The older ``gemini chat -m <msg>``
    form silently misinterprets ``chat`` as a positional prompt and ``-m`` as
    ``--model``, producing garbage output — do not use it.
    """
    if cli == "gemini":
        return ["gemini", "-y", "-p", instruction]
    return [
        "claude", "-p", instruction,
        "--allowedTools", "Read,Write,Glob,Grep",
        "--max-turns", "25",
    ]


def run_llm_prompt(prompt_path: Path, source_path: Path, output_path: Path,
                   config_path: Path, cli: str = "claude",
                   extra_context: str = "") -> bool:
    """Run a customisation prompt via the chosen CLI. Returns True on success."""
    prompt_text = prompt_path.read_text()

    instruction = (
        f"{prompt_text}\n\n"
        f"---\n"
        f"Read the organisation config from: {config_path}\n"
        f"Read the source file(s) from: {source_path}\n"
    )
    if APP_GUIDE.exists():
        instruction += f"Read the application guide from: {APP_GUIDE}\n"
    if extra_context:
        instruction += f"\n{extra_context}\n"
    instruction += f"\nWrite the personalised output to: {output_path}\n"

    cmd = _build_cli_command(cli, instruction)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,
        )
        if result.returncode != 0:
            log.warning("Prompt failed for %s: %s", source_path, result.stderr[:200])
            return False
        return True
    except FileNotFoundError:
        cli_name = "Gemini CLI" if cli == "gemini" else "Claude CLI"
        log.error("%s not found. Install it or use the GitHub Action.", cli_name)
        sys.exit(1)
    except subprocess.TimeoutExpired:
        log.warning("Prompt timed out for %s", source_path)
        return False


def copy_directory(src: Path, dst: Path) -> None:
    """Copy a directory tree, creating parents as needed."""
    if src.is_dir():
        shutil.copytree(src, dst, dirs_exist_ok=True)
    elif src.is_file():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def copy_generic_pages(output_docs: Path) -> None:
    """Copy pages that stay unchanged (methodology stages, etc.)."""
    for rel_path in COPY_AS_IS:
        src = DOCS_DIR / rel_path
        dst = output_docs / rel_path
        if src.exists():
            copy_directory(src, dst)
            log.info("Copied unchanged: %s", rel_path)


def personalise_sections(output_docs: Path, config_path: Path,
                         cli: str = "claude") -> list[str]:
    """Run customisation prompts for each personalisable section."""
    failures = []
    for rel_path, prompt_name in CUSTOMISATIONS.items():
        src = DOCS_DIR / rel_path
        dst = output_docs / rel_path
        prompt = PROMPTS_DIR / prompt_name

        if not src.exists():
            log.warning("Source not found, skipping: %s", src)
            continue

        dst.parent.mkdir(parents=True, exist_ok=True)
        log.info("Personalising: %s", rel_path)

        success = run_llm_prompt(prompt, src, dst, config_path, cli=cli)
        if not success:
            log.warning("Falling back to generic: %s", rel_path)
            copy_directory(src, dst)
            failures.append(rel_path)

    return failures


def generate_worked_examples(output_docs: Path, config: dict,
                             config_path: Path,
                             cli: str = "claude") -> list[str]:
    """Generate one worked example per role in the org config."""
    failures = []
    roles = config.get("roles", [])
    org_name = config["organisation"].get("name", "Organisation")
    prompt = PROMPTS_DIR / "worked-example.md"

    for role in roles:
        role_name = role.get("name", "").strip()
        if not role_name:
            continue

        slug = role_name.lower().replace(" ", "-")
        example_dir = output_docs / f"worked-example-{slug}"
        example_dir.mkdir(parents=True, exist_ok=True)

        # Write an index page for the worked example.
        index_content = (
            f"# Worked Example ({role_name})\n\n"
            f"A complete Stage 1-6 worked example for the **{role_name}** role "
            f"at {org_name}.\n\n"
            f"This example was generated from {org_name}'s organisation config "
            f"and follows the same structure as the generic worked examples.\n\n"
            f"| Stage | Page |\n|---|---|\n"
            f"| 1. Decompose | [Decompose](decompose.md) |\n"
            f"| 2. Select | [Select](select.md) |\n"
            f"| 3. Scope | [Scope](scope.md) |\n"
            f"| 4. Design | [Design](design.md) |\n"
            f"| 5. Build | [Build](build.md) |\n"
            f"| 6. Evaluate | [Evaluate](evaluate.md) |\n"
        )
        (example_dir / "index.md").write_text(index_content)

        log.info("Generating worked example for: %s", role_name)

        extra = (
            f"Generate the worked example for role: {role_name}\n"
            f"Role description: {role.get('description', '')}\n"
            f"Write the six stage files (decompose.md, select.md, scope.md, "
            f"design.md, build.md, evaluate.md) into: {example_dir}\n"
        )

        success = run_llm_prompt(
            prompt, DOCS_DIR / "worked-example", example_dir,
            config_path, cli=cli, extra_context=extra,
        )
        if not success:
            failures.append(f"worked-example-{slug}")
            log.warning("Worked example generation failed for: %s", role_name)

    return failures


# Personalise/*.md pages that canonical docs link to but fork.py excludes.
# See write_personalise_stubs() below for why these exist.
PERSONALISE_STUB_PAGES = [
    "personalise/index.md",
    "personalise/apply.md",
    "personalise/learn.md",
    "personalise/customise.md",
    "personalise/business-case.md",
    "personalise/change-management.md",
]


def write_personalise_stubs(output_docs: Path, org_name: str) -> None:
    """Create stub pages for every personalise/* file the canonical docs link to.

    fork.py deliberately excludes ``personalise/*`` from the output because it
    is meta-content: the tool that produced this site, not part of the site's
    methodology. But several canonical pages (framework-overview.md,
    enablement/index.md, stages/02-select.md, worked-example/build.md) have
    hardcoded markdown links to ``personalise/*`` pages. Without these stubs,
    those links become 404s in the forked site.

    Each stub explains why the page exists and points readers back to the
    upstream framework if they want the personalise feature itself.
    """
    stub = (
        "# Personalise (meta-content)\n"
        "\n"
        f"This site was personalised for **{org_name}** using the Agentic "
        "Workflow Framework's personalise feature. Personalisation is "
        "**meta-content** — it's the tool that produced this site, not part of "
        "the site's methodology.\n"
        "\n"
        "If you want to personalise the framework for your own organisation, "
        "see the **upstream** Agentic Workflow Framework repository. It "
        "contains the Application Guide, Training Materials, and Custom Site "
        "generators, plus the Business Case template and the Change Management "
        "mapping.\n"
        "\n"
        "!!! info \"Why this page exists\"\n"
        "    An earlier page in this site linked here because the personalise "
        "section lives in the canonical framework documentation but is "
        "deliberately excluded from forked sites. This stub prevents a 404 "
        "and explains why you landed here.\n"
    )
    for rel_path in PERSONALISE_STUB_PAGES:
        dst = output_docs / rel_path
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(stub)
        log.info("Wrote personalise stub: %s", rel_path)


def copy_remaining_pages(output_docs: Path) -> None:
    """Copy any docs/ pages not already handled."""
    for src_path in DOCS_DIR.rglob("*.md"):
        rel = src_path.relative_to(DOCS_DIR)
        dst = output_docs / rel

        # Skip the personalise section — it is meta-content.
        if str(rel).startswith("personalise"):
            continue

        if not dst.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_path, dst)

    # Copy non-markdown assets (images, downloads, etc.).
    for src_path in DOCS_DIR.rglob("*"):
        if src_path.is_file() and src_path.suffix != ".md":
            rel = src_path.relative_to(DOCS_DIR)
            if str(rel).startswith("personalise"):
                continue
            dst = output_docs / rel
            if not dst.exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_path, dst)


def write_mkdocs_config(config: dict, output_site: Path,
                        generated_roles: list[str]) -> None:
    """Write a customised mkdocs.yml for the forked site."""
    org_name = config["organisation"].get("name", "Organisation")
    mkdocs_src = REPO_ROOT / "mkdocs.yml"
    mkdocs_config = yaml.safe_load(mkdocs_src.read_text())

    # Update site name and description.
    mkdocs_config["site_name"] = f"{org_name} — Agentic Workflow Framework"
    mkdocs_config["site_description"] = (
        f"Agentic Workflow Framework personalised for {org_name}"
    )

    # Build nav entries for generated worked examples and prepend them to the
    # existing "Worked Examples" umbrella so personalised examples appear above
    # the generic CSM/BA/SE examples in the dropdown.
    nav = mkdocs_config.get("nav", [])
    roles = config.get("roles", [])

    personalised_entries = []
    for role in roles:
        role_name = role.get("name", "").strip()
        if not role_name:
            continue
        slug = role_name.lower().replace(" ", "-")
        example_dir = f"worked-example-{slug}"
        personalised_entries.append({
            f"{role_name} ({org_name})": [
                {f"{example_dir}/index.md": f"{example_dir}/index.md"},
                {"Decompose": f"{example_dir}/decompose.md"},
                {"Select": f"{example_dir}/select.md"},
                {"Scope": f"{example_dir}/scope.md"},
                {"Design": f"{example_dir}/design.md"},
                {"Build": f"{example_dir}/build.md"},
                {"Evaluate": f"{example_dir}/evaluate.md"},
            ]
        })

    if personalised_entries:
        inserted = False
        for item in nav:
            if isinstance(item, dict) and "Worked Examples" in item:
                # Prepend personalised entries above the generic ones.
                existing = item["Worked Examples"] or []
                item["Worked Examples"] = personalised_entries + existing
                inserted = True
                break
        if not inserted:
            # Fallback: canonical mkdocs.yml was restructured or the umbrella
            # was renamed. Append a new "Worked Examples" umbrella at the end
            # so the personalised content is still reachable.
            log.warning(
                "No 'Worked Examples' umbrella found in nav — appending a new "
                "one with personalised entries only."
            )
            nav.append({"Worked Examples": personalised_entries})

    # Remove the Personalise section from nav (it is meta-content).
    nav = [item for item in nav if not _nav_item_is("Personalise", item)]

    mkdocs_config["nav"] = nav

    with open(output_site / "mkdocs.yml", "w") as f:
        # Use safe_dump explicitly so the _PreservedYamlTag representer fires
        # (safe_dump routes through SafeDumper where the representer is
        # registered; plain yaml.dump uses Dumper).
        yaml.safe_dump(mkdocs_config, f, default_flow_style=False, sort_keys=False)

    log.info("Wrote customised mkdocs.yml")


def _nav_item_is(label: str, item) -> bool:
    """Check if a nav item has the given top-level label."""
    if isinstance(item, dict):
        return label in item
    return False


def write_version_metadata(output_site: Path) -> None:
    """Write the framework version hash for drift detection."""
    version_file = output_site / ".framework-version"
    version_hash = framework_version_hash()
    version_file.write_text(version_hash + "\n")
    log.info("Framework version hash: %s", version_hash)


def build_site(output_site: Path) -> bool:
    """Run mkdocs build to verify the forked site."""
    try:
        result = subprocess.run(
            ["mkdocs", "build"],
            cwd=output_site,
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            log.error("mkdocs build failed:\n%s", result.stderr[:500])
            return False
        log.info("Site built successfully.")
        return True
    except FileNotFoundError:
        log.warning("mkdocs not found — skipping build verification.")
        return True
    except subprocess.TimeoutExpired:
        log.warning("mkdocs build timed out.")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Generate a personalised fork of the framework site."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=REPO_ROOT / "personalise" / "org-config.yaml",
        help="Path to the organisation config file.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=OUTPUT_DIR,
        help="Output directory for the forked site.",
    )
    parser.add_argument(
        "--cli",
        choices=["claude", "gemini"],
        default="claude",
        help="Which AI CLI to use for prompt execution (default: claude).",
    )
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="Skip the mkdocs build verification step.",
    )
    args = parser.parse_args()

    # Fail-fast checks before we touch the filesystem.
    _verify_repo_layout()
    _check_cli_available(args.cli)

    config_path = args.config.resolve()
    output_site = args.output.resolve()
    output_docs = output_site / "docs"

    if not config_path.exists():
        log.error("Config not found: %s", config_path)
        sys.exit(1)

    config = load_config(config_path)
    org_name = config["organisation"].get("name", "Organisation")
    log.info("Personalising framework for: %s", org_name)

    # Clean and recreate output directory.
    if output_site.exists():
        shutil.rmtree(output_site)
    output_docs.mkdir(parents=True)

    # Step 1: Copy pages that stay unchanged.
    copy_generic_pages(output_docs)

    # Step 2: Run personalisation prompts.
    failures = personalise_sections(output_docs, config_path, cli=args.cli)

    # Step 3: Generate org-specific worked examples.
    role_names = [r.get("name", "").strip() for r in config.get("roles", []) if r.get("name")]
    example_failures = generate_worked_examples(output_docs, config, config_path, cli=args.cli)
    failures.extend(example_failures)

    # Step 4: Copy any remaining pages not yet handled.
    copy_remaining_pages(output_docs)

    # Step 4b: Write stub pages for personalise/* so canonical-doc links
    # (framework-overview, enablement/index, stages/02-select,
    # worked-example/build) do not 404 in the forked site.
    write_personalise_stubs(output_docs, org_name)

    # Step 5: Write customised mkdocs.yml.
    write_mkdocs_config(config, output_site, role_names)

    # Step 6: Write version metadata.
    write_version_metadata(output_site)

    # Step 7: Build the site.
    if not args.skip_build:
        build_site(output_site)

    # Summary.
    if failures:
        log.warning(
            "Completed with %d fallback(s) to generic: %s",
            len(failures), ", ".join(failures),
        )
    else:
        log.info("All sections personalised successfully.")

    log.info("Output: %s", output_site)


if __name__ == "__main__":
    main()
