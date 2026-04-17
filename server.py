#!/usr/bin/env python3
"""
Protocol MCP Server (Cloud Edition) - Streamable HTTP transport.
Protocols are bundled in the container image from protocols/ directory.
OCAP Lint tool bundled from tools/ocap_lint.py.

Author: Barry Kramer + Claude
License: MIT
"""

import json
import logging
import re
import os
import sys
from pathlib import Path
from typing import List, Dict, Any

from fastmcp import FastMCP

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

SERVER_NAME = "protocol_mcp"
SERVER_VERSION = "2.1.0-cloud"

_BASE_DIR = Path(__file__).resolve().parent
PROTOCOLS_DIR = _BASE_DIR / "protocols"
PROTOCOLS_DIR.mkdir(exist_ok=True)

# --- OCAP Lint integration ---
TOOLS_DIR = _BASE_DIR / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

try:
    import ocap_lint as _ocap_lint_mod
    OCAP_LINT_AVAILABLE = True
    logger.info("ocap_lint loaded successfully")
except ImportError as e:
    OCAP_LINT_AVAILABLE = False
    logger.warning(f"ocap_lint not available: {e}")

mcp = FastMCP(SERVER_NAME)

# --- Parsing ---

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
_HEADING_RE = re.compile(
    r"###\s*(?:Phase|Check)\s+(\d+)\s*[:\-\u2014]\s*(.+?)(?:\n|$)(.*?)"
    r"(?=###\s*(?:Phase|Check)\s+\d+|## [A-Z]|---|\Z)",
    re.DOTALL | re.IGNORECASE,
)
_BOLD_CHECK_RE = re.compile(
    r"\*\*Check\s+(\d+)\s*[:\-\u2014]\s*(.+?)\*\*\s*(.*?)"
    r"(?=\*\*Check\s+\d+|###\s*Check\s+\d+|## [A-Z]|---|\Z)",
    re.DOTALL | re.IGNORECASE,
)

def _parse_frontmatter(text):
    match = _FRONTMATTER_RE.match(text)
    if not match: return {}
    meta = {}
    for line in match.group(1).splitlines():
        line = line.strip()
        if ":" in line:
            key, _, val = line.partition(":")
            meta[key.strip().lower()] = val.strip().strip('"').strip("'")
    return meta

def _parse_phases(text):
    found = {}
    for m in _HEADING_RE.finditer(text):
        num = int(m.group(1))
        found[num] = {"number": num, "title": m.group(2).strip(), "content": m.group(3).strip()}
    for m in _BOLD_CHECK_RE.finditer(text):
        num = int(m.group(1))
        if num not in found:
            found[num] = {"number": num, "title": m.group(2).strip().rstrip("."), "content": m.group(3).strip()}
    return sorted(found.values(), key=lambda p: p["number"])

def _body_without_frontmatter(text):
    match = _FRONTMATTER_RE.match(text)
    return text[match.end():] if match else text

# --- Protocol Loader ---

def _load_all_protocols():
    protocols = {}
    if not PROTOCOLS_DIR.exists(): return protocols
    for fp in sorted(PROTOCOLS_DIR.glob("*.md")):
        try:
            raw = fp.read_text(encoding="utf-8")
            meta = _parse_frontmatter(raw)
            body = _body_without_frontmatter(raw)
            phases = _parse_phases(raw)
            pid = meta.get("id", fp.stem)
            protocols[pid] = {
                "id": pid, "name": meta.get("name", fp.stem.replace("-", " ").title()),
                "version": meta.get("version", "1.0"), "trigger": meta.get("trigger", ""),
                "summary": meta.get("summary", ""), "phase_count": len(phases),
                "phases": phases, "body": body, "raw": raw, "file": fp.name,
            }
        except Exception as exc:
            protocols[fp.stem] = {
                "id": fp.stem, "name": fp.stem, "version": "?", "trigger": "",
                "summary": f"Error: {exc}", "phase_count": 0,
                "phases": [], "body": "", "raw": "", "file": fp.name,
            }
    return protocols

# --- Tools ---

@mcp.tool()
def protocol_list() -> str:
    """List all protocols available in the protocol library."""
    protocols = _load_all_protocols()
    if not protocols: return "No protocols found."
    lines = ["# Protocol Library", ""]
    for p in protocols.values():
        lines.append(f"## {p['name']} (`{p['id']}`)")
        lines.append(f"- **Version**: {p['version']}")
        if p["trigger"]: lines.append(f"- **Trigger**: `{p['trigger']}`")
        if p["summary"]: lines.append(f"- **Summary**: {p['summary']}")
        lines.append(f"- **Phases**: {p['phase_count']}")
        lines.append("")
    return "\n".join(lines)

@mcp.tool()
def protocol_load(protocol_id: str) -> str:
    """Load the complete content of a protocol into the conversation context."""
    protocols = _load_all_protocols()
    pid = protocol_id.lower()
    if pid not in protocols:
        return f"Error: Protocol '{pid}' not found. Available: {', '.join(sorted(protocols.keys()))}"
    return protocols[pid]["raw"]

@mcp.tool()
def protocol_describe(protocol_id: str) -> str:
    """Get a protocol summary and phase list without loading full content."""
    protocols = _load_all_protocols()
    pid = protocol_id.lower()
    if pid not in protocols:
        return f"Error: Protocol '{pid}' not found. Available: {', '.join(sorted(protocols.keys()))}"
    p = protocols[pid]
    lines = [f"# {p['name']} (`{p['id']}`)", "", f"**Version**: {p['version']}"]
    if p["trigger"]: lines.append(f"**Trigger**: `{p['trigger']}`")
    lines.append("")
    if p["summary"]: lines.extend([p["summary"], ""])
    if p["phases"]:
        lines.extend(["## Phases", ""])
        for ph in p["phases"]:
            lines.append(f"- **Phase {ph['number']}**: {ph['title']}")
        lines.append("")
    return "\n".join(lines)

