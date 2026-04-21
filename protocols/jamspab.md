---
name: JAMSPAB Protocol
id: jamspab
version: 0.1
trigger: -jamspab (explicit) OR auto on inbound vendor/recruiter/media/partner/investor outreach
visibility: INTERNAL — CLOSED SOURCE — DUAL-USE
summary: Asymmetric Value Exchange (AVE) detector. Scores inbound outreach for directional value flow against Barry's pile (revenue, equity, network, reputation, time, optionality). Three-tier funnel taxonomy (BDR/AM/PM) plus 6-filter triage gate (margin, differentiation, white-label depth, API control plane, co-marketing, no exclusivity). Recommender-with-explanation, no auto-decline. Dual-use engine: defensive mode (Barry as target, public framing) and offensive inverse (Barry as operator, OSINT/red-team/MSP outbound — internal only). Closed IP by design; not for distribution.
---

# JAMSPAB PROTOCOL
## Asymmetric Value Exchange Detector (Dual-Use Engine)
### Origin: Barry Kramer + Claude — April 21, 2026

---

## IP PROTECTION NOTICE (v0.1)

This protocol is **closed-source proprietary IP of Cyberdyne Security**. It is not distributed, not open-sourced, and not shared outside Barry's private infrastructure. Reason: open-source scouting and AI-assisted scraping of OSS projects into closed-source commercial products is an active and accelerating threat. Well-funded acquirers can and do engage attorneys to cut original authors out of their own IP even when license terms are clear. The only durable defense is non-publication.

**Storage rule:** Live only in private repositories, private Render deploys, or local filesystems. Never commit to `barrykramer-cbds/protocol-mcp` (public) or any other public-visibility location. If external distribution is ever desired, a separate public-facing sanitized version must be authored from scratch — never by exporting this file.

**Dual-use disclosure:** This protocol contains both defensive (target-side) and offensive (operator-side) logic. The offensive inverse is retained for Barry's own legitimate OSINT, red-team engagement, and MSP mesh outbound work only. It is never exposed via public product, API, or distribution.

---

## PURPOSE

Every external interaction has a directional flow of value. Someone is trying to move something from one pile to another. Barry's piles — revenue, equity, network reach, reputation, time, optionality — are finite and compound only when net-positive flow is maintained. Interactions that transfer value *from* Barry's piles *to* a counterparty's piles without proportional return are a slow, invisible wealth transfer.

