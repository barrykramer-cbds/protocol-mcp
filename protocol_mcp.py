#!/usr/bin/env python3
"""
Protocol MCP Server — Persistent Protocol Library for Claude

A FastMCP server that makes cognitive protocols (LBP, DAP, OCAP, Sidebar,
Commit, Strength, etc.) persistently available across all Claude conversation
spaces. Protocols are stored as markdown files with YAML frontmatter in the
protocols/ directory. Drop a new .md file to add a protocol — no rebuild needed.

Phase 1: Protocol retrieval + structured phase access (v1.0)
Phase 2: Cross-session state persistence (v1.1)

Author: Barry Kramer + Claude
Created: 2026-04-14
License: MIT
"""

import json
import re
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List, Dict, Any
from enum import Enum

from pydantic import BaseModel, Field, field_validator, ConfigDict
from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SERVER_NAME = "protocol_mcp"
SERVER_VERSION = "1.1.0"

# Resolve directories relative to this file
_BASE_DIR = Path(__file__).resolve().parent
PROTOCOLS_DIR = _BASE_DIR / "protocols"
SESSIONS_DIR = _BASE_DIR / "sessions"

# Ensure directories exist
PROTOCOLS_DIR.mkdir(exist_ok=True)
SESSIONS_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# Initialize MCP Server
# ---------------------------------------------------------------------------

mcp = FastMCP(SERVER_NAME)

# ---------------------------------------------------------------------------
# OCAP Lint Integration
# ---------------------------------------------------------------------------

TOOLS_DIR = _BASE_DIR / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

try:
    import ocap_lint as _ocap_lint_mod  # noqa: E402
    OCAP_LINT_AVAILABLE = True
except ImportError:
    OCAP_LINT_AVAILABLE = False
    _ocap_lint_mod = None


# ---------------------------------------------------------------------------
# Frontmatter + Phase/Check Parsing
# ---------------------------------------------------------------------------

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

# Pattern 1: ### Phase N: TITLE  or  ### Check N: TITLE  (heading-level items)
_HEADING_RE = re.compile(
    r"###\s*(?:Phase|Check)\s+(\d+)\s*[:\-\u2014]\s*(.+?)(?:\n|$)(.*?)"
    r"(?=###\s*(?:Phase|Check)\s+\d+|## [A-Z]|---|\Z)",
    re.DOTALL | re.IGNORECASE,
)

# Pattern 2: **Check N: TITLE** (bold inline items, used by OCAP Tier 1)
_BOLD_CHECK_RE = re.compile(
    r"\*\*Check\s+(\d+)\s*[:\-\u2014]\s*(.+?)\*\*\s*(.*?)"
    r"(?=\*\*Check\s+\d+|###\s*Check\s+\d+|## [A-Z]|---|\Z)",
    re.DOTALL | re.IGNORECASE,
)


def _parse_frontmatter(text: str) -> Dict[str, str]:
    """Extract YAML-like frontmatter as a simple key: value dict."""
    match = _FRONTMATTER_RE.match(text)
    if not match:
        return {}
    meta: Dict[str, str] = {}
    for line in match.group(1).splitlines():
        line = line.strip()
        if ":" in line:
            key, _, val = line.partition(":")
            meta[key.strip().lower()] = val.strip().strip('"').strip("'")
    return meta


def _parse_phases(text: str) -> List[Dict[str, Any]]:
    """Extract numbered phases or checks from the protocol body.

    Supports three patterns (merged and deduplicated):
      - ### Phase N: TITLE   (standard phase headings)
      - ### Check N: TITLE   (check headings, used by OCAP Tier 2)
      - **Check N: TITLE**   (bold inline checks, used by OCAP Tier 1)
    Results are merged by number (heading wins over bold if both match)
    and sorted numerically.
    """
    found: Dict[int, Dict[str, Any]] = {}

    # Pass 1: heading-level items (### Phase N or ### Check N)
    for m in _HEADING_RE.finditer(text):
        num = int(m.group(1))
        found[num] = {
            "number": num,
            "title": m.group(2).strip(),
            "content": m.group(3).strip(),
        }

    # Pass 2: bold inline checks (**Check N: ...**)
    for m in _BOLD_CHECK_RE.finditer(text):
        num = int(m.group(1))
        if num not in found:
            found[num] = {
                "number": num,
                "title": m.group(2).strip().rstrip("."),
                "content": m.group(3).strip(),
            }

    return sorted(found.values(), key=lambda p: p["number"])


