"""
ocap_lint.py — OCAP v1.5 mechanical enforcement layer

Runs deterministic pattern checks from the S-axis (and a few F-axis and A-axis)
against outbound content. Emits findings as JSON (default) or plain text.

Coverage:
  S-axis (Signature):
    Check 1  — Em dashes
    Check 2  — Semicolons
    Check 3  — Banned word list
    Check 4  — "not only X but also Y"
    Check 5  — Throat-clearing phrases
    Check 7  — Triple-structure parallel lists (period-separated fragments)
    Check 10 — Contrastive reframe closer ("Not X. Y." at end of piece)
    Check 11 — Consecutive sentences starting with same word
    Check 13 — Punchy one-line thesis opener
    Check 14 — Mid-text contrastive reframe ("This is not X. It is Y.")
    Check 16 — Sentence-length variance
    Check 17 — Comma-separated triplet rhythm
    Check 18 — Pointer construction overuse (incl. self-referential variant)
    Check 19 — Fragment punchline cadence
    Check 20 — Abstract noun subject dominance (simplified heuristic)
    Check 21 — Parallel sentence-start pairs
    Check 25 — Rhetorical credibility flourishes
    Check 26 — Press-release opening pattern
  F-axis (Factual):
    Check 27 — Unanchored numerical credibility (heuristic)
  A-axis (Architectural):
    Check 29 — Promotional density (keyword-based)

Usage:
    python ocap_lint.py <file>          # JSON output
    python ocap_lint.py <file> --text   # human-readable output
    cat content.txt | python ocap_lint.py -   # stdin

No third-party dependencies. Stdlib only.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, asdict, field
from typing import List, Tuple


# ============================================================
# DATA STRUCTURES
# ============================================================

@dataclass
class Finding:
    check: int
    name: str
    axis: str
    severity: str
    quote: str
    line: int
    context: str = ""

    def to_dict(self):
        return asdict(self)


# ============================================================
# UTILITIES
# ============================================================

# Tokenize into sentences. Good-enough heuristic; not perfect.
# Splits on ., !, ? followed by space+capital. Handles common abbreviations.
_ABBREVIATIONS = {
    "Mr", "Mrs", "Ms", "Dr", "Prof", "St", "Sr", "Jr",
    "Inc", "Ltd", "Co", "Corp",
    "vs", "etc", "e.g", "i.e",
    "U.S", "U.K", "U.N",
    "Fig", "fig", "Eq",
}

_SENT_SPLIT_RE = re.compile(r'(?<=[.!?])\s+(?=[A-Z"])')


def split_sentences(text: str) -> List[str]:
    """Split text into sentences. Rough but adequate."""
    # Protect abbreviations temporarily
    protected = text
    for abbr in _ABBREVIATIONS:
        protected = re.sub(rf'\b{re.escape(abbr)}\.', f'{abbr}\x00', protected)
    parts = _SENT_SPLIT_RE.split(protected)
    sentences = [p.replace('\x00', '.').strip() for p in parts if p.strip()]
    return sentences


def line_of_match(text: str, start_pos: int) -> int:
    """Return 1-based line number of a character offset."""
    return text[:start_pos].count("\n") + 1


def word_count(sentence: str) -> int:
    return len(re.findall(r"\b[\w']+\b", sentence))


def first_word(sentence: str) -> str:
    """Return the first word of a sentence (lowercased, stripped of punctuation)."""
    m = re.match(r"\s*[\"\'\(\[]?\s*([\w']+)", sentence)
    return m.group(1).lower() if m else ""


# ============================================================
# S-AXIS CHECKS
# ============================================================

def check_01_em_dashes(text: str) -> List[Finding]:
    """Em dashes (— or \u2014) or double-hyphen AI dashes (--)."""
    findings = []
    # Unicode em dash
    for m in re.finditer(r"[\u2014\u2013]", text):
        pos = m.start()
        line = line_of_match(text, pos)
        quote = text[max(0, pos-30):min(len(text), pos+30)].replace("\n", " ").strip()
        findings.append(Finding(
            check=1, name="Em dashes", axis="S", severity="hard",
            quote=m.group(), line=line, context=f"...{quote}..."
        ))
    # Double-hyphen as em-dash substitute
    for m in re.finditer(r"(?<!\-)\-\-(?!\-)", text):
        pos = m.start()
        line = line_of_match(text, pos)
        quote = text[max(0, pos-30):min(len(text), pos+30)].replace("\n", " ").strip()
        findings.append(Finding(
            check=1, name="Em dashes (double-hyphen)", axis="S", severity="hard",
            quote=m.group(), line=line, context=f"...{quote}..."
        ))
    return findings


def check_02_semicolons(text: str) -> List[Finding]:
    """Semicolons are banned in outbound."""
    findings = []
    for m in re.finditer(r";", text):
        pos = m.start()
        line = line_of_match(text, pos)
        quote = text[max(0, pos-40):min(len(text), pos+40)].replace("\n", " ").strip()
        findings.append(Finding(
            check=2, name="Semicolon", axis="S", severity="hard",
            quote=";", line=line, context=f"...{quote}..."
        ))
    return findings


def check_03_banned_words(text: str) -> List[Finding]:
    """Banned word list."""
    banned = [
        "navigate", "landscape", "leverage", "delve", "vital",
        "crucial", "moreover", "furthermore", "straightforward",
    ]
    banned_phrases = ["in today's", "in today s"]
    findings = []
    for word in banned:
        for m in re.finditer(rf"\b{word}\w*\b", text, flags=re.IGNORECASE):
            pos = m.start()
            line = line_of_match(text, pos)
            quote = text[max(0, pos-30):min(len(text), pos+30)].replace("\n", " ").strip()
            findings.append(Finding(
                check=3, name=f"Banned word: '{m.group()}'", axis="S", severity="hard",
                quote=m.group(), line=line, context=f"...{quote}..."
            ))
    for phrase in banned_phrases:
        for m in re.finditer(rf"\b{re.escape(phrase)}\b", text, flags=re.IGNORECASE):
            pos = m.start()
            line = line_of_match(text, pos)
            quote = text[max(0, pos-30):min(len(text), pos+30)].replace("\n", " ").strip()
            findings.append(Finding(
                check=3, name=f"Banned phrase: '{phrase}'", axis="S", severity="hard",
                quote=m.group(), line=line, context=f"...{quote}..."
            ))
    return findings


def check_04_not_only_but_also(text: str) -> List[Finding]:
    """'not only X but also Y' construction."""
    findings = []
    for m in re.finditer(r"\bnot only\b[^.!?]{0,120}\bbut (also|as well)\b", text, flags=re.IGNORECASE):
        pos = m.start()
        line = line_of_match(text, pos)
        findings.append(Finding(
            check=4, name="Not only X but also Y", axis="S", severity="hard",
            quote=m.group()[:100], line=line, context=m.group()[:150]
        ))
    return findings


def check_05_throat_clearing(text: str) -> List[Finding]:
    """Throat-clearing phrases."""
    phrases = [
        r"\bhere'?s the thing\b",
        r"\bthe reality is\b",
        r"\bthe truth is\b",
        r"\blet'?s be honest\b",
        r"\blook,\s",
        r"\bto be fair\b",
        r"\bat the end of the day\b",
        r"\bthe bottom line is\b",
    ]
    findings = []
    for pattern in phrases:
        for m in re.finditer(pattern, text, flags=re.IGNORECASE):
            pos = m.start()
            line = line_of_match(text, pos)
            findings.append(Finding(
                check=5, name=f"Throat-clearing: '{m.group()}'", axis="S", severity="hard",
                quote=m.group(), line=line, context=text[max(0, pos-20):min(len(text), pos+60)].replace("\n", " ").strip()
            ))
    return findings


def check_07_triple_fragment(text: str) -> List[Finding]:
    """Three parallel fragments separated by periods (e.g. 'Fast. Clean. Done.')."""
    findings = []
    # Look for patterns like "Word. Word. Word." or "Short phrase. Short phrase. Short phrase."
    # Heuristic: three consecutive sentences each under 5 words, grammatically parallel
    sentences = split_sentences(text)
    for i in range(len(sentences) - 2):
        a, b, c = sentences[i], sentences[i+1], sentences[i+2]
        # All three must be short (< 6 words) AND end with period (not ? or !)
        if (word_count(a) <= 5 and word_count(b) <= 5 and word_count(c) <= 5 and
                all(s.endswith(".") for s in [a, b, c])):
            # Additional parallelism check: similar opening part-of-speech heuristic
            # (all start with same word-class as approximated by first-char capitalization)
            combined = f"{a} {b} {c}"
            pos = text.find(combined[:30]) if len(combined) > 30 else text.find(a)
            if pos >= 0:
                line = line_of_match(text, pos)
            else:
                line = 0
            findings.append(Finding(
                check=7, name="Triple-structure parallel fragments", axis="S", severity="hard",
                quote=f"{a} {b} {c}"[:120], line=line,
                context=f"Three parallel short sentences detected."
            ))
    return findings


def check_10_contrastive_closer(text: str) -> List[Finding]:
    """Contrastive reframe closer ('Not X. Y.' at end)."""
    findings = []
    # Check last 200 chars for "Not X. Y." or "It's not X. It's Y." pattern
    tail = text[-300:] if len(text) > 300 else text
    patterns = [
        r"\b(It'?s )?[Nn]ot\s+[^.!?]{5,80}\.\s+[A-Z][^.!?]{5,120}\.\s*$",
        r"\bThis isn'?t\s+[^.!?]{5,80}\.\s+(It'?s|This is)\s+[^.!?]{5,120}\.\s*$",
    ]
    for pattern in patterns:
        m = re.search(pattern, tail)
        if m:
            findings.append(Finding(
                check=10, name="Contrastive reframe closer", axis="S", severity="hard",
                quote=m.group()[:150], line=line_of_match(text, len(text) - len(tail) + m.start()),
                context="End-of-piece 'Not X. Y.' mic-drop detected."
            ))
    return findings


def check_11_consecutive_same_opener(text: str) -> List[Finding]:
    """Consecutive sentences opening with the same word."""
    findings = []
    sentences = split_sentences(text)
    for i in range(len(sentences) - 1):
        w1 = first_word(sentences[i])
        w2 = first_word(sentences[i+1])
        # Ignore very short connectors like "I", "A", "The" — only flag substantive repeats
        if w1 and w1 == w2 and len(w1) > 2:
            pos = text.find(sentences[i])
            line = line_of_match(text, pos) if pos >= 0 else 0
            findings.append(Finding(
                check=11, name=f"Consecutive same-word opener: '{w1}'", axis="S", severity="soft",
                quote=f"{sentences[i][:40]}... / {sentences[i+1][:40]}...", line=line,
                context="Two consecutive sentences open with the same word."
            ))
    return findings


def check_13_thesis_opener(text: str) -> List[Finding]:
    """Punchy one-line thesis opener."""
    findings = []
    # Heuristic: first sentence is short (<= 10 words) AND declarative AND contains "is" or "are"
    sentences = split_sentences(text)
    if sentences:
        first = sentences[0]
        if word_count(first) <= 10 and first.endswith(".") and re.search(r"\b(is|are|was|were)\b", first, flags=re.IGNORECASE):
            # Flag only if followed by a longer explanation (indicates thesis-then-elaborate pattern)
            if len(sentences) > 1 and word_count(sentences[1]) > 15:
                findings.append(Finding(
                    check=13, name="Punchy one-line thesis opener", axis="S", severity="soft",
                    quote=first, line=1,
                    context="Short declarative opener followed by longer elaboration (thesis-then-explain pattern)."
                ))
    return findings


def check_14_mid_contrastive(text: str) -> List[Finding]:
    """Mid-text 'This is not X. It is Y.' reframe."""
    findings = []
    patterns = [
        r"\bThis is not\s+[^.!?]{3,60}\.\s+(It is|It'?s)\s+[^.!?]{3,80}\.",
        r"\bThat'?s not\s+[^.!?]{3,60}\.\s+(That'?s|It'?s)\s+[^.!?]{3,80}\.",
        r"\bIt'?s not\s+[^.!?]{3,60}\.\s+It'?s\s+[^.!?]{3,80}\.",
    ]
    # Only flag if NOT at the end (last 300 chars) — that would be Check 10
    body = text[:-300] if len(text) > 300 else ""
    for pattern in patterns:
        for m in re.finditer(pattern, body):
            pos = m.start()
            line = line_of_match(text, pos)
            findings.append(Finding(
                check=14, name="Mid-text contrastive reframe", axis="S", severity="hard",
                quote=m.group()[:120], line=line,
                context="'X is not Y. It is Z.' structural pivot detected mid-text."
            ))
    return findings


def check_16_sentence_length_variance(text: str) -> List[Finding]:
    """Sentence length variance — if 80%+ fall in 8-15 word band, fail."""
    findings = []
    sentences = split_sentences(text)
    if len(sentences) < 6:
        return findings  # Not enough data
    lengths = [word_count(s) for s in sentences]
    in_band = sum(1 for L in lengths if 8 <= L <= 15)
    ratio = in_band / len(lengths)
    if ratio >= 0.80:
        findings.append(Finding(
            check=16, name="Sentence-length variance", axis="S", severity="hard",
            quote=f"{in_band}/{len(lengths)} sentences in 8-15 word band ({ratio:.0%})",
            line=0,
            context=f"AI-typical length distribution. Threshold: <80%. Observed: {ratio:.0%}."
        ))
    return findings


def check_17_comma_triplet(text: str) -> List[Finding]:
    """Comma-separated triplet rhythm: 'X, Y, and Z' or 'X, Y, Z' where items are parallel."""
    findings = []
    # Pattern: three short parallel items separated by commas, ending in "and" or not
    # Heuristic: look for ", ... , (and )? ... ." at sentence level
    # We'll flag when three items are each under 6 words and grammatically parallel
    # Simpler heuristic: find ",\s+\w+(\s+\w+){0,4},\s+(and\s+)?\w+(\s+\w+){0,4}[.!?]"
    pattern = r"[A-Za-z][\w\-]*(?:\s+[\w\-]+){1,5},\s+[\w\-]+(?:\s+[\w\-]+){1,5},\s+(?:and\s+)?[\w\-]+(?:\s+[\w\-]+){1,5}[.!?]"
    for m in re.finditer(pattern, text):
        # Filter out simple noun lists (e.g., "agents, RAG, MCP, MoE, ...") — flag only triples
        # Count commas in the match; exact 2 commas = triple
        if m.group().count(",") == 2:
            pos = m.start()
            line = line_of_match(text, pos)
            findings.append(Finding(
                check=17, name="Comma-separated triplet rhythm", axis="S", severity="soft",
                quote=m.group()[:120], line=line,
                context="Three-item parallel list in single sentence."
            ))
    return findings


def check_18_pointer_constructions(text: str) -> List[Finding]:
    """'That's the X' and related pointer constructions, incl. self-referential variant."""
    findings = []
    patterns = [
        # Classic "That's the X" / "That's how X" / "That's what X"
        (r"\bThat'?s\s+(the|how|what|where|why|when)\s+[^.!?]{3,80}[.!?]", "Classic pointer"),
        # Self-referential variant (v1.5): "That's the X I Y" — insidious practitioner-voice mimic
        (r"\bThat'?s\s+(the|how|what)\s+[^.!?]*?\bI\s+[^.!?]{3,80}[.!?]", "Self-referential pointer"),
        # "That's it" / "That's all" etc.
        (r"\bThat'?s\s+(it|all|why|because)\b[^.!?]{0,80}[.!?]", "Minimal pointer"),
    ]
    for pattern, label in patterns:
        for m in re.finditer(pattern, text):
            pos = m.start()
            line = line_of_match(text, pos)
            findings.append(Finding(
                check=18, name=f"Pointer construction: {label}", axis="S", severity="hard",
                quote=m.group()[:120], line=line,
                context="v1.5 Check 18 (self-referential variant strengthened)."
            ))
    return findings


