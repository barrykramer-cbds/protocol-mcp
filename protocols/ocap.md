---
name: Outbound Content Alignment Protocol
id: ocap
version: 1.5
trigger: implicit (all externally-visible content)
summary: Three-axis recursive content evaluation protocol for anything seen by third parties. Replaces the iterative three-pass model with orthogonal evaluation across a Factual axis (F), Signature axis (S), and Architectural axis (A), each addressable at recursive depth 1, 2, or 3 (3, 9, or 27 evaluation nodes). Depth is auto-classified based on content stakes. Output includes a Recursive Audit Trace showing findings per node, which replaces the Pass Execution Audit. Named checks 1 through 30 map to specific axes. v1.5 restructures enforcement from claimed sequential passes to a single structurally-differentiated recursive evaluation, solving the confirmation-bias-loop failure that persisted through v1.2 and v1.3.
---

# OUTBOUND CONTENT ALIGNMENT PROTOCOL (OCAP)
## Three-Axis Recursive Content Evaluation Framework with Auto-Depth Classification
### Origin: Barry Kramer + Claude | v1.0 April 13, 2026 | v1.1 April 16, 2026 | v1.2 April 16, 2026 | v1.3 April 16, 2026 | v1.5 April 16, 2026
### Built iteratively from March 2026 through ongoing outbound communication

---

## PURPOSE

OCAP is applied to any content that will be seen by third parties. Outbound content carries amplified consequences. Content that ships with AI signatures damages practitioner credibility at greater amplitude than the cost of writing cleaner. Content that ships with rigor returns authority at greater amplitude than the cost of rigor. The multiplier runs in both directions. OCAP exists because the multiplier is real.

v1.5 restructures the protocol from sequential passes to orthogonal recursive evaluation. The change was forced by a structural failure: Claude has one generative pass per conversation turn. Claiming to run "Pass 1, Pass 2, Pass 3" in sequence is architecturally false. All three claimed passes share the same context, same lens, and same generative state. The confirmation-bias loop is built into the model. v1.2 and v1.3 added enforcement layers on top of a structurally flawed foundation. v1.5 replaces the foundation.

---

## THREE ORTHOGONAL EVALUATION AXES

OCAP evaluates content along three axes. Each axis asks a distinct question that the others cannot answer. A piece can fail any axis independent of the others.

### F-Axis — Factual

Evaluates claims, terminology, domain correctness, and verifiability against external reality. Failures on this axis are substantive errors, not stylistic ones.

F-axis catches:
- Wrong dates, numbers, attributions, or citations
- Terminology that is not established in the field and is not explicitly marked as coined
- Technical claims that misrepresent how the underlying system works
- Unanchored numerical credibility ("three of my current engagements" with no anchor)
- Mis-cited sources or fabricated attributions

### S-Axis — Signature

Evaluates surface-pattern AI tells. These are word- and sentence-level patterns that signal machine authorship regardless of whether the content is factually correct or structurally sound.

S-axis catches:
- All current Checks 1 through 21 (em dashes, semicolons, banned words, pointer constructions, fragment cadence, parallel openers, sentence-length variance, and so on)
- Rhetorical credibility flourishes ("I'd hand this to a board without prep")
- Press-release opening patterns ("Source X did Y this week")

### A-Axis — Architectural

Evaluates composition, argument structure, intent preservation, and piece-level structural integrity. Failures here are failures of purpose or composition, not of voice or fact.

A-axis catches:
- All current Checks 22 through 24 (Anti-Reductive Capacitance, Glaze Test, Escape Route Audit)
- Promotional stacking in close
- Multi-surface inconsistency
- Intent drift between sections
- AI editorial architecture (thesis-setup-triplet-closer patterns)

---

## RECURSIVE ADDRESSING

Each axis recurses. Depth is chosen based on content stakes. The recursion produces an addressable evaluation tree where each node asks a distinct question.

