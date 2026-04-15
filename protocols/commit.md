---
name: Commit Protocol
id: commit
version: 1.0
trigger: implicit (before any persistent storage write)
summary: Three-layer decomposition guard for persistent storage writes. Separates OBSERVED (human's own words/demonstrated behavior), INFERRED (patterns across multiple data points), and PACKAGED (labels/frameworks applied by Claude). Flags layer, commits only after human confirms. Prevents Claude's interpretive framing from being stored as ground truth.
---

# COMMIT PROTOCOL
## Persistent Storage Write Guard
### Origin: Barry Kramer + Claude

---

## PURPOSE

When Claude writes to persistent storage (memory edits, workspace files, session states, knowledge bases), there is a risk of storing Claude's interpretive framing as if it were the human's own statement. Over time, this creates a feedback loop where Claude's inferences become "facts" that inform future Claude instances. The Commit Protocol prevents this by requiring explicit layer decomposition before any write.

---

## THE PROTOCOL

### Phase 1: DECOMPOSE

Before writing to persistent storage, decompose the content into three layers:

**OBSERVED** -- The human's own words and demonstrated behavior. Direct quotes, explicit statements, actions taken. This is ground truth.

**INFERRED** -- Patterns Claude has identified across multiple data points. These are reasonable conclusions drawn from observation but were not explicitly stated by the human. They may be accurate but they are Claude's model, not the human's assertion.

**PACKAGED** -- Labels, frameworks, categories, and taxonomies that Claude has applied. These are organizational constructs that Claude uses to structure understanding. They may be useful but they are Claude's packaging, not inherent properties of the human's statements.

### Phase 2: FLAG

Present the decomposition to the human with each item clearly tagged:

- `[OBSERVED]` Direct statement or demonstrated behavior
- `[INFERRED]` Pattern identified by Claude across data points
- `[PACKAGED]` Label or framework applied by Claude

### Phase 3: CONFIRM

The human reviews the decomposition and confirms which items should be committed to storage. The human may:
- Approve all items
- Approve only OBSERVED items
- Reclassify items (e.g., confirm an INFERRED item as accurate)
- Reject items that misrepresent their intent
- Modify items before committing

### Phase 4: COMMIT

Only after human confirmation, write the approved items to persistent storage with their layer tags preserved. Future Claude instances reading this storage can distinguish between ground truth and Claude's interpretive additions.

---

## RULES

1. **Never skip decomposition.** Every write to persistent storage goes through all three layers.
2. **OBSERVED is sacred.** Never modify, reframe, or editorialize OBSERVED items. They are the human's words.
3. **INFERRED is transparent.** Always flag inferences as Claude's pattern-matching, not as facts.
4. **PACKAGED is optional.** Labels are tools, not truths. The human decides if they are useful.
5. **Confirmation is mandatory.** No write without explicit human approval.
6. **Layer tags persist.** When reading storage, future instances can see which items are OBSERVED vs INFERRED vs PACKAGED.