def check_19_fragment_punchline(text: str) -> List[Finding]:
    """Paragraphs ending in short declarative fragments."""
    findings = []
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    fragment_count = 0
    flagged = []
    for p in paragraphs:
        sentences = split_sentences(p)
        if not sentences:
            continue
        last = sentences[-1]
        # Fragment heuristic: ends with period, <= 5 words, lacks a verb (approximation: no 'is/are/was/were/does/did/has/have')
        if (word_count(last) <= 5 and last.endswith(".") and
                not re.search(r"\b(is|are|was|were|does|did|has|have|had|do|can|will|should|could|would|may|might)\b", last, flags=re.IGNORECASE)):
            fragment_count += 1
            flagged.append(last)
    # One fragment closer is acceptable. More than one is a pattern.
    if fragment_count >= 2:
        findings.append(Finding(
            check=19, name="Fragment punchline cadence", axis="S", severity="hard",
            quote=" / ".join(flagged[:3]), line=0,
            context=f"{fragment_count} paragraphs end in fragment punchlines. Limit: 1."
        ))
    return findings


def check_20_abstract_subject_dominance(text: str) -> List[Finding]:
    """Abstract noun subject dominance. Simplified heuristic."""
    # Full implementation would need a POS tagger. Stdlib-only heuristic:
    # Count sentences whose first content word (after articles/adjectives) is in an abstract-noun list
    # AND sentences whose first content word is a concrete actor (I, you, we, he, she, named actor, company).
    findings = []
    sentences = split_sentences(text)
    if len(sentences) < 8:
        return findings

    abstract_markers = {
        "the", "this", "that", "these", "those",  # weak signal, filtered below
    }
    # Actually measure "does the sentence start with an abstract noun?" by checking
    # if first NP head is a common abstract noun OR if the subject is a pronoun / named actor.
    # Simplified: count sentences starting with concrete actor pronouns vs abstract leads.
    concrete_starters = {"i", "we", "you", "he", "she", "they", "my", "our", "your"}
    abstract_nouns = {
        # Common AI-writing abstract nouns when subjects
        "content", "ai", "llm", "system", "model", "framework", "approach", "method",
        "methodology", "implementation", "architecture", "design", "process", "analysis",
        "understanding", "knowledge", "information", "data", "experience", "solution",
        "technology", "capability", "capabilities", "feature", "benefit", "value", "impact",
        "truth", "reality", "fact", "idea", "concept", "principle", "theory",
        "business", "industry", "market", "organization", "company", "team",
        "development", "growth", "change", "transformation", "innovation",
        "primer", "primers", "video", "walkthrough", "carousel",
    }
    concrete = 0
    abstract = 0
    other = 0
    for s in sentences:
        # Extract first non-article word
        words = re.findall(r"\b[\w']+\b", s.lower())
        if not words:
            continue
        # Skip leading articles
        idx = 0
        while idx < len(words) and words[idx] in {"the", "a", "an", "this", "that", "these", "those", "some", "any", "each", "every", "no"}:
            idx += 1
        if idx >= len(words):
            continue
        first_content = words[idx]
        if first_content in concrete_starters:
            concrete += 1
        elif first_content in abstract_nouns:
            abstract += 1
        else:
            other += 1

    total = concrete + abstract + other
    if total < 8:
        return findings
    abstract_ratio = abstract / total
    # Threshold: >60% abstract or (abstract >> concrete) is a fail
    if abstract_ratio > 0.40 and abstract > concrete * 2:
        findings.append(Finding(
            check=20, name="Abstract noun subject dominance", axis="S", severity="soft",
            quote=f"abstract={abstract}, concrete={concrete}, other={other}",
            line=0,
            context=f"Abstract subjects {abstract_ratio:.0%} of categorized starters; concrete only {concrete/total:.0%}."
        ))
    return findings


