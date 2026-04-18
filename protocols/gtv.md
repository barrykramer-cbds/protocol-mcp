---
name: Ground Truth Validation
id: gtv
version: 1.0
trigger: -gtv
summary: Evidence-tiered validation gate for behavioral claims about external systems. When a plan depends on how a detection system, rate limiter, API, platform, or anti-automation layer will respond, validate load-bearing assumptions against Tier A field evidence before committing analytical or operational cycles. Prevents confident assertion from training data, vendor marketing, or prior-behavior inference without fresh evidence.
---

# GROUND TRUTH VALIDATION (GTV)
## Evidence-Tiered Claim Gate for External System Behavior
### Origin: Barry Kramer + Claude | April 17, 2026

---

## THE CORE INSIGHT

Vendor documentation, target-system published policies, and training-data confidence diverge frequently from field reality for fast-moving external systems. Anti-bot detection, rate limit enforcement, platform fraud heuristics, API compatibility, and TOS enforcement change faster than their documentation. Most analytical failures in this class do not come from bad reasoning. They come from reasoning correctly on stale or aspirational premises.

GTV forces a tier classification and commit gate on evidence before behavioral claims about external systems are allowed to carry weight. Tier A is recent field data. Tier D is vendor marketing and target-system self-claims, rejected. No amount of Tier D makes up for zero Tier A.

This is not formal evidence-based reasoning. It is a fast heuristic: classify each source, score evidence density, apply a commit gate, proceed or stop.

---

## THE PROTOCOL

### Phase 1: CLAIM EXTRACTION

List every load-bearing falsifiable assumption the plan depends on. One claim per line. Phrase each claim as a concrete, testable statement.

**Discipline:** A claim that cannot be phrased as something that could be shown true or false does not belong in this phase. Reframe or drop it.

**Example claims from a LinkedIn scraping decision:**
- "LinkedIn will not flag Playwright MCP Bridge extension usage at low volume."
- "Reading own inbound messages is not the detection target."
- "Barry has successfully scraped LinkedIn in the past."
- "Browser-extension automation category has lower restriction rate than cloud-automation category."

### Phase 2: SOURCE TIER CLASSIFICATION

For each claim, gather available sources and classify into one of four tiers.

**Tier A (load-bearing):**
- Live probes or canaries run by the user or Claude in-session
- Active practitioner reports within the last 90 days
- Account-level incident reports with dates and target-system identifiers
- Relevant GitHub issues or commits within the last 90 days
- Production postmortems from teams operating at scale

**Tier B (supporting):**
- Community forums (Reddit, HN, Discord, GitHub discussions) within the last 12 months with corroborating reports from multiple independent sources
- Red team or penetration test writeups
- Bug bounty disclosures that touched the relevant system
- Published studies with methodology disclosed

