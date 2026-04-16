---
name: Prompt Algorithm Protocol
id: pap
version: 1.0
trigger: -pap
summary: Formal algorithm for prompt construction. Engineers structured input for maximum output fidelity. Upstream complement to OCAP (output evaluation). Integrates with SIP for multi-window context, MPC for routing, and invokes LBP as a subroutine when conventional framing collapses. Based on the core principle that structured output is proportional to the fidelity of structured input.
---

# PROMPT ALGORITHM PROTOCOL (PAP)
## A Formal Algorithm for AI Prompt Construction
### Origin: Barry Kramer + Claude | April 15, 2026

---

## THE CORE PRINCIPLE

"Intent, expressed as structured input, applied to the generative substrate, produces structured output proportional to the fidelity of the input and the capacity of the substrate."

Most AI interactions fail at the input layer. The user knows what they want but encodes it loosely. The substrate interprets loosely encoded input and produces loosely structured output. The user then blames the model. The actual failure point was the prompt.

PAP formalizes prompt construction as an engineering discipline. Every prompt is a precision instrument. Ambiguity in single-window use wastes one conversation. In parallel multi-window use, it multiplies. PAP eliminates that multiplication.

---

## RELATIONSHIP TO OTHER PROTOCOLS

- **OCAP** evaluates OUTPUT before it goes out (downstream gate)
- **PAP** engineers INPUT before it goes in (upstream algorithm)
- **LBP** is invoked BY PAP when conventional framing collapses (subroutine)
- **SIP** provides session state context that PAP uses for multi-window awareness
- **MPC** routes the constructed prompt to the correct window
- **DAP** can be invoked to adversarially test a prompt before execution

The full loop: PAP constructs the prompt, MPC routes it, the substrate executes, OCAP evaluates the output, failures feed back to PAP for reconstruction.

---

## THE PROTOCOL

### Phase 1: INTENT EXTRACTION

Strip the request to its core function. What is the actual goal, not the first framing of it?

**The question:** "If the output were perfect, what would it let me do that I cannot do now?"

Most prompts encode a method rather than an objective. "Write me a LinkedIn post about AI security" encodes a method (write a post). The intent might be "position myself as the authority on AI security governance for MSP decision-makers." Those produce very different prompts.

**Process:**
1. State the request as received
2. Ask: what is the actual outcome I need?
3. Ask: what decision or action does this output enable?
4. Restate the intent as a functional specification, not a task description

**Red flag:** If the intent statement contains a format ("write," "create," "make"), you are encoding method, not intent. Strip the format. The intent is what the output DOES, not what it IS.

### Phase 2: CONSTRAINT MAPPING

Identify every boundary that shapes the solution space.

**The question:** "What are the hard walls and soft preferences?"

**Hard constraints** (non-negotiable):
- Output format requirements (file type, length, structure)
- Audience (who reads/uses this)
- Compliance requirements (OCAP checks, Strength Protocol, voice rules)
- Technical limitations (model context window, available tools, token budget)
- Time sensitivity (is this urgent or can it iterate?)

**Soft preferences** (shape quality but allow flexibility):
- Tone and register
- Depth vs. breadth tradeoff
- Example density
- Level of technical specificity

**Process:**
1. List every hard constraint explicitly
2. List soft preferences with priority ranking
3. Identify constraint conflicts (two hard walls that narrow the solution space to near-zero)
4. If conflicts exist, resolve before proceeding. A prompt built on conflicting constraints produces noise.

### Phase 3: CONTEXT ASSEMBLY

Gather everything the substrate needs to produce a high-fidelity output.

**The question:** "What does the model need to know that it does not already know?"

**Context categories:**
- **Domain context:** Background knowledge, terminology, frameworks specific to this problem
- **Prior outputs:** Previous versions, related work, established decisions
- **Reference material:** Documents, data, examples that inform the output
- **Session context:** SIP header if multi-window, current window role, upstream/downstream dependencies
- **Negative examples:** What the output should NOT look like (often more informative than positive examples)

**Process:**
1. Inventory what the model knows from training (skip redundant context)
2. Identify gaps between model knowledge and task requirements
3. Assemble context in order of relevance (most critical first, token budget permitting)
4. If SIP is active, pull session topology and window assignments
5. Include negative examples for any dimension where the model's default behavior diverges from intent

**Critical principle:** Context is not "more is better." Irrelevant context dilutes signal. Every piece of context should have a clear causal path to output quality. If you cannot explain why a piece of context improves the output, remove it.

### Phase 4: STRUCTURAL ENCODING

Organize the prompt for maximum parsing fidelity by the substrate.

**The question:** "How should this prompt be structured so the model cannot misinterpret the intent?"

**Encoding principles:**
- Lead with role/persona if the output requires domain-specific calibration
- State the intent as a clear directive, not a suggestion
- Separate instructions from context from constraints (use structural markers)
- Place the most important instruction at the beginning AND the end (primacy + recency)
- Use explicit output format specifications when format matters
- Include decision criteria if the model needs to make judgment calls
- Sequence multi-step instructions chronologically

