## 2024-05-18 - [Optimizing Multiple Regex Target Looks in Large Texts]
**Learning:** When checking for many individual target words in large texts within the codebase (e.g., linting scripts), using a dictionary of pre-compiled regexes and iteratively running multiple regex passes leads to O(N*M) time complexity, becoming a bottleneck.
**Action:** Use a single pre-compiled alternation regex with `finditer()` to achieve O(L) complexity, rather than iteratively running multiple regex passes.
