## 2024-06-25 - [O(N) vs O(1) in Regex Matching]
**Learning:** Checking a regular expression match `re.match(s, i)` at every single index in a long string (character-by-character while loop) creates severe overhead.
**Action:** Use `re.search(s, i)` to immediately jump to the next match and grab the intervening text with a string slice `s[i:mm.start()]`. This dramatically speeds up text processing in linters and parsers.
