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
      "args": ["C:\\Dev\\protocol-mcp\\protocol_mcp.py"],
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

The server discovers new protocols automatically. No restart needed. Both `### Phase N:` headings and `**Check N:**` bold formats are supported.

## Shipped Protocols

| ID | Name | Trigger | Items |
|----|------|---------|-------|
| `lbp` | Lateral Bore Protocol | `-lbp` | 7 phases |
| `ora` | Objective Recursive Analysis | `-ora` | 9 phases |
| `pi` | Probability Index | `-pi` | 4 phases |
| `ocap` | Outbound Content Alignment Protocol | implicit | 18 checks |
| `dap` | Devil's Advocate Protocol | `-dap` | 6 phases |
| `sidebar` | Sidebar Protocol | `-sidebar` | 4 phases |
| `commit` | Commit Protocol | implicit | 4 phases |
| `strength` | Strength Protocol | global | 3 phases |

## Author

Barry Kramer + Claude | April 14-15, 2026

License: MIT