@mcp.tool()
def protocol_get_phase(protocol_id: str, phase_number: int) -> str:
    """Load a single phase from a protocol for focused execution."""
    protocols = _load_all_protocols()
    pid = protocol_id.lower()
    if pid not in protocols:
        return f"Error: Protocol '{pid}' not found. Available: {', '.join(sorted(protocols.keys()))}"
    p = protocols[pid]
    phase = next((ph for ph in p["phases"] if ph["number"] == phase_number), None)
    if phase is None:
        if not p["phases"]: return f"No phases parsed for '{p['name']}'. Use protocol_load."
        return f"Error: Phase {phase_number} not found. Available: {', '.join(str(ph['number']) for ph in p['phases'])}"
    return f"# {p['name']} -- Phase {phase['number']}: {phase['title']}\n\n{phase['content']}"

@mcp.tool()
def protocol_search(query: str) -> str:
    """Search across all protocols for a keyword or concept."""
    protocols = _load_all_protocols()
    q = query.lower()
    results = []
    for p in protocols.values():
        score, matches = 0, []
        if q in p["name"].lower(): score += 10; matches.append("name")
        if q in p["id"].lower(): score += 8; matches.append("id")
        if q in p.get("trigger", "").lower(): score += 8; matches.append("trigger")
        if q in p.get("summary", "").lower(): score += 5; matches.append("summary")
        for ph in p["phases"]:
            if q in ph["title"].lower(): score += 3; matches.append(f"phase {ph['number']}")
        if q in p.get("body", "").lower():
            score += 1
            if "content" not in matches: matches.append("content")
        if score > 0:
            results.append({"id": p["id"], "name": p["name"], "score": score,
                            "matches": matches, "summary": p["summary"]})
    results.sort(key=lambda r: r["score"], reverse=True)
    if not results: return f"No protocols matched '{query}'."
    lines = [f"# Search: '{query}'", f"Found {len(results)} match(es).", ""]
    for r in results:
        lines.append(f"## {r['name']} (`{r['id']}`) -- score {r['score']}")
        lines.append(f"- **Matched in**: {', '.join(r['matches'])}")
        if r["summary"]: lines.append(f"- **Summary**: {r['summary']}")
        lines.append("")
    return "\n".join(lines)


@mcp.tool()
def ocap_lint(content: str, output_format: str = "markdown") -> str:
    """Run OCAP v1.5 mechanical checks against outbound content.

    Executes deterministic pattern checks from the S-axis, F-axis, and A-axis.
    Returns findings as a structured report. Use this before presenting any
    outbound content to satisfy the OCAP v1.6 Recursive Audit Trace requirement
    for mechanical-check enforcement.

    Args:
        content: The text to lint. Typically a draft of outbound content
                 (LinkedIn post, email, article, caption, slide text).
        output_format: 'markdown' (default, human-readable) or 'json' (structured).

    Returns:
        A findings report. Empty findings means the mechanizable subset of
        OCAP checks passed. Non-empty findings enumerate each violation with
        check number, axis, severity, quoted text, and context. Judgment-based
        checks (F-axis facts, A.A intent integrity, some composition patterns)
        are NOT run by this tool and must be evaluated separately.
    """
    if not OCAP_LINT_AVAILABLE:
        return "ERROR: ocap_lint module not available. Check tools/ocap_lint.py deployment."

    if not content or not content.strip():
        return "ERROR: No content provided."

    try:
        findings = _ocap_lint_mod.lint(content)
    except Exception as exc:
        return f"ERROR running lint: {exc}"

    fmt = (output_format or "markdown").lower()

    if fmt == "json":
        return json.dumps({
            "total_findings": len(findings),
            "findings": [f.to_dict() for f in findings],
        }, indent=2)

    # Markdown format
    if not findings:
        return "# OCAP Lint — CLEAN\n\nZero mechanical findings. Judgment-based checks still required."

    lines = [f"# OCAP Lint — {len(findings)} finding(s)", ""]
    by_axis = {"F": [], "S": [], "A": []}
    for f in findings:
        by_axis[f.axis].append(f)
    for axis_label, axis_name in [("F", "F-axis (Factual)"), ("S", "S-axis (Signature)"), ("A", "A-axis (Architectural)")]:
        axis_findings = by_axis[axis_label]
        if not axis_findings:
            continue
        lines.append(f"## {axis_name} — {len(axis_findings)} finding(s)")
        lines.append("")
        for f in axis_findings:
            lines.append(f"- **Check {f.check:02d}** ({f.severity}) — {f.name}")
            lines.append(f"  - Quote: `{f.quote}`")
            if f.line:
                lines.append(f"  - Line: {f.line}")
            if f.context and f.context != f.quote:
                lines.append(f"  - Context: {f.context}")
        lines.append("")
    lines.append("---")
    lines.append("Judgment-based checks not covered by this tool must be evaluated separately.")
    return "\n".join(lines)


# --- Entrypoint ---

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"Starting protocol_mcp {SERVER_VERSION} on port {port}")
    logger.info(f"Protocols found: {len(list(PROTOCOLS_DIR.glob('*.md')))}")
    logger.info(f"OCAP lint available: {OCAP_LINT_AVAILABLE}")
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port)
