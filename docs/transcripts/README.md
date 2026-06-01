# Development transcripts

Per the **Statement of Provenance and Acknowledgments** in [`../../preregistration.md`](../../preregistration.md), this directory archives the working AI-collaboration transcripts that developed the pre-registration — so the exact evolution of the methodology, and the true nature of the human–AI synthesis, are open to inspection.

## What's here

| File | Source | Notes |
|------|--------|-------|
| [`claude-session.md`](claude-session.md) | Anthropic Claude (Claude Code) | Auto-exported from the local session log by [`../../tools/export_transcript.py`](../../tools/export_transcript.py). |
| [`gemini-session.md`](gemini-session.md) | Google Gemini | Captured manually — pasted by the investigator (Gemini has no transcript API). |

## Redaction and fidelity

These are the **complete** conversations, with only minimal, disclosed redaction:

- Personal identifiers (email addresses, local home paths) are removed.
- System scaffolding (harness reminders, system prompts) is omitted.
- **Tool actions** (file edits, web searches, shell commands, git operations) are **summarized**, not shown in full — every change's complete effect is preserved in this repository's **git history**, which is the authoritative record.

Human prompts and AI prose are otherwise preserved verbatim.

## Gemini sessions

Gemini provides no export API and its share pages are JavaScript-rendered, so its transcripts cannot be captured automatically. They are added here manually from the investigator's copy.

A copy of the shared session is archived here as [`gemini-session.md`](gemini-session.md) (pasted by the investigator). The original share link — which may change or expire, so the archived copy is the durable record — was: <https://gemini.google.com/share/7b970cdc72af>
