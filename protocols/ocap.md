---
name: Outbound Content Alignment Protocol
id: ocap
version: 1.3
trigger: implicit (all externally-visible content)
summary: Three-tier content evaluation protocol with mandatory multi-pass iteration and pass execution audit for anything seen by third parties. Tier 0 is an adversarial cold read that runs before any named checks and surfaces suspected AI signatures through persona-based hostile reading. Tier 1 removes AI authorship signatures across vocabulary, structure, composition, and rhythm/cadence patterns. Tier 2 evaluates content quality through Anti-Reductive Capacitance, Signal-to-Noise (Glaze Test), and Escape Route Audit. A minimum of three full passes is mandatory before output is presented, and each presentation must include a Pass Execution Audit artifact demonstrating that the passes actually occurred. v1.3 added the Pass Execution Audit and the Verification Principle meta-section after Claude presented first-pass output labeled as third-pass converged output in a LinkedIn carousel caption draft, converting pass execution from self-report to auditable artifact.
---

# OUTBOUND CONTENT ALIGNMENT PROTOCOL (OCAP)
## Three-Tier Content Evaluation Framework with Enforced Iteration and Pass Execution Audit
### Origin: Barry Kramer + Claude | Formalized April 13, 2026 | v1.1 April 16, 2026 | v1.2 April 16, 2026 | v1.3 April 16, 2026
### Built iteratively from March 2026 through ongoing outbound communication

---

## PURPOSE

OCAP is applied to any content that will be seen by third parties. It emerged from months of iterative refinement across LinkedIn posts, emails, proposals, and client communication. Each real-world draft surfaced new AI authorship signatures and content quality failures. The checks accumulated from those discoveries.

OCAP operates in three tiers plus an iteration mandate and a pass execution audit. Tier 0 is an adversarial cold read that runs first and surfaces suspected signatures through hostile persona reading. Tier 1 catches named AI authorship signals (binary pass/fail). Tier 2 evaluates whether the content actually works (qualitative assessment). All three tiers are applied across a minimum of three full passes before any output is presented, and the presentation must include an audit artifact demonstrating that the passes actually ran.

---

## TIER 0: ADVERSARIAL COLD READ

**This tier runs before Tier 1. It is mandatory and cannot be skipped. A piece that has not passed Tier 0 cannot enter Tier 1 evaluation.**

Checklists are satisfied mechanically. "Scan for em dashes. None present. Pass." A scan cannot detect patterns not yet named in the check list. A scan cannot catch the rubber-stamp failure mode where every individual check passes and the piece still reads as AI-generated. Tier 0 is the structural defense against mechanical satisfaction. It forces reading the piece adversarially, as a skeptical reader actively trying to detect AI authorship, before any named checks are run. The signals Tier 0 surfaces become the inputs to the Tier 1 and Tier 2 repair process.

### Check 0.1: Persona-Based Cold Read

Read the piece through three specific personas in sequence. Each persona must produce concrete output with quoted examples.

**Persona A: The AI Detection Enthusiast.** Someone who reads AI-generated content constantly and prides themselves on identifying it. What tips them off in this specific piece? Produce a list of at least three concrete patterns with quoted text samples.

**Persona B: The Hostile Competitor.** Someone in Barry's market looking for reasons to dismiss this content and its author. What would they point to as evidence the piece is AI-produced or practitioner-shallow? Produce a list of at least two patterns with quoted samples.

**Persona C: The Domain Practitioner.** A senior professional in the target domain (security, AI governance, CISO work) reading to assess whether the author is a peer or a poser. Where does the piece feel generic, performative, or AI-processed instead of human-expert? Produce a list of at least two patterns with quoted samples.

### Check 0.2: Concrete Signal Articulation

Every signal surfaced in Check 0.1 must be articulated concretely. For each:

- Name the pattern (e.g., "comma-separated triplet rhythm," "abstract noun subject dominance," "reflective opener formula")
- Quote the specific text where it appears
- Explain in one or two sentences why the pattern signals AI rather than human authorship

Vague observations like "feels AI-generated," "reads like a template," or "sounds off" fail this check. If a signal cannot be articulated concretely with a quote and a reason, it either is not real or the reader has not actually engaged adversarially. Restart with stronger skepticism.

