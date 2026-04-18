# Protocol MCP Server

A FastMCP server that makes cognitive protocols persistently available across all Claude conversation spaces. Available as both a local server (stdio) and a cloud-hosted service (streamable HTTP).

## What It Does

Protocols are cognitive frameworks (LBP, DAP, OCAP, ORA, PI, GTV, PAP, Sidebar, Commit, Strength) that dramatically alter Claude's reasoning quality when loaded into context. Without this server, every new conversation starts from zero.

This MCP server makes all protocols **always available, everywhere**. Claude can discover, describe, load, and execute any protocol on demand. Protocol execution persists across sessions. New protocols are added by dropping a `.md` file in the `protocols/` directory.

## Two Deployment Modes

| Mode | File | Transport | Tools | Use Case |
|------|------|-----------|-------|----------|
| **Local** | `protocol_mcp.py` | stdio | 9 (retrieval + sessions) | Claude Desktop, full features |
| **Cloud** | `server.py` | streamable HTTP | 5 (retrieval) | Any device, any Claude conversation |

The cloud server is live at **`https://protocol-mcp.onrender.com/mcp/`** (Render free tier, auto-deploys from this repo).

## Prerequisites

- **Python 3.10+** (tested on 3.14, should work on 3.10+)
- **Claude Desktop** (any platform: Windows, macOS, Linux)
- **pip** for dependency installation

The local server uses stdio transport and runs as a subprocess of Claude Desktop. The cloud server uses streamable HTTP via the standalone `fastmcp` package. Both are platform-independent.

## Tools

### Protocol Retrieval (Phase 1) — both local and cloud

| Tool | Purpose |
|------|---------|
| `protocol_list` | Enumerate all available protocols with summaries |
| `protocol_load` | Load a full protocol into conversation context |
| `protocol_describe` | Get summary + phase list without full content load |
| `protocol_get_phase` | Load a single phase for focused execution |
| `protocol_search` | Search across all protocols by keyword |

### Session Persistence (Phase 2) — local only

| Tool | Purpose |
|------|---------|
| `protocol_start_session` | Begin tracked protocol execution, returns session_id |
| `protocol_save_state` | Save current phase + working data to session file |
| `protocol_resume` | Load prior session state into new conversation |
| `protocol_list_sessions` | Find previous sessions, filterable by protocol |

## Installation (Local)

```bash
git clone https://github.com/barrykramer-cbds/protocol-mcp.git
cd protocol-mcp
pip install -r requirements.txt
```

## Claude Desktop Configuration

### Local Server (stdio)

**Windows:**
```json
{
  "mcpServers": {
    "protocol_mcp": {
      "command": "python",
      "args": ["C:\\path\\to\\protocol-mcp\\protocol_mcp.py"],
      "env": {}
    }
  }
}
```

**macOS / Linux:**
```json
{
  "mcpServers": {
    "protocol_mcp": {
      "command": "python3",
      "args": ["/path/to/protocol-mcp/protocol_mcp.py"],
      "env": {}
    }
  }
}
```

### Cloud Server (remote via mcp-remote)

```json
{
  "mcpServers": {
    "protocol_mcp_cloud": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://protocol-mcp.onrender.com/mcp/"],
      "env": {}
    }
  }
}
```

Requires Node.js installed. The `mcp-remote` package bridges Claude Desktop's stdio transport to the remote streamable HTTP server.

Both entries can coexist in the same config. Local for zero-latency access at your desk, cloud for access from any device.

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

The local server discovers new protocols automatically (no restart needed). The cloud server picks up changes on the next deploy from GitHub.

Both `### Phase N:` headings and `**Check N:**` bold formats are supported by the parser.

## Shipped Protocols

| ID | Name | Trigger | Items | Description |
|----|------|---------|-------|-------------|
| `lbp` | Lateral Bore Protocol | `-lbp` | 7 phases | Systematic lateral thinking. Trace causal chains backward, repurpose tools cross-domain, stack signals for conviction, generate zero-competition channels. |
| `ora` | Objective Recursive Analysis | `-ora` | 9 phases | Recursive depth-drilling. Each level examines previous level's assumptions. Terminates at decision fork or foundational truth. |
| `pi` | Probability Index | `-pi` | 4 phases | Rapid Bayesian scoring for competing interpretations. Score against evidence fit, prior frequency, structural plausibility. |
| `gtv` | Ground Truth Validation | `-gtv` | 7 phases | Evidence-tiered validation gate for behavioral claims about external systems. Tier A (live probes, <90d practitioner data) through Tier D (vendor marketing, rejected). GREEN/AMBER/RED commit gate. Catches confident assertion from stale premises. |
| `ocap` | Outbound Content Alignment Protocol | implicit | 30 checks | Three-axis recursive content evaluation for anything seen by third parties. Factual (F), Signature (S), Architectural (A) axes at recursive depth 1/2/3. Auto-classified by stakes. Recursive Audit Trace output. `ocap_lint` provides mechanical enforcement for ~60% of checks. |
| `pap` | Prompt Algorithm Protocol | `-pap` | 8 phases | Formal algorithm for prompt construction. Engineers structured input for maximum output fidelity. Upstream complement to OCAP. Integrates with SIP for multi-window context, MPC for routing, invokes LBP as subroutine when conventional framing collapses. |
| `dap` | Devil's Advocate Protocol | `-dap` | 6 phases | Adversarial audit. Score factors +5 to -5, produce scorecard, deliver honest interpretation with no motivational close. |
| `sidebar` | Sidebar Protocol | `-sidebar` | 4 phases | Context-isolated tangent. Multi-turn supported. Clean exit back to main thread. |
| `commit` | Commit Protocol | implicit | 4 phases | Storage write guard. Decomposes into OBSERVED/INFERRED/PACKAGED layers. Commits only after human confirms. |
| `strength` | Strength Protocol | global | 3 phases | Output filter. No age math, no weakness projection, CISO+AI+research intersection positioning. |

## Architecture

```
protocol_mcp.py        # Local server v1.1.0 (stdio, mcp[cli] SDK, ~580 lines)
server.py              # Cloud server v2.0.0 (streamable HTTP, standalone fastmcp)
Dockerfile             # Container image for cloud deployment
render.yaml            # Render.com auto-deploy configuration
protocols/             # Drop-in protocol library (10 protocols, shared by both servers)
sessions/              # Cross-session state persistence (local server only)
```

### How It Works

Both servers scan `protocols/` for `.md` files with YAML frontmatter. The parser uses a dual-pattern regex that handles both `### Phase N:` headings and `**Check N:**` bold inline formats, merging and deduplicating by number. The local server stores session state as JSON files in `sessions/` with automatic history tracking and shallow data merge on save.

### Design Decisions

This server was built after an Objective Recursive Analysis (ORA) determined that the original plan (wrapping reasoning frameworks as MCP tools) scored 0/4 on the MCP value criteria (external data, computation, persistence, action). The architecture was reframed: protocols belong in context (the document IS the tool), but making them *persistently available across all conversation spaces* requires MCP infrastructure. The server provides persistence and universal access. The protocols provide the reasoning frameworks. They compose naturally.

## Author

Barry Kramer + Claude | April 14-17, 2026

License: MIT
