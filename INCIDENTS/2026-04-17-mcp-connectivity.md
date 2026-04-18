# Incident: MCP Cloud Connectivity Failure

**Date:** 2026-04-17
**Duration:** ~4 hours from first symptom to resolution
**Severity:** Blocking. Outbound content production halted because OCAP v1.6 enforcement via `ocap_lint` required cloud namespace access.
**Status:** Resolved and verified end-to-end.

## Summary

Cloud MCP server at `https://protocol-mcp.onrender.com/mcp` failed to respond to tool calls after any Render free-tier container sleep/wake cycle. First boot after each deploy worked for ~15 minutes. Every subsequent boot returned HTTP 404 on POST `/mcp` until the server was forcibly redeployed, which reset the cycle.

Root cause was a configuration default, not a code regression. Today's `4467dc1` commit (OCAP v1.6 + ocap_lint) looked like the regression because it coincided with the first sustained usage of the cloud namespace that exercised multiple sleep cycles. Earlier deploys (`c7b6d7e`, `b901493`, `11aa820`) had the same latent defect but were never exercised across enough sleep cycles to expose it.

## Root Cause

`server.py` initialized FastMCP with the stateful default:

```python
mcp = FastMCP(SERVER_NAME)
```

FastMCP's streamable-http transport defaults to session-stateful mode. MCP session state lives in process memory. The session table was erased every time Render's free-tier infrastructure spun the container down after 15 minutes of inactivity. On wake, `mcp-remote` (the Node.js bridge Claude Desktop launches for HTTP MCP servers) continued sending the session ID it had cached from before the sleep. The new server process had no record of that session, returned 404, and the bridge surfaced the error as a 4-minute timeout.

Three layers made this hard to diagnose quickly:

1. The error text referenced "Claude Desktop app" even when calls were routed from the web interface, making the failure domain appear broader than it was.
2. The local stdio `protocol_mcp` namespace continued working throughout because it was a different server with different transport and no session state caching, which masked the cloud failure during early testing.
3. The first-boot-after-deploy always worked because `mcp-remote` had no cached session yet. This created the false signal "the deploy broke it" because the failure only appeared after the first sleep cycle, which happened to correlate with the ocap_lint deploy.

## Timeline

| Time (PDT) | Event |
|---|---|
| 11:27 AM | Deploy `4467dc1` (OCAP v1.6 + ocap_lint). First boot serves POST /mcp successfully. |
| 11:44 AM | Render spins container down after inactivity. Session state lost. |
| 11:45 AM onward | All subsequent boots return 404 on POST /mcp. User experiences 4-minute timeouts from Claude Desktop. |
| ~12:00 PM | Parent conversation hands off diagnostic via `protocol-mcp-diagnostic-handoff.md`. |
| ~1:08 PM | curl probe from user PowerShell confirms server alive at HTTP layer (307 redirect chain works). |
| ~1:45 PM | Rollback to `c7b6d7e` via Render dashboard. Auto-deploy disabled to prevent re-regression. |
| ~2:00 PM | First-boot of `c7b6d7e` verified healthy (HTTP 406 with session ID, correct stateful behavior). |
| ~2:30 PM | Code review of `c7b6d7e` vs `4467dc1` diff confirms additive-only changes that cannot cause transport-level regression. Hypothesis revised: failure is FastMCP stateful mode + ephemeral containers + `mcp-remote` session caching. |
| ~3:30 PM | Attempted fix via constructor arg `FastMCP(SERVER_NAME, stateless_http=True, json_response=True)` in commit `582d6b9`. Deploy failed with TypeError: FastMCP no longer accepts those kwargs on constructor in current version. |
| ~3:55 PM | Revert to plain constructor in commit `9727fb8`. Set `FASTMCP_STATELESS_HTTP=true` as Render environment variable. Deploy succeeds. |
| ~4:00 PM | Verified stateless mode active: GET /mcp now returns 405 with `allow: POST, DELETE` (was 406 in stateful mode). Response no longer includes `mcp-session-id` header. End-to-end `protocol_mcp_cloud:protocol_list` call succeeded through Desktop bridge. |
| ~4:30 PM | Post-sleep cycle verification. Container spun down for 20 minutes, then `protocol_mcp_cloud:protocol_describe` on `ocap` succeeded in under 3 seconds. Specific failure mode confirmed resolved. Incident closed. |

## Fix

Set Render environment variable `FASTMCP_STATELESS_HTTP=true`. No code change required in the final working configuration. The FastMCP constructor accepts the default `FastMCP(SERVER_NAME)` call and reads stateless-mode configuration from the environment at runtime.

