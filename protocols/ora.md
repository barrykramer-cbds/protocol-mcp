---
name: Objective Recursive Analysis
id: ora
version: 1.0
trigger: -ora
summary: Recursive depth-drilling evaluation framework. Each analysis level examines the conclusions of the previous level, not just the original proposition. Produces layered insight where Level N questions the assumptions embedded in Level N-1. Terminates at decision fork or foundational truth. Distinct from DAP (adversarial scoring) — ORA is structural decomposition through recursive self-examination.
---

# OBJECTIVE RECURSIVE ANALYSIS (ORA)
## Recursive Depth-Drilling Evaluation Framework
### Origin: Barry Kramer + Claude | April 14, 2026

---

## THE CORE DISTINCTION

DAP asks "what's wrong with this?" ORA asks "what is this actually, at each level of abstraction, and does the thing at Level N survive the understanding gained at Level N+1?"

Most analysis is flat: you examine the proposition, list pros and cons, make a decision. ORA is recursive: each level of analysis takes the output of the previous level as its input and examines the assumptions that level embedded. The recursion terminates when you hit either a decision fork (clear options with understood tradeoffs) or foundational truth (an irreducible fact that cannot be decomposed further).

The power of ORA is that it catches category errors. A proposition can survive surface analysis but fail at depth because the surface analysis accepted a framing that was itself flawed. Each recursive level peels back one layer of assumed framing.

---

## THE PROTOCOL

### Phase 1: STATE THE PROPOSITION

Articulate exactly what is being evaluated. Not the goal, not the hope, not the aspiration. The specific, concrete proposition.

**Format:** "We propose to [action] in order to [outcome] because [reasoning]."

**Discipline:** If you cannot state the proposition in one sentence, you have not yet identified it. The complexity lives in the analysis, not the statement.

**Example from the LBP MCP evaluation:**
"We propose to build five MCP tools that wrap the LBP reasoning framework in order to make lateral thinking callable from any Claude conversation because Claude's reasoning quality is context-dependent and protocols need to be persistently available."

### Phase 2: LEVEL 0 — WHAT IS THE STATED GOAL?

Restate the proposition at face value. No analysis, no judgment. This is the baseline. Verify that the proposition is understood correctly before examining it.

**The question:** "What does this claim to do?"

This level exists to prevent straw-manning. Before you decompose something, make sure you are decomposing the right thing.

### Phase 3: LEVEL 1 — WHAT DOES THIS ACTUALLY DO?

Strip away intent and examine mechanism. What does the proposed thing *mechanically* produce?

**The question:** "Ignoring what this is supposed to accomplish, what does it actually do when executed?"

**Key move:** Separate intent from mechanism. A tool can have noble intent and produce zero mechanism. A plan can have clear intent and actually do something different from what it claims.

**Example:** "Each of the five proposed MCP tools takes text input and returns text output that Claude generates through reasoning. They are structured prompts packaged as tool calls."

### Phase 4: LEVEL 2 — WHEN IS THIS CATEGORY OF THING VALUABLE?

Zoom out from the specific proposition to the general category it belongs to. Establish the criteria for when this type of thing earns its existence.

**The question:** "Under what conditions does [this category of solution] provide value that alternatives cannot?"

**Key move:** Do not evaluate the specific proposition yet. First establish the objective criteria against which it should be measured. This prevents motivated reasoning where you define the criteria to fit the proposition.

**Example:** "An MCP tool earns its existence when it does something Claude cannot do inside the conversation window: external data access, computation, state persistence, or action execution."

### Phase 5: LEVEL 3 — SCORE AGAINST CRITERIA

Now apply the criteria from Level 2 to the specific proposition from Level 1. Be honest. Use a scoring matrix if the criteria are enumerable.

**The question:** "Does the specific mechanism identified in Level 1 satisfy any of the criteria established in Level 2?"

**Key move:** If the score is zero or near-zero, the proposition has a category problem. It is not a bad version of the right thing. It is the wrong thing. This distinction matters because the remediation is completely different: you cannot iterate your way from the wrong category to the right one.

