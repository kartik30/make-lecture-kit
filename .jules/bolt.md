
## 2024-10-20 - Optimizing multiple keyword searches in linters
**Learning:** When checking for many individual target words in large texts within the codebase (e.g., linting scripts like `_plain_language.py`), using a dictionary of pre-compiled regexes and testing each word individually scales poorly (O(M * L), where M is number of words and L is text length).
**Action:** Use a single pre-compiled alternation regex with `finditer()` to achieve O(L) complexity. Crucially, sort the target words by length descending (`sorted(keys, key=len, reverse=True)`) when building the regex to prevent shorter phrases from masking longer overlapping ones (alternation masking), and maintain a mapping back to the exact original dictionary keys to prevent KeyErrors.
