
## 2024-10-23 - Optimizing multi-keyword text search
**Learning:** Checking for numerous individual target phrases or words using multiple regex passes results in poor O(N*L) time complexity where N is the target phrase count and L is the length of the string.
**Action:** When searching a long string for matches against a list of keys, build a single pre-compiled regular expression that uses alternation (e.g. `(word1|word2)`). Ensure target words are sorted by length descending so that shorter patterns don't mask longer ones. Keep a dictionary mapping to recover original keys from the matches. This drops time complexity to O(L).
