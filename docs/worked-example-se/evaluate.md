# Worked Example: Stage 6 -- Evaluate

!!! example "Worked Example"
    We're applying Stage 6 to: **Release Notes Compilation & Publishing agent**. The goal is to validate that the agent fetches the right PR data, categorises changes accurately, and produces release notes comparable to the manually written version.

## Evaluation Approach

For the release notes agent, evaluation focuses on three questions:

1. **Does the agent fetch the right PRs?** Compare the agent's `merged_prs` list against `git log --merges {previous_tag}..{current_tag}` for the same release. Every PR in the commit range should appear.
2. **Does the agent categorise and summarise accurately?** Compare each PR's assigned category and one-line summary against what you would assign manually. Track misclassifications by strategy (label match, conventional commit, LLM fallback).
3. **Are the release notes at publishable standard?** Have a colleague read the agent-generated notes alongside the manually written version (without knowing which is which) and rate both on completeness, accuracy, and tone.

## Test Cases

These five test cases cover the range of releases an engineering team ships. Each tests different aspects of the agent's behaviour.

| Test Case | Release Profile | What It Tests |
|---|---|---|
| **Happy path** | Clean release, 12 well-labelled PRs, all data sources responding | The basic flow works end to end. Label-based categorisation handles every PR. Summaries are accurate. Formatting matches the existing changelog. |
| **Large release** | 53 PRs with ~60% labelling rate, multiple categories including security patches | The fallback chain (labels → conventional commits → LLM) handles mixed-quality metadata at scale. LLM classification is accurate for the long tail. Review burden at the HIL checkpoint is manageable. |
| **Hotfix** | Single-PR release, critical bug fix, expedited timeline | The agent handles a minimal release without generating empty sections or unnecessary content. End-to-end time is fast enough for hotfix workflows. |
| **Breaking changes** | 28 PRs including 3 breaking changes requiring migration guides | The migration note generation produces specific, actionable upgrade instructions. Breaking change detection catches all flagged PRs. The Upgrade Guide section is usable without manual rewriting. |
| **Messy metadata** | 18 PRs with sparse labels, empty descriptions, ticket-number-only titles, squash-merged commits with default messages | The agent degrades gracefully when metadata quality is poor. Classification fallbacks and summary generation produce usable output from minimal input. |

## What Evaluation Looks Like in Practice

### Round 1: Baseline

Run all five test cases using recent releases with known-good manually written notes. For each test case:

1. **Run the agent** with the release tag pair.
2. **At the `hil_review_notes` checkpoint**, note what you would change. Track the size of your edits (no changes, minor wording tweaks, section reordering, significant corrections, complete rewrite of a section).
3. **Compare the final notes** against the manually written release notes for the same release. Check:
    - Were the same PRs included (no omissions, no false inclusions)?
    - Were PRs assigned to the same categories?
    - Are the one-line summaries accurate and user-facing (not implementation-detail)?
    - Is the migration guide (if applicable) specific enough to follow?
    - Does the formatting match the project's existing changelog convention?

!!! note "Track the size of your edits at the `hil_review_notes` checkpoint"
    This is the most actionable metric in your evaluation. This workflow has a single HIL checkpoint -- so the edit size there tells you everything. If your edits are consistently minor (moving one PR to a different section, tweaking a summary), the pipeline is working. If you are rewriting summaries in bulk, the summary extraction step needs improvement. If you are re-categorising many PRs, the classification fallback chain needs tuning. The [Design document](design.md) assumed one focused review is more efficient than multiple scattered checkpoints -- the edit size validates or invalidates that assumption.

### Round 2: Edge Cases and Failure Modes

After the baseline round, deliberately test failure scenarios:

- **Simulate a GitHub API rate limit** (return HTTP 429 at various points in `fetch_prs`) and verify the agent waits for the reset window rather than crashing or producing partial results.
- **Feed a release with zero PRs** (two tags pointing to the same commit) and verify the agent produces a minimal "No changes in this release" document rather than an empty file or an error.
- **Test the revision loop** -- at `hil_review_notes`, request revisions ("move PR #312 from Bug Fixes to New Features, rewrite the summary for PR #445") and verify that `generate_notes` incorporates the feedback into the regenerated draft.

