#!/usr/bin/env python3
"""Shared plain-English word lists + readability helpers for BOTH linters.

`lint.py` (the lecture HTML) and `lint_tex.py` (the companion PDF source) import
this module so the two gates enforce the *same* rules and never drift apart. The
human-readable rulebook these lists mirror is `references/plain_language.md`.

Pure standard library. No third-party deps, no network. Works unchanged on any
agent platform (Claude / Codex / Jules / Cursor / CI).
"""

import re

# Sentence-length policy (mirrors plain_language.md §1).
WORD_AIM = 15            # the target average
WORD_CEILING = 22        # a single sentence longer than this is "long"

# --------------------------------------------------------------------------- #
# 1. Hand-waving — BANNED OUTRIGHT (hard FAIL).  plain_language.md §4.
#    Each entry is matched case-insensitively as a phrase / whole word.
# --------------------------------------------------------------------------- #
HANDWAVE_PHRASES = [
    "it can be shown",
    "it can be proven",
    "it is easy to see",
    "it is clear that",
    "it should be apparent",
    "it should be obvious",
    "left to the reader",
    "left as an exercise",
    "the details are omitted",
    "after some algebra",
    "after simplification",
    "as is well known",
    "needless to say",
    "it goes without saying",
    "suffice it to say",
]
# Single hedge words that almost always precede a skipped step.
HANDWAVE_WORDS = [
    "clearly", "obviously", "evidently", "trivially", "plainly",
]

# --------------------------------------------------------------------------- #
# 2. Literary / filler flourishes — flagged (WARN; many => FAIL).
# --------------------------------------------------------------------------- #
FLOURISH_PHRASES = [
    "dissolve into", "dissolved into", "dissolves into",
    "the machinery of",
    "earns its keep", "earn its keep",
    "the chase for",
    "a tapestry of", "the dance of", "the symphony of",
    "lies at the intersection of", "at the intersection of",
    "in the realm of", "in the world of",
    "it is important to note that", "it is worth noting that",
    "in essence", "essentially,", "fundamentally,",
]

# --------------------------------------------------------------------------- #
# 3. Fancy words -> plain swaps (WARN; many => FAIL).  plain_language.md §3.
#    Keyed by a whole-word regex fragment; value is the suggested plain word.
# --------------------------------------------------------------------------- #
FANCY_WORDS = {
    "utilize": "use", "utilise": "use", "utilizes": "uses", "utilises": "uses",
    "utilizing": "using", "utilising": "using", "utilization": "use",
    "utilisation": "use",
    "leverage": "use", "leverages": "uses", "leveraging": "using",
    "facilitate": "help", "facilitates": "help", "facilitating": "helping",
    "demonstrate": "show", "demonstrates": "shows", "demonstrated": "showed",
    "obtain": "get", "obtains": "gets", "obtained": "got",
    "sufficient": "enough", "insufficient": "not enough",
    "numerous": "many", "myriad": "many", "plethora": "a lot",
    "additional": "more", "approximately": "about",
    "subsequently": "then", "commence": "start", "commences": "starts",
    "terminate": "end", "terminates": "ends",
    "furthermore": "also", "moreover": "also",
    "thus": "so", "hence": "so", "therefore": "so", "consequently": "so",
    "whence": "so",
    "nevertheless": "but", "nonetheless": "still",
    "regarding": "about", "pertaining": "about",
    "aforementioned": "this", "possess": "have", "possesses": "has",
    "comprise": "include", "comprises": "includes", "encompass": "include",
    "encompasses": "includes", "elucidate": "explain", "expound": "explain",
    "ascertain": "find out", "endeavour": "try", "endeavor": "try",
    "crucial": "key", "pivotal": "key", "paramount": "key",
    "robust": "strong", "ubiquitous": "everywhere", "salient": "main",
    "methodology": "method", "dichotomy": "split",
    "cognizant": "aware", "delineate": "describe",
}

# Pre-compiled matchers ------------------------------------------------------ #
_FANCY_KEYS_SORTED = sorted(FANCY_WORDS.keys(), key=len, reverse=True)
_FANCY_PATTERN = r"\b(" + "|".join(re.escape(w) for w in _FANCY_KEYS_SORTED) + r")\b"
_FAST_FANCY_RE = re.compile(_FANCY_PATTERN, re.IGNORECASE)

_HANDWORD_RE = {
    w: re.compile(r"\b" + re.escape(w) + r"\b", re.IGNORECASE)
    for w in HANDWAVE_WORDS
}
_VOWEL_GROUP = re.compile(r"[aeiouy]+")
_WORD = re.compile(r"[A-Za-z']+")
_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")


def find_handwaving(text):
    """Return [(phrase, count)] for every banned hand-wave found (hard FAIL)."""
    low = text.lower()
    hits = []
    for p in HANDWAVE_PHRASES:
        c = low.count(p)
        if c:
            hits.append((p, c))
    for w, rx in _HANDWORD_RE.items():
        c = len(rx.findall(text))
        if c:
            hits.append((w, c))
    return hits


def find_flourishes(text):
    """Return [(phrase, count)] for literary/filler flourishes (WARN)."""
    low = text.lower()
    return [(p, low.count(p)) for p in FLOURISH_PHRASES if low.count(p)]


def find_fancy(text):
    """Return [(word, suggestion, count)] for fancy words (WARN)."""
    counts = {}
    for m in _FAST_FANCY_RE.finditer(text):
        w = m.group(1).lower()
        counts[w] = counts.get(w, 0) + 1

    out = []
    for w, count in counts.items():
        out.append((w, FANCY_WORDS[w], count))
    out.sort(key=lambda t: (-t[2], t[0]))
    return out


def count_syllables(word):
    """Cheap, robust syllable estimate (good enough for a readability score)."""
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    groups = _VOWEL_GROUP.findall(w)
    n = len(groups)
    if w.endswith("e") and n > 1:
        n -= 1
    return max(1, n)


def flesch_reading_ease(text):
    """Return (score, n_words, n_sentences). Higher = easier.

    Flesch Reading Ease = 206.835 - 1.015*(words/sentences) - 84.6*(syll/words).
    ~90+ very easy, 60-70 plain English (≈ grade 8-9), <50 fairly hard,
    <30 very hard. We treat this as an informative WARN signal, not a hard gate,
    because heavily mathematical prose scores low for honest reasons.
    """
    sentences = [s for s in _SENT_SPLIT.split(text) if s.strip()]
    words = _WORD.findall(text)
    n_sent = max(1, len(sentences))
    n_words = len(words)
    if n_words == 0:
        return (100.0, 0, n_sent)
    syll = sum(count_syllables(w) for w in words)
    score = (206.835
             - 1.015 * (n_words / n_sent)
             - 84.6 * (syll / n_words))
    return (round(score, 1), n_words, n_sent)
