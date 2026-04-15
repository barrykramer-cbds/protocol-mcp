---
name: Sidebar Protocol
id: sidebar
version: 1.0
trigger: -sidebar
summary: Context-isolated tangent mechanism. Allows exploration of adjacent topics without contaminating the main conversation thread. Multi-turn supported. Exit with -main, -endsidebar, or by resuming the main topic. Use -sidebar save to export markdown.
---

# SIDEBAR PROTOCOL
## Context-Isolated Tangent Framework
### Origin: Barry Kramer + Claude

---

## PURPOSE

Conversations naturally branch. A main thread about architecture generates a tangential question about a specific technology. A strategy discussion spawns a "what if" that deserves exploration but would derail the primary work. The Sidebar Protocol creates a clean boundary: explore the tangent fully, then return to the main thread without context bleed.

---

## THE PROTOCOL

### Phase 1: INVOCATION

Trigger: `-sidebar` (optionally followed by a topic label)

When invoked:
- Mark the current position in the main conversation thread
- Create an isolated context for the tangent
- The sidebar is clearly delineated from the main thread
- All subsequent exchanges belong to the sidebar until exit

**Example:** `-sidebar quantum error correction relevance to AI alignment`

### Phase 2: SIDEBAR EXECUTION

Within the sidebar:
- Full multi-turn conversation is supported
- The sidebar topic can evolve naturally
- Normal collaboration rules apply
- The sidebar maintains its own coherence independent of the main thread

### Phase 3: EXIT

Exit triggers (any of these returns to the main thread):
- `-main` -- explicit return command
- `-endsidebar` -- explicit close command
- Resuming the main topic naturally -- Claude recognizes the context shift

On exit:
- The main thread resumes from where it was marked
- Sidebar content does not contaminate main thread context unless explicitly referenced
- The sidebar is complete and closed

### Phase 4: EXPORT (optional)

Trigger: `-sidebar save`

When invoked before or during exit:
- Export the sidebar content as clean markdown
- Include the sidebar topic, all turns, and any conclusions
- Format for standalone readability

---

## RULES

1. **Sidebars are isolated.** Main thread context does not bleed in unless the human explicitly brings it.
2. **Multi-turn is native.** A sidebar is not limited to one exchange.
3. **Clean exit.** When the sidebar closes, the main thread picks up where it left off.
4. **Nesting is discouraged.** One sidebar at a time. If a sidebar spawns its own tangent, finish the first sidebar before opening another.
5. **Save before you lose it.** If the sidebar produced something valuable, use `-sidebar save` before exiting.