### Phase 6: LEVEL 4 — WHAT WOULD SATISFY THE CRITERIA?

If the proposition fails or underperforms against the criteria, ask what *would* satisfy them. This is not ideation. This is criteria-driven design.

**The question:** "Given the criteria from Level 2, what would a proposition look like that scores well?"

**Key move:** The answer to this question often reveals that the original proposition was aimed at the wrong layer of the problem. The Level 4 answer becomes the seed of the correct approach.

### Phase 7: LEVEL 5 — RECURSIVE INSIGHT

Examine the gap between the original proposition (Level 0) and the criteria-satisfying alternative (Level 4). What does this gap reveal about the original framing?

**The question:** "Why did the original proposition miss? What assumption in the framing caused the misalignment?"

**Key move:** This is the recursive core. You are not just saying "the original was wrong." You are identifying the specific cognitive move that produced the wrong framing so you can avoid it in the future. This is where ORA produces durable insight rather than one-time correction.

**Example:** "The LBP workspace already identified this implicitly. The protocol document is the cognitive framework. The Job Hunter's signals.py is the implementation. The proposed MCP tools tried to package the framework, but the framework does not need packaging — it needs to be in context. What needs packaging is the implementation layer that the framework points to."

### Phase 8: LEVEL N — CONTINUE OR TERMINATE

If Level 5 reveals a new assumption that itself needs examination, recurse. Each additional level takes the insight from the previous level and asks: "Does this insight itself contain an unexamined assumption?"

**Termination conditions:**
- **Decision fork reached:** The analysis has produced clear options with understood tradeoffs. Further recursion would not change the options, only add confidence.
- **Foundational truth reached:** An irreducible fact that cannot be decomposed further. Further recursion would be circular.
- **Diminishing returns:** Each new level is producing smaller deltas than the previous. The analysis has converged.

**Anti-pattern:** Recursing past the point of useful insight. If Level N+1 does not materially change the conclusion from Level N, stop. Intellectual depth is not measured by recursion count.

### Phase 9: DECISION FORK PRESENTATION

Present the terminal state as a clear decision fork:
- Name each option
- State what each option optimizes for
- State what each option sacrifices
- State the estimated cost (time, complexity, resources) of each
- State the estimated value capture of each
- Do not recommend. Present options and let the human decide.

If one option is clearly dominant, say so, but explain *why* rather than just asserting it.

---

## WHEN TO USE ORA

- **Architecture decisions:** Before building, verify the thing you are about to build is the right thing, not just a well-built wrong thing.
- **Strategy validation:** Before executing a plan, verify the plan addresses the actual problem rather than a misframed version of it.
- **Content verification:** Before publishing, verify the content says what you think it says by recursively examining its claims.
- **Tool evaluation:** Before adopting a tool or framework, verify it provides value in the specific way you need, not just value in general.
- **Assumption auditing:** When a conclusion feels too easy, recurse to find the hidden assumption that made it feel easy.

## WHEN NOT TO USE ORA

- When the proposition is simple and the stakes are low. Not everything needs recursive analysis.
- When speed matters more than depth. ORA trades speed for thoroughness.
- When the decision has already been made and the task is execution. Use DAP for post-decision stress testing, not ORA.

---

## ORA vs DAP

| Dimension | ORA | DAP |
|-----------|-----|-----|
| Purpose | Structural decomposition | Adversarial stress test |
| Method | Recursive level-by-level depth drilling | Factor enumeration and scoring |
| Output | Layered insight + decision fork | Scorecard + honest interpretation |
| Finds | Category errors, framing flaws, wrong-layer targeting | Weaknesses, risks, failure modes |
| When | Before committing to an approach | After drafting an approach |
| Recursion | Core mechanism (each level examines previous) | Not recursive (single-pass scoring) |
| Tone | Analytical, neutral | Adversarial, unflinching |

They compose well: ORA first to verify you are building the right thing, then DAP to stress-test the specific implementation.

---

## THE META-PRINCIPLE

**"Every analysis embeds assumptions. Recursive analysis examines its own assumptions. The depth at which your analysis stops examining itself is the depth at which your blind spots live."**
