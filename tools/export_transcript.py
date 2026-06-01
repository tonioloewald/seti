#!/usr/bin/env python3
"""Render a Claude Code session JSONL into a readable, PII-scrubbed markdown
transcript, for transparency archival alongside the pre-registration.

Tool calls (edits, searches, shell, git) are summarized, not dumped — the full
effect of every change is in the git history. Human prompts and Claude's prose
are preserved. Personal paths/emails are scrubbed.

Usage:  python3 tools/export_transcript.py [path/to/session.jsonl]
        (with no arg, picks the most recent session for this project)
"""
import json, glob, os, re, sys
from collections import Counter

PROJECT_DIR = os.path.expanduser("~/.claude/projects/-home-tonio-seti")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "docs", "transcripts", "claude-session.md")

def latest_jsonl():
    files = glob.glob(os.path.join(PROJECT_DIR, "*.jsonl"))
    return max(files, key=os.path.getmtime) if files else None

def scrub(s):
    if not s:
        return ""
    s = re.sub(r"<system-reminder>.*?</system-reminder>", "", s, flags=re.DOTALL)
    s = re.sub(r"</?command-[a-z-]+>", "", s)
    s = s.replace("/home/tonio", "~")
    s = re.sub(r"[\w.+-]+@[\w.-]+\.\w+", "[email]", s)
    return s.strip()

def parse_content(content):
    """Return (text, tool_names, is_tool_result)."""
    if isinstance(content, str):
        return content, [], False
    texts, tools = [], []
    for b in content:
        if not isinstance(b, dict):
            continue
        t = b.get("type")
        if t == "text":
            texts.append(b.get("text", ""))
        elif t == "tool_use":
            tools.append(b.get("name", "tool"))
        elif t == "tool_result":
            return "", [], True
    return "\n".join(texts), tools, False

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else latest_jsonl()
    if not path:
        sys.exit("no session JSONL found")
    out = [
        "# Claude Code session transcript",
        "",
        "*The working conversation that developed this pre-registration, exported "
        "for transparency. Tool calls (file edits, web searches, git commits, shell "
        "commands) are summarized rather than shown in full — the complete effect of "
        "every change is recorded in the git history. Personal paths and addresses "
        "are scrubbed.*",
        "",
        "---",
        "",
    ]
    nh = na = 0
    last_role = None
    for line in open(path, encoding="utf-8"):
        try:
            o = json.loads(line)
        except Exception:
            continue
        if o.get("isMeta"):
            continue  # skip skill instructions / injected scaffolding (not conversation)
        if o.get("isCompactSummary") or o.get("isVisibleInTranscriptOnly"):
            continue  # auto-generated context-compaction summary, injected with a
            # user role — NOT something Tonio said. The turns it summarizes are
            # already present verbatim earlier in this same log, so dropping it
            # loses nothing and avoids mis-attributing a machine summary to a human.
        typ = o.get("type")
        msg = o.get("message")
        if not isinstance(msg, dict):
            continue
        text, tools, is_tr = parse_content(msg.get("content"))
        if typ == "user":
            if is_tr:
                continue
            text = scrub(text)
            if not text:
                continue
            out.append("### 🧑 Tonio\n")
            out.append(text + "\n")
            last_role = "user"
            nh += 1
        elif typ == "assistant":
            text = scrub(text)
            block = ""
            if last_role != "assistant":
                block += "### 🤖 Claude\n\n"
            if text:
                block += text + "\n"
            if tools:
                c = Counter(tools)
                summ = ", ".join(f"{k}×{v}" if v > 1 else k for k, v in c.items())
                block += f"\n_[tools: {summ}]_\n"
            if text or tools:
                out.append(block)
                last_role = "assistant"
                na += 1
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print(f"wrote {OUT}")
    print(f"human turns: {nh}, assistant blocks: {na}, "
          f"size: {os.path.getsize(OUT)//1024} KB")

if __name__ == "__main__":
    main()
