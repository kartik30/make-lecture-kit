## 2024-10-12 - Single-Pass Combined Regex for Dictionaries
**Learning:** Checking for the presence of many specific words (like a dictionary of 50-100 words) using individual regex evaluations in a loop (`for word in WORDS: len(regex[word].findall(text))`) scales poorly and is computationally expensive for large texts. Python's `re` engine optimizes `|` alternation quite well.
**Action:** Replace loops of single regexes over large text with a single combined regex using `re.compile(r"\b(" + "|".join(re.escape(w) for w in WORDS) + r")\b")` and `finditer()` to make a single fast pass over the string.

## 2024-10-12 - Avoiding re.sub when string operations suffice
**Learning:** `re.sub(r"[^a-z]", "", word)` is slow for simple cleaning. If previous tokenization guarantees a limited character set (e.g. only alpha and apostrophes), replacing `re.sub` with simple string replacement like `word.replace("'", "")` can be significantly faster.
**Action:** Prefer string methods (`replace`, `strip`, `lower`) over `re.sub` for simple character removals when the input domain is known and constrained.
