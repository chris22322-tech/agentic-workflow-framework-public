# Layer 3: Custom Site

!!! tip "One-file shortcut"
    Use `personalise/PERSONALISE-L3-CUSTOM-SITE.md` — one file to open, edit, and run with any AI CLI (Gemini, Claude, ChatGPT). [Quick start →](index.md#quick-start-one-file-one-command)

Generate your own version of this documentation site — with your org's name throughout, worked examples using your roles and workflows, templates pre-filled with your systems, and decision trees extended with your constraints.

The output is a complete MkDocs site that reads as if it was written for your organisation. The six-stage methodology stays unchanged — it is universal. Everything around it adapts.

## What this costs

| Layer | Input tokens | Output tokens | Estimated cost (Claude Sonnet) | Estimated cost (Gemini Pro) |
|---|---|---|---|---|
| **Layer 3** (full site fork) | ~200-400K | ~100-200K | $5.00-15.00 | $1.50-4.00 |

Most of the cost comes from generating worked examples (one per role). Orgs with 2 roles cost less than orgs with 5.

## Prerequisites

- [x] Layer 1 completed: `org-config.yaml` filled in, application guide generated
- [ ] Layer 2 completed (recommended): at least one personalised worked example generated per role
- [ ] Python 3.11+
- [ ] MkDocs, MkDocs Material, and PyYAML installed (`pip install mkdocs mkdocs-material pyyaml`)
- [ ] Claude Code CLI authenticated (`claude --version` works)

---

## What gets personalised

| Section | Personalised? | What changes |
|---|---|---|
| **Getting Started** | Partially | "Who it's for" section adds org-specific role descriptions. Prerequisites adds org's systems. |
| **Stages 1-6** | No | Methodology is universal. Stays as-is. |
| **Worked Examples** | Yes — new examples added | The generic CSM/BA/SWE examples stay. New org-specific examples are added for each role in the org config. |
| **Templates** | Partially | Templates pre-fill the "Systems Touched" column, the Data Inventory "Data Source" column, and the Integration Requirements section with the org's systems. |
| **Glossary** | Extended | Org-specific terms added alongside the generic ones. |
| **Decision Trees** | Extended | Org-specific constraints added as early gates. |
| **Checklist** | Extended | Org-specific checklist items added. |
| **Quick Start** | Partially | The mini-example uses an org-specific role and workflow. |

---

## Running the fork

=== "Option A (Recommended): GitHub Action"

    The GitHub Action is the simplest path. It removes the need for any local
    tooling beyond a text editor and Git.

    1. Fork this repo
    2. Fill in `personalise/org-config.yaml` and push
    3. The GitHub Action triggers automatically and:
        - Installs dependencies
        - Runs `personalise/fork.py`
        - Commits the generated site to a `gh-pages-custom` branch
        - Deploys to GitHub Pages (if configured)
    4. Your personalised site is live — update the config and push again to refresh

    The action also runs when you manually trigger the workflow via the GitHub
    Actions UI ("Run workflow" button).

=== "Option B (Advanced): Run locally"

    ```bash
    cd your-framework-clone/
    pip install mkdocs mkdocs-material pyyaml
    python personalise/fork.py --config personalise/org-config.yaml
    ```

    The script:

    1. Creates `personalise/output/site/` with the full MkDocs structure
    2. Copies generic pages unchanged
    3. Runs personalisation prompts for customisable sections
    4. Generates worked examples for each role in the org config
    5. Builds the personalised site

    To preview:

    ```bash
    cd personalise/output/site/
    mkdocs serve
    ```

---

## What to review

After the fork builds, check:

- [ ] Worked examples use realistic workflows for your roles
- [ ] Templates have your systems pre-filled in the right columns
- [ ] Glossary terms are accurate for your domain
- [ ] Decision tree constraints match your actual requirements
- [ ] Quick Start example makes sense for a new joiner in your org
- [ ] Site builds and navigates without errors

---

## Keeping up to date

When the upstream framework releases a new version:

```bash
git pull upstream main
python personalise/fork.py --config personalise/org-config.yaml
```

The script re-generates personalised content while preserving the updated generic methodology.

### Version drift detection

The fork script stores a hash of the upstream framework version in the forked site's metadata (`personalise/output/site/.framework-version`). A companion script compares the current framework to the version your fork was built from:

```bash
python personalise/check-upstream.py
```

The script categorises changes:

Safe direct merge
:   Changes to methodology text, typo fixes, new reference pages. Pull in without re-personalisation.

Requires re-personalisation
:   Changes to templates, worked example structure, decision trees, or personalisation prompts. Pull changes, then re-run `fork.py`.

Review recommended
:   Changes to stage definitions or the config schema. May require updates to your org config before re-personalisation.

---

## Handover

When the champion or owner of the personalised site changes roles, use the handover prompt to generate a continuity document:

```bash
claude -p "$(cat personalise/prompts/customise/handover.md)" \
  --allowedTools Read,Write,Glob,Grep \
  --max-turns 15
```

The handover document covers:

- **Current state** — which layers are completed, when was the last re-personalisation, which framework version
- **Active agents** — agents in development or production, their owners and status
- **How to update** — step-by-step instructions for pulling upstream changes and re-running the fork
- **Key contacts** — policy approvers, repo access, model champions per team

Output: `personalise/output/HANDOVER.md`

---

## Prompt inventory

| Prompt | What it generates | When to use it |
|---|---|---|
| `worked-example.md` | Complete Stage 1-6 worked example for a role | Called per role by `fork.py` |
| `templates.md` | Pre-filled template fields with org systems | Called once by `fork.py` |
| `glossary.md` | Extended glossary with org domain terms | Called once by `fork.py` |
| `decision-trees.md` | Org-specific constraint gates in decision trees | Called once by `fork.py` |
| `checklist.md` | Org-specific checklist items per stage | Called once by `fork.py` |
| `quick-start.md` | Adapted Quick Start with org-specific mini-example | Called once by `fork.py` |
| `getting-started.md` | Getting Started page with org context added | Called once by `fork.py` |
| `handover.md` | Handover document for site ownership transitions | Run manually when needed |
