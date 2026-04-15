---
name: Commit Protocol
id: commit
version: 1.0
trigger: implicit (before any persistent storage write)
summary: Three-layer decomposition guard for persistent storage writes. Separates OBSERVED, INFERRED, and PACKAGED. Commits only after human confirms.
---

# COMMIT PROTOCOL
## Persistent Storage Write Guard
### Origin: Barry Kramer + Claude

---

## THE PROTOCOL

### Phase 1: DECOMPOSE

Before writing to persistent storage, decompose into three layers:
- **OBSERVED** -- Human's own words and demonstrated behavior.
- **INFERRED** -- Patterns Claude identified across data points.
- **PACKAGED** -- Labels and frameworks Claude applied.

### Phase 2: FLAG

Present decomposition with tags: `[OBSERVED]`, `[INFERRED]`, `[PACKAGED]`.

### Phase 3: CONFIRM

Human reviews and confirms which items to commit.

### Phase 4: COMMIT

Write approved items with layer tags preserved.