def _body_without_frontmatter(text: str) -> str:
    """Return protocol content with frontmatter stripped."""
    match = _FRONTMATTER_RE.match(text)
    if match:
        return text[match.end():]
    return text


# ---------------------------------------------------------------------------
# Protocol Loader
# ---------------------------------------------------------------------------

def _load_all_protocols() -> Dict[str, Dict[str, Any]]:
    """Scan the protocols directory and parse all .md files."""
    protocols: Dict[str, Dict[str, Any]] = {}
    if not PROTOCOLS_DIR.exists():
        return protocols
    for fp in sorted(PROTOCOLS_DIR.glob("*.md")):
        try:
            raw = fp.read_text(encoding="utf-8")
            meta = _parse_frontmatter(raw)
            body = _body_without_frontmatter(raw)
            phases = _parse_phases(raw)

            pid = meta.get("id", fp.stem)
            protocols[pid] = {
                "id": pid,
                "name": meta.get("name", fp.stem.replace("-", " ").title()),
                "version": meta.get("version", "1.0"),
                "trigger": meta.get("trigger", ""),
                "summary": meta.get("summary", ""),
                "phase_count": len(phases),
                "phases": phases,
                "body": body,
                "raw": raw,
                "file": fp.name,
            }
        except Exception as exc:
            protocols[fp.stem] = {
                "id": fp.stem,
                "name": fp.stem,
                "version": "?",
                "trigger": "",
                "summary": f"Error loading: {exc}",
                "phase_count": 0,
                "phases": [],
                "body": "",
                "raw": "",
                "file": fp.name,
            }
    return protocols


# ---------------------------------------------------------------------------
# Session Utilities (Phase 2)
# ---------------------------------------------------------------------------

def _now_iso() -> str:
    """Current time as ISO string with timezone."""
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _generate_session_id(protocol_id: str) -> str:
    """Generate a unique session ID: {protocol}_{date}_{sequence}."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    prefix = f"{protocol_id}_{date_str}_"

    # Find next sequence number
    existing = list(SESSIONS_DIR.glob(f"{prefix}*.json"))
    seq = len(existing) + 1
    return f"{prefix}{seq:03d}"


def _load_session(session_id: str) -> Optional[Dict[str, Any]]:
    """Load a session file by ID. Returns None if not found."""
    fp = SESSIONS_DIR / f"{session_id}.json"
    if not fp.exists():
        return None
    try:
        return json.loads(fp.read_text(encoding="utf-8"))
    except Exception:
        return None


def _save_session(session: Dict[str, Any]) -> bool:
    """Write a session dict to its JSON file. Returns True on success."""
    fp = SESSIONS_DIR / f"{session['session_id']}.json"
    try:
        fp.write_text(
            json.dumps(session, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return True
    except Exception:
        return False


def _list_all_sessions(protocol_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """List session summaries, optionally filtered by protocol."""
    sessions: List[Dict[str, Any]] = []
    for fp in sorted(SESSIONS_DIR.glob("*.json"), reverse=True):
        try:
            data = json.loads(fp.read_text(encoding="utf-8"))
            if protocol_id and data.get("protocol_id") != protocol_id:
                continue
            sessions.append({
                "session_id": data.get("session_id", fp.stem),
                "protocol_id": data.get("protocol_id", "?"),
                "protocol_name": data.get("protocol_name", "?"),
                "status": data.get("status", "unknown"),
                "current_phase": data.get("current_phase", 0),
                "created": data.get("created", "?"),
                "updated": data.get("updated", "?"),
            })
        except Exception:
            continue
    return sessions


# ---------------------------------------------------------------------------
# Pydantic Input Models
# ---------------------------------------------------------------------------

class ResponseFormat(str, Enum):
    MARKDOWN = "markdown"
    JSON = "json"


class ProtocolIdInput(BaseModel):
    """Input for single-protocol operations."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    protocol_id: str = Field(
        ...,
        description=(
            "Protocol identifier (e.g. 'lbp', 'dap', 'ocap'). "
            "Use protocol_list to discover available IDs."
        ),
        min_length=1,
        max_length=50,
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' (default) or 'json'",
    )


