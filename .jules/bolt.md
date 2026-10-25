## 2023-10-25 - [O(N) to O(1) matching in _plain_language.py]
**Learning:** When checking for many individual target words in large texts, use a single pre-compiled alternation regex with `finditer()` to achieve O(L) complexity instead of O(N*L). Sort the target words by length descending to prevent shorter phrases from masking longer ones.
**Action:** Always use combined alternation regexes sorted by length for fixed dictionary matching instead of iterating multiple regexes.
