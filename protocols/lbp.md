---
name: Lateral Bore Protocol
id: lbp
version: 1.0
trigger: -lbp
summary: Systematic lateral thinking framework. Pursue topics to foundational depth, then tunnel laterally into adjacent domains at that depth. Traces causal chains backward from exhaust trails, identifies observable signals at each stage, repurposes cross-domain tools, stacks signals for conviction, and generates zero-competition channels.
---

# LATERAL BORE PROTOCOL (LBP)
## A Framework for Systematic Lateral Thinking in AI-Human Collaboration
### Origin: Barry Kramer + Claude | April 14, 2026

---

## THE CORE INSIGHT

Most problem-solving follows the surface of a domain. You identify the obvious solution category, select the best option within that category, and implement it. This works for 80% of problems. For the remaining 20% the ones where competition is fierce, resources are constrained, or conventional approaches have diminishing returns you need to go lateral.

**Lateral boring** is Barry Kramer's term for a cognitive pattern: pursue a topic to foundational depth, then tunnel laterally into adjacent domains *at that depth* rather than surfacing. The key distinction is that the lateral move happens at depth, not at the surface. Surface-level lateral thinking produces analogies. Deep lateral thinking produces architecture.

---

## THE PROTOCOL

### Phase 1: IDENTIFY THE EXHAUST TRAIL

Every system has an observable output that most people treat as the starting point. That output is actually the *end* of a causal chain. The protocol begins by identifying what everyone else treats as the input and reframing it as the exhaust.

**The question:** "What does everyone else use as their starting point?"

**Job hunting example:** Job postings on LinkedIn/Indeed are the exhaust trail. Everyone starts there. But the posting is the LAST step in: Business Need > Internal Discussion > Budget Approval > JD Written > Posted on Career Page > Syndicated to Boards > Bot Saturation.

**Generalized:** For any problem where you're competing with others for the same resource, identify the signal chain that CREATES that resource. The further upstream you intercept, the less competition exists.

### Phase 2: MAP THE CAUSAL CHAIN BACKWARD

From the exhaust trail, work backward through every step that had to happen for that output to exist.

**The question:** "What had to be true for this to appear?"

For a job posting to appear on LinkedIn:
1. A company had to have a business need (breach, growth, departure, regulatory)
2. Someone had to approve headcount/budget
3. Someone had to write the JD
4. HR had to post it on the company career page
5. The career page had to syndicate to boards
6. Boards had to index it

Each step is a potential interception point with decreasing competition.

### Phase 3: IDENTIFY OBSERVABLE SIGNALS AT EACH STAGE

For each stage in the causal chain, ask: "Is there a publicly observable signal that this stage has occurred?"

| Stage | Signal | Observable? | Source |
|-------|--------|-------------|--------|
| Business need (breach) | SEC 8-K filing, news, HIBP | Yes | EDGAR, NewsAPI, HIBP |
| Business need (growth) | Funding round | Yes | Crunchbase, SEC, news |
| Business need (regulatory) | FTC/HIPAA enforcement | Yes | FTC.gov, HHS portal |
| Budget approved | Executive departure announced | Sometimes | LinkedIn, news |
| JD written | Career page updated | Yes | Company website |
| Posted on career page | Career page changed | Yes | Web scraping |
| Syndicated to boards | Appears on LinkedIn | Yes (but crowded) | JSearch API |

### Phase 4: CROSS-DOMAIN TOOL REPURPOSING

This is where the lateral bore happens. You have tools built for one purpose. Ask: "What else can this tool detect?"

**The question:** "I built [tool X] for [purpose A]. What else does [tool X] observe that could be useful for [purpose B]?"

**Job hunting example:**
- HIBP API was built for security auditing > repurposed for breach-to-hire detection
- PDL was built for OSINT background checks > repurposed for decision maker identification
- SEC EDGAR was built for investor research > repurposed for executive departure and cyber incident detection
- Career page scraping was built for competitive intelligence > repurposed for pre-syndication job detection

**The principle:** Every data source contains multiple signal types. Most people extract one. The lateral thinker asks what ELSE that data reveals.

### Phase 5: INVERSION

Remove the conventional solution entirely and ask what you'd build from scratch.

**The question:** "If job boards didn't exist, how would I find companies that need my skills?"

Answers:
- I'd look for companies in crisis (breaches)
- I'd look for companies growing fast (funding)
- I'd look for companies under regulatory pressure (enforcement actions)
- I'd look for companies with obvious gaps (no CISO on leadership page)
- I'd ask my network (conference contacts, recruiter relationships)
- I'd read the news for signals (executive departures, incidents)

Every one of these is a detection layer the daemon can automate.

### Phase 6: SIGNAL STACKING

Individual signals have noise. Stacked signals have conviction.

A company that:
- Just raised $50M (funding signal)
- Has no CISO on their leadership page (gap signal)
- Recently posted a DevSecOps role on their career page (career signal)
- Is in healthcare (regulatory pressure signal)

...is almost certainly going to hire a CISO within 90 days. Four independent signals pointing to the same conclusion. The conviction level is far higher than any single signal.

**The principle:** Stack multiple weak signals from different domains to produce one strong signal. This is cross-domain triangulation.

### Phase 7: GENERATE THE ZERO-COMPETITION CHANNEL

The final move: create a channel where competition is mathematically zero because you're responding to a need that hasn't been publicly expressed yet.

- Breach-to-hire: You detect the breach. You outreach the CTO. The job doesn't exist yet. Zero competition.
- Leadership gap: You identify the missing CISO. You propose fractional engagement. The job doesn't exist yet. Zero competition.
- Funding signal: You detect the Series C. You outreach the CEO about security readiness. Zero competition.

**This is signal intelligence.** The daemon automates the detection. The enricher identifies the decision maker. The mailer sends the outreach. You wake up to a Telegram notification that says "Sent outreach to [CTO name] at [company] -- breach detected 6 hours ago."

---

## APPLYING LBP TO OTHER DOMAINS

The protocol is domain-agnostic. Here is how it maps to problems beyond job hunting:

**Sales Prospecting:** Exhaust trail is published RFPs. Upstream signals include budget approvals (SEC filings), executive hires (LinkedIn), technology adoption (job postings for specific tools), pain indicators (Glassdoor reviews, support forums).

**Investment Research:** Exhaust trail is stock price movements and analyst reports. Upstream signals include patent filings, hiring patterns, supply chain shifts, regulatory approvals.

**Threat Intelligence:** Exhaust trail is published CVEs and breach reports. Upstream signals include dark web chatter, vulnerability research publications, exploit code commits on GitHub, infrastructure changes in threat actor toolkits.

**Product Development:** Exhaust trail is competitor product launches. Upstream signals include patent applications, job postings (what skills are competitors hiring?), research paper publications, open source contributions.

---

## THE META-PRINCIPLE

**"The obvious input to your system is the exhaust trail of someone else's system. Trace their chain backward. Every link you traverse upstream reduces your competition by an order of magnitude."**

---

## IMPLEMENTATION NOTES

This protocol works best when:
1. The AI partner has access to diverse data sources (APIs, web scraping, databases)
2. The human partner has deep domain expertise to evaluate signal quality
3. Both partners can traverse domains at depth (lateral bore, not lateral skim)
4. The detection can be automated (daemon/agent pattern)
5. The signals can be stacked for conviction

The protocol fails when:
1. The causal chain is too short (no upstream stages to intercept)
2. The signals are not publicly observable
3. The domain has no competition to avoid (you are the only supplier)