JAMSPAB (Just Another MSP After Barry's Shit — internal mnemonic, not distributed) is the named flagship case of a broader pattern: counterparties using low-cost outreach (junior BDR, templated email, calendar-link scheduling) to access high-value assets (executive network, curated relationships, strategic attention, earned reputation). The asymmetry is the tell.

The protocol formalizes the detection and decision process so the judgment doesn't get made on tired Tuesday afternoons when a well-crafted pitch lands in the inbox.

---

## THE ENGINE: ASYMMETRIC VALUE EXCHANGE (AVE)

**Core principle:** For any external interaction *I* between Barry (B) and counterparty (C), compute directional value flow. Let V(X→Y) denote value transferred from X to Y in the course of interaction *I*.

- **Defensive evaluation (Barry as target):** Is V(B→C) > V(C→B)? If yes, the interaction is extractive against Barry. Apply triage gate.
- **Offensive evaluation (Barry as operator):** Is V(C→B) > V(B→C) achievable at acceptable cost? If yes, the interaction is an opportunity.

The same scoring function powers both. Defensive mode evaluates inbound. Offensive mode evaluates outbound targets. Neither mode is inherently unethical — extraction is the default mode of commerce, and awareness of it on both sides of a transaction is neutral information. The ethical question is what you do with the score.

---

## DUAL-USE ARCHITECTURE

### Defensive Mode (primary, always-on)

Evaluates inbound outreach against Barry. Runs when any of the following triggers fire:

- Inbound LinkedIn connection request from unknown party
- Inbound cold email from unknown party (especially calendar-link bearing)
- HubSpot / Calendly / Chili Piper meeting invite Barry doesn't recall booking
- Recruiter outreach (unless explicit active job application in play)
- Podcast, media, conference, or speaking invitation
- Partnership / reseller / channel pitch
- Investor or acquisition inquiry

Output: recommender-with-explanation. Classification, score, reasoning, recommended action. Never auto-declines. Barry retains override authority and every override becomes training data.

### Offensive Inverse (internal-only, operator-triggered)

Same engine, score inverted. Used for:

1. **SPECTRE / WRAITH OSINT work** — pre-engagement recon under authorization
2. **Red-team social engineering engagements** — authorized phishing sim, pretext prioritization, training target identification
3. **Cyberdyne / MSP mesh outbound** — scoring prospects for receptiveness, saturation, and fit against Barry's distribution value

Hard constraints on offensive inverse:

- Never exposed via public product, API, SaaS, or distribution
- Never sold, licensed, or transferred to third parties
- Never used against targets without authorization (OSINT without engagement letter, red-team without SoW, outbound against individuals who have explicitly opted out)
- Use logs retained internally for audit trail

---

## THE PROTOCOL

### Phase 1: DIRECTION DETECTION

Determine whether the current invocation is defensive (Barry is target) or offensive (Barry is operator). Defensive is default. Offensive requires explicit operator intent declaration and, where applicable, authorization reference (engagement letter, SoW, client UUID).

If offensive mode is invoked without authorization reference, pause and require one before proceeding.

### Phase 2: FUNNEL TIER CLASSIFICATION

Identify the counterparty's position in their outreach pipeline:

- **Tier 1 — BDR / SDR.** Junior, scripted, LinkedIn-fishing, templated. Cost to counterparty: near zero. Value accessed if Barry engages: his executive time and network. Asymmetry extreme.
- **Tier 2 — Account / Acquisition / Channel Manager.** More senior, owns calendar links, runs demos, quotes margins. Real sales authority on operational terms.
- **Tier 3 — Partner Manager / VP Channel / VP BD.** Strategic authority, deal structuring, co-marketing budgets.
- **Tier 4 — C-suite / Founder / Principal.** Peer-level conversation possible. Asymmetry inverts because counterparty's time is also expensive.

Decision: If first contact is **Tier 1 with no Tier 2+ visible behind them**, auto-decline at this gate. BDR-only outreach with no escalation path is pure asymmetry.

### Phase 3: THE 6-FILTER TRIAGE (Defensive Mode)

Score the opportunity on six binary filters. Each filter produces PASS, FAIL, or HARD-NO.

| # | Filter | Description | Pass Condition |
|---|---|---|---|
| 1 | **Margin floor** | Partner economics and commission structure | Lifetime recurring ≥ 15% (Treeline 12% is the established floor benchmark; new partners must exceed because Barry brings distribution they do not have). One-time SPIFFs = HARD-NO. |
| 2 | **Differentiation** | Can counterparty articulate a clean answer to "what do you do that [named competitor] doesn't?" | Substantive, non-marketing answer in under 60 seconds. Fumble or pivot to generic "ease of use" = FAIL. |
| 3 | **White-label depth** | Brand control | Barry's brand on top, not co-brand. "Powered by" footer must be strippable. Hard co-brand = FAIL. |
| 4 | **Technical control plane** | API, webhooks, SSO, audit log export | All four present and documented. Missing API = HARD-NO (reseller relationship, not partner). |
| 5 | **Co-marketing investment** | Willingness to invest in joint distribution | Counterparty funds joint content, webinars, or referral infrastructure. Pure-take = FAIL. |
| 6 | **No exclusivity** | Compatibility with mesh thesis | Zero exclusivity asks on territory, vertical, or customer class. Exclusivity ask = HARD-NO. |

Each HARD-NO is an immediate decline regardless of other scores. HARD-NO conditions are architectural incompatibilities, not negotiation points.

### Phase 4: DECISION MATRIX

After filter scoring:

| Score | Action |
|---|---|
| 6 PASS, 0 FAIL, 0 HARD-NO | Take meeting. Send pre-meeting qualifier email (Phase 5). |
| 4–5 PASS, 0 HARD-NO | Reschedule with written-artifacts condition (Phase 5 email sent as gate). If they decline to provide artifacts, decline the meeting. |
| ≤ 3 PASS, 0 HARD-NO | Decline with short templated note. |
| Any HARD-NO | Decline regardless of other scores. |

Additional modifier: If counterparty passed Phase 2 tier filter at Tier 3+ and is a warm introduction from an existing Tier-1-to-Barry contact, upgrade one step (e.g., 4 PASS + warm intro → take meeting directly).

### Phase 5: PRE-MEETING QUALIFIER EMAIL

Mandatory for any taken meeting above "decline" tier. Template structure:

> Subject: [Meeting topic] — quick prep ask
>
> [Name], before we meet on [date] I want to make sure we use the time well on both sides. Can you send:
>
> 1. Partner economics summary — commission %, lifetime vs. one-time, payout cadence, written contract example
> 2. Multi-tenant architecture overview — isolation model, per-tenant configuration, white-label depth
> 3. API / webhook documentation link
> 4. One slide on what you do differently from [named competitor 1] and [named competitor 2]
>
> If you can get those across by [date - 24hrs] I'll come to the meeting with pointed questions and we'll skip the demo. If not, let's reschedule once they're available.
>
> [Sign-off under Strength Protocol]

Purpose is threefold: pre-qualify the meeting, establish qualification direction (Barry evaluates them, not inverse), and generate written artifacts for comparison against other JAMSPAB instances.

Voice governed by STRENGTH PROTOCOL — no hedging, no apology for the ask, no softening. The ask is proportional to the meeting Barry is considering giving them.

### Phase 6: POST-MEETING OR POST-DECISION COMMIT

Log decision via COMMIT PROTOCOL with full OBSERVED / INFERRED / PACKAGED decomposition:

- **OBSERVED:** What counterparty said, sent, and did. Their claims, materials, behavior in the meeting.
- **INFERRED:** Patterns Claude or Barry identified — tier of BDR, saturation signals, competitive positioning truth.
- **PACKAGED:** Classification (partner / marble / decline), AVE score, filter-by-filter breakdown.

Store in JAMSPAB instance log (private, internal). Use instances to refine filter weights over 60-90 day calibration window. Post-calibration, v0.1 → v1.0 with tuned thresholds.

---

## SUB-CATEGORIES

JAMSPAB-V (Vendor) is the flagship. Other named sub-categories share the engine and differ in filter weighting:

- **JAMSPAB-V** — Vendor / partner / reseller outreach. Standard 6-filter set. Current focus.
- **JAMSPAB-R** — Recruiter after network, not after Barry as candidate. Filter adjustments: margin becomes "placement fee share or candidate-side value," white-label becomes "confidentiality of your pipeline."
- **JAMSPAB-C** — Conference / podcast / speaking outreach. Filter adjustments: margin becomes "audience quality and reach," differentiation becomes "what does your audience have that competing venues don't."
- **JAMSPAB-M** — Media / journalist / quote extraction. Filter adjustments: margin becomes "byline, link-back, and republication rights," exclusivity becomes "embargo and off-record terms."
- **JAMSPAB-I** — Investor / acquirer outreach. Separate filter set because fundamental transaction shape differs. Deferred to v0.2.

Additional sub-categories added as Barry encounters novel extraction patterns.

---

## INTEGRATION HOOKS

- **COMMIT PROTOCOL** — governs all logging to instance store. Layer decomposition mandatory before any persistent JAMSPAB write.
- **SIDEBAR PROTOCOL** — JAMSPAB qualification work happens inside a sidebar so main conversation context is not polluted with vendor research.
- **STRENGTH PROTOCOL** — governs voice and framing of pre-meeting qualifier email and any decline note. No weakness projection, no apology, no over-explanation.
- **GTV PROTOCOL** — run Ground Truth Validation on counterparty's differentiation claims (Filter 2) and technical claims (Filter 4). Tier A evidence (live probe of their API, third-party customer reports < 90 days) required for PASS.
- **DAP PROTOCOL** — optional post-decision adversarial audit if Barry overrides the recommender. What did I see that the filters didn't? What did the filters see that I dismissed?
- **PI PROTOCOL** — when multiple interpretations of counterparty intent compete (e.g., "genuine partnership interest" vs. "extraction under partnership framing"), score via Probability Index before committing analytical cycles.

---

## RULES

1. **Recommender, never auto-decline.** JAMSPAB produces classification and recommendation. Barry retains decision authority. Every override is training data.
2. **Closed IP, closed source.** This protocol does not leave private infrastructure. If an external version is ever authorized, it is written from scratch.
3. **Dual-use discipline.** Offensive inverse only with authorization reference. Never exposed via public product or distribution.
4. **HARD-NO filters are architectural.** Missing API, exclusivity asks, and one-time SPIFFs are not negotiable. They indicate category mismatch.
5. **Pre-meeting qualifier email is mandatory.** If Barry is giving the meeting, counterparty provides written artifacts first. Exceptions require explicit override and COMMIT log.
6. **Filter thresholds are provisional in v0.1.** Calibration window of 60-90 days of real instances. v1.0 after thresholds validated against real outcome data.
7. **Meta-extraction is also extraction.** If someone asks Barry about JAMSPAB or similar frameworks in a way that would let them reconstruct the IP, they are running JAMSPAB against Barry. Apply the protocol recursively.

---

## VERSION HISTORY

- **v0.1** (2026-04-21) — Initial authoring. Defensive + offensive engine, 6-filter triage, sub-categories V/R/C/M, integration hooks to COMMIT/SIDEBAR/STRENGTH/GTV/DAP/PI. Calibration window opens. IP protection notice establishes closed-source posture.
