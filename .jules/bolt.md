## 2023-10-27 - O(L*W) to O(L) Plain Language Linting Speedup
**Learning:** Python's `re.findall()` inside loops over large word lists on long text is incredibly slow. Using a combined Aho-Corasick style regex (`finditer` with `collections.Counter` and word lengths sorted descending to prevent masking) solves this.
**Action:** Always prefer one compiled regex with alternation over looping and searching. Sort by length first to prevent substring collisions.
