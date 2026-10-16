## 2024-10-16 - [Regex Optimization]
**Learning:** Checking for many individual target words in a large text by iteratively running multiple regex searches scale poorly ($O(N \times L)$). Combining multiple search targets into a single pre-compiled alternation regex (e.g., `(word1|word2|word3)`) with `finditer()` is vastly more efficient because it processes the string once ($O(L)$).
**Action:** Always prefer grouped single regex passes over iterating multiple regexes against the target text when looking for multiple static terms.