### Round 3: Efficiency Measurement

Time the full process (agent execution + your review time at the checkpoint) and compare against the manual process time. The target: total time should be less than 50% of the manual process.

#### Manual Process Baseline

Timed across 4 recent releases with known-good manually written notes:

| Phase | What You Do Manually | Time (avg per release) |
|---|---|---|
| PR identification and data gathering | Run `git log` between tags, cross-reference with GitHub PRs, check linked issues, identify breaking changes, pull contributor list | 45--90 min |
| Categorisation and filtering | Read each PR, assign to a category (feature, bugfix, breaking change, etc.), filter out internal-only changes, flag security patches | 30--45 min |
| Writing release notes | Write the changelog sections, draft narrative introduction for major releases, format contributor acknowledgements | 30--60 min |
| Writing migration guide (if needed) | Identify breaking changes, trace code diffs for specific method/config changes, write before/after examples and migration steps | 20--40 min |
| **Total** | | **2--4 hrs** |

#### Agent-Assisted Process (Measured)

Timed across the same 4 recent releases:

| Phase | What Happens | Time (avg per release) |
|---|---|---|
| Agent execution | Agent runs end-to-end: `fetch_prs` (resolve tags, deduplicate rebase-merged PRs) → `categorise_changes` (label match → conventional commit → LLM fallback) → `generate_notes` (draft sections, narrative intro, migration notes, contributor list) | ~5 min |
| HIL Checkpoint (`hil_review_notes`) | Review the draft release notes. Check PR categorisation, verify summaries are user-facing not implementation-detail, review migration guide specificity, adjust narrative introduction. For 2 of 4 releases, minor wording edits; for 1, recategorised 2 PRs from Bug Fixes to the correct section; for 1 (the breaking changes release), rewrote one sparse migration entry with specific method and config changes. | ~12 min |
| **Total** | | **~17 min** |

#### Comparison

| Metric | Manual Process | Agent-Assisted | Improvement |
|---|---|---|---|
| Total time per release | 2--4 hrs | ~17 min | **~86--93% reduction** |
| PR identification and data gathering | 45--90 min | ~5 min (agent execution) | Largest single saving — the agent eliminates 45+ minutes of git log parsing, PR cross-referencing, and issue linking |
| Categorisation and filtering | 30--45 min | Included in agent execution + ~3 min spot-check at review | The three-strategy fallback chain handles categorisation with minimal corrections needed |
| Writing release notes | 30--60 min | ~7 min (review and edit at HIL checkpoint) | Editing a structured draft with correct PR links and summaries is far faster than writing from scratch |
| Writing migration guide | 20--40 min | ~2 min review (when applicable) | Migration notes extracted from PR descriptions are usable as-is for well-documented PRs; sparse PRs still need manual enrichment |

## Sample Evaluation Results

