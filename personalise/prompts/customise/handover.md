# Handover Document Generator

You are producing a handover document for the champion or owner of a
personalised framework site. This document ensures continuity when the person
responsible for maintaining the personalised site changes roles or leaves the
team.

## Inputs

1. **Organisation config**: Read `personalise/org-config.yaml` for the
   organisation's context and roles.
2. **Application guide**: Read `personalise/output/APPLICATION-GUIDE.md` (if it
   exists) for the rollout plan and current state.
3. **Forked site metadata**: Read `personalise/output/site/.framework-version`
   (if it exists) for the current framework version.
4. **Learning materials**: Check `personalise/output/learning/` for which roles
   have learning paths generated.

## Output Structure

Produce a single markdown document with the following sections:

### 1. Current State

- Which personalisation layers have been completed (L1, L2, L3)
- When was the last re-personalisation run (check file modification dates)
- Which framework version the fork was built from
- What org config was used (summary of key fields)

### 2. Active Agents

- List of agents currently in development or production (if documented in the
  output directory)
- For each: name, owning role, status, key systems involved
- If no agents have been built yet, note the recommended first workflow from
  the application guide

### 3. How to Update the Site

Step-by-step instructions:

1. Pull upstream framework changes: `git pull upstream main`
2. Run the version check: `python personalise/check-upstream.py`
3. Review which files changed and whether re-personalisation is needed
4. Re-run the fork script: `python personalise/fork.py --config personalise/org-config.yaml`
5. Review the output and verify the site builds
6. Commit and push (if using GitHub Pages deployment)

### 4. Key Contacts

- Who approved the AI usage policy (if `regulatory_environment.existing_ai_policy: true`)
- Who has access to the GitHub repo
- Who the model champions are in each team (if a champion programme was set up)
- Engineering contact for Stages 4-6 support

### 5. Configuration Reference

- Location of the org config file
- Location of the output directory
- How to modify the org config and re-run personalisation
- What to do if a new role or system is added

## Output

Write to `personalise/output/HANDOVER.md`.

## Quality Standards

- Instructions must be actionable by someone unfamiliar with the framework's
  internals
- File paths must be accurate and relative to the repo root
- Do not assume knowledge of the personalisation pipeline — explain each step
- If information is not available (e.g., no agents built yet), say so clearly
  rather than leaving the section blank