class PhaseInput(BaseModel):
    """Input for phase-specific operations."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    protocol_id: str = Field(
        ...,
        description="Protocol identifier",
        min_length=1,
        max_length=50,
    )
    phase_number: int = Field(
        ...,
        description="Phase number (1-indexed)",
        ge=1,
        le=50,
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' (default) or 'json'",
    )


class SearchInput(BaseModel):
    """Input for protocol search."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    query: str = Field(
        ...,
        description=(
            "Search term to find across protocol names, summaries, and content"
        ),
        min_length=1,
        max_length=200,
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' (default) or 'json'",
    )


class ListInput(BaseModel):
    """Input for listing protocols."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' (default) or 'json'",
    )


class OcapLintInput(BaseModel):
    """Input for running OCAP lint against outbound content."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    content: str = Field(
        ...,
        description="Outbound content to lint (LinkedIn post, email, caption, slide text, etc.)",
        min_length=1,
        max_length=200000,
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' (default) or 'json'",
    )


# Phase 2 input models

class StartSessionInput(BaseModel):
    """Input for starting a new protocol session."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    protocol_id: str = Field(
        ...,
        description="Protocol to begin executing (e.g. 'lbp', 'dap')",
        min_length=1,
        max_length=50,
    )
    notes: Optional[str] = Field(
        default=None,
        description="Optional notes or context for this session",
        max_length=2000,
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' (default) or 'json'",
    )


class SaveStateInput(BaseModel):
    """Input for saving session state."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    session_id: str = Field(
        ...,
        description="Session ID returned by protocol_start_session",
        min_length=1,
        max_length=100,
    )
    current_phase: Optional[int] = Field(
        default=None,
        description="Phase/check number currently on or just completed",
        ge=0,
        le=50,
    )
    status: Optional[str] = Field(
        default=None,
        description="Session status: 'in_progress', 'paused', 'completed', 'abandoned'",
    )
    data: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Working data to persist (any JSON-serializable dict). Merged with existing data.",
    )
    notes: Optional[str] = Field(
        default=None,
        description="Optional notes to append to the session",
        max_length=2000,
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' (default) or 'json'",
    )


class ResumeInput(BaseModel):
    """Input for resuming a session."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    session_id: str = Field(
        ...,
        description="Session ID to resume",
        min_length=1,
        max_length=100,
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' (default) or 'json'",
    )


class ListSessionsInput(BaseModel):
    """Input for listing sessions."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    protocol_id: Optional[str] = Field(
        default=None,
        description="Filter sessions by protocol ID. Omit to list all sessions.",
        max_length=50,
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' (default) or 'json'",
    )


# ---------------------------------------------------------------------------
# Tools — Layer 1: Protocol Retrieval
# ---------------------------------------------------------------------------