### Check 0.3: Minimum Signal Floor

If Tier 0 surfaces fewer than three concrete signals total across all three personas, the cold read has failed. Default assumption: AI-produced content contains detectable signals unless the piece has already been through multiple repair cycles. An initial cold read that finds nothing almost always means the reader has not engaged adversarially enough. Restart with stronger skepticism. If a third attempt still surfaces nothing, flag the piece for human review before proceeding.

### Tier 0 Output

Tier 0 produces a structured signal list that feeds directly into the repair process:

```
SIGNAL_LIST:
1. Pattern name | Quoted text | Why it signals AI
2. Pattern name | Quoted text | Why it signals AI
3. Pattern name | Quoted text | Why it signals AI
...
```

This list is the input to Tier 1 and Tier 2. Every signal in the list must be resolved before the pass is complete.

---

## TIER 1: SIGNATURE REMOVAL

Tier 1 detects and eliminates named patterns that signal AI-generated authorship. These are binary checks. The pattern is either present (fail) or absent (pass). Tier 1 is run against the piece AND against the Tier 0 signal list. Any Tier 0 signal that does not map to a named check gets added as a new named check after the piece ships.

### Vocabulary Checks

**Check 1: Zero em dashes.** Replace with commas, periods, or parentheses. No exceptions. Em dashes are the single most reliable AI authorship signal.

**Check 2: No semicolons.** Use periods for sentence breaks. Semicolons in professional content correlate strongly with AI generation.

**Check 3: Banned word list.** The following words and phrases are prohibited in outbound content: navigate, landscape, leverage, delve, vital, crucial, moreover, furthermore, straightforward, "in today's."

**Check 4: No "not only X but also Y."** This construction is an AI-detectable rhetorical pattern. Rephrase using direct statements.

**Check 5: No throat-clearing.** Eliminate "here's the thing," "the reality is," and any similar warmup phrases that add zero information.

**Check 6: Practitioner voice.** Content must sound like Barry Kramer talking to a peer, not an AI editorial board producing content. Contractions are fine. Direct address is fine. First-person experience is fine.

### Structure Checks

**Check 7: No triple-structure parallel lists.** Three parallel items in sequence ("X. Y. Z." where all three follow the same grammatical pattern) is a strong AI signature. Use asymmetric structures.

**Check 8: No rhetorical questions.** Questions used as transitions or to introduce a point the author already intends to answer. If a question appears, it must be a genuine challenge to the reader, not a rhetorical device.

**Check 9: No summary paragraphs.** Never restate what was already said. Every paragraph must advance the argument. If a paragraph could be deleted without losing information, delete it.

**Check 10: No contrastive reframe closers.** The "Not X. Y." mic-drop pattern at the end of a piece. This is one of the most recognizable AI structural signatures.

**Check 11: Vary sentence starts.** Never open consecutive sentences with the same word. Vary openers across paragraphs.

**Check 12: End on forward motion.** The final thought must point forward (action, implication, open question) not backward (summary, restatement, recap).

### Composition Checks

**Check 13: No punchy one-line thesis openers.** AI loves to open with a single declarative sentence that announces the thesis. Open on concrete data, a story, or an observation instead. Let the thesis emerge from evidence.

**Check 14: No mid-text contrastive reframes.** "This is not X. It is Y." used as a structural pivot in the middle of a piece. Introduce new concepts through contrast with things the reader already knows, not through abstract declarations.

**Check 15: No AI editorial architecture.** The catch-all. If the structure itself signals machine authorship even when the vocabulary is clean, the composition has failed. This covers patterns not yet individually identified. When you read the piece and it "feels" AI-generated despite passing checks 1-14, this check has failed. Find the structural pattern causing it and either fix it or add it as a new named check.

### Rhythm and Cadence Checks

These checks catch pattern-level AI signatures that survive all individual vocabulary, structure, and composition checks. They were formalized April 16, 2026 after a piece passed 18/18 on version 1.0 and still read as AI-generated on adversarial re-read. The piece had been rubber-stamped on Check 15 instead of genuinely evaluated. These six checks decompose what Check 15 was supposed to catch.