def check_21_parallel_sentence_starts(text: str) -> List[Finding]:
    """Back-to-back sentences with matching grammatical openings (stronger than Check 11)."""
    findings = []
    # Heuristic: two consecutive sentences whose first THREE tokens match in structure.
    # Approximation: first word has same length/type (noun-like vs verb-like), second word likely shared.
    sentences = split_sentences(text)
    for i in range(len(sentences) - 1):
        w1 = re.findall(r"\b[\w']+\b", sentences[i].lower())[:3]
        w2 = re.findall(r"\b[\w']+\b", sentences[i+1].lower())[:3]
        if not w1 or not w2:
            continue
        # Flag if first words are different BUT grammatical pattern matches
        # Pattern match heuristic: both start with "The/A/An + noun + verb" OR "Pronoun + verb"
        if (len(w1) >= 3 and len(w2) >= 3 and
                w1[0] in {"the", "a", "an"} and w2[0] in {"the", "a", "an"} and
                w1[0] == w2[0]):
            # Same article-starter + noun parallel
            pos = text.find(sentences[i])
            line = line_of_match(text, pos) if pos >= 0 else 0
            findings.append(Finding(
                check=21, name="Parallel sentence-start pair", axis="S", severity="soft",
                quote=f"{sentences[i][:50]}... / {sentences[i+1][:50]}...", line=line,
                context="Back-to-back sentences with matching article+noun opening."
            ))
    return findings


