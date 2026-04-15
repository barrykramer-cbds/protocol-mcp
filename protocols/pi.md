---
name: Probability Index
id: pi
version: 1.0
trigger: -pi
summary: Rapid Bayesian interpretation scoring for competing explanations. When multiple interpretations of the same evidence exist, score each against observable data, prior frequency, and structural plausibility before committing analytical resources. Prevents wasted cycles on low-probability interpretations and catches framing errors early.
---

# PROBABILITY INDEX (PI)
## Rapid Bayesian Interpretation Scoring
### Origin: Barry Kramer + Claude | April 14, 2026

---

## THE CORE INSIGHT

When two or more interpretations of the same data exist, the natural instinct is to debate their merits. This is expensive. Most of the time, one interpretation is overwhelmingly more probable than the others and the debate is wasted energy. The Probability Index short-circuits the debate by scoring probability *before* committing analytical resources.

This is not formal Bayesian inference. It is a fast heuristic: score each interpretation against three dimensions, pick the highest-probability one, and proceed. If the scores are close, that itself is useful information indicating genuine ambiguity that warrants deeper analysis.

---

## THE PROTOCOL

### Phase 1: ENUMERATE INTERPRETATIONS

List every plausible interpretation of the evidence or situation. Do not evaluate yet. Just enumerate. Include interpretations that feel unlikely. The goal is completeness, not pre-filtering.

**Discipline:** If you can only think of one interpretation, you are not thinking hard enough. There are always at least two.

### Phase 2: SCORE EACH INTERPRETATION

Score each interpretation on three dimensions:

**Observable Evidence Fit (0-10):** How well does this interpretation explain ALL the observable data? Not just the convenient data. All of it. Deduct points for evidence the interpretation cannot explain or must explain away.

**Prior Frequency (0-10):** How often does this type of thing actually happen in the relevant domain? A common occurrence scores high. A rare or unprecedented occurrence scores low. This is the base rate check, the dimension humans are worst at because rare events feel more plausible than they are when you are looking directly at them.

**Structural Plausibility (0-10):** Does the mechanism implied by this interpretation make structural sense? Could the causal chain actually work the way this interpretation requires? An interpretation can fit the evidence and have reasonable base rates but still be mechanistically implausible.

**Total score:** Sum of all three dimensions (max 30).

### Phase 3: COMPARE AND DECIDE

Present the scorecard:

| Interpretation | Evidence Fit | Prior Frequency | Structural Plausibility | Total |
|----------------|:-----------:|:--------------:|:----------------------:|:-----:|
| Interpretation A | X | X | X | XX |
| Interpretation B | X | X | X | XX |

**Decision rules:**

- **Clear winner (gap of 8+):** Proceed with the highest-scoring interpretation. The gap is large enough that the losing interpretation is almost certainly wrong. Do not waste further analytical cycles on it.

- **Moderate gap (4-7):** Proceed with the highest-scoring interpretation but flag the alternative. Note what additional evidence would flip the ranking. Stay alert for disconfirming data.

- **Close scores (gap of 0-3):** Genuine ambiguity. Do NOT pick one arbitrarily. Instead, identify the single observation or data point that would decisively separate the two interpretations. Go find that data point before proceeding.

### Phase 4: STATE THE IMPLICATION

After scoring, state what the winning interpretation means for the current task. Do not just announce the winner and move on. Translate the probability assessment into an action or a reframing of the problem.

**Example:** "Interpretation B scores 27 vs Interpretation A's 11. This means the OCAP 14 checks are 14 distinct items discovered over months of iteration, not 14 passes of 3 rules. This reframes the OCAP protocol file: instead of 3 layers with a recursive pass instruction, we need to enumerate 14 specific named checks organized into categories."

---

## WHEN TO USE PI

- Two or more explanations exist for the same observation
- A conversation is about to spend significant time debating interpretations
- Someone (including Claude) has committed to an interpretation without checking probability
- A framing assumption feels accepted but untested
- Before building something, to verify the build is targeting the right interpretation of the requirement

## WHEN NOT TO USE PI

- Only one interpretation exists (use ORA instead to check if you are missing alternatives)
- The choice between interpretations has no practical consequence (does not matter which is true)
- Formal statistical analysis is available and appropriate (use the math, not the heuristic)

---

## PI vs ORA vs DAP

| Dimension | PI | ORA | DAP |
|-----------|-----|-----|-----|
| Purpose | Choose between competing interpretations | Decompose a proposition recursively | Stress-test a specific plan |
| Speed | Fast (minutes) | Slow (thorough) | Medium |
| Input | Multiple interpretations of same data | Single proposition | Single plan or strategy |
| Output | Probability ranking + action implication | Layered insight + decision fork | Scorecard + honest assessment |
| When | Before committing to an interpretation | Before committing to an approach | After drafting an approach |

They chain naturally: PI to pick the right interpretation, ORA to decompose it, DAP to stress-test the implementation.

---

## THE META-PRINCIPLE

**"The most expensive analytical error is not getting the wrong answer. It is thoroughly analyzing the wrong question. Score probability before committing depth."**