**Tier C (context-only):**
- Tool vendor documentation (knows the tool, does not know target system's current response)
- Target system policy documents or TOS (states rules, not enforcement state)
- Third-party blogs older than 12 months

**Tier D (rejected):**
- Vendor marketing content
- Target system's own claims about their detection capability
- Training-data-derived confidence with no fresh citation
- Asserted "I have done this before" without evidence that the target system is still behaving the same way

### Phase 3: EVIDENCE DENSITY SCORING

Per claim, count Tier A and Tier B sources.

**Minimum viable evidence:** 1 Tier A source OR 3 Tier B sources, all within the recency window.

Below minimum = insufficient. Mark the claim UNVERIFIED.

If only Tier C/D evidence exists for a load-bearing claim, the plan is operating on documentation or marketing, not reality.

### Phase 4: DELTA CHECK

For every Tier C or Tier D claim, check for contradicting Tier A or Tier B evidence.

- Large delta between vendor claim and field reality → vendor claim is marketing or aspirational. Reject.
- Small delta → vendor claim is approximately reliable. Can support Tier B evidence.
- No Tier A/B to check against → vendor claim remains unverified. Do not upgrade.

### Phase 5: COMMIT GATE

Apply the gate per claim, then aggregate for the plan.

**GREEN:** Every load-bearing claim has minimum viable evidence. No contradicting Tier A evidence. Proceed.

**AMBER:** Partial evidence. One or more claims at minimum threshold but fragile. Proceed only with a live probe designed to confirm the fragile claim before committing full operational weight.

**RED:** At least one load-bearing claim has contradicting Tier A evidence, OR has zero Tier A/B evidence. Stop. Reassess or gather more evidence before proceeding.

Aggregate plan-level status is the worst claim-level status.

### Phase 6: OUTPUT FORMAT

Present the validation as a structured table, one row per claim.

| Claim | Tier A Count | Tier B Count | Contradicting | Status |
|-------|:------------:|:------------:|:-------------:|:------:|
| <statement> | N (cites) | N (cites) | any A/B against | GREEN / AMBER / RED |

Below the table, state the aggregate plan-level status and the reasoning trail for any RED or AMBER claim.

### Phase 7: POST-COMMIT MONITORING

AMBER commits require follow-up: the live probe result must be recorded and fed back into the evidence cache. Without this, the system learns nothing from its own operation.

GREEN commits require no follow-up but should be re-validated if the target system's public behavior appears to change.

RED outcomes require a reassessment loop: revise the plan to depend on different assumptions, or gather the missing Tier A/B evidence through targeted research or live probes, then re-run GTV.

---

## WHEN TO USE GTV

- Before committing analytical or operational cycles to a plan that depends on an external system's behavior
- When producing a playbook describing how a target system will respond to specific actions
- When making confident assertions about fast-moving systems (anti-bot, rate limits, TOS enforcement, detection, fingerprinting, API quotas)
- When vendor documentation and field reports historically diverge for this class of system
- When Claude or the user is about to fill in a narrative from thin evidence

## WHEN NOT TO USE GTV

- Trivial behavioral claims ("HTTP GET returns a response body")
- Claims fully verifiable from first principles ("sorting N items is O(N log N)")
- Internal reasoning that does not depend on external system behavior
- Execution tasks where the decision has already been validated

---

## KNOWN LIMITATIONS (v1.0)

Identified during ORA review before shipping. Real use will show which to prioritize for v1.1.

1. **No user-consultation step.** Some load-bearing claims are about the user specifically (what they have done, what tooling they have, what their account state is). Web search cannot validate these. v1.0 relies on the caller recognizing user-specific claims and asking the user directly. v1.1 target: explicit phase for user-specific claims before or alongside external source gathering.

2. **No source-quality check beyond tier classification.** Tier B requires "corroborating reports" but does not distinguish genuine practitioner signal from astroturf or paid placement wearing practitioner clothes. v1.0 relies on judgment to sniff this out. v1.1 target: explicit quality heuristics (author history, account age, site reputation, incentive check, affiliation disclosure).

3. **No temporal scope handling.** Future-behavior claims ("how will the detection algorithm respond to pattern X next week") cannot be wild-validated because no Tier A can exist for unrealized events. v1.0 would flag these RED. v1.1 target: a separate track for future-behavior claims requiring live canary design instead of historical evidence scoring.

---

## GTV vs PI vs DAP vs ORA

| Dimension | GTV | PI | DAP | ORA |
|-----------|-----|-----|-----|-----|
| Purpose | Validate evidence for external-system claims | Choose between competing interpretations of existing evidence | Stress-test a specific plan | Decompose a proposition recursively |
| Scope | External world, fast-moving | Evidence already in hand | Plan or strategy | Single proposition |
| Output | Tier-scored claim table + gate | Probability ranking + action implication | Scorecard + honest assessment | Layered insight + decision fork |
| When | Before committing cycles to external-system assumptions | Before committing to one interpretation | After drafting an approach | Before committing to an approach |

They compose: GTV validates the evidence, ORA decomposes the proposition built on it, PI picks between interpretations of the validated evidence, DAP stress-tests the chosen path.

---

## THE META-PRINCIPLE

**"Confident reasoning on stale premises fails more quietly than bad reasoning on fresh premises. The premises are the product."**