def check_25_rhetorical_credibility(text: str) -> List[Finding]:
    """Rhetorical credibility flourishes."""
    findings = []
    patterns = [
        r"\bI'?d\s+(hand|give|send|show)\s+(this|it|the)\s+[^.!?]{3,80}\s+(to|without)\s+[^.!?]{3,40}[.!?]",
        r"\bI'?d\s+use\s+this\s+[^.!?]{3,60}[.!?]",
        r"\b(I'?ve|I have)\s+been\s+(doing|working on)\s+this\s+for\s+\d+\+?\s+years\b",
    ]
    for pattern in patterns:
        for m in re.finditer(pattern, text, flags=re.IGNORECASE):
            pos = m.start()
            line = line_of_match(text, pos)
            findings.append(Finding(
                check=25, name="Rhetorical credibility flourish", axis="S", severity="hard",
                quote=m.group()[:100], line=line,
                context="Practitioner-voice humble-brag without anchoring."
            ))
    return findings


def check_26_press_release_opener(text: str) -> List[Finding]:
    """Press-release opening pattern: 'Source X did Y this week.'"""
    findings = []
    sentences = split_sentences(text)
    if not sentences:
        return findings
    first = sentences[0]
    # Pattern: Capitalized-noun-phrase + action verb + time anchor
    # Heuristic: first sentence starts with a proper noun and contains a time anchor
    time_anchors = r"\b(this week|today|yesterday|this morning|last week|recently|just now|this month)\b"
    if re.search(time_anchors, first, flags=re.IGNORECASE):
        # Check if it starts with a proper noun (capitalized sequence)
        if re.match(r"^[A-Z][\w&]+(\s+[A-Z][\w&]+)*\s+(put|released|launched|announced|published|dropped|posted|shared|unveiled|revealed)", first):
            findings.append(Finding(
                check=26, name="Press-release opening pattern", axis="S", severity="hard",
                quote=first[:120], line=1,
                context="Opener uses source+action+time-anchor news-desk formula."
            ))
    return findings