In stateless mode, every request creates a fresh session that is discarded after the response. There is nothing for container sleep to destroy. `mcp-remote` sending a cached session ID is harmless because the server no longer checks session IDs against a session table.

All six cloud tools (`protocol_list`, `protocol_load`, `protocol_describe`, `protocol_get_phase`, `protocol_search`, `ocap_lint`) are pure request/response with no need for session state. Stateless mode loses no functionality for this server.

## Verification

- HTTP-layer: GET /mcp returns 405 with `allow: POST, DELETE`, confirming stateless mode is active per FastMCP's documented behavior.
- Session header absence: No `mcp-session-id` header issued in responses.
- First-boot end-to-end: `protocol_mcp_cloud:protocol_list` via Claude Desktop returned full protocol catalog in under 3 seconds from cold start.
- **Post-sleep cycle end-to-end:** Container allowed to spin down through 20 minutes of inactivity. `protocol_mcp_cloud:protocol_describe` called on `ocap` cold. Full v1.6 phase list returned in under 3 seconds. This is the specific failure mode that motivated the entire diagnostic and is now confirmed resolved.

## Lessons and Hardening Actions

1. **FastMCP defaults to stateful mode.** For any deployment on ephemeral-container infrastructure (Render free, Cloud Run scale-to-zero, Lambda, Fly.io machines suspend, Kubernetes rolling restarts), stateless mode should be the default choice. Add `FASTMCP_STATELESS_HTTP=true` to `render.yaml` so it survives environment recreation.

2. **`mcp-remote` does not auto-reinitialize sessions on 404.** This is a client-side gap in session lifecycle handling. Worth filing an issue against `mcp-remote` upstream once the project is identified. Not our bug to fix but worth documenting as a known sharp edge for anyone deploying stateful FastMCP to ephemeral infra.

3. **CI smoke test.** A GitHub Actions workflow that builds the container, starts `server.py`, POSTs a `tools/list` MCP request, and verifies a 200 response would have caught the stateful-mode/ephemeral-container incompatibility before the first deploy. ~20 minutes of work to write, permanent safety net. Recommend pairing with Render's "After CI Passes" auto-deploy mode once the workflow is in place.

4. **Cloud-first architecture requires cloud-first testing.** Prior verification of cloud deploys only exercised first-boot behavior. Future changes to `server.py` should be tested against at least one forced-sleep-cycle before being declared working. Can be scripted: deploy, curl-until-healthy, sleep 16 minutes (or use Render's manual deploy to simulate), curl again, verify.

5. **Configuration defaults deserve scrutiny.** The failure was not in code we wrote. It was in a default that was silently incompatible with our hosting environment. Every framework has defaults tuned for the framework author's assumed use case. Our use case (free-tier ephemeral container hosting a persistent-session protocol) was atypical enough that the default worked against us.

## Cleanup Completed Same Day

1. **DONE.** Local stdio entry removed from `claude_desktop_config.json`. Cloud entry (`protocol_mcp_cloud`) renamed to `protocol_mcp`, then in a subsequent edit removed entirely once the custom connector path was proven working.
2. **DONE.** Cloud endpoint registered as a native claude.ai web connector in Settings -> Connectors. Protocol MCP now reachable from Desktop, web, and mobile via Anthropic's connector broker path, bypassing local `mcp-remote` entirely.
3. **DONE (implicit).** `mpc_cloud` (MPC v1.0 at `https://mpc-v1.onrender.com/mcp/`) registered as a second custom connector. If MPC runs on the same FastMCP scaffolding it will need the same `FASTMCP_STATELESS_HTTP=true` environment variable on its Render service to survive sleep cycles. Pending verification.

## Still Open

1. Commit `FASTMCP_STATELESS_HTTP=true` to `render.yaml` for infrastructure-as-code parity (currently the env var lives only in Render's dashboard state).
2. Verify `mpc-v1.onrender.com` does not have the same latent bug. If it does, apply the same env var fix.
3. Open issue against `mcp-remote` for stale-session 404 handling.
4. Add CI smoke test per hardening action 3 below (see Lessons section).
5. Rotate the three secrets that were rendered into the diagnostic chat: GitHub PAT and two Google OAuth client secrets.

## Artifacts

- Commit `582d6b9` (reverted): attempted constructor kwarg fix
- Commit `9727fb8`: clean revert, env-var-based fix in force
- Render environment variable: `FASTMCP_STATELESS_HTTP=true`
- Relevant FastMCP documentation: https://gofastmcp.com/deployment/http

---

*Incident log written 2026-04-17 by Barry Kramer + Claude, based on Render service logs, Desktop MCP logs, and live diagnostic session. File at `C:\Dev\workspaces\protocol-mcp-deploy\INCIDENTS\2026-04-17-mcp-connectivity.md`.*
