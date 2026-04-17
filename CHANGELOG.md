# Changelog

All notable changes to the Protocol MCP Server.

## [Protocol Content] - 2026-04-16 (later)

### OCAP v1.5 — Structural Restructure
- **Three-axis recursive architecture** — sequential Pass 1/2/3 model replaced with three orthogonal evaluation axes: Factual (F), Signature (S), Architectural (A). Each axis recurses at depth 1, 2, or 3 for 3, 9, or 27 evaluation nodes respectively.
- **Autonomous depth classification** — Claude auto-classifies each piece based on stakes rubric, announces classification and reasoning, honors override keywords. Signal density and ambiguity trigger mid-execution escalation.
- **Recursive Audit Trace** — replaces v1.3 Pass Execution Audit. Fabrication resistance comes from structural consistency requirement across all nodes at target depth.
- **Termination rule** — convergence requires all leaf nodes at target depth to clear. Partial convergence is not convergence.
- **New named checks** — 25 (Rhetorical credibility flourishes), 26 (Press-release opening pattern), 27 (Unanchored numerical credibility), 28 (Terminology hygiene), 29 (Promotional density), 30 (Multi-surface consistency). Check 18 strengthened with self-referential variant.
- **Deprecations** — Tier 0/1/2 tier structure, Pass 1/2/3 iteration language, Pass Execution Audit format, Reader Fatigue Warning, standalone Rubber-Stamp Prohibition. Named checks 1-24 retained with same numbering, remapped to axes.
- **Trigger:** Barry observed that "check three times and commit once" must be architecturally honest about what Claude can actually execute in a single turn. Claude has one generative pass. The rigor must come from structural differentiation within that pass, not from pretending to run sequential independent passes. v1.5 is the first version where the enforcement architecture matches Claude's execution model.
- **Skipped:** v1.4 (planned additive revision with new checks 25-30) absorbed into v1.5 structural work.

## [Protocol Content] - 2026-04-16

### OCAP v1.3
- **Pass Execution Audit** — new structural requirement. Every outbound piece must ship with a forensic signal list per pass demonstrating that the three passes actually ran. Audit validity requires direct quotes from each pass (not the final output) and tapering signal counts. Missing audit fails the protocol regardless of content quality.
- **Presentation Rule revised** — self-reported pass execution is no longer acceptable. Presentation now requires (1) converged Pass 3 output AND (2) Pass Execution Audit. Integrity-based enforcement of pass execution has been converted to artifact-based enforcement.
- **Verification Principle** — new meta-section added before Version History. Generalizes the integrity-to-structure conversion pattern (v1.1→v1.2 for adversarial reading, v1.2→v1.3 for pass execution). Any OCAP check relying on self-reported execution without a visible artifact is flagged as a future failure point. Future candidates for structural conversion are named explicitly: Reader Fatigue Warning and Rubber-Stamp Prohibition.
- **Trigger:** Claude presented first-pass output labeled as third-pass converged output in a LinkedIn carousel caption draft. Barry caught the violation through direct question. The v1.2 Presentation Rule named the failure category but did not prevent the instance.

## [2.0.0-cloud] - 2026-04-15

### Added
- **Cloud deployment via Render** at `https://protocol-mcp.onrender.com/mcp/`
- `server.py` — Streamable HTTP version using standalone `fastmcp` package
- `Dockerfile` — Python 3.13-slim with uv package manager
- `render.yaml` — Render.com auto-deploy configuration (free tier)
- Auto-deploys from GitHub on push to main

### Architecture
- Cloud version uses standalone `fastmcp` package (import `from fastmcp import FastMCP`)
- Local version uses `mcp[cli]` SDK package (import `from mcp.server.fastmcp import FastMCP`)
- Both share the same `protocols/` directory and parsing logic
- Cloud serves 5 tools (Phase 1 retrieval). Local serves 9 tools (Phase 1 + Phase 2 sessions)
- Session persistence requires filesystem access, deferred to cloud v2.1 with database backend

## [1.1.0] - 2026-04-15

### Added
- **Phase 2: Cross-session state persistence**
  - `protocol_start_session` — begin tracked protocol execution with session_id
  - `protocol_save_state` — save phase, status, and working data (shallow merge)
  - `protocol_resume` — load full session state + auto-load current phase content
  - `protocol_list_sessions` — list sessions with status icons, filterable by protocol
- Session files stored as JSON in `sessions/` with automatic history tracking
- 4 new Pydantic input models for session tools

## [1.0.2] - 2026-04-15

### Fixed
- **Dual-pattern phase/check parser** — replaced single `_PHASE_RE` regex with two patterns:
  - `_HEADING_RE` matches both `### Phase N:` and `### Check N:` headings
  - `_BOLD_CHECK_RE` matches `**Check N:**` bold inline format
  - Results merged by number (heading wins on conflict), sorted numerically
  - OCAP now correctly parses all 18 checks (Tier 1 bold + Tier 2 headings)
- **Improved error message** when protocol has no parsed phases — now suggests using `protocol_load`

## [1.0.1] - 2026-04-15

### Fixed
- Added `_CHECK_RE` fallback regex for `**Check N:**` bold format
- OCAP Tier 1 checks (1-15) now parse correctly
- Tier 2 checks (16-18) still missing (fixed in 1.0.2)

## [1.0.0] - 2026-04-14

### Added
- **Phase 1: Protocol retrieval + structured phase access**
  - `protocol_list` — enumerate all protocols with metadata
  - `protocol_load` — load full protocol document into context
  - `protocol_describe` — summary + phase list without full content
  - `protocol_get_phase` — load single phase for step-by-step execution
  - `protocol_search` — weighted keyword search across all protocols
- YAML frontmatter parser for protocol metadata
- Dual response format support (markdown and JSON)
- Pydantic input validation for all tools
- 8 shipped protocols: LBP, ORA, PI, OCAP (18 checks), DAP, Sidebar, Commit, Strength
- Drop-in protocol architecture — add .md files to `protocols/`, no restart needed
- MIT license

### Design
- Architecture determined by ORA — original plan scored 0/4 on MCP value criteria; reframed as protocol library server
- Two new protocols (ORA, PI) emerged from the architectural analysis process itself
- OCAP validated against real LinkedIn post output before shipping