### Node Address Semantics

A two-character address `X.Y` means: *evaluating Y concerns within the X domain*.

- `F.F` — Raw facts within the factual domain. Are the claims themselves correct?
- `F.S` — Signature concerns within the factual domain. Is factual content presented with signature-clean phrasing, or does the factual framing reveal AI patterns?
- `F.A` — Architectural concerns within the factual domain. Does the factual frame hold up architecturally? Are facts load-bearing or decorative?
- `S.F` — Factual concerns within the signature domain. Do the signature patterns (voice choices) accurately reflect the author's actual register, or does the voice make claims the author would not make?
- `S.S` — Pure signature check. Named Checks 1 through 21 live here.
- `S.A` — Architectural concerns within the signature domain. Does the voice match the piece's structural intent, or does it work against the argument?
- `A.F` — Factual concerns within the architectural domain. Is the structure anchored by load-bearing facts, or is it decorative architecture around hollow content?
- `A.S` — Signature concerns within the architectural domain. Does the composition use AI-formula architecture (thesis-setup-triplet-closer)?
- `A.A` — Pure architectural check. Intent integrity, escape routes, anti-reductive capacitance. Named Checks 22 through 24 live here.

Depth 3 extends this to three-character addresses (F.F.F through A.A.A) with the same semantics applied at a third level.

### Depth Definitions

**Depth 1 — 3 nodes (F, S, A).** Minimum viable evaluation. Used for low-stakes outbound.

**Depth 2 — 9 nodes (F.F through A.A).** Default. Used for standard outbound content.

**Depth 3 — 27 nodes (F.F.F through A.A.A).** Full recursive check. Used for high-stakes outbound content where the amplification multiplier justifies the attention cost.

---

## AUTONOMOUS DEPTH CLASSIFICATION

Claude classifies depth for each piece of outbound content based on the following rubric. Classification is announced before execution. The human reviewer can override with a keyword.

### Classification Rubric

**Depth 1 triggers (pick any):**
- Content under 50 words
- Agreement, acknowledgment, or congratulatory reply with no substantive expertise claim
- Private DM with no positioning content

**Depth 2 triggers (default when no other depth applies):**
- Standard LinkedIn posts
- Prospect or partner emails
- Comments with substantive opinion content
- Any content not explicitly flagged for Depth 1 or Depth 3

**Depth 3 triggers (pick any):**
- Content explicitly called whitepaper, carousel, article, or long-form
- Content over 500 words
- Material intended for public publication on cyberdynesecurity.com
- Content with direct promotional CTAs to commercial offerings
- Content making specific technical claims a domain expert would scrutinize
- Content positioning against a named competitor or vendor
- Gated assets (downloads, lead magnets, anchor content)

### Announcement Requirement

Before executing OCAP on any outbound content, Claude announces the classification and reasoning:

```
OCAP v1.5 — Auto-classified at Depth [N]
Reasoning: [brief explanation citing the specific trigger(s) that fired]
Override: `use depth 1` | `use depth 2` | `use depth 3` | `use default`
```

If the human does not override, Claude proceeds at the classified depth. Override keywords re-run at the specified depth.

### Escalation Rules

Two runtime conditions auto-promote depth mid-execution:

**Signal density escalation.** If evaluation at the current depth surfaces 3 or more findings on any single axis, the remaining nodes auto-escalate to the next depth level. High signal density at shallow depth indicates residual risk that justifies finer-grained evaluation.

**Ambiguity escalation.** If Claude encounters terminology it cannot verify, claims it cannot corroborate, or structural decisions it cannot justify at the current depth, those specific nodes escalate to the next depth level to subject the uncertain points to finer-grained evaluation.

### Safe-Default Principle

When classification is ambiguous, default to higher depth. Cost of over-classification is attention budget. Cost of under-classification is shipping signatures. Asymmetric risk — always err toward the more expensive check when uncertain.