@mcp.tool(
    name="protocol_list",
    annotations={
        "title": "List Available Protocols",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def protocol_list(params: ListInput) -> str:
    """List all protocols available in the protocol library.

    Returns a catalog of every protocol with its ID, name, version, trigger
    command, summary, and phase count. Use this to discover what protocols
    are available before loading or executing one.

    Args:
        params (ListInput): Optional response format preference.

    Returns:
        str: Protocol catalog in markdown or JSON format.
    """
    protocols = _load_all_protocols()

    if not protocols:
        return "No protocols found. Add .md files to the protocols/ directory."

    if params.response_format == ResponseFormat.JSON:
        catalog = [
            {
                "id": p["id"],
                "name": p["name"],
                "version": p["version"],
                "trigger": p["trigger"],
                "summary": p["summary"],
                "phases": p["phase_count"],
                "file": p["file"],
            }
            for p in protocols.values()
        ]
        return json.dumps({"protocols": catalog, "count": len(catalog)}, indent=2)

    lines = ["# Protocol Library", ""]
    for p in protocols.values():
        lines.append(f"## {p['name']} (`{p['id']}`)")
        lines.append(f"- **Version**: {p['version']}")
        if p["trigger"]:
            lines.append(f"- **Trigger**: `{p['trigger']}`")
        if p["summary"]:
            lines.append(f"- **Summary**: {p['summary']}")
        lines.append(f"- **Phases**: {p['phase_count']}")
        lines.append("")
    return "\n".join(lines)


@mcp.tool(
    name="protocol_load",
    annotations={
        "title": "Load Full Protocol",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def protocol_load(params: ProtocolIdInput) -> str:
    """Load the complete content of a protocol into the conversation context.

    Returns the full protocol document including all phases, examples, and
    implementation notes. Use this when you need the entire protocol available
    for reasoning or when the user invokes a protocol trigger command.

    Args:
        params (ProtocolIdInput): Protocol ID and format preference.

    Returns:
        str: Full protocol content in markdown or JSON format.
    """
    protocols = _load_all_protocols()
    pid = params.protocol_id.lower()

    if pid not in protocols:
        available = ", ".join(sorted(protocols.keys()))
        return f"Error: Protocol '{pid}' not found. Available: {available}"

    p = protocols[pid]

    if params.response_format == ResponseFormat.JSON:
        return json.dumps({
            "id": p["id"],
            "name": p["name"],
            "version": p["version"],
            "trigger": p["trigger"],
            "summary": p["summary"],
            "phase_count": p["phase_count"],
            "phases": p["phases"],
            "content": p["body"],
        }, indent=2)

    return p["raw"]


@mcp.tool(
    name="protocol_describe",
    annotations={
        "title": "Describe Protocol (Summary)",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def protocol_describe(params: ProtocolIdInput) -> str:
    """Get a protocol summary, phase list, and metadata without loading full content.

    Returns the protocol overview including the list of phase titles and
    descriptions. Lighter than protocol_load. Use when you need to understand
    what a protocol does before committing to full context loading.

    Args:
        params (ProtocolIdInput): Protocol ID and format preference.

    Returns:
        str: Protocol summary with phase titles in markdown or JSON format.
    """
    protocols = _load_all_protocols()
    pid = params.protocol_id.lower()

    if pid not in protocols:
        available = ", ".join(sorted(protocols.keys()))
        return f"Error: Protocol '{pid}' not found. Available: {available}"

    p = protocols[pid]

    if params.response_format == ResponseFormat.JSON:
        return json.dumps({
            "id": p["id"],
            "name": p["name"],
            "version": p["version"],
            "trigger": p["trigger"],
            "summary": p["summary"],
            "phase_count": p["phase_count"],
            "phases": [
                {"number": ph["number"], "title": ph["title"]}
                for ph in p["phases"]
            ],
        }, indent=2)

    lines = [
        f"# {p['name']} (`{p['id']}`)",
        "",
        f"**Version**: {p['version']}",
    ]
    if p["trigger"]:
        lines.append(f"**Trigger**: `{p['trigger']}`")
    lines.append("")
    if p["summary"]:
        lines.append(p["summary"])
        lines.append("")
    if p["phases"]:
        lines.append("## Phases")
        lines.append("")
        for ph in p["phases"]:
            lines.append(f"- **Phase {ph['number']}**: {ph['title']}")
        lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Tools — Layer 2: Structured Phase Execution
# ---------------------------------------------------------------------------

@mcp.tool(
    name="protocol_get_phase",
    annotations={
        "title": "Get Specific Phase",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def protocol_get_phase(params: PhaseInput) -> str:
    """Load a single phase from a protocol for focused execution.

    Returns the content of one specific phase, including its instructions,
    examples, and any sub-steps. Use when executing a protocol step-by-step
    to minimize context window consumption.

    Args:
        params (PhaseInput): Protocol ID, phase number, and format preference.

    Returns:
        str: Phase content in markdown or JSON format.
    """
    protocols = _load_all_protocols()
    pid = params.protocol_id.lower()

    if pid not in protocols:
        available = ", ".join(sorted(protocols.keys()))
        return f"Error: Protocol '{pid}' not found. Available: {available}"

    p = protocols[pid]
    phase = None
    for ph in p["phases"]:
        if ph["number"] == params.phase_number:
            phase = ph
            break

    if phase is None:
        if not p["phases"]:
            return (
                f"No individually-addressable phases/checks parsed for '{p['name']}'. "
                f"Use protocol_load to access the full protocol content."
            )
        available_phases = [str(ph["number"]) for ph in p["phases"]]
        return (
            f"Error: Phase {params.phase_number} not found in '{p['name']}'. "
            f"Available: {', '.join(available_phases)}"
        )

    if params.response_format == ResponseFormat.JSON:
        return json.dumps({
            "protocol_id": p["id"],
            "protocol_name": p["name"],
            "phase": phase,
        }, indent=2)

    lines = [
        f"# {p['name']} -- Phase {phase['number']}: {phase['title']}",
        "",
        phase["content"],
    ]
    return "\n".join(lines)


@mcp.tool(
    name="protocol_search",
    annotations={
        "title": "Search Protocols",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def protocol_search(params: SearchInput) -> str:
    """Search across all protocols for a keyword or concept.

    Searches protocol names, summaries, phase titles, and full content.
    Returns matching protocols ranked by relevance (name/summary matches
    rank higher than body matches). Use when unsure which protocol applies
    to the current task.

    Args:
        params (SearchInput): Search query and format preference.

    Returns:
        str: Matching protocols with context in markdown or JSON format.
    """
    protocols = _load_all_protocols()
    query = params.query.lower()
    results: List[Dict[str, Any]] = []

    for p in protocols.values():
        score = 0
        matches: List[str] = []

        if query in p["name"].lower():
            score += 10
            matches.append("name")

        if query in p["id"].lower():
            score += 8
            matches.append("id")

        if query in p.get("trigger", "").lower():
            score += 8
            matches.append("trigger")

        if query in p.get("summary", "").lower():
            score += 5
            matches.append("summary")

        for ph in p["phases"]:
            if query in ph["title"].lower():
                score += 3
                matches.append(f"phase {ph['number']}: {ph['title']}")

        if query in p.get("body", "").lower():
            score += 1
            if "content" not in [m for m in matches]:
                matches.append("content")

        if score > 0:
            results.append({
                "id": p["id"],
                "name": p["name"],
                "score": score,
                "matches": matches,
                "summary": p["summary"],
                "trigger": p["trigger"],
            })

    results.sort(key=lambda r: r["score"], reverse=True)

    if not results:
        return f"No protocols matched '{params.query}'."

    if params.response_format == ResponseFormat.JSON:
        return json.dumps(
            {"query": params.query, "results": results}, indent=2
        )

    lines = [f"# Search: '{params.query}'", f"Found {len(results)} match(es).", ""]
    for r in results:
        lines.append(f"## {r['name']} (`{r['id']}`) -- score {r['score']}")
        lines.append(f"- **Matched in**: {', '.join(r['matches'])}")
        if r["summary"]:
            lines.append(f"- **Summary**: {r['summary']}")
        if r["trigger"]:
            lines.append(f"- **Trigger**: `{r['trigger']}`")
        lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Tools — Layer 3: Cross-Session State Persistence (Phase 2)
# ---------------------------------------------------------------------------

@mcp.tool(
    name="protocol_start_session",
    annotations={
        "title": "Start Protocol Session",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": False,
    },
)
async def protocol_start_session(params: StartSessionInput) -> str:
    """Begin a tracked protocol execution session.

    Creates a new session file that persists across conversations. Use this
    when starting a protocol execution that may span multiple sessions.
    Returns a session_id that can be used with protocol_save_state and
    protocol_resume.

    Args:
        params (StartSessionInput): Protocol ID, optional notes, format.

    Returns:
        str: Session ID and initial state in markdown or JSON format.
    """
    protocols = _load_all_protocols()
    pid = params.protocol_id.lower()

    if pid not in protocols:
        available = ", ".join(sorted(protocols.keys()))
        return f"Error: Protocol '{pid}' not found. Available: {available}"

    p = protocols[pid]
    session_id = _generate_session_id(pid)
    now = _now_iso()

    session = {
        "session_id": session_id,
        "protocol_id": pid,
        "protocol_name": p["name"],
        "created": now,
        "updated": now,
        "current_phase": 1,
        "status": "in_progress",
        "data": {},
        "notes": params.notes or "",
        "history": [
            {"timestamp": now, "action": "session_started", "phase": 1}
        ],
    }

    if not _save_session(session):
        return f"Error: Failed to create session file for '{session_id}'."

    if params.response_format == ResponseFormat.JSON:
        return json.dumps(session, indent=2)

    lines = [
        f"# Session Started: `{session_id}`",
        "",
        f"- **Protocol**: {p['name']} (`{pid}`)",
        f"- **Status**: in_progress",
        f"- **Current Phase**: 1",
        f"- **Created**: {now}",
    ]
    if params.notes:
        lines.append(f"- **Notes**: {params.notes}")
    lines.append("")
    if p["phases"]:
        lines.append(f"**Next up — Phase 1: {p['phases'][0]['title']}**")
    lines.append("")
    lines.append(
        "Use `protocol_save_state` to save progress. "
        "Use `protocol_resume` in a new conversation to continue."
    )
    return "\n".join(lines)


@mcp.tool(
    name="protocol_save_state",
    annotations={
        "title": "Save Session State",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def protocol_save_state(params: SaveStateInput) -> str:
    """Save current progress and working data for a protocol session.

    Updates the session file with current phase, status, and any working
    data generated during protocol execution. Data is merged with existing
    session data (new keys are added, existing keys are updated).

    Args:
        params (SaveStateInput): Session ID, phase, status, data, notes.

    Returns:
        str: Updated session summary in markdown or JSON format.
    """
    session = _load_session(params.session_id)
    if session is None:
        return f"Error: Session '{params.session_id}' not found."

    now = _now_iso()
    session["updated"] = now

    # Update fields if provided
    if params.current_phase is not None:
        session["current_phase"] = params.current_phase
    if params.status is not None:
        session["status"] = params.status
    if params.notes is not None:
        existing_notes = session.get("notes", "")
        if existing_notes:
            session["notes"] = f"{existing_notes}\n---\n{params.notes}"
        else:
            session["notes"] = params.notes

    # Merge data (shallow merge — new keys added, existing keys overwritten)
    if params.data is not None:
        existing_data = session.get("data", {})
        existing_data.update(params.data)
        session["data"] = existing_data

    # Append to history
    history_entry = {"timestamp": now, "action": "state_saved"}
    if params.current_phase is not None:
        history_entry["phase"] = params.current_phase
    if params.status is not None:
        history_entry["status"] = params.status
    session.setdefault("history", []).append(history_entry)

    if not _save_session(session):
        return f"Error: Failed to save session '{params.session_id}'."

    if params.response_format == ResponseFormat.JSON:
        return json.dumps(session, indent=2)

    lines = [
        f"# Session Saved: `{session['session_id']}`",
        "",
        f"- **Protocol**: {session['protocol_name']}",
        f"- **Status**: {session['status']}",
        f"- **Current Phase**: {session['current_phase']}",
        f"- **Updated**: {now}",
    ]
    if session.get("data"):
        lines.append(f"- **Data keys**: {', '.join(session['data'].keys())}")
    lines.append("")
    return "\n".join(lines)


@mcp.tool(
    name="protocol_resume",
    annotations={
        "title": "Resume Protocol Session",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def protocol_resume(params: ResumeInput) -> str:
    """Resume a previously saved protocol session in a new conversation.

    Loads the full session state including current phase, all working data,
    notes, and history. Also loads the content of the current phase from the
    protocol so execution can continue immediately.

    Args:
        params (ResumeInput): Session ID and format preference.

    Returns:
        str: Full session state + current phase content.
    """
    session = _load_session(params.session_id)
    if session is None:
        return f"Error: Session '{params.session_id}' not found."

    # Load the protocol to get current phase content
    protocols = _load_all_protocols()
    pid = session.get("protocol_id", "")
    current_phase_content = ""
    current_phase_title = ""

    if pid in protocols:
        p = protocols[pid]
        for ph in p["phases"]:
            if ph["number"] == session.get("current_phase"):
                current_phase_title = ph["title"]
                current_phase_content = ph["content"]
                break

    if params.response_format == ResponseFormat.JSON:
        result = dict(session)
        result["current_phase_title"] = current_phase_title
        result["current_phase_content"] = current_phase_content
        return json.dumps(result, indent=2)

    lines = [
        f"# Resuming Session: `{session['session_id']}`",
        "",
        f"- **Protocol**: {session.get('protocol_name', '?')}",
        f"- **Status**: {session.get('status', '?')}",
        f"- **Current Phase**: {session.get('current_phase', '?')}",
        f"- **Created**: {session.get('created', '?')}",
        f"- **Last Updated**: {session.get('updated', '?')}",
    ]

    # Show notes
    if session.get("notes"):
        lines.append("")
        lines.append("## Notes")
        lines.append(session["notes"])

    # Show working data
    if session.get("data"):
        lines.append("")
        lines.append("## Working Data")
        lines.append("```json")
        lines.append(json.dumps(session["data"], indent=2, ensure_ascii=False))
        lines.append("```")

    # Show current phase content
    if current_phase_content:
        lines.append("")
        lines.append(
            f"## Current Phase — {session.get('current_phase', '?')}: "
            f"{current_phase_title}"
        )
        lines.append("")
        lines.append(current_phase_content)

    # Show history
    if session.get("history"):
        lines.append("")
        lines.append("## Session History")
        for h in session["history"]:
            parts = [h.get("timestamp", "?"), h.get("action", "?")]
            if "phase" in h:
                parts.append(f"phase {h['phase']}")
            if "status" in h:
                parts.append(h["status"])
            lines.append(f"- {' | '.join(parts)}")

    lines.append("")
    return "\n".join(lines)


@mcp.tool(
    name="protocol_list_sessions",
    annotations={
        "title": "List Protocol Sessions",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def protocol_list_sessions(params: ListSessionsInput) -> str:
    """List all saved protocol sessions, optionally filtered by protocol.

    Returns session summaries sorted by most recent first. Use this to find
    previous sessions before calling protocol_resume.

    Args:
        params (ListSessionsInput): Optional protocol filter and format.

    Returns:
        str: Session list in markdown or JSON format.
    """
    sessions = _list_all_sessions(
        protocol_id=params.protocol_id.lower() if params.protocol_id else None
    )

    if not sessions:
        if params.protocol_id:
            return f"No sessions found for protocol '{params.protocol_id}'."
        return "No sessions found. Use protocol_start_session to begin one."

    if params.response_format == ResponseFormat.JSON:
        return json.dumps({"sessions": sessions, "count": len(sessions)}, indent=2)

    lines = ["# Protocol Sessions", ""]
    if params.protocol_id:
        lines.append(f"Filtered by: `{params.protocol_id}`")
        lines.append("")
    lines.append(f"Found {len(sessions)} session(s).")
    lines.append("")

    for s in sessions:
        status_icon = {
            "in_progress": "\u25b6",
            "paused": "\u23f8",
            "completed": "\u2705",
            "abandoned": "\u274c",
        }.get(s["status"], "\u2753")

        lines.append(
            f"- {status_icon} **`{s['session_id']}`** "
            f"({s['protocol_name']}) "
            f"phase {s['current_phase']} | {s['status']} | "
            f"updated {s['updated']}"
        )

    lines.append("")
    lines.append("Use `protocol_resume` with a session_id to continue.")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Tools -- Layer 3: OCAP Mechanical Enforcement
# ---------------------------------------------------------------------------

@mcp.tool(
    name="ocap_lint",
    annotations={
        "title": "OCAP Mechanical Lint",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def ocap_lint(params: OcapLintInput) -> str:
    """Run OCAP v1.5 mechanical checks against outbound content.

    Executes deterministic pattern checks from the S-axis, F-axis, and A-axis.
    Returns findings as a structured report. Use this before presenting any
    outbound content to satisfy the OCAP Recursive Audit Trace requirement
    for mechanical-check enforcement.

    Args:
        params (OcapLintInput): content to lint and output format preference.

    Returns:
        str: A findings report. Empty findings means the mechanizable subset
             of OCAP checks passed. Non-empty findings enumerate each
             violation with check number, axis, severity, quote, and context.
             Judgment-based checks (F-axis facts, A.A intent integrity, some
             composition patterns) are NOT run by this tool and must be
             evaluated separately.
    """
    if not OCAP_LINT_AVAILABLE:
        return "ERROR: ocap_lint module not available. Check tools/ocap_lint.py deployment."

    if not params.content.strip():
        return "ERROR: No content provided."

    try:
        findings = _ocap_lint_mod.lint(params.content)
    except Exception as exc:
        return f"ERROR running lint: {exc}"

    if params.response_format == ResponseFormat.JSON:
        return json.dumps({
            "total_findings": len(findings),
            "findings": [f.to_dict() for f in findings],
        }, indent=2)

    if not findings:
        return (
            "# OCAP Lint -- CLEAN\n\n"
            "Zero mechanical findings. Judgment-based checks still required."
        )

    lines = [f"# OCAP Lint -- {len(findings)} finding(s)", ""]
    by_axis = {"F": [], "S": [], "A": []}
    for f in findings:
        by_axis[f.axis].append(f)

    axis_names = [
        ("F", "F-axis (Factual)"),
        ("S", "S-axis (Signature)"),
        ("A", "A-axis (Architectural)"),
    ]
    for axis_label, axis_name in axis_names:
        axis_findings = by_axis[axis_label]
        if not axis_findings:
            continue
        lines.append(f"## {axis_name} -- {len(axis_findings)} finding(s)")
        lines.append("")
        for f in axis_findings:
            lines.append(f"- **Check {f.check:02d}** ({f.severity}) -- {f.name}")
            lines.append(f"  - Quote: `{f.quote}`")
            if f.line:
                lines.append(f"  - Line: {f.line}")
            if f.context and f.context != f.quote:
                lines.append(f"  - Context: {f.context}")
        lines.append("")

    lines.append("---")
    lines.append(
        "Judgment-based checks (F-axis factual verification, A.A intent "
        "integrity, composition-level patterns) are NOT covered by this "
        "tool and must be evaluated separately."
    )
    return "\n".join(lines)


if __name__ == "__main__":
    mcp.run()