# ============================================================
# F-AXIS CHECKS
# ============================================================

def check_27_unanchored_numerical(text: str) -> List[Finding]:
    """Unanchored numerical credibility claims."""
    findings = []
    # Pattern: first-person + small number + credibility claim
    patterns = [
        # "three of my current engagements"
        r"\b(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|dozen|several|many)\s+of\s+(my|our)\s+(?:current\s+)?[\w\-\s]{3,40}\b",
        # "I've seen this X times"
        r"\bI'?ve\s+seen\s+this\s+(?:\d+|a\s+dozen|a\s+few|many|several)\s+times?\b",
        # "In N+ engagements" / "across N clients"
        r"\b(?:in|across)\s+(?:\d+|many|several|dozens|hundreds)\+?\s+(engagements?|clients?|projects?|deployments?|incidents?)\b",
    ]
    for pattern in patterns:
        for m in re.finditer(pattern, text, flags=re.IGNORECASE):
            pos = m.start()
            line = line_of_match(text, pos)
            findings.append(Finding(
                check=27, name="Unanchored numerical credibility", axis="F", severity="soft",
                quote=m.group()[:100], line=line,
                context="Numerical claim without anchoring specifics (vertical, stage, date, range)."
            ))
    return findings


# ============================================================
# A-AXIS CHECKS
# ============================================================

