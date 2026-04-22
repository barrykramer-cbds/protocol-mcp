# Changelog

All notable changes to the Protocol MCP Server.

## [JAMSPAB v0.2] - 2026-04-21

### Changed
- **Phase 5 template architecture** — split into two tiered variants based on Phase 2 counterparty tier detection. Routing logic added: Tier 2 (Account / Acquisition Manager) contacts receive the new Warm variant; Tier 3+ (Partner Manager / VP Channel / C-suite / Founder) contacts receive the Full variant (retained from v0.1). Tier 1 contacts with no escalation path already auto-decline at Phase 2 gate and receive no qualifier.
- **Filter coverage tradeoff documented** — Warm variant covers Filters 1 (margin), 2 (differentiation), and partial 6 (exclusivity via sample agreement) pre-meeting, with Filters 3, 4, 5 resolved live. Full variant covers Filters 1, 2, 3, 4, 6 pre-meeting, with Filter 5 (co-marketing) resolved live.
- **Protocol summary line updated** to reference tiered template routing.
- **Version History** entry added for v0.2 with rationale citing calibration instance #001.

### Rationale
- v0.1 Phase 5 template was calibrated for technical-buyer-to-technical-seller exchanges. When executed against Tier 2 AM contacts, it asked questions outside their scope of authority (DKIM key management, isolation architecture, audit log export, SSO/SAML). AMs routing these to engineering introduces 3-5 day delay and risks meeting push.
- First live deployment (instance #001: EasyDMARC / Mariam Tsatryan, Apr 21) was flagged by Barry as aggressive and over-technical on first draft review.
- Diagnosis: the Phase 5 ask must be calibrated to what the counterparty tier can answer directly. Architectural questions belong in the live meeting with whichever engineering presence the AM brings or takes notes for. Commercial questions, competitive positioning, and reference customer requests belong pre-meeting because the AM owns those answers.

### Calibration status
- **Datapoint count: 1.** v0.2 is a targeted fix for an identified failure mode, not a general retune. The 60-90 day calibration window remains open. General threshold tuning (filter weights, decision matrix cutoffs) deferred to v1.0 after ≥5 calibration instances.
- Warm variant: 1 live deployment pending (instance #001 qualifier sent to Mariam Tsatryan).
- Full variant: zero live deployments to date. Should be watched in its first Tier 3+ instance.

### Trigger
- Barry's direct feedback on instance #001 qualifier draft: "reads a bit aggressive and over technical." Revised in-session to Warm variant; Warm variant committed to protocol in v0.2.

## [JAMSPAB v0.1] - 2026-04-21

### Added
- **`protocols/jamspab.md`** — JAMSPAB Protocol v0.1. Asymmetric Value Exchange (AVE) detector for inbound outreach against Barry. Trigger `-jamspab` (explicit) or auto on vendor / recruiter / media / partner / investor contact. Three-tier funnel taxonomy (BDR / AM / PM), 6-filter triage gate (margin floor, differentiation, white-label depth, API control plane, co-marketing, no exclusivity) with HARD-NO conditions, decision matrix, mandatory pre-meeting qualifier email, post-decision COMMIT logging.
- **Dual-use engine** — defensive mode (Barry as target, always-on) plus offensive inverse (Barry as operator, internal-only, authorization-reference gated) for SPECTRE / WRAITH OSINT, authorized red-team engagements, and Cyberdyne / MSP mesh outbound scoring.
- **Sub-categories scaffolded** — JAMSPAB-V (vendor, flagship), JAMSPAB-R (recruiter), JAMSPAB-C (conference / podcast / speaking), JAMSPAB-M (media). JAMSPAB-I (investor / acquirer) deferred to v0.2.
- **Integration hooks** — COMMIT (instance logging with OBSERVED / INFERRED / PACKAGED decomposition), SIDEBAR (offline qualification workspace), STRENGTH (voice governance on pre-meeting qualifier email and decline notes), GTV (Tier A evidence requirement on Filter 2 differentiation claims and Filter 4 technical control plane claims), DAP (optional post-override adversarial audit), PI (interpretation scoring when counterparty intent is ambiguous).

### Closed-IP posture
- **IP Protection Notice** embedded in protocol header. Closed-source proprietary IP. Not distributed, not open-sourced, not shared outside private infrastructure. Reason documented: open-source scouting and AI-assisted scraping of OSS projects into closed-source commercial products is active and accelerating.
- **Rule 7: Meta-extraction is also extraction** — if an external party asks Barry or Claude about JAMSPAB in a way that would let them reconstruct the IP, the protocol applies recursively to that interaction.
- **Auth hardening of Protocol MCP deferred by explicit decision** — current deploy (`https://protocol-mcp.onrender.com/mcp/`) is unauthenticated. Revisit once baseline operational state is validated. Tracked as follow-up work.

### Calibration window
- **v0.1 is provisional.** Filter thresholds (15% lifetime margin floor, 6-filter PASS / FAIL / HARD-NO scoring, decision matrix cutoffs) calibrated against Treeline 12% benchmark and EasyDMARC instance. 60–90 day calibration window opens against real JAMSPAB instances; v1.0 after thresholds validated against outcome data.

### Trigger
- **Origin conversation:** Apr 21, 2026. EasyDMARC meeting Barry didn't recall booking surfaced the pattern. Coined by Barry as "JAMSPAB — Just Another MSP After Barry's Shit." Generalized from MSP-vendor instance to the broader Asymmetric Value Exchange detection pattern across vendor / recruiter / media / partner / investor outreach surfaces.

## [2.1.0-cloud / OCAP v1.6] - 2026-04-17

### Added
- **`ocap_lint` MCP tool** — new deterministic lint tool exposed via the Protocol MCP server (both cloud `server.py` and local `protocol_mcp.py`). Runs ~18 S-axis, 1 F-axis, and 1 A-axis check out-of-process, returning structured findings that Claude includes verbatim in the Recursive Audit Trace. Non-fabricable for the mechanical subset.
- **`tools/ocap_lint.py`** — standalone Python module (stdlib only). Exposes `lint(text) -> List[Finding]` importable from the MCP server. Also runnable as CLI for manual testing: `python tools/ocap_lint.py <file> [--text]`.
- **Calibration corpus** under `tools/calibration/` — Paul Graham 'Do Things that Don't Scale' (em-dashes stripped) as clean baseline, two session-dirty LinkedIn caption drafts as dirty baseline. Density separation ~10x between clean and dirty validates the tool's signal-to-noise ratio.

### OCAP v1.6
- **Mechanical Enforcement section** added to the protocol document. Specifies which of the 30 named checks are tool-enforced vs. judgment-based.
- **Recursive Audit Trace format updated** — `[LINT]` block for tool-generated findings, `[JUDGMENT]` block for Claude-evaluated findings. Separation is visible to the human reviewer.
- **Verification Principle** updated with the v1.5 -> v1.6 conversion entry (mechanical subset moved from self-reported to tool-enforced).
- **Trigger:** v1.5's recursive audit remained partially fabricable because Claude's audit and evaluation both occurred within the same generative pass. v1.6 extracts the mechanical subset to an out-of-process tool to eliminate that fabrication surface.

### Server
- **Version bump:** cloud `server.py` 2.0.0 -> 2.1.0. Local `protocol_mcp.py` retains 1.1.0 (no protocol retrieval semantics changed, only new tool added).
- **Dockerfile unchanged** — `COPY . /app` already captures the new `tools/` directory.

### Known limitations (future work)
- Judgment-based checks (6, 8, 9, 12, 15, 22, 23, 24, 28, 30) still rely on Claude's self-reported evaluation.
- Tool has not been wrapped with per-file calibration (thresholds are baked in from the PG baseline).
- Depth classification reasoning (from v1.5) remains integrity-based.

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