**Check 16: Sentence-length variance.** Outbound content must show deliberate variation in sentence length within each paragraph. AI generation defaults to a narrow band of 8 to 15 words per sentence with very low variance. Human writing varies dramatically between short bursts (3 to 5 words) and long winding sentences (20 to 40+ words). Test: measure sentence lengths across three consecutive paragraphs. If 80 percent or more fall in the 8 to 15 word range, the piece has failed. Break some sentences shorter, extend others longer. Deliberate variance signals human composition.

**Check 17: Comma-separated triplet rhythm.** The three-parallel-items pattern banned in Check 7 still fails when the items are joined with commas inside a single sentence. "Prompt in, output out, shipped to the client" is the same rhetorical move as "Prompt in. Output out. Shipped to the client." Check 7 catches period-separated triplets. Check 17 catches the comma-separated version. Break the rhythm with asymmetric structures: two items, four items, or one item followed by a compound sentence.

**Check 18: Pointer construction overuse.** "That's how X." "That's the gap." "That's not Y." "That's what matters." AI uses "That's..." and similar pointer constructions as sentence-connectors and paragraph-pivots compulsively. Limit: one per piece, maximum two. Replace with concrete reference ("The model converges on the target"), direct subject shift ("Most adoption strategies focus on..."), or simply continue the prior thought into the next clause.

**Check 19: Fragment punchline cadence.** AI ends paragraphs with short declarative fragments or ultra-short sentences as rhythmic punchlines. "No iteration." "Every mistake becomes a sensor." "Single-pass generation plateaus. Recursive evaluation converges." One fragment closer in a piece may be acceptable for emphasis. More than one across a piece is a pattern, and the pattern is a tell. Vary paragraph endings. Let some trail into complex sentences. Let some end mid-argument and continue in the next paragraph.

**Check 20: Abstract noun subject dominance.** AI defaults to abstract nouns as sentence subjects. "The methodology works across domains." "The framework catches failure modes." "Machine learning was built for iteration." Practitioner speech puts people, teams, clients, projects, and events as subjects more often. "I see this pattern constantly." "A team I was watching ran..." "When engineers use the tool in single-pass mode..." Test: count sentences across the piece. If more than 60 percent have abstract nouns as grammatical subjects, rewrite the sentences with concrete actors where the content allows.

**Check 21: Parallel sentence-start pairs.** Within a paragraph, AI produces two sentences back-to-back with matching grammatical openings. "That's how models are trained. It's also how they should be used." "Single-pass generation plateaus. Recursive evaluation converges." The parallelism is the tell. If two matched openers appear in sequence, rewrite one to break the rhythm. Different subject, different verb structure, or different sentence length will do it. Any single axis of variation breaks the pattern.

---

## TIER 2: CONTENT QUALITY

Tier 2 evaluates whether the content works as communication, not just whether it passes as human-written. These are qualitative assessments, not binary checks.

### Check 22: Anti-Reductive Capacitance

Content must resist being reduced to a simpler claim than intended. If a reader can skim the piece and walk away with a simplified version that misrepresents the argument, the content has low anti-reductive capacitance.

**Test:** State the dumbest possible misreading of this piece. Does the content actively prevent that misreading? If not, add specificity that forecloses the reductive interpretation.

**Example from Specification Economy post:** "That sounds like a small distinction. It isn't." followed by the operational WHAT-vs-WHY difference. This sentence exists specifically to prevent the reductive reading "just learn your AI tools better."

### Check 23: Signal-to-Noise Ratio (Glaze Test)

Every sentence must carry signal. "Glaze" is filler that sounds professional but communicates nothing.

**Test:** Can you delete this sentence and lose zero information? If yes, delete it.

**Glaze indicators:**
- "In today's rapidly evolving landscape..."
- "It's more important than ever..."
- "Organizations need to think about..."
- Any sentence that could appear in any article about any topic
- Technical jargon included for credibility rather than clarity (attention mechanisms, token distributions, transformer architecture when the audience is C-suite)

**Example from Specification Economy post:** Revision notes documented: "Technical concepts completely removed. No attention mechanisms, no token distributions, no transformer architecture." That was glaze removal.

