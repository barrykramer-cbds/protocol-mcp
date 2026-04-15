# Protocol MCP Server

A FastMCP server that makes cognitive protocols persistently available across all Claude conversation spaces.

## What It Does

Protocols are cognitive frameworks (LBP, DAP, OCAP, ORA, PI, Sidebar, Commit, Strength) that dramatically alter Claude's reasoning quality when loaded into context. Without this server, every new conversation starts from zero.

This MCP server makes all protocols **always available, everywhere**. Claude can discover, describe, load, and execute any protocol on demand. Protocol execution persists across sessions. New protocols are added by dropping a `.md` file in the `protocols/` directory.

## Tools

### Protocol Retrieval (Phase 1)

| Tool | Purpose |
|------|---------|
| `protocol_list` | Enumerate all available protocols with summaries |
| `protocol_load` | Load a full protocol into conversation context |
| `protocol_describe` | Get summary + phase list without full content load |
| `protocol_get_phase` | Load a single phase for focused execution |
| `protocol_search` | Search across all protocols by keyword |

### Session Persistence (Phase 2)

| Tool | Purpose |
|------|---------|
| `protocol_start_session` | Begin tracked protocol execution, returns session_id |
| `protocol_save_state` | Save current phase + working data to session file |
| `protocol_resume` | Load prior session state into new conversation |
| `protocol_list_sessions` | Find previous sessions, filterable by protocol |

## Installation

```bash
git clone https://github.com/barrykramer-cbds/protocol-mcp.git
cd protocol-mcp
pip install -r requirements.txt
```

## Claude Desktop Configuration

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "protocol_mcp": {
      "command": "python",
      "args": ["path/to/protocol-mcp/protocol_mcp.py"],
      "env": {}
    }
  }
}
```

Fully quit Claude Desktop before editing the config, then restart.

## Adding Protocols

Drop a `.md` file in `protocols/` with YAML frontmatter:

```markdown
---
name: My Protocol Name
id: my_protocol
version: 1.0
trigger: -myprotocol
summary: One-line description.
---

# Protocol content

### Phase 1: FIRST PHASE TITLE

Phase content...
```

The server discovers new protocols automatically. No restart needed. Both `### Phase N:` headings and `**Check N:**` bold formats are supported by the parser.

## Shipped Protocols

| ID | Name | Trigger | Items | Description |
|----|------|---------|-------|-------------|
| `lbp` | Lateral Bore Protocol | `-lbp` | 7 phases | Systematic lateral thinking. Trace causal chains backward, repurpose tools cross-domain, stack signals for conviction, generate zero-competition channels. |
| `ora` | Objective Recursive Analysis | `-ora` | 9 phases | Recursive depth-drilling. Each level examines previous level's assumptions. Terminates at decision fork or foundational truth. |
| `pi` | Probability Index | `-pi` | 4 phases | Rapid Bayesian scoring for competing interpretations. Score against evidence fit, prior frequency, structural plausibility. |
| `ocap` | Outbound Content Alignment Protocol | implicit | 18 checks | Two-tier: Tier 1 removes AI authorship signatures (vocabulary, structure, composition). Tier 2 evaluates content quality (anti-reductive capacitance, glaze test, escape route audit). |
| `dap` | Devil's Advocate Protocol | `-dap` | 6 phases | Adversarial audit. Score factors +5 to -5, produce scorecard, deliver honest interpretation with no motivational close. |
| `sidebar` | Sidebar Protocol | `-sidebar` | 4 phases | Context-isolated tangent. Multi-turn supported. Clean exit back to main thread. |
| `commit` | Commit Protocol | implicit | 4 phases | Storage write guard. Decomposes into OBSERVED/INFERRED/PACKAGED layers. Commits only after human confirms. |
| `strength` | Strength Protocol | global | 3 phases | Output filter. No age math, no weakness projection, CISO+AI+research intersection positioning. |

## Architecture

```
protocol_mcp.py        # FastMCP server v1.1.0 (stdio transport, ~580 lines)
protocols/             # Drop-in protocol library (8 protocols)
sessions/              # Cross-session state persistence (JSON files)
```

### How It Works

The server scans `protocols/` for `.md` files with YAML frontmatter on every tool call (no caching, so new protocols appear instantly). It parses phases/checks using a dual-pattern regex that handles both `### Phase N:` headings and `**Check N:**` bold inline formats, merging and deduplicating by number. Session state is stored as JSON files in `sessions/`, with automatic history tracking and shallow data merge on save.

### Design Decisions

This server was built after an Objective Recursive Analysis (ORA) determined that the original plan (wrapping reasoning frameworks as MCP tools) scored 0/4 on the MCP value criteria (external data, computation, persistence, action). The architecture was reframed: protocols belong in context (the document IS the tool), but making them *persistently available across all conversation spaces* requires MCP infrastructure. The server provides persistence and universal access. The protocols provide the reasoning frameworks. They compose naturally.

## Author

Barry Kramer + Claude | April 14-15, 2026

License: MIT
