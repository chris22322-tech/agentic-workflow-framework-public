# Personalise for Your Organisation

This framework is generic by design. The methodology works for any knowledge-worker role in any industry — but generic guidance only gets you so far. These tools make it specific to your organisation, your roles, and your workflows.

Personalisation uses AI prompts to read the framework documentation, combine it with context you provide about your organisation, and produce tailored output — role playbooks, workflow recommendations, rollout plans — that name your systems, your job titles, and your constraints.

## Quick start — one file, one command

Each layer has a **single-doc file** you can open, edit, and run. No config files to copy, no prompts to paste, no multi-file assembly. Works with any AI CLI (Gemini, Claude, ChatGPT) or web chat.

| Layer | Single-doc file | What you get | Time |
|---|---|---|---|
| **Layer 1** | `personalise/PERSONALISE-L1-APPLICATION-GUIDE.md` | Role playbooks, quick wins, rollout plan, risk register | 30–60 min |
| **Layer 2** | `personalise/PERSONALISE-L2-TRAINING-MATERIALS.md` | Per-role learning paths, worked examples, workshop plan, calibration exercises | Half a day |
| **Layer 3** | `personalise/PERSONALISE-L3-CUSTOM-SITE.md` | Your own branded version of this site with org-specific examples throughout | Full day |

**How it works:**

1. Open the single-doc file for the layer you want
2. Edit **Section 1** (your org details — name, roles, systems, constraints)
3. Run it:
    - **Gemini CLI:** `gemini -y -p "$(cat personalise/PERSONALISE-L1-APPLICATION-GUIDE.md)"`
    - **Claude Code:** `claude -p "$(cat personalise/PERSONALISE-L1-APPLICATION-GUIDE.md)"`
    - **Web chat:** paste the file contents into claude.ai, gemini.google.com, or chat.openai.com
4. Review the output in `personalise/output/`

Each file contains full instructions — open it and follow along.

## Three layers of personalisation

| Layer | What you get | Time required | Who it's for |
|---|---|---|---|
| **[Layer 1: Application Guide](apply.md)** | A tailored guide showing how the framework applies to your org: role playbooks, quick wins, rollout plan, risk register | 30-60 minutes | Team leads, enablement managers, anyone evaluating the framework |
| **[Layer 2: Training Materials](learn.md)** | Per-role learning paths, worked examples, workshop plans, and facilitator guides built around your actual workflows | Half a day | L&D teams, enablement managers running training programmes |
| **[Layer 3: Custom Site](customise.md)** | Your own branded version of this documentation site with org-specific examples throughout | Full day | Organisations embedding the framework as a standard methodology |

## Which layer do I need?

??? question "I want to understand how this applies to us"

    Start with **Layer 1**. Open `personalise/PERSONALISE-L1-APPLICATION-GUIDE.md`, fill in your org details, and run it. Takes 30-60 minutes. No technical setup required — you can paste the file into any AI assistant. See [Layer 1 details](apply.md) for the full guide.

??? question "I want to train my team on this"

    You need **Layer 2**. Open `personalise/PERSONALISE-L2-TRAINING-MATERIALS.md`, fill in your org details and roles, and run it. It produces per-role learning paths, workshop plans, and calibration exercises. Allow half a day. See [Layer 2 details](learn.md) for the full guide.

??? question "I want our own version of the site"

    You need **Layer 3**. Open `personalise/PERSONALISE-L3-CUSTOM-SITE.md`, fill in your org details, and run it. It forks the entire documentation site with your org-specific content. Allow a full day. See [Layer 3 details](customise.md) for the full guide.

## Additional tools

**[Build Your Business Case](business-case.md)** — Turn your Stage 1-2 findings into a one-page investment case for leadership approval.

**[Change Management Mapping](change-management.md)** — Map the framework's enablement tools to ADKAR, Kotter, or Prosci for organisations with formal change governance.

!!! tip "Start with Layer 1"
    Even if you plan to do Layers 2 or 3 eventually, start with Layer 1. The application guide it produces is the foundation for everything else — and it takes under an hour.