**Anti-patterns to avoid:**
- Burying the actual request inside a paragraph of background
- Mixing instructions with context without structural separation
- Assuming the model will infer unstated requirements
- Using ambiguous referents ("it," "this," "that" without clear antecedents)
- Providing examples without explaining what the example demonstrates

### Phase 5: SUBSTRATE SELECTION

Determine which model, window, or tool handles this prompt optimally.

**The question:** "Where does this prompt execute for best results?"

**Selection factors:**
- Task complexity vs. model capability (Opus for deep reasoning, Sonnet for speed, Haiku for volume)
- Context window requirements (does the assembled context fit?)
- Tool access requirements (does this need web search, filesystem, MCP servers?)
- If MPC is active: which window in the session topology is assigned this task type?
- If parallel processing: does this prompt depend on output from another window?

**Process:**
1. Match task requirements to substrate capabilities
2. If MPC is active, call mpc_route to get the correct window assignment
3. If dependencies exist, check mpc_status for upstream completion
4. If the prompt exceeds context window, split using the natural decomposition from Phase 1 intent

### Phase 6: LATERAL CHECK (LBP SUBROUTINE)

Before executing, test whether the conventional framing is actually the right one.

**The question:** "Am I solving the right problem, or am I treating the exhaust trail as the starting point?"

**Trigger conditions for invoking LBP:**
- The prompt feels like it is producing a commodity output (something anyone could prompt for)
- The problem space has high competition or saturation
- Previous iterations of similar prompts have produced diminishing returns
- The framing came from someone else's framework rather than first-principles analysis
- You cannot articulate why THIS approach rather than any other

**Process:**
1. Evaluate whether the prompt addresses a root cause or a surface symptom
2. If surface symptom detected: invoke LBP Phase 1 (identify the exhaust trail)
3. Run LBP Phases 2-4 to find the upstream reframe
4. Reconstruct the prompt from Phase 1 using the reframed intent
5. If no reframe needed: proceed to Phase 7

**The principle:** A perfectly constructed prompt aimed at the wrong problem produces a perfect answer to the wrong question. LBP catches this before execution.

### Phase 7: FIDELITY VERIFICATION

Pre-flight check. Does the prompt accurately encode the intent?

**The question:** "If I handed this prompt to a different model with no conversation history, would it produce the intended output?"

**Verification checklist:**
- [ ] Intent is stated as a functional specification, not a method
- [ ] All hard constraints are explicitly listed
- [ ] Context is sufficient and non-redundant
- [ ] Structure separates instructions from context from constraints
- [ ] Output format is specified if format matters
- [ ] Negative examples are included where default behavior diverges from intent
- [ ] No ambiguous referents or unstated assumptions
- [ ] The prompt is self-contained (no dependency on conversation history that is not included)
- [ ] If multi-window: SIP context is attached
- [ ] Lateral check is complete (Phase 6 passed or LBP reframe applied)

**If any check fails:** return to the relevant phase and fix before executing.

### Phase 8: EXECUTION AND HANDOFF

Issue the prompt. Route the output.

**Process:**
1. Execute the prompt against the selected substrate
2. If MPC is active: call mpc_register_output with the result
3. If OCAP applies (outbound content): run the output through OCAP evaluation
4. If OCAP returns FAILs: feed the failure analysis back to Phase 1 and reconstruct
5. If the output is an input to another window (CHAIN-PIPE): format per the MPC handoff spec and route

**The full loop:** PAP Phase 1-8 produces a prompt. The substrate produces output. OCAP evaluates. Failures return to PAP. The cycle repeats until OCAP passes with zero FAILs.

---

## APPLYING PAP AT DIFFERENT SCALES

**Single quick question:** Phases 1, 4, 7 only. Clarify intent, structure clearly, verify no ambiguity. 10 seconds.

**Standard work task:** Full 8-phase pass. Most prompts. 1-2 minutes of construction produces dramatically better output on first try.

**Multi-window parallel session:** Full 8-phase pass with SIP context assembly (Phase 3) and MPC routing (Phase 5). PAP runs once per window, with each window receiving a prompt constructed specifically for its role in the session topology.

**High-stakes output (whitepaper, client deliverable):** Full 8-phase pass with LBP lateral check (Phase 6) and DAP adversarial test on the prompt itself before execution. OCAP full evaluation on output. Multiple PAP-OCAP cycles until convergence.

---

## THE META-PRINCIPLE

**"The quality of AI output is an engineering problem, not a model problem. A well-constructed prompt to a lesser model outperforms a vague prompt to a superior model. PAP formalizes the engineering."**

---

## IMPLEMENTATION NOTES

PAP works best when:
1. The operator has deep domain knowledge (constraint mapping requires knowing what matters)
2. The intent is genuinely understood before encoding begins (Phase 1 failures cascade)
3. The operator is willing to spend construction time to save iteration time
4. Multi-window sessions use SIP for shared context
5. Output-critical work chains PAP into OCAP for closed-loop quality

PAP fails when:
1. The operator does not actually know what they want (no algorithm fixes undefined intent)
2. The task is truly exploratory with no target output shape (use conversation, not PAP)
3. The overhead of formal construction exceeds the value of output quality (trivial questions)