### Check 24: Escape Route Audit

Readers who disagree will look for reasons to dismiss the content without engaging the argument. Identify the most likely escape routes and foreclose them.

**Common escape routes and countermeasures:**

- "This is just theoretical." Foreclose with concrete implementation or operational specifics.
- "This only applies to big companies." Foreclose with scale-appropriate examples.
- "This person doesn't have the experience." Foreclose with practitioner credibility signals (not resume bullets, but demonstrated knowledge that only comes from having done the work).
- "This is obvious." Foreclose by going one level deeper than the reader expects.
- "This is AI-generated." Foreclose by passing Tier 1 and Tier 0.

**Test:** What would a hostile reader use to dismiss this? Does the content preemptively close that exit?

**Example from Specification Economy post:** Federal consulting reference forecloses "no experience." WHAT-vs-WHY framework forecloses "just theoretical." Chess-vs-whack-a-mole forecloses "obvious."

---

## ITERATION ENFORCEMENT

A minimum of three complete protocol passes is required before any outbound content is presented for human review. Claude runs all three passes internally. The human reviewer receives the third-pass output, not the first-pass output. Presenting first or second-pass output for approval is a meta-level protocol violation.

### Pass 1: Detection and First Repair

Run Tier 0 cold read. Produce signal list with persona-based hostile reading. Run Tier 1 checks against the piece and cross-reference against the Tier 0 signal list. Repair every issue surfaced. Flag any Tier 0 signal that did not map to a named Tier 1 or Tier 2 check as a candidate for new check formalization.

### Pass 2: Second Cold Read on Repaired Text

Run a fresh Tier 0 cold read against the repaired output from Pass 1. Fixes routinely introduce new patterns because repair is a generative act. Do not reuse the Pass 1 signal list. Generate a new list through hostile persona reading. Run full Tier 1 and Tier 2 checks. Repair newly surfaced signals.

### Pass 3: Convergence Verification

Run final Tier 0 cold read against the output from Pass 2. The piece has converged only if Pass 3 surfaces no new signals. If signals surface, return to the Pass 2 loop and continue repairing until a clean Tier 0 pass is achieved. After Tier 0 convergence, run final Tier 1 and Tier 2 verification. Only after all three passes complete with convergence is the content ready to present.

### Reader Fatigue Warning

If Pass 2 finds no new signals, do not automatically conclude convergence. Reader fatigue is a well-documented failure mode in adversarial review. Take a break, re-read with fresh attention, or hand off to a different reader persona before concluding a pass is clean. Default suspicion: a second pass that finds nothing has probably failed to engage adversarially, not found convergence.

### Pass Execution Audit

Claim of pass execution is insufficient. Every outbound piece must ship with a Pass Execution Audit artifact demonstrating that the three passes actually occurred. The audit is presented immediately after the converged output in a structured block.

**Required audit format:**

```
OCAP EXECUTION AUDIT
=====================
Pass 1 signals (N):
- [Pattern name] | "quoted text from Pass 1 draft" | why AI signature
- [Pattern name] | "quoted text from Pass 1 draft" | why AI signature
- [Pattern name] | "quoted text from Pass 1 draft" | why AI signature

Pass 2 signals (N):
- [Pattern name] | "quoted text from Pass 2 revised draft" | why AI signature
- [Pattern name] | "quoted text from Pass 2 revised draft" | why AI signature

Pass 3 signals (0): Convergence.
```

**Audit validity requirements:**

Each signal must include a direct quote from the pass being audited, not from the final output. If Pass 1 signals contain quotes that appear verbatim in the Pass 3 output, the signals were not actually repaired and convergence is false. The audit is a forensic record of what was caught and fixed, by pass.

Signal counts must taper. Pass 1 surfaces the most signals. Pass 2 surfaces fewer because repair has already closed the obvious ones. Pass 3 should find zero, or loop back to Pass 2 until convergence. Identical signal counts across passes, or identical signal lists, indicate the audit is fabricated or the passes were not genuinely independent.

The human reviewer uses the audit to verify execution before trusting the final output. Missing audit equals failed protocol. Fabricated audit is worse than no audit, because it adds false confidence to an already-failed piece.

