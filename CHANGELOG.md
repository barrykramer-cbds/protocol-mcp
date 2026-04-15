# Changelog

All notable changes to the Protocol MCP Server.

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
- **Improved error message** when protocol has no parsed phases — now suggests using `protocol_load` instead of showing empty phase list

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
- YAML frontmatter parser for protocol metadata (name, id, version, trigger, summary)
- `### Phase N:` heading parser for phase extraction
- Dual response format support (markdown and JSON)
- Pydantic input validation for all tools
- Tool annotations (readOnlyHint, destructiveHint, idempotentHint, openWorldHint)
- 8 shipped protocols: LBP, ORA, PI, OCAP (18 checks), DAP, Sidebar, Commit, Strength
- Drop-in protocol architecture — add .md files to `protocols/`, no restart needed
- MIT license

### Design
- Architecture determined by ORA (Objective Recursive Analysis) — original plan to wrap reasoning in MCP tools scored 0/4 on MCP value criteria; reframed as protocol library server providing persistence + universal access
- Two new protocols (ORA, PI) emerged from the architectural analysis process itself
- OCAP validated against real LinkedIn post output before shipping
