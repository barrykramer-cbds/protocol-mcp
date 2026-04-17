# OCAP Lint Calibration Corpus

Reference texts used to calibrate and validate `ocap_lint.py` thresholds.

## Files

**`clean_pg_ds.txt`** — Paul Graham, "Do Things that Don't Scale" (July 2013).
Fetched from http://paulgraham.com/ds.html. Em-dashes stripped for calibration
purposes (PG uses em-dashes heavily, which overlaps with the strongest AI
authorship signal — comma substitutions applied). Clean baseline: professionally
edited 2013 essay, practitioner-analytical voice, approximately 8000 words.
Current score at v1.6: 15 findings (~0.19 per 100 words). This is the
*floor*, not zero — PG's writing patterns legitimately overlap with some
OCAP-flagged patterns (semicolons, pointer constructions, fragment
punchlines). Density is the signal.

**`dirty_pass1_caption.txt`** — First-pass AI-generated LinkedIn caption from
the April 16 session. Known-dirty: produced without OCAP filtering, contains
press-release opener, fragment closers, stacked promotional beats.
Current score at v1.6: 3 findings (~2.52 per 100 words, ~13x clean baseline).

**`dirty_claimed_pass3.txt`** — LinkedIn caption that Claude labeled as
"Pass 3 converged" but had actually only been through Pass 1 refinement
(the v1.2 -> v1.3 trigger event). Contains the self-referential pointer
construction ("That's the gap I spend most client engagements inside") that
directly triggered the Check 18 strengthening in v1.5.
Current score at v1.6: 7 findings (~2.02 per 100 words, ~10x clean baseline).

## Running the lint against the corpus

From `protocol-mcp-deploy/tools/`:

```
python ocap_lint.py calibration\clean_pg_ds.txt --text
python ocap_lint.py calibration\dirty_pass1_caption.txt --text
python ocap_lint.py calibration\dirty_claimed_pass3.txt --text
```

Windows note: if Python appears to hang, redirect stdin with `< NUL` via
`cmd /c`, and set `$env:PYTHONIOENCODING="utf-8"` for UTF-8 stdout. Known
Python 3.13 + Windows stdin-allocation behavior.

## When to re-run

Re-calibrate whenever:
- New named checks are added to ocap_lint.py
- Existing check thresholds are tuned
- Suspicion that tool has drifted (false positive or negative noticed in
  real-world use)

Target: clean baseline density should stay in the 0.1-0.3 findings/100w
range. Dirty samples should stay at 5-15x that. If the ratio collapses
below 5x, tool is under-sensitive. If clean baseline exceeds 0.5/100w,
tool is over-sensitive.