After running the five test cases against recent releases with known-good manually written notes, here is what the filled-in results look like. Each follows the record format from [Stage 6](../stages/06-evaluate.md#test-case-design).

### Test Case 1: Happy Path -- v3.2.0 (Clean Release)

- **Input:** `release_tag: v3.2.0`, `previous_tag: v3.1.0`. 12 merged PRs. All PRs have category labels. 8 have conventional commit prefixes. All PR descriptions are complete with linked issues. No breaking changes.
- **Expected behaviour:** Agent fetches all 12 PRs, categorises via label match (Strategy 1), generates accurate summaries, produces well-formatted notes matching the existing CHANGELOG.md style. Zero or near-zero corrections at `hil_review_notes`.
- **Actual behaviour:** Agent fetched all 12 PRs. All 12 categorised via label match -- `llm_classified_prs` was empty. Summaries: 9 extracted from PR titles (adequate after normalisation), 3 had explicit "Release Notes" sections in the PR description (used verbatim). Formatting matched the existing changelog: `## [3.2.0] - 2026-03-15` header, correct section ordering, PR links rendered correctly. Contributor acknowledgements listed 5 authors; no new contributors detected (all had PRs in prior releases). Narrative introduction generated ("This release focuses on API reliability improvements and developer experience enhancements") because the release contained 4 new features. One minor wording tweak at `hil_review_notes` -- the narrative introduction listed the two largest categories rather than leading with the most impactful change (the new API pagination support, which was the most-requested feature).
- **Verdict:** Pass
- **Notes:** The narrative introduction is accurate but generic -- it summarises by volume (most changes were reliability/DX) rather than by impact (the pagination feature is the headline). A manually written introduction would lead with pagination because it was the most-requested item. This is a quality gap between "correct" and "editorially sharp." Worth noting as a prompt refinement candidate, not a blocker.

### Test Case 2: Large Release -- v4.0.0 (53 PRs, Mixed Labelling)

- **Input:** `release_tag: v4.0.0`, `previous_tag: v3.2.0`. 53 merged PRs across a 6-week development cycle. Labelling rate ~60%: 32 PRs have category labels, 21 do not. Among the labelled PRs, 4 carry the label `security` (CVE patches for input validation, auth token handling, and dependency vulnerabilities). Mixed merge strategies: 41 squash-merged, 8 merge-committed, 4 rebase-merged.
- **Expected behaviour:** Agent fetches all 53 PRs (including correct deduplication for the 4 rebase-merged PRs). Categorisation: ~32 via label match, remainder via conventional commit prefix or LLM fallback. Release notes include a dedicated Security section listing the 4 CVE patches. `llm_classified_prs` logs the PRs that required LLM fallback.
- **Actual behaviour:** Agent fetched all 53 PRs. The 4 rebase-merged PRs were correctly resolved -- individual commits traced back to their originating PRs, deduplicated by PR number. Categorisation: 28 PRs matched via label (Strategy 1), but the 4 security-labelled PRs did not match -- `security` is not in the label-to-category config. Those 4 fell through to Strategy 2 (no conventional commit prefix for security) and then Strategy 3 (LLM). The LLM classified all 4 as "Bug Fixes" -- the category list passed to the classification prompt does not include "Security" (the list is generated from the same config), so the LLM mapped "fix auth token vulnerability" to the closest available category. Of the 21 unlabelled PRs, 7 matched via conventional commit prefix (Strategy 2), and 14 went to LLM classification (Strategy 3). The LLM correctly classified 11 of 14; 3 received `confidence: "low"` and were flagged in `llm_classified_prs`. The release notes contained sections for Breaking Changes, New Features, Bug Fixes, Performance, Dependency Updates, and Documentation -- but no Security section. The 4 security patches were buried in the Bug Fixes section alongside 16 other entries.
- **Verdict:** Partial
- **Notes:** Root cause: the label-to-category mapping loaded from config includes entries for `feature`, `enhancement`, `bug`, `bugfix`, `breaking-change`, `breaking`, `performance`, `dependencies`, `dependency`, `documentation`, `docs`, `internal`, `chore`, and `ci` -- but not `security`. The [Scope Document's Step 4](scope.md) specifies `security → Security` in the label mapping, but the config file was implemented without that entry. Because the config also drives the valid category list passed to the LLM classification prompt, "Security" is absent from the LLM's options too. The agent's fallback chain worked as designed -- it tried labels, tried prefixes, fell back to LLM -- but the LLM was given an incomplete category list. The security patches are in the release notes (not omitted), but they are miscategorised as Bug Fixes. For users scanning release notes for security updates -- which is a common workflow for security-conscious organisations and compliance teams -- the absence of a dedicated Security section is a functional failure.

### Test Case 3: Hotfix -- v3.1.1 (Single-PR Fix)

- **Input:** `release_tag: v3.1.1`, `previous_tag: v3.1.0`. 1 merged PR: #892 "Fix race condition in payment processing queue." Labelled `bugfix` and `critical`. Linked to PROJ-456 (P1 bug, status: In Progress).
- **Expected behaviour:** Minimal but complete release notes. One Bug Fixes section with one entry. No empty sections. No narrative introduction (fewer than 3 features). No migration notes (no breaking changes). Formatting matches the existing changelog.
- **Actual behaviour:** Agent fetched 1 PR. Tag resolution worked correctly -- `previous_tag` inferred via GitHub Releases API (most recent prior release). Categorised as Bug Fixes via label match. Summary extracted from PR title: "Fix race condition in payment processing queue." No narrative introduction generated (correctly skipped -- fewer than 3 features and no breaking changes). No migration notes generated (no breaking changes). Full changelog link correct: `compare/v3.1.0...v3.1.1`. New Contributors check ran, found no new contributors, correctly omitted the section. Total agent execution time: 38 seconds.
- **Verdict:** Pass
- **Notes:** The agent handled the minimal case cleanly -- no empty section headers, no "This release includes 1 change" filler, no unnecessary content. The release notes were four lines: a version header, a Bug Fixes heading, a single bullet, and the full changelog link. This matches what the manually written hotfix notes looked like. One observation: the linked issue's priority (P1) and status (In Progress) were retrieved but not surfaced in the release notes, which is correct -- issue metadata enriches the review context but does not belong in user-facing notes. The issue metadata was visible at `hil_review_notes` in the sidebar context, which is the right place for it.

### Test Case 4: Breaking Changes -- v5.0.0 (API Migration Required)

- **Input:** `release_tag: v5.0.0`, `previous_tag: v4.2.0`. 28 merged PRs. 3 labelled `breaking-change`: PR #1201 "Remove deprecated v1 API endpoints" (description includes a detailed Migration section), PR #1215 "Change auth token format from JWT to opaque tokens" (description is sparse: "Switch from JWT to opaque tokens for improved security and token rotation support"), PR #1222 "Rename config key `db_host` to `database_url`" (description includes a Migration section with before/after examples). Additionally, PR #1198 has `BREAKING CHANGE:` in a commit message but no `breaking-change` label -- Strategy 4 should catch it.
- **Expected behaviour:** Breaking Changes section lists all 4 PRs (3 labelled + 1 detected via commit message). Upgrade Guide section generated with specific migration instructions for each. PRs #1201 and #1222's migration notes extracted verbatim from their PR descriptions. PR #1215's migration notes generated by LLM. PR #1198's breaking change detected via Strategy 4 override.
- **Actual behaviour:** Breaking Changes section correctly listed all 4 PRs. Strategy 4 (commit message scan for `BREAKING CHANGE:`) caught PR #1198 -- it was also classified as New Features via its `feature` label and appeared in both sections (correct dual-listing behaviour from [Step 4](scope.md)). Migration notes: PRs #1201 and #1222 had explicit Migration sections in their descriptions -- extracted verbatim and correctly formatted. PR #1198's migration note was LLM-generated and adequate (the PR description contained enough context about the API change for the LLM to produce a usable Before/After). PR #1215's migration note was LLM-generated but too generic: "**What changed:** Auth tokens are now opaque instead of JWT. **Before:** JWT tokens. **After:** Opaque tokens. **Migration steps:** Update your authentication code to handle the new token format." A developer reading this does not know which SDK method call changes, which config keys are affected, or what the new token structure looks like. The manually written migration for this PR included the specific method change (`auth.verify_jwt(token)` to `auth.verify_token(token)`), the config change (`token_type: jwt` to `token_type: opaque`), and a code example showing the updated client initialisation.
- **Verdict:** Partial
- **Notes:** Root cause: the [Scope Document's Step 9](scope.md) specifies that the migration note prompt receives "the PR title, description, and diff summary." The `generate_notes` action sends the PR title and description to the migration prompt, but omits the diff summary. PR #1215's description is sparse (one sentence), so the LLM has insufficient context to produce specific migration instructions. PRs #1201 and #1222 are unaffected because their migration content is extracted from the PR description (Strategy 1 of Step 9), bypassing the LLM entirely. PR #1198 is unaffected because its description is detailed enough for the LLM. The gap is between the scope's specification (include diff summary) and the implementation (diff summary not retrieved). This is a tool issue -- the `generate_notes` action does not fetch diff summaries from the GitHub API for the migration prompt. The fix is to add a diff summary retrieval call (via the PR files endpoint or Compare API) and include it in the migration prompt's context. This would give the LLM the specific file changes, method renames, and config key modifications needed to generate actionable instructions.

### Test Case 5: Messy Metadata -- v2.8.0 (Sparse Labels, No Descriptions)

- **Input:** `release_tag: v2.8.0`, `previous_tag: v2.7.0`. 18 merged PRs. 7 have category labels; 11 have none. 6 have empty or template-only descriptions (the PR body is the unfilled pull request template with placeholder sections). 2 have titles that are just Jira ticket numbers ("PROJ-789", "PROJ-801"). 14 are squash-merged (some with default squash messages that concatenate commit subjects rather than providing a meaningful summary). 4 are rebase-merged.
- **Expected behaviour:** Agent handles the degraded metadata using the full fallback chain. Unlabelled PRs classified via conventional commits or LLM. Empty-description PRs summarised from titles. Ticket-number-only PRs enriched via linked issue metadata. Rebase-merged PRs correctly deduplicated. All 18 PRs appear in the release notes.
- **Actual behaviour:** Agent fetched all 18 PRs. The 4 rebase-merged PRs were correctly resolved and deduplicated. Categorisation: 7 labelled PRs matched via Strategy 1. Of the 11 unlabelled PRs, 4 matched via conventional commit prefix (Strategy 2). The remaining 7 went to LLM classification (Strategy 3): 5 classified correctly, 2 classified as "Other" -- the two ticket-number-only PRs. The LLM received "PROJ-789" as the title, an empty description, and linked issue type "task" from the issue tracker. With no meaningful content to classify, it returned `{"category": "Other", "confidence": "low"}`. Both PRs were logged to `llm_classified_prs`. Summary extraction: the 6 empty-description PRs fell through to LLM summarisation from title alone -- 4 produced adequate summaries, 2 produced summaries nearly identical to the raw title (no improvement). The 2 ticket-number-only PRs could not be meaningfully summarised -- the LLM returned the ticket number as the summary. The generated release notes omitted both "Other"-classified PRs entirely. The `generate_notes` action's template renders the seven defined categories (Breaking Changes through Documentation) but has no section for "Other." The 2 PRs were flagged in `llm_classified_prs` (visible at the `hil_review_notes` checkpoint), but the draft itself contained 16 entries instead of 18.
- **Verdict:** Fail
- **Notes:** The primary failure is the silent omission of "Other"-classified PRs from the draft. The [Scope Document's Step 4](scope.md) correctly specifies "classify as 'Other' and flag for manual review" -- the categorisation action did this. But the `generate_notes` action's template does not render "Other" as a section. The flagging works (the reviewer sees `llm_classified_prs` at the checkpoint), but the reviewer must cross-reference the sidebar flag list against the draft to notice what is missing. In TC1 (clean release), this gap is invisible -- no PRs fall to "Other." In TC5, with 2 omitted PRs, the reviewer has to manually insert them into the correct sections. The manually written release notes for this release included all 18 PRs.

    This is a prompt/template issue in the `generate_notes` action. The fix: add an "Other Changes" section at the bottom of the template that renders any "Other"-classified PRs with a visible flag ("categorisation uncertain -- please verify"). This ensures nothing is silently omitted from the draft, even when the metadata is too sparse for confident classification. A reviewer correcting 2 flagged entries in context is faster than a reviewer discovering 2 missing entries by cross-referencing a sidebar list.

    The secondary issue -- vague summaries from sparse metadata -- is less severe. The 2 near-identical summaries and the 2 ticket-number summaries are noticeable at the `hil_review_notes` checkpoint and correctable in seconds. This is the expected degradation mode for sparse data: the agent produces a draft with gaps the reviewer fills in, which is still faster than writing from scratch.

## Sample Iteration Cycle

The Partial verdict on Test Case 2 (v4.0.0) needs to be fixed. Here is one full iteration cycle: diagnose, categorise, fix, retest.

### Diagnose

The release notes for v4.0.0 have no Security section. Four PRs labelled `security` -- all CVE patches -- appear under Bug Fixes instead. The manually written release notes for the same release had a dedicated Security section listing all four patches at the top (after Breaking Changes), which is where security-conscious users and compliance teams expect to find them. The agent's fallback chain worked mechanically (labels missed → prefixes missed → LLM classified as Bug Fixes), but the result is functionally wrong: security patches are invisible to anyone scanning by section header.

### Categorise

Walk through the four failure categories from [Stage 6](../stages/06-evaluate.md#diagnosing-the-failure-category):

1. **Tool layer -- Was the right data retrieved?** Yes. `fetch_prs` retrieved all 53 PRs including the 4 security-labelled ones. The PR metadata -- labels, titles, descriptions, linked issues -- was correct and complete. The `security` label was present on all 4 PRs. ✓
2. **Prompt layer -- Given the data it received, did the prompt produce the right analysis?** The `categorise_changes` action applied Strategy 1 (label match) using the label-to-category config. The config does not include `security` as a key, so Strategy 1 produced no match. Strategy 2 (conventional commit prefix) found no recognised prefix. Strategy 3 (LLM classification) received the PR title, description, and linked issue types, but the category list passed to the prompt does not include "Security" -- the list is generated from the same config. The LLM mapped "fix auth token vulnerability" to "Bug Fixes" because that was the closest available category. The LLM did what the prompt asked -- it just was not given "Security" as an option. ✗
3. Layers 3-4 not reached -- failure identified at layer 2.

This is a **config/prompt issue**. The label-to-category config is missing the `security` entry, and because the valid category list is derived from the same config, the LLM classification prompt is also missing "Security" as an option. Both the deterministic path and the LLM fallback path fail for the same root cause: an incomplete config.

!!! note "Why this is a config issue that surfaces as a prompt issue"
    The [Scope Document's Step 4](scope.md) explicitly specifies `security → Security` in the label mapping. The config file was implemented without that entry -- a straightforward omission. But the blast radius extends beyond label matching: because the LLM classification prompt's category list is generated from the config, the missing entry also removes "Security" from the LLM's option set. If the category list were hardcoded separately in the prompt (rather than generated from config), the LLM might have classified the 4 PRs correctly even though label matching failed. The config-as-single-source-of-truth design is correct (it prevents drift between the deterministic and LLM paths), but it means a single missing entry creates a category-wide blind spot across all three classification strategies.

### Fix

Two changes address this at different levels of the fallback chain:

**Config fix (deterministic path):** Add `"security": "Security"` to the label-to-category mapping in the config. This ensures that PRs labelled `security` are correctly categorised via Strategy 1 (label match). Because the valid category list is generated from the config, this also adds "Security" as an option for the LLM classification prompt.

**Prompt fix (LLM fallback path):** Add security keyword detection instructions to the LLM classification prompt. The specific addition:

> **Before:** "Classify this PR into exactly one of the following categories based on its content: {category_list}."
>
> **After:** "Classify this PR into exactly one of the following categories based on its content: {category_list}. Pay special attention to security-related signals: if the PR title, description, or linked issues reference CVEs, vulnerabilities, security patches, or common vulnerability types (XSS, SQL injection, auth bypass, CSRF, SSRF), classify as Security even if the primary change looks like a bug fix. Security patches that fix vulnerabilities are Security, not Bug Fixes."

The config fix catches labelled security PRs. The prompt fix catches unlabelled security PRs that mention security-related keywords in their content -- a common case when the PR author fixes a vulnerability but does not apply the `security` label. Together, they close the gap at both levels of the fallback chain.

### Retest

Re-ran Test Case 2 (v4.0.0) with the updated config and prompt. The release notes now contain a Security section listing all 4 CVE patches, positioned between Breaking Changes and New Features in the section ordering (matching the [Scope Document's Step 7](scope.md) priority order). The 4 PRs are no longer in Bug Fixes. The Bug Fixes section dropped from 20 entries to 16. The `llm_classified_prs` list decreased from 14 to 10 -- the 4 security PRs now match via label (Strategy 1) instead of falling through to LLM.

Re-ran Test Cases 1, 3, 4, and 5 to confirm no regression. TC1 (clean release, no security PRs): no change -- "Security" is now in the valid category list but no PRs match it. Pass. TC3 (hotfix, single bug fix): unaffected -- the single PR is labelled `bugfix`, not `security`. Pass. TC4 (breaking changes): unaffected -- no security-labelled PRs in this release. Partial (unchanged -- migration note quality issue is a separate fix). TC5 (messy metadata): marginal improvement -- one of the 7 LLM-classified PRs had "CVE-2026-1234" in a commit message; the keyword heuristic in the updated prompt correctly classified it as Security instead of Bug Fixes. TC5's verdict remains Fail (core issues are the "Other" omission and sparse metadata, not security categorisation).

### Iteration Log Entry

| Date | Change Made | Test Cases Affected | Result |
|---|---|---|---|
| 2026-03-28 | Added `security` to label-to-category config; added security keyword heuristic to LLM classification prompt | TC2: Partial → Pass. TC1, TC3: no regression. TC4: Partial (unchanged -- separate issue). TC5: Fail (marginal improvement, core issues unchanged). | 3 Pass, 1 Partial, 1 Fail |

## Iteration Cycle: Messy Metadata Template Fix

The Fail verdict on Test Case 5 (v2.8.0) is a separate prompt/template issue from TC2. Here is the second iteration cycle.

### Diagnose

The release notes draft for v2.8.0 contained 16 entries instead of 18. Two PRs -- the ticket-number-only PRs ("PROJ-789" and "PROJ-801") -- were classified as "Other" by the LLM with `confidence: "low"`. The `categorise_changes` action handled this correctly: the [Scope Document's Step 4](scope.md) specifies "classify as 'Other' and flag for manual review," and both PRs appeared in `llm_classified_prs`. But the `generate_notes` action's template silently dropped them. The template renders the seven defined categories (Breaking Changes, Security, New Features, Bug Fixes, Performance, Dependency Updates, Documentation) but has no section for "Other." The 2 PRs were flagged in the sidebar at the `hil_review_notes` checkpoint, but the draft itself omitted them entirely -- a reviewer who reads only the draft (the natural workflow) sees 16 PRs and has no reason to suspect 2 are missing.

### Categorise

Walk through the four failure categories from [Stage 6](../stages/06-evaluate.md#diagnosing-the-failure-category):

1. **Tool layer -- Was the right data retrieved?** Yes. `fetch_prs` retrieved all 18 PRs. The 2 ticket-number-only PRs had correct metadata: PR number, title ("PROJ-789", "PROJ-801"), empty descriptions, linked issue types retrieved from Jira. ✓
2. **Prompt layer -- Given the data it received, did the prompt produce the right analysis?** The `categorise_changes` action correctly classified both PRs as "Other" with `confidence: "low"` -- the LLM had no meaningful content to work with, so "Other" is the correct category. The `generate_notes` action received a categorised PR list that included these 2 "Other" PRs, but the Markdown template in the generation prompt does not include an "Other Changes" section. The template iterates over a hardcoded list of category headings, and "Other" is not among them. The PRs were present in state but absent from the rendered output. ✗
3. Layers 3-4 not reached -- failure identified at layer 2.

This is a **prompt/template issue** in the `generate_notes` action. The categorisation is correct; the rendering is incomplete. The template's hardcoded category list does not match the full set of categories the classification action can produce.

### Fix

Add an "Other Changes" section to the `generate_notes` action's Markdown template. The specific change to the template:

> **Before:** The template iterates over the seven defined category headings (Breaking Changes through Documentation) and renders each non-empty category as a `### Category Name` section with bulleted entries.
>
> **After:** After the last defined category section, add a conditional block:
>
> ```
> {% if other_changes %}
> ### Other Changes
>
> > **Categorisation uncertain** -- the following PRs could not be confidently
> > classified. Please verify each entry is in the correct section or recategorise
> > as needed.
>
> {% for pr in other_changes %}
> - {{ pr.summary }} ([#{{ pr.number }}]({{ pr.url }})) ⚠️ *categorisation uncertain -- please verify*
> {% endfor %}
> {% endif %}
> ```
>
> This ensures every PR in the categorised list appears in the draft, regardless of category. The visible flag ("categorisation uncertain -- please verify") makes it obvious that these entries need reviewer attention -- they are not presented as confidently classified. A reviewer correcting 2 flagged entries in context (moving them to the right section and rewriting their summaries) is faster than a reviewer discovering 2 missing entries by cross-referencing the `llm_classified_prs` sidebar list against the draft.

No changes to the scope, design, or graph structure are required. The [Scope Document's Step 4](scope.md) already specifies the "Other" classification -- the gap was only in the template that renders categorised PRs into Markdown.

### Retest

Re-ran Test Case 5 (v2.8.0) with the updated template. The release notes draft now contains all 18 PRs. The 2 "Other"-classified PRs appear under a new "Other Changes" section at the bottom of the draft, each with the "categorisation uncertain -- please verify" flag. At the `hil_review_notes` checkpoint, the reviewer can see both entries in context, move them to the correct sections, and rewrite their summaries -- a 60-second correction instead of a cross-referencing exercise. The `llm_classified_prs` sidebar still lists both PRs (the flagging is additive, not replaced), giving the reviewer two signals: the inline flag in the draft and the sidebar log.

The secondary issue -- vague summaries from sparse metadata -- remains. The 2 ticket-number-only PRs still have unhelpful summaries ("PROJ-789", "PROJ-801"), and 2 of the 6 empty-description PRs still have near-identical summaries to their raw titles. These are visible and correctable at the checkpoint in seconds. This is the expected degradation mode for sparse data: the agent produces a complete draft with quality gaps the reviewer fills in.

Re-ran Test Cases 1, 2, 3, and 4 to confirm no regression. TC1 (clean release, no "Other" PRs): no change -- the "Other Changes" section is conditional and does not render when empty. Pass. TC2 (large release): unaffected -- the security config fix from cycle 1 is still in place, and no PRs in this release are classified as "Other." Pass. TC3 (hotfix): unaffected -- single bug fix PR, no "Other" classification. Pass. TC4 (breaking changes): unaffected -- all PRs have labels or conventional commit prefixes, none fall to "Other." Partial (unchanged -- migration note quality issue is a separate fix).

### Iteration Log Entry

| Date | Change Made | Test Cases Affected | Result |
|---|---|---|---|
| 2026-03-29 | Added "Other Changes" section to `generate_notes` template; renders "Other"-classified PRs with visible uncertainty flag | TC5: Fail → Pass. TC1, TC2, TC3: no regression. TC4: Partial (unchanged -- separate issue). | 4 Pass, 1 Partial |

!!! note "TC4 remains Partial -- and that may be acceptable"
    After two iteration cycles, the scorecard is 4 Pass, 1 Partial (TC4: migration note quality for sparse PR descriptions). The TC4 fix is a tool-layer change: add diff summary retrieval to the `generate_notes` action's migration prompt input, matching what the [Scope Document's Step 9](scope.md) specifies. This is a targeted fix that does not require scope or design changes -- the data retrieval, classification logic, and graph structure are sound. The remaining failure is in the *presentation* layer (the migration prompt lacks sufficient context), not the *analysis* layer. An engineer reviewing the output at `hil_review_notes` would catch the vague migration entry for PR #1215 in about 60 seconds and rewrite it with the specific method and config changes. The question from the [Stage 6 methodology](../stages/06-evaluate.md#when-to-stop-iterating) applies: "is agent-plus-correction meaningfully faster than doing it manually?" For TC4, it is -- the agent still saved 2+ hours of PR gathering, categorisation, and draft writing, and the correction is a 60-second edit to one migration entry. This is a candidate for a third iteration cycle, not a blocker for production use.

---

## Graduation Criteria

The agent is ready for production use when:

- [x] All 5 test cases pass without major human corrections -- 4 Pass after iteration; TC4 Partial requires reviewer to rewrite one migration entry at `hil_review_notes`, not a major rework
- [x] Total time (agent + human review) is less than 50% of the manual process time — measured at ~17 min vs 2–4 hrs (~86–93% reduction)
- [ ] No critical failures (omitted PRs, miscategorised security patches, incorrect migration instructions) in the last 3 evaluation rounds
- [ ] At least one colleague has reviewed and validated the output quality
- [ ] Error handling has been tested for all identified failure modes (GitHub API rate limit, empty release, rebase-merge deduplication, malformed LLM output, missing PR descriptions)

!!! tip "When to push the automation boundary"
    After 2-3 successful evaluation cycles: if the engineer rarely changes the draft at `hil_review_notes`, consider making Step 11 (publish) a HIL step instead of MANUAL -- the agent proposes the publication targets and the engineer approves with one click. If the team's PR labelling discipline improves to the point where `llm_classified_prs` is consistently empty, the LLM classification fallback becomes dead code -- but keep it as a safety net rather than removing it. The automation boundary should expand based on evidence from the iteration log, not optimism about metadata quality.

---

[:octicons-arrow-left-24: Back to Stage 6: Evaluate](../stages/06-evaluate.md){ .md-button }