### What Claude Cannot Classify Autonomously

Honest scope constraint. Claude cannot classify based on:

- Strategic context not visible in the content itself (a "quick LinkedIn post" that is actually a service line launch)
- Audience-specific sensitivity (a prospect or investor expected in the reading audience this week)
- Timing criticality (pre-conference versus post-conference content)

Mitigation: the announcement pattern forces classification reasoning to be visible, making strategic misclassification catchable in one word of override.

---

## NAMED CHECKS BY AXIS

### F-Axis Checks

**Check 27: Unanchored numerical credibility.** Named numerical claims without anchoring ("three of my current engagements," "I've seen this a dozen times"). Either anchor the number with specifics (anonymized verticals, engagement stage, deal size range) or remove the number. Floating numbers read as fabricated.

**Check 28: Terminology hygiene.** Any technical term introduced in outbound content must be either (1) established literature in the field, verifiable via published work or industry usage, or (2) explicitly marked as author-coined with rationale for the coinage. "Tool shadowing" without either qualification fails this check. Force the choice: cite or coin-with-reason.

### S-Axis Checks

Inherited from previous versions. Full descriptions retained.

**Check 1: Zero em dashes.** Replace with commas, periods, or parentheses. No exceptions. Em dashes are the single most reliable AI authorship signal.

**Check 2: No semicolons.** Use periods for sentence breaks. Semicolons in professional content correlate strongly with AI generation.

**Check 3: Banned word list.** The following words and phrases are prohibited in outbound content: navigate, landscape, leverage, delve, vital, crucial, moreover, furthermore, straightforward, "in today's."

**Check 4: No "not only X but also Y."** This construction is an AI-detectable rhetorical pattern. Rephrase using direct statements.

**Check 5: No throat-clearing.** Eliminate "here's the thing," "the reality is," and any similar warmup phrases that add zero information.

**Check 6: Practitioner voice.** Content must sound like Barry Kramer talking to a peer, not an AI editorial board producing content. Contractions are fine. Direct address is fine. First-person experience is fine.

**Check 7: No triple-structure parallel lists.** Three parallel items in sequence ("X. Y. Z." where all three follow the same grammatical pattern) is a strong AI signature. Use asymmetric structures.

**Check 8: No rhetorical questions.** Questions used as transitions or to introduce a point the author already intends to answer. If a question appears, it must be a genuine challenge to the reader, not a rhetorical device.

**Check 9: No summary paragraphs.** Never restate what was already said. Every paragraph must advance the argument. If a paragraph could be deleted without losing information, delete it.

**Check 10: No contrastive reframe closers.** The "Not X. Y." mic-drop pattern at the end of a piece. This is one of the most recognizable AI structural signatures.

**Check 11: Vary sentence starts.** Never open consecutive sentences with the same word. Vary openers across paragraphs.

**Check 12: End on forward motion.** The final thought must point forward (action, implication, open question) not backward (summary, restatement, recap).

**Check 13: No punchy one-line thesis openers.** AI loves to open with a single declarative sentence that announces the thesis. Open on concrete data, a story, or an observation instead. Let the thesis emerge from evidence.

**Check 14: No mid-text contrastive reframes.** "This is not X. It is Y." used as a structural pivot in the middle of a piece. Introduce new concepts through contrast with things the reader already knows, not through abstract declarations.

**Check 15: No AI editorial architecture.** Catch-all for structure-level signature patterns not yet individually named. When the piece reads AI-generated despite passing all other S-axis checks, this check has failed. Find the pattern causing it and either repair it or promote it to a named check.

**Check 16: Sentence-length variance.** Deliberate variation in sentence length within each paragraph. AI defaults to 8-to-15-word range with low variance. If 80 percent or more of sentences across three consecutive paragraphs fall in the 8-to-15 word range, the piece has failed.

