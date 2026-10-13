## 2023-10-13 - [O(N) Regex Searching]
**Learning:** Checking for many literal strings or whole-word strings in text sequentially (`for w in words: re.findall(w, text)`) can easily become a major performance bottleneck (O(N*M)) in text linting tools like `lint.py` and `lint_tex.py`.
**Action:** Combine word lists into a single `|` joined regular expression (`re.compile(r"\b(" + "|".join(map(re.escape, sorted(words, key=len, reverse=True))) + r")\b")`) and use `collections.Counter` to bucket the hits. This transforms the regex scan to a single O(N) pass, generating >80% speed improvements.