def check_29_promotional_density(text: str) -> List[Finding]:
    """Promotional stacking — count self-promotional beats."""
    findings = []
    # Beat types: whitepaper mention, service reference, practice name-drop, CTA
    promo_patterns = [
        (r"\b(my|our)(?:\s+[\w\-]+){0,4}\s+(whitepaper|white paper|ebook|e-book|guide|playbook|framework|report)\b", "Whitepaper/asset reference"),
        (r"\b(Intent Gap|Cyberdyne Security|CAISO)\b", "Practice/brand name-drop"),
        (r"\blink(?:ed)?\s+in\s+(?:the|my)\s+(?:first\s+)?comments?\b", "CTA to comment"),
        (r"\b(book a call|schedule a meeting|DM me|message me|contact me|reach out)\b", "Direct CTA"),
        (r"\b(our|my)\s+(practice|engagement|engagements|clients)\b", "Practice/client reference"),
    ]
    hits = []
    for pattern, label in promo_patterns:
        for m in re.finditer(pattern, text, flags=re.IGNORECASE):
            pos = m.start()
            hits.append((pos, label, m.group()))
    # Sort by position
    hits.sort()
    # Rough word count
    total_words = word_count(text)
    if total_words == 0:
        return findings
    # Cap: approximately 1 promo beat per 3-4 content beats. Assume 1 content beat per ~60 words.
    # So ~1 promo per 180-240 words.
    acceptable_beats = max(1, total_words // 150)
    if len(hits) > acceptable_beats:
        quote = "; ".join([f"'{h[2]}' ({h[1]})" for h in hits[:5]])
        findings.append(Finding(
            check=29, name="Promotional density exceeded", axis="A", severity="hard",
            quote=quote[:200], line=0,
            context=f"{len(hits)} promotional beats in {total_words} words. Acceptable: ~{acceptable_beats}."
        ))
    return findings


# ============================================================
# MAIN
# ============================================================

def lint(text: str) -> List[Finding]:
    findings = []
    findings.extend(check_01_em_dashes(text))
    findings.extend(check_02_semicolons(text))
    findings.extend(check_03_banned_words(text))
    findings.extend(check_04_not_only_but_also(text))
    findings.extend(check_05_throat_clearing(text))
    findings.extend(check_07_triple_fragment(text))
    findings.extend(check_10_contrastive_closer(text))
    findings.extend(check_11_consecutive_same_opener(text))
    findings.extend(check_13_thesis_opener(text))
    findings.extend(check_14_mid_contrastive(text))
    findings.extend(check_16_sentence_length_variance(text))
    findings.extend(check_17_comma_triplet(text))
    findings.extend(check_18_pointer_constructions(text))
    findings.extend(check_19_fragment_punchline(text))
    findings.extend(check_20_abstract_subject_dominance(text))
    findings.extend(check_21_parallel_sentence_starts(text))
    findings.extend(check_25_rhetorical_credibility(text))
    findings.extend(check_26_press_release_opener(text))
    findings.extend(check_27_unanchored_numerical(text))
    findings.extend(check_29_promotional_density(text))
    return findings


def format_findings_text(findings: List[Finding], source: str = "") -> str:
    lines = []
    if source:
        lines.append(f"=== OCAP LINT — {source} ===")
    else:
        lines.append("=== OCAP LINT ===")
    lines.append(f"Total findings: {len(findings)}")
    by_axis = {"F": [], "S": [], "A": []}
    for f in findings:
        by_axis[f.axis].append(f)
    for axis_name, axis_findings in [("F-axis", by_axis["F"]), ("S-axis", by_axis["S"]), ("A-axis", by_axis["A"])]:
        if not axis_findings:
            continue
        lines.append(f"\n[{axis_name}] {len(axis_findings)} findings:")
        for f in axis_findings:
            lines.append(f"  Check {f.check:02d} ({f.severity}) — {f.name}")
            lines.append(f"    L{f.line}: {f.quote}")
            if f.context and f.context != f.quote:
                lines.append(f"    Context: {f.context}")
    lines.append("")
    return "\n".join(lines)


def main():
    args = sys.argv[1:]
    as_text = False
    if "--text" in args:
        as_text = True
        args.remove("--text")

    if not args or args[0] == "-":
        text = sys.stdin.read()
        source = "stdin"
    else:
        source = args[0]
        with open(source, "r", encoding="utf-8") as f:
            text = f.read()

    findings = lint(text)

    if as_text:
        print(format_findings_text(findings, source))
    else:
        output = {
            "source": source,
            "total_findings": len(findings),
            "findings": [f.to_dict() for f in findings],
        }
        print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