**Check 17: Comma-separated triplet rhythm.** Three-parallel-items pattern using commas inside a single sentence. Check 7 catches period-separated triplets; Check 17 catches the comma-separated version.

**Check 18: Pointer construction overuse.** "That's how X," "That's the gap," "That's not Y," "That's what matters," "That's the X I Y" (the self-referential variant). AI uses these compulsively as paragraph-pivots and sentence-connectors. Limit: one per piece, maximum two. The self-referential variant ("That's the gap I spend time in") is the most insidious because it uses first-person to smuggle in the pattern.

**Check 19: Fragment punchline cadence.** Short declarative fragments as rhythmic paragraph-closers. One may be acceptable for emphasis. More than one across a piece is a detectable pattern.

**Check 20: Abstract noun subject dominance.** If more than 60 percent of sentences across the piece have abstract nouns as grammatical subjects, rewrite with concrete actors where the content allows.

**Check 21: Parallel sentence-start pairs.** Two back-to-back sentences with matching grammatical openings. The parallelism is the tell.

**Check 25: Rhetorical credibility flourishes.** Phrases like "I'd hand this to a board without prep," "I'd give this to a client," "I'd use this Monday morning." These are practitioner-voice humble-brags that AI generates to sound grounded. They function as credibility pseudo-anchors without actually anchoring anything. Ban.

**Check 26: Press-release opening pattern.** "Source X did Y this week." Date-anchor plus corporate subject plus action verb is news-desk formula. Real practitioner posts open with reaction, tension, or observation, not with bylined announcements.

### A-Axis Checks

Inherited from v1.3 plus new.

**Check 22: Anti-Reductive Capacitance.** Content must resist being reduced to a simpler claim than intended. Test: state the dumbest possible misreading. Does the content actively prevent that misreading?

**Check 23: Signal-to-Noise Ratio (Glaze Test).** Every sentence must carry signal. Test: can you delete this sentence and lose zero information? If yes, delete it.

**Check 24: Escape Route Audit.** Readers who disagree will look for reasons to dismiss the content without engaging the argument. Identify likely escape routes and foreclose them. Common routes: "just theoretical," "only applies to big companies," "no experience," "obvious," "AI-generated."

**Check 29: Promotional density.** No more than one explicit self-promotional beat per major section of outbound content. Whitepaper reference, service reference, and practice name-drops each count as promotional beats. Cap: approximately one promotional beat per 3 to 4 content beats. Close section can contain one of: whitepaper mention, engagement claim, or CTA — not all three.

**Check 30: Multi-surface consistency.** When outbound content spans multiple surfaces (caption plus carousel, post plus first-comment, email plus attachment), all surfaces must converge independently AND cross-reference each other. Version skew between drafts at different surfaces is a detected failure mode. Terminology used in the caption must match terminology used in slide text. A signature pattern repaired in one surface must not persist in another.

---

## ADVERSARIAL PERSONA READ (AXIS INPUT)

The persona-based adversarial read from previous Tier 0 is retained as an input method for S-axis and A-axis evaluation. It is not a separate tier. At each S-axis and A-axis node, Claude reads the content through three personas and uses the signals they surface as the input to the axis's named checks.

**Persona A: The AI Detection Enthusiast.** Someone who reads AI-generated content constantly. What tips them off in this piece? Produce at least three concrete patterns with quoted text samples.

**Persona B: The Hostile Competitor.** Someone in Barry's market looking for reasons to dismiss this content. What evidence would they point to? At least two patterns with quoted samples.

**Persona C: The Domain Practitioner.** A senior professional in the target domain reading to assess whether the author is peer or poser. Where does the piece feel generic, performative, or AI-processed? At least two patterns with quoted samples.

Signal Articulation Requirement: every signal surfaced through persona reading must include pattern name, direct quote from the content, and explanation of why the pattern signals AI. Vague signals ("feels AI-generated") fail the articulation requirement and must be restated concretely or discarded.