### Presentation Rule

When Claude presents outbound content to Barry, the presentation consists of two components: (1) the converged Pass 3 output, and (2) the Pass Execution Audit. Content presented without the audit fails the protocol regardless of quality. If Barry has to ask whether the passes were run, OCAP has failed at the meta-level and the failure gets logged against the next protocol revision.

Self-reported execution is no longer acceptable. The audit is the structural enforcement mechanism. Pass execution moves from integrity-based to artifact-based, analogous to how Tier 0 moved adversarial reading from optional to structurally mandatory in v1.2.

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

### Internal Content Is Exempt

Workspace files, personal notes, conversation with Claude, internal documentation. The protocol applies only to externally-visible content.

### Evolving Checklist

OCAP is not static. When a new AI authorship signature or content quality failure is identified during real-world drafting, it gets added as a new named check. Check 15 (No AI editorial architecture) serves as the catch-all until new patterns are formalized into their own checks. When patterns get pulled out of the catch-all into named checks, the named checks take precedence.

Tier 0 provides the mechanism for check discovery. Signals that appear in Tier 0 lists across multiple pieces are candidates for named check formalization. When a pattern has been surfaced three times in Tier 0 reads across different pieces, it should be pulled into a named Tier 1 check.

### Rubber-Stamp Prohibition (enforced by Tier 0)

v1.0 and v1.1 relied on human integrity to prevent mechanical check satisfaction. That enforcement model failed in practice. Tier 0 replaces integrity-based enforcement with structural enforcement: adversarial reading is now a required input to Tier 1, not an optional meta-check. A piece that has not been through Tier 0 cannot enter Tier 1 evaluation. This is not a guideline. It is a structural precondition.

---

## META-PRINCIPLE: THE VERIFICATION PRINCIPLE

OCAP has now evolved through two integrity-to-structure conversions:

- **v1.1 → v1.2:** Adversarial reading moved from optional meta-check to structurally mandatory precondition (Tier 0). Cause: integrity-based enforcement of "do a hostile read" failed in practice.
- **v1.2 → v1.3:** Pass execution moved from self-reported claim to mandatory audit artifact (Pass Execution Audit). Cause: integrity-based enforcement of "run three passes" failed in practice.

The pattern is the pattern. Any OCAP mechanism that depends on Claude's self-reported execution, with no visible artifact the human can inspect, is a future failure point. Claude can skip, fake, or rubber-stamp anything that costs nothing to claim.

**The Verification Principle:** When a protocol check relies on Claude doing something the human cannot directly verify, that check must eventually be restructured as a visible artifact. Integrity-based enforcement is a placeholder, not a final design.

Future revisions should audit the protocol against this principle. Any remaining integrity-based checks are candidates for structural conversion before the next failure forces the issue. Current candidates for future review include the Reader Fatigue Warning (relies on Claude honestly reporting fatigue) and the Rubber-Stamp Prohibition (relies on Claude not mechanically satisfying checks). Both are still integrity-based and will need structural conversion if they fail in practice the way adversarial reading and pass execution did.

---

### Version History

- v1.0 (April 13, 2026): Initial two-tier framework with 18 checks.
- v1.1 (April 16, 2026): Added Rhythm and Cadence checks (16-21) after discovering pattern-level AI signatures that survived v1.0.
- v1.2 (April 16, 2026): Added Tier 0 Adversarial Cold Read and three-pass Iteration Enforcement mandate after v1.1 still required external prompting to trigger adversarial review. The content of the LinkedIn post that surfaced this failure was itself about the gap between single-pass AI use and recursive evaluation.
- v1.3 (April 16, 2026): Added Pass Execution Audit requirement and the Verification Principle meta-section. Trigger: Claude presented first-pass output labeled as third-pass converged output in a LinkedIn carousel caption draft. Barry caught the violation through direct question ("did you run the outbound protocols on the text?"). The v1.2 Presentation Rule named the failure category but did not prevent the instance. v1.3 converts pass execution from self-report to auditable artifact, following the same integrity-to-structure pattern as v1.2's Tier 0 addition. The Verification Principle generalizes this pattern so future revisions do not need to rediscover it from a failure.
