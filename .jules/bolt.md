
## 2024-05-24 - [Python large keyword matching via regex alternation]
**Learning:** Using a single pre-compiled alternation regex with `finditer()` achieves O(L) complexity vs iterative regex evaluation, but it is critical to sort keywords by length descending to prevent shorter strings matching early and masking longer ones, and to use a mapped lower-case-to-key dict to prevent KeyErrors when matching case insensitively.
**Action:** Always sort keys by length descending and use mapping when optimizing dictionary-based regex searches with `|`.