Minimum Signal Floor: if fewer than three concrete signals surface across all personas on a piece that has not been repaired before, the adversarial read has not engaged hard enough. Restart with stronger skepticism.

---

## RECURSIVE AUDIT TRACE

Every outbound piece ships with a Recursive Audit Trace showing findings per evaluation node at the classified depth. The audit replaces v1.3's Pass Execution Audit.

### Depth 1 Audit Format

```
OCAP v1.5 RECURSIVE AUDIT — DEPTH 1
====================================
[F] Factual axis:        [findings or "clear"]
[S] Signature axis:      [findings or "clear"]
[A] Architectural axis:  [findings or "clear"]

CONVERGENCE: [yes / no — all 3 nodes must clear]
```

### Depth 2 Audit Format

```
OCAP v1.5 RECURSIVE AUDIT — DEPTH 2
====================================

[F] Factual axis
  [F.F] Raw facts:            [findings or "clear"]
  [F.S] Factual terminology:  [findings or "clear"]
  [F.A] Factual architecture: [findings or "clear"]

[S] Signature axis
  [S.F] Voice-claim alignment: [findings or "clear"]
  [S.S] Surface AI patterns:   [findings or "clear"]
  [S.A] Voice-intent fit:      [findings or "clear"]

[A] Architectural axis
  [A.F] Load-bearing structure: [findings or "clear"]
  [A.S] Composition patterns:   [findings or "clear"]
  [A.A] Intent integrity:       [findings or "clear"]

CONVERGENCE: [yes / no — all 9 nodes must clear]
```

### Depth 3 Audit Format

Same structure extended to 27 nodes (F.F.F through A.A.A). Reserved for whitepaper-class content where the attention cost is justified.

### Finding Format

Each finding at each node includes:

- Pattern name or check number (e.g., "Check 18 fail" or "F-axis: unverified claim")
- Direct quote from the content showing the issue
- Brief explanation of why it fails

### Termination Rule

The audit shows CONVERGENCE: yes only when every leaf node at the target depth clears. Partial convergence (some leaves clear, some dirty) is not convergence. If any leaf finds a signal, repair happens and the recursion re-runs from that leaf's parent axis upward. The recursion is closed only when all leaves clear in the same execution.

### Presentation Rule

Content presented without the Recursive Audit Trace fails the protocol regardless of apparent quality. The audit is the presentation format, not a supplement to it. If Barry receives content without the audit, OCAP has failed at the meta-level and the failure gets logged against the next protocol revision.

---

## APPLICATION

### Triggers

OCAP activates for anything a third party will read:
- LinkedIn posts and comments
- Emails to prospects, clients, or partners
- Proposals and pitch decks
- Website content
- Whitepapers and articles
- Resumes and professional profiles
- Conference presentation content
- Any text rendered in an image, slide, carousel, poster, video caption, or thumbnail — even when accompanying body text has already been evaluated, visual-embedded text is a separate surface and requires independent evaluation

### Internal Content Is Exempt

Workspace files, personal notes, conversation with Claude, internal documentation. The protocol applies only to externally-visible content.

### Multi-Surface Packages

When outbound content spans multiple surfaces, each surface is a distinct evaluation target. Surfaces must each converge at their classified depth AND the package as a whole must pass Check 30 (multi-surface consistency). A caption and its carousel are two surfaces. An email and its attachment are two surfaces. A post and its first comment are two surfaces.

### Evolving Checklist

OCAP is not static. When a new AI authorship signature or content quality failure is identified during real-world drafting, it gets added as a new named check and mapped to the appropriate axis. Check 15 remains the S-axis catch-all. When patterns get pulled out of the catch-all into named checks, the named checks take precedence.

Persona-based adversarial reads provide the mechanism for check discovery. A signal surfaced three times across different pieces is a candidate for named check promotion.

---

## META-PRINCIPLE: THE VERIFICATION PRINCIPLE

OCAP has now evolved through three integrity-to-structure conversions:

