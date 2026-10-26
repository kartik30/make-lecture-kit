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
# Optimisation: single pre-compiled alternation regex with finditer() for O(L) complexity.
_FANCY_KEYS_SORTED = sorted(FANCY_WORDS.keys(), key=len, reverse=True)
_FANCY_RE_ALL = re.compile(r"\b(" + "|".join(map(re.escape, _FANCY_KEYS_SORTED)) + r")\b", re.IGNORECASE)
_FANCY_KEY_MAP = {k.lower(): k for k in FANCY_WORDS.keys()}

_HW_PHRASES_SORTED = sorted(HANDWAVE_PHRASES, key=len, reverse=True)
_HW_PHRASES_RE_ALL = re.compile("(?i)(" + "|".join(map(re.escape, _HW_PHRASES_SORTED)) + ")")
_HW_PHRASES_KEY_MAP = {k.lower(): k for k in HANDWAVE_PHRASES}

_HW_WORDS_SORTED = sorted(HANDWAVE_WORDS, key=len, reverse=True)
_HW_WORDS_RE_ALL = re.compile(r"\b(" + "|".join(map(re.escape, _HW_WORDS_SORTED)) + r")\b", re.IGNORECASE)
_HW_WORDS_KEY_MAP = {k.lower(): k for k in HANDWAVE_WORDS}

_FLOURISH_SORTED = sorted(FLOURISH_PHRASES, key=len, reverse=True)
_FLOURISH_RE_ALL = re.compile("(?i)(" + "|".join(map(re.escape, _FLOURISH_SORTED)) + ")")
_FLOURISH_KEY_MAP = {k.lower(): k for k in FLOURISH_PHRASES}

_VOWEL_GROUP = re.compile(r"[aeiouy]+")
_WORD = re.compile(r"[A-Za-z']+")
_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")


def find_handwaving(text):
    """Return [(phrase, count)] for every banned hand-wave found (hard FAIL)."""
    hits = []

    phrase_counts = {}
    for m in _HW_PHRASES_RE_ALL.finditer(text):
        match_str = m.group(1).lower()
        phrase_counts[_HW_PHRASES_KEY_MAP[match_str]] = phrase_counts.get(_HW_PHRASES_KEY_MAP[match_str], 0) + 1

    for p in HANDWAVE_PHRASES:
        if phrase_counts.get(p, 0) > 0:
            hits.append((p, phrase_counts[p]))

    word_counts = {}
    for m in _HW_WORDS_RE_ALL.finditer(text):
        match_str = m.group(1).lower()
        word_counts[_HW_WORDS_KEY_MAP[match_str]] = word_counts.get(_HW_WORDS_KEY_MAP[match_str], 0) + 1

    for w in HANDWAVE_WORDS:
        if word_counts.get(w, 0) > 0:
            hits.append((w, word_counts[w]))

    return hits


def find_flourishes(text):
    """Return [(phrase, count)] for literary/filler flourishes (WARN)."""
    counts = {}
    for m in _FLOURISH_RE_ALL.finditer(text):
        match_str = m.group(1).lower()
        counts[_FLOURISH_KEY_MAP[match_str]] = counts.get(_FLOURISH_KEY_MAP[match_str], 0) + 1

    return [(p, counts.get(p, 0)) for p in FLOURISH_PHRASES if counts.get(p, 0) > 0]


def find_fancy(text):
    """Return [(word, suggestion, count)] for fancy words (WARN)."""
    counts = {}
    for m in _FANCY_RE_ALL.finditer(text):
        match_str = m.group(1).lower()
        counts[_FANCY_KEY_MAP[match_str]] = counts.get(_FANCY_KEY_MAP[match_str], 0) + 1

    out = []
    for w, c in counts.items():
        out.append((w, FANCY_WORDS[w], c))
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