- **v1.1 → v1.2:** Adversarial reading moved from optional meta-check to structurally mandatory precondition. Cause: integrity-based enforcement of "do a hostile read" failed in practice.
- **v1.2 → v1.3:** Pass execution moved from self-reported claim to mandatory audit artifact. Cause: integrity-based enforcement of "run three passes" failed in practice.
- **v1.3 → v1.5:** Evaluation structure moved from sequential iterative passes to orthogonal recursive axes. Cause: integrity-based enforcement of "three independent passes" failed in practice because Claude has one generative pass per turn and cannot run three truly independent evaluations sequentially within it.

**The Verification Principle:** When a protocol check relies on Claude doing something the human cannot directly verify, that check must eventually be restructured as a visible artifact or as a structural property of the evaluation architecture itself. Integrity-based enforcement is a placeholder, not a final design.

Remaining integrity-based components flagged for future review:

- **Signal articulation requirement.** Relies on Claude honestly judging whether a signal is concrete enough. Candidate for conversion to a regex-checkable format or a mechanical linter.
- **Persona read depth.** Relies on Claude engaging adversarially rather than performing adversarial engagement. Currently mitigated by the minimum signal floor requirement but still integrity-based at its core.
- **Depth classification reasoning.** Relies on Claude honestly matching content against the rubric. Currently mitigated by the announcement pattern but the rubric match itself is not externally verified.

Future revisions should audit each of these against the Verification Principle.

---

## DEPRECATED IN v1.5

The following v1.3 components are deprecated and replaced:

- **Tier 0 / Tier 1 / Tier 2 structure** → replaced by F / S / A axes. Named checks retained with same numbering.
- **Pass 1 / Pass 2 / Pass 3 iteration enforcement** → replaced by recursive depth enforcement. "Three passes" as a discipline is replaced by "three axes at recursive depth" as architecture.
- **Pass Execution Audit** → replaced by Recursive Audit Trace.
- **Reader Fatigue Warning** → no longer needed. Recursion does not depend on fresh reads across time; structural differentiation between nodes prevents the fatigue failure mode.
- **Rubber-Stamp Prohibition (standalone section)** → absorbed into the Verification Principle and the recursive structure itself. Structural incommensurability between axes prevents the rubber-stamp mode at its source.

---

### Version History

- v1.0 (April 13, 2026): Initial two-tier framework with 18 checks.
- v1.1 (April 16, 2026): Added Rhythm and Cadence checks (16-21) after discovering pattern-level AI signatures that survived v1.0.
- v1.2 (April 16, 2026): Added Tier 0 Adversarial Cold Read and three-pass Iteration Enforcement mandate after v1.1 still required external prompting to trigger adversarial review.
- v1.3 (April 16, 2026): Added Pass Execution Audit requirement and the Verification Principle meta-section. Trigger: Claude presented first-pass output labeled as third-pass converged output in a LinkedIn carousel caption draft.
- v1.4: SKIPPED. Planned additive revision (new named checks 25-30) was absorbed into the v1.5 structural restructure.
- v1.5 (April 16, 2026): Structural restructure from sequential passes to three-axis recursive evaluation (F / S / A axes, recursive depth 1/2/3). Added autonomous depth classification with escalation rules. Added Checks 25 through 30 (rhetorical credibility flourishes, press-release opening pattern, unanchored numerical credibility, terminology hygiene, promotional density, multi-surface consistency). Strengthened Check 18 with the self-referential variant. Deprecated the Pass Execution Audit in favor of the Recursive Audit Trace. Trigger: Barry observed that "checking three times and committing once" must be architecturally honest about what Claude can actually execute in a single turn. Claude has one generative pass. The rigor must come from structural differentiation of evaluation concerns within that pass, not from pretending to run sequential independent passes. v1.5 is the first version where the enforcement architecture is structurally aligned with Claude's actual execution model.
