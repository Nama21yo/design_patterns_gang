# DSA - Study Syllabus (Bloomberg-focused)

Local source of truth for the Notion "DSA" page tree. Every leaf below becomes one Notion
subpage. Companion to `../system-design/SYLLABUS.md` - that one covers the design round,
this one covers the coding rounds.

## What this is built from

1. **Real interview reports** from a candidate group chat covering the Oct-Dec 2025
   Bloomberg new-grad and internship loops. These are questions that were *actually asked*,
   with the *actual* follow-ups. Part 23 is the bank; it is the highest-value section here.
2. **The company-tagged LeetCode list** (`snehasishroy/leetcode-companywise-interview-questions`,
   bloomberg): 1213 questions, each with a recency window (30 days / 3 months / 6 months / all
   time) and a frequency score.
3. **Topic tags pulled from the LeetCode API** for all 1213 questions, so the classification
   into patterns is authoritative rather than guessed.
4. The user's existing notebooks in `../dsa_notes/`.

## Tiers

- **Tier A (220 questions)** - appeared in the 30-day or 3-month window, or scored >= 50%
  frequency in the 6-month window. These get a full note: link, problem statement, intuition,
  approach, clean Python solution, how to present it out loud, follow-ups and variations,
  time and space complexity.
- **Tier B (993 questions)** - the rest of the tagged list. These live in a per-topic index
  page (title, difficulty, link, recency, frequency) so nothing is left behind, and get
  promoted to Tier A on request.

## Note format (every Tier A + Part 23 page)

    Link  |  Difficulty  |  Reported in round  |  Frequency
    1. Problem statement          (restated precisely, with the examples)
    2. Clarifying questions       (what to ask before writing anything)
    3. Intuition                  (the one idea that unlocks it)
    4. Approach                   (numbered steps, brute force -> optimal)
    5. Solution                   (clear, commented Python)
    6. Complexity                 (time and space, justified)
    7. How to present it          (the script: what to say, in what order, what to draw)
    8. Follow-ups and variations  (including what the interviewer can change)
    9. Pitfalls                   (the mistakes people actually made)

## Legend

`[bl]` = reported verbatim from a real Bloomberg round.


## Part 0 - Orientation

- 0.1 How to use this syllabus + an 8-week study plan
- 0.2 The Bloomberg coding interview: the loop, what each round tests, timing
- 0.3 The solving framework: clarify -> examples -> brute force -> optimise -> code -> test
- 0.4 How to present a solution out loud (the script that earns the hire signal)
- 0.5 Complexity analysis cheat sheet (including amortised and recursive costs)
- 0.6 Python toolkit for interviews (collections, heapq, bisect, itertools, and their costs)
- 0.7 Testing your own code in the room: edge cases, dry runs, invariants


## Part 1 - Arrays, Hashing and Prefix Sums

*Trade memory for time: a dict or a running total turns a nested loop into one pass.*

82 Bloomberg-tagged questions: 11 Tier A, 71 Tier B.

- 1.0 Pattern primer
    - What a hash table actually is (buckets, load factor, resize, collisions)
    - Recognition signals: 'have I seen', 'count of', 'pair that sums'
    - The complement trick (Two Sum family)
    - Frequency maps and Counter idioms
    - Prefix sums: 1D, 2D, and prefix-sum + hashmap for subarray targets
    - Difference arrays for range updates
    - Python: dict, defaultdict, Counter, set - costs and gotchas

- 1.1 [E] Two Sum  (100% / 30d)
- 1.2 [M] Subarray Sum Equals K  (88% / 30d)
- 1.3 [E] Find Pivot Index  (62% / 30d)
- 1.4 [M] Find the Maximum Number of Elements in Subset  (62% / 30d)
- 1.5 [M] Product of Array Except Self  (50% / 3mo)
- 1.6 [E] Max Consecutive Ones  (50% / 3mo)
- 1.7 [H] Number of Ships in a Rectangle [premium]  (38% / 3mo)
- 1.8 [E] Check if Array Is Sorted and Rotated  (62% / 3mo)
- 1.9 [M] Contiguous Array  (50% / 3mo)
- 1.10 [E] Valid Mountain Array  (38% / 3mo)
- 1.11 [E] Kids With the Greatest Number of Candies  (38% / 3mo)
- 1.12 Full Bloomberg question index for this topic (82 questions)

## Part 2 - Two Pointers

*Two indices moving under an invariant, usually on a sorted array or from both ends.*

53 Bloomberg-tagged questions: 17 Tier A, 36 Tier B.

- 2.0 Pattern primer
    - Opposite-ends pointers (sorted pair sum, container with most water)
    - Same-direction (fast/slow) pointers and in-place compaction
    - Why sorting first is often the whole trick
    - Dedup logic in k-sum problems
    - Partitioning (Dutch national flag)
    - Proving the pointer move is safe - the exchange argument

- 2.1 [M] 3Sum  (75% / 30d)
- 2.2 [E] Remove Duplicates from Sorted Array  (62% / 30d)
- 2.3 [E] Valid Palindrome  (62% / 30d)
- 2.4 [M] Container With Most Water  (62% / 3mo)
- 2.5 [M] Next Permutation  (62% / 3mo)
- 2.6 [E] Merge Sorted Array  (50% / 3mo)
- 2.7 [E] Move Zeroes  (50% / 3mo)
- 2.8 [M] 4Sum  (38% / 3mo)
- 2.9 [E] Remove Element  (38% / 3mo)
- 2.10 [E] Find the Index of the First Occurrence in a String  (50% / 3mo)
- 2.11 [M] Sort Colors  (62% / 3mo)
- 2.12 [E] Squares of a Sorted Array  (50% / 3mo)
- 2.13 [E] Merge Strings Alternately  (38% / 3mo)
- 2.14 [M] Next Greater Element III  (38% / 3mo)
- 2.15 [M] Rearrange Array Elements by Sign  (38% / 3mo)
- 2.16 [M] Rotate Array  (50% / 6mo)
- 2.17 [E] Reverse String  (50% / 6mo)
- 2.18 Full Bloomberg question index for this topic (53 questions)

## Part 3 - Sliding Window

*A contiguous window that grows on the right and shrinks on the left while a condition holds.*

61 Bloomberg-tagged questions: 12 Tier A, 49 Tier B.

- 3.0 Pattern primer
    - Fixed-size vs variable-size windows
    - The universal template (expand, violate, contract, record)
    - Window state: counter, distinct count, sum, max in window
    - At-most-K trick for exactly-K problems
    - When a window is NOT valid (negative numbers, non-monotonic conditions)
    - Amortised O(n) argument

- 3.1 [M] Longest Substring Without Repeating Characters  (88% / 30d)
- 3.2 [H] Sliding Window Maximum  (62% / 30d)
- 3.3 [M] Find All Anagrams in a String  (62% / 30d)
- 3.4 [M] Longest Repeating Character Replacement  (62% / 3mo)
- 3.5 [H] Substring with Concatenation of All Words  (50% / 3mo)
- 3.6 [M] Minimum Size Subarray Sum  (50% / 3mo)
- 3.7 [E] Contains Duplicate II  (38% / 3mo)
- 3.8 [M] Fruit Into Baskets  (50% / 3mo)
- 3.9 [M] Binary Subarrays With Sum  (50% / 3mo)
- 3.10 [M] Frequency of the Most Frequent Element  (38% / 3mo)
- 3.11 [M] Jump Game VII  (50% / 3mo)
- 3.12 [M] Permutation in String  (38% / 3mo)
- 3.13 Full Bloomberg question index for this topic (61 questions)

## Part 4 - Stacks, Queues and Monotonic Stacks

*LIFO for matching and nesting; monotonic stacks for next-greater and span problems.*

62 Bloomberg-tagged questions: 14 Tier A, 48 Tier B.

- 4.0 Pattern primer
    - Matching and nesting (parentheses, path simplification)
    - Expression evaluation and the calculator family
    - Monotonic stack: next greater / previous smaller
    - Histogram and trapping-water as span problems
    - Monotonic deque for sliding window maximum
    - Stack-based iterative traversal as a recursion replacement

- 4.1 [H] Trapping Rain Water  (88% / 30d)
- 4.2 [H] Basic Calculator  (62% / 30d)
- 4.3 [E] Next Greater Element I  (62% / 30d)
- 4.4 [M] Next Greater Element II  (62% / 30d)
- 4.5 [E] Valid Parentheses  (62% / 3mo)
- 4.6 [M] Decode String  (75% / 3mo)
- 4.7 [E] First Unique Character in a String  (50% / 3mo)
- 4.8 [M] Asteroid Collision  (62% / 3mo)
- 4.9 [H] Largest Rectangle in Histogram  (50% / 3mo)
- 4.10 [M] Daily Temperatures  (38% / 3mo)
- 4.11 [H] Maximal Rectangle  (38% / 3mo)
- 4.12 [E] Number of Students Unable to Eat Lunch  (38% / 3mo)
- 4.13 [M] Remove All Adjacent Duplicates in String II  (62% / 6mo)
- 4.14 [M] Minimum Remove to Make Valid Parentheses  (50% / 6mo)
- 4.15 Full Bloomberg question index for this topic (62 questions)

## Part 5 - Binary Search

*Halve a search space that is monotone in the answer - not just sorted arrays.*

64 Bloomberg-tagged questions: 18 Tier A, 46 Tier B.

- 5.0 Pattern primer
    - The two invariants (lower_bound / upper_bound) and why off-by-one bugs happen
    - bisect_left vs bisect_right, and rolling your own
    - Binary search on the answer (minimise the maximum)
    - Rotated and modified sorted arrays
    - Search in 2D matrices
    - Predicate framing: find the first True in a FFFTTT sequence

- 5.1 [H] Median of Two Sorted Arrays  (62% / 30d)
- 5.2 [M] Search in Rotated Sorted Array  (62% / 30d)
- 5.3 [M] Find First and Last Position of Element in Sorted Array  (50% / 3mo)
- 5.4 [E] Search Insert Position  (50% / 3mo)
- 5.5 [M] Find Peak Element  (38% / 3mo)
- 5.6 [M] Koko Eating Bananas  (38% / 3mo)
- 5.7 [E] Missing Number  (38% / 3mo)
- 5.8 [E] First Bad Version  (38% / 3mo)
- 5.9 [E] Intersection of Two Arrays  (38% / 3mo)
- 5.10 [M] Valid Triangle Number  (38% / 3mo)
- 5.11 [M] Peak Index in a Mountain Array  (38% / 3mo)
- 5.12 [M] Capacity To Ship Packages Within D Days  (50% / 3mo)
- 5.13 [E] Earliest Finish Time for Land and Water Rides I  (50% / 3mo)
- 5.14 [M] Minimum Number of Days to Make m Bouquets  (38% / 3mo)
- 5.15 [M] Closest Equal Element Queries  (38% / 3mo)
- 5.16 [E] Sqrt(x)  (50% / 6mo)
- 5.17 [M] Find Minimum in Rotated Sorted Array  (50% / 6mo)
- 5.18 [M] Two Sum II - Input Array Is Sorted  (50% / 6mo)
- 5.19 Full Bloomberg question index for this topic (64 questions)

## Part 6 - Sorting and Custom Ordering

*Choosing the right key, comparator, or counting scheme - often the entire solution.*

39 Bloomberg-tagged questions: 8 Tier A, 31 Tier B.

- 6.0 Pattern primer
    - Comparison sorts vs counting/radix/bucket sort
    - Python sort: key functions, stability, functools.cmp_to_key
    - Custom alphabets and non-standard collation orders
    - Sorting by multiple criteria and by derived scores
    - Quickselect for k-th order statistics
    - When NOT to sort (heap, counting, or bucketing is cheaper)

- 6.1 [M] Group Anagrams  (88% / 30d)
- 6.2 [E] Majority Element  (75% / 3mo)
- 6.3 [E] Valid Anagram  (50% / 3mo)
- 6.4 [E] Contains Duplicate  (38% / 3mo)
- 6.5 [M] Majority Element II  (38% / 3mo)
- 6.6 [E] Can Make Arithmetic Progression From Sequence  (38% / 3mo)
- 6.7 [H] Maximum Building Height  (38% / 3mo)
- 6.8 [M] Invalid Transactions  (62% / 6mo)
- 6.9 Full Bloomberg question index for this topic (39 questions)

## Part 7 - Linked Lists

*Pointer surgery: dummy heads, fast/slow pointers, and careful re-linking.*

38 Bloomberg-tagged questions: 13 Tier A, 25 Tier B.

- 7.0 Pattern primer
    - Dummy-head pattern and why it removes edge cases
    - Reversal: iterative, recursive, and in k-groups
    - Fast/slow pointers: middle, cycle detection, cycle start (Floyd)
    - Merging and partitioning lists
    - Doubly and multilevel lists (flatten)
    - Drawing the pointers before writing code

- 7.1 [H] Merge k Sorted Lists  (62% / 30d)
- 7.2 [M] Swap Nodes in Pairs  (62% / 30d)
- 7.3 [M] Add Two Numbers  (75% / 3mo)
- 7.4 [E] Merge Two Sorted Lists  (50% / 3mo)
- 7.5 [E] Reverse Linked List  (50% / 3mo)
- 7.6 [H] Reverse Nodes in k-Group  (50% / 3mo)
- 7.7 [M] Rotate List  (50% / 3mo)
- 7.8 [E] Remove Duplicates from Sorted List  (50% / 3mo)
- 7.9 [M] Reorder List  (38% / 3mo)
- 7.10 [M] Partition List  (38% / 3mo)
- 7.11 [E] Palindrome Linked List  (50% / 6mo)
- 7.12 [M] Copy List with Random Pointer  (50% / 6mo)
- 7.13 [M] Add Two Numbers II  (50% / 6mo)
- 7.14 Full Bloomberg question index for this topic (38 questions)

## Part 8 - Trees and Binary Search Trees

*Recursion with a clear contract: what the call returns and what the parent does with it.*

93 Bloomberg-tagged questions: 14 Tier A, 79 Tier B.

- 8.0 Pattern primer
    - Traversals: preorder, inorder, postorder, level-order (and iterative forms)
    - The recursive contract: define the return value first
    - BST invariant and why inorder is sorted
    - Lowest common ancestor family
    - Path problems (root-to-leaf, any-to-any, path sums)
    - Serialisation and reconstruction from traversals
    - Height, balance, diameter - postorder aggregation

- 8.1 [M] Count Subarrays With Majority Element I  (62% / 30d)
- 8.2 [E] Symmetric Tree  (50% / 3mo)
- 8.3 [E] Maximum Depth of Binary Tree  (38% / 3mo)
- 8.4 [M] Construct Binary Tree from Preorder and Inorder Traversal  (50% / 3mo)
- 8.5 [E] Balanced Binary Tree  (50% / 3mo)
- 8.6 [M] Lowest Common Ancestor of a Binary Search Tree  (38% / 3mo)
- 8.7 [M] Lowest Common Ancestor of a Binary Tree  (50% / 3mo)
- 8.8 [M] Number of Longest Increasing Subsequence  (50% / 3mo)
- 8.9 [H] Binary Tree Maximum Path Sum  (38% / 3mo)
- 8.10 [M] Employee Importance  (38% / 3mo)
- 8.11 [M] Create Binary Tree From Descriptions  (38% / 3mo)
- 8.12 [H] Number of Ways to Assign Edge Weights II  (38% / 3mo)
- 8.13 [M] Validate Binary Search Tree  (50% / 6mo)
- 8.14 [E] Diameter of Binary Tree  (50% / 6mo)
- 8.15 Full Bloomberg question index for this topic (93 questions)

## Part 9 - Tries and Prefix Structures

*A tree keyed by characters - makes prefix queries O(length) instead of O(corpus).*

18 Bloomberg-tagged questions: 8 Tier A, 10 Tier B.

- 9.0 Pattern primer
    - Node design: dict of children vs fixed array; is_word flag
    - Insert, search, startsWith
    - Autocomplete: top-k completions per prefix
    - Wildcard and regex-lite matching over a trie
    - Bitwise trie for XOR maximisation
    - Memory cost and when a sorted list + binary search is better

- 9.1 [E] Longest Common Prefix  (62% / 30d)
- 9.2 [M] Word Break  (38% / 3mo)
- 9.3 [H] Word Break II  (38% / 3mo)
- 9.4 [M] Implement Trie (Prefix Tree)  (38% / 3mo)
- 9.5 [M] Lexicographical Numbers  (38% / 3mo)
- 9.6 [M] Maximum XOR of Two Numbers in an Array  (38% / 3mo)
- 9.7 [M] Search Suggestions System  (38% / 3mo)
- 9.8 [M] Find the Length of the Longest Common Prefix  (38% / 3mo)
- 9.9 Full Bloomberg question index for this topic (18 questions)

## Part 10 - Heaps and Top-K

*Keep only what you need: a size-k heap answers top-k in O(n log k).*

36 Bloomberg-tagged questions: 4 Tier A, 32 Tier B.

- 10.0 Pattern primer
    - Binary heap mechanics: sift up/down, heapify in O(n)
    - Min-heap of size k for top-k largest (and why it is inverted)
    - heapq API, tuples as keys, lazy deletion, the (priority, counter, item) idiom
    - Two-heap median maintenance
    - K-way merge
    - Heap vs quickselect vs bucket sort for top-k

- 10.1 [M] Kth Largest Element in an Array  (38% / 3mo)
- 10.2 [M] Top K Frequent Elements  (50% / 3mo)
- 10.3 [M] Sort Characters By Frequency  (38% / 3mo)
- 10.4 [M] Reorganize String  (38% / 3mo)
- 10.5 Full Bloomberg question index for this topic (36 questions)

## Part 11 - Intervals and Line Sweep

*Sort by an endpoint, then sweep - almost every interval problem reduces to this.*

11 Bloomberg-tagged questions: 4 Tier A, 7 Tier B.

- 11.0 Pattern primer
    - Merge / insert / erase intervals
    - Overlap test and the two canonical sorts (by start vs by end)
    - Line sweep with +1/-1 events (meeting rooms, max concurrency)
    - Min-heap of end times as an alternative sweep
    - Interval scheduling (greedy, by earliest end)
    - Intervals that wrap past midnight and other real-world edge cases

- 11.1 [M] Merge Intervals  (62% / 30d)
- 11.2 [M] Meeting Rooms II [premium]  (62% / 3mo)
- 11.3 [M] Remove Covered Intervals  (38% / 3mo)
- 11.4 [M] Non-overlapping Intervals  (50% / 6mo)
- 11.5 Full Bloomberg question index for this topic (11 questions)

## Part 12 - Greedy

*Take the locally best move - and be ready to prove it stays globally optimal.*

55 Bloomberg-tagged questions: 6 Tier A, 49 Tier B.

- 12.0 Pattern primer
    - Exchange argument: the standard proof sketch to say out loud
    - Sort-then-scan greedies
    - Greedy with a heap (regret / replacement greedies)
    - Jump-game style reachability greedies
    - Stock buy/sell family
    - How to tell greedy from DP (and how to fall back safely)

- 12.1 [E] Longest Palindrome  (62% / 30d)
- 12.2 [M] Maximum Element After Decreasing and Rearranging  (62% / 30d)
- 12.3 [H] Candy  (50% / 3mo)
- 12.4 [E] Minimum Cost of Buying Candies With Discount  (50% / 3mo)
- 12.5 [M] Two City Scheduling  (50% / 6mo)
- 12.6 [M] Gas Station  (50% / 6mo)
- 12.7 Full Bloomberg question index for this topic (55 questions)

## Part 13 - Recursion and Backtracking

*Enumerate a decision tree, undo each choice, and prune as early as possible.*

40 Bloomberg-tagged questions: 7 Tier A, 33 Tier B.

- 13.0 Pattern primer
    - The choose / explore / un-choose template
    - Subsets, permutations, combinations - and their dedup rules
    - Pruning: sorting, bounds, and feasibility checks
    - Grid backtracking (word search, path enumeration)
    - Constraint problems (n-queens, sudoku)
    - Complexity of exponential search and how to state it

- 13.1 [M] Letter Combinations of a Phone Number  (62% / 30d)
- 13.2 [M] Subsets II  (62% / 30d)
- 13.3 [M] Subsets  (38% / 3mo)
- 13.4 [M] Word Search  (50% / 3mo)
- 13.5 [M] Generate Parentheses  (50% / 3mo)
- 13.6 [H] Sudoku Solver  (38% / 3mo)
- 13.7 [M] Permutations  (38% / 3mo)
- 13.8 Full Bloomberg question index for this topic (40 questions)

## Part 14 - Graphs, Grids and Union-Find

*Model the problem as nodes and edges first; the algorithm is then almost forced.*

87 Bloomberg-tagged questions: 14 Tier A, 73 Tier B.

- 14.0 Pattern primer
    - Representations: adjacency list, matrix, implicit grids
    - BFS (shortest path in unweighted graphs) and DFS (connectivity, paths)
    - Grid traversal / flood fill and the boundary trick
    - Topological sort (Kahn and DFS) and cycle detection
    - Dijkstra, Bellman-Ford, and when each is needed
    - Union-Find with path compression and union by rank
    - Enumerating all paths vs shortest path - different tools
    - Bipartite checking and colouring

- 14.1 [M] Accounts Merge  (62% / 30d)
- 14.2 [H] Network Recovery Pathways  (62% / 30d)
- 14.3 [M] Number of Islands  (75% / 3mo)
- 14.4 [M] Longest Consecutive Sequence  (75% / 3mo)
- 14.5 [M] Flatten a Multilevel Doubly Linked List  (50% / 3mo)
- 14.6 [H] Word Ladder  (38% / 3mo)
- 14.7 [M] Coin Change  (62% / 3mo)
- 14.8 [M] Evaluate Division  (50% / 3mo)
- 14.9 [M] Rotting Oranges  (62% / 3mo)
- 14.10 [M] Perfect Squares  (50% / 3mo)
- 14.11 [M] Number of Provinces  (38% / 3mo)
- 14.12 [M] Surrounded Regions  (38% / 3mo)
- 14.13 [M] Minimize Hamming Distance After Swap Operations  (38% / 3mo)
- 14.14 [M] All Paths From Source to Target  (50% / 6mo)
- 14.15 Full Bloomberg question index for this topic (87 questions)

## Part 15 - Dynamic Programming

*Define the state, write the recurrence, then decide memo or table.*

137 Bloomberg-tagged questions: 23 Tier A, 114 Tier B.

- 15.0 Pattern primer
    - Optimal substructure and overlapping subproblems - how to verify both
    - State design: what is the smallest thing that determines the rest
    - Top-down memoisation vs bottom-up tabulation, and space rolling
    - 1D: climbing stairs, house robber, coin change, LIS
    - 2D: grid paths, edit distance, LCS, knapsack
    - Interval DP and partition DP
    - DP on strings with matching (regex, wildcard, word break)
    - Bitmask DP
    - Reconstructing the answer, not just its value

- 15.1 [E] Best Time to Buy and Sell Stock  (88% / 30d)
- 15.2 [H] Regular Expression Matching  (75% / 30d)
- 15.3 [M] Maximum Subarray  (75% / 30d)
- 15.4 [E] Climbing Stairs  (62% / 30d)
- 15.5 [M] Triangle  (75% / 30d)
- 15.6 [M] Jump Game  (62% / 30d)
- 15.7 [M] Valid Parenthesis String  (62% / 30d)
- 15.8 [M] Longest Palindromic Substring  (75% / 3mo)
- 15.9 [M] House Robber  (62% / 3mo)
- 15.10 [M] Jump Game II  (38% / 3mo)
- 15.11 [M] Unique Paths II  (38% / 3mo)
- 15.12 [M] Best Time to Buy and Sell Stock II  (38% / 3mo)
- 15.13 [M] Maximum Product Subarray  (38% / 3mo)
- 15.14 [M] Longest Increasing Subsequence  (38% / 3mo)
- 15.15 [H] Split Array Largest Sum  (38% / 3mo)
- 15.16 [H] Total Waviness of Numbers in Range II  (50% / 3mo)
- 15.17 [M] Decode Ways  (38% / 3mo)
- 15.18 [M] Guess Number Higher or Lower II  (38% / 3mo)
- 15.19 [H] Maximum Profit in Job Scheduling  (38% / 3mo)
- 15.20 [H] Number of Paths with Max Score  (38% / 3mo)
- 15.21 [H] Number of ZigZag Arrays II  (38% / 3mo)
- 15.22 [E] Pascal's Triangle  (50% / 6mo)
- 15.23 [M] Sort Integers by The Power Value  (62% / 6mo)
- 15.24 Full Bloomberg question index for this topic (137 questions)

## Part 16 - Bit Manipulation

*XOR cancellation, masks, and the handful of tricks that keep reappearing.*

35 Bloomberg-tagged questions: 5 Tier A, 30 Tier B.

- 16.0 Pattern primer
    - AND/OR/XOR/shift semantics and Python's arbitrary-precision ints
    - XOR identities: a^a=0, a^0=a, and the single-number family
    - Low bit isolation x & -x, clearing x & (x-1), popcount
    - Bitmask as a set (subset enumeration)
    - Building addition/multiplication without operators
    - Signed-integer simulation and 32-bit overflow in Python

- 16.1 [E] Single Number  (62% / 30d)
- 16.2 [M] Divide Two Integers  (38% / 3mo)
- 16.3 [E] Power of Two  (38% / 3mo)
- 16.4 [E] Set Mismatch  (38% / 3mo)
- 16.5 [M] Find the Prefix Common Array of Two Arrays  (38% / 3mo)
- 16.6 Full Bloomberg question index for this topic (35 questions)

## Part 17 - Math, Number Theory and Geometry

*Primes, modular arithmetic, digit manipulation, randomisation and coordinate geometry.*

59 Bloomberg-tagged questions: 6 Tier A, 53 Tier B.

- 17.0 Pattern primer
    - Overflow, integer parsing and clamping (atoi, reverse integer)
    - GCD/LCM, Euclid, and modular inverse
    - Primes: trial division, sieve, segmented sieve, factorisation
    - Fast exponentiation (binary and modular)
    - Digit DP-lite: counting and constructing numbers
    - Random sampling and reservoir sampling
    - Geometry: points, slopes, clock angles, rectangle overlap

- 17.1 [E] Palindrome Number  (62% / 30d)
- 17.2 [M] Angle Between Hands of a Clock  (62% / 30d)
- 17.3 [M] Reverse Integer  (50% / 3mo)
- 17.4 [M] Pow(x, n)  (50% / 3mo)
- 17.5 [E] Plus One  (38% / 3mo)
- 17.6 [E] Find Numbers with Even Number of Digits  (38% / 3mo)
- 17.7 Full Bloomberg question index for this topic (59 questions)

## Part 18 - Matrix and Simulation

*Index arithmetic done carefully, plus problems that simply ask you to follow the rules.*

50 Bloomberg-tagged questions: 9 Tier A, 41 Tier B.

- 18.0 Pattern primer
    - In-place rotation, transpose, and reflection
    - Spiral and diagonal traversal
    - Using the first row/column as marker storage
    - Game-of-life style in-place state encoding
    - Direction vectors and boundary handling
    - Simulation problems: read the spec twice, then encode it literally

- 18.1 [M] Multiply Strings  (62% / 30d)
- 18.2 [M] Process String with Special Operations I  (62% / 30d)
- 18.3 [M] Rotate Image  (75% / 3mo)
- 18.4 [M] Spiral Matrix  (38% / 3mo)
- 18.5 [M] Set Matrix Zeroes  (50% / 3mo)
- 18.6 [M] Valid Sudoku  (50% / 3mo)
- 18.7 [E] Concatenation of Array  (50% / 3mo)
- 18.8 [E] Fizz Buzz  (38% / 3mo)
- 18.9 [E] Robot Return to Origin  (38% / 3mo)
- 18.10 Full Bloomberg question index for this topic (50 questions)

## Part 19 - Strings and Parsing

*Tokenising, comparing and transforming text - plus the pattern-matching classics.*

65 Bloomberg-tagged questions: 10 Tier A, 55 Tier B.

- 19.0 Pattern primer
    - Python string costs: immutability, slicing, join vs +=
    - Palindromes: two-pointer, expand-around-centre, DP
    - Anagram signatures (sorted key vs count key)
    - Parsing: tokenising, nesting, and recursive descent (decode string, calculator)
    - Substring search: naive, KMP, Rabin-Karp
    - Encoding/decoding and run-length compression
    - Word-splitting with a dictionary (trie + DP)

- 19.1 [E] Ransom Note  (62% / 30d)
- 19.2 [E] Maximum Number of Balloons  (62% / 30d)
- 19.3 [E] Roman to Integer  (50% / 3mo)
- 19.4 [M] String to Integer (atoi)  (50% / 3mo)
- 19.5 [E] Remove Letter To Equalize Frequency  (38% / 3mo)
- 19.6 [E] Furthest Point From Origin  (62% / 3mo)
- 19.7 [E] Length of Last Word  (38% / 3mo)
- 19.8 [E] Isomorphic Strings  (38% / 3mo)
- 19.9 [E] Rotate String  (50% / 3mo)
- 19.10 [M] Bulls and Cows  (38% / 3mo)
- 19.11 Full Bloomberg question index for this topic (65 questions)

## Part 20 - Data Structure Design

*Compose two structures so every operation hits its target complexity.*

45 Bloomberg-tagged questions: 9 Tier A, 36 Tier B.

- 20.0 Pattern primer
    - The design-round recipe: list operations, target complexity, pick structures
    - Hash map + doubly linked list (LRU) and hash map + array (O(1) random)
    - Hash map + heap, and the lazy-deletion pattern
    - Time-indexed stores and binary search over timestamps
    - Iterators, streams and lazy evaluation
    - Thread-safety and what to say if asked
    - Writing clean class APIs under time pressure

- 20.1 [M] Design Underground System  (75% / 30d)
- 20.2 [M] Insert Delete GetRandom O(1)  (62% / 3mo)
- 20.3 [M] LRU Cache  (50% / 3mo)
- 20.4 [M] Min Stack  (38% / 3mo)
- 20.5 [E] Number of Recent Calls  (50% / 3mo)
- 20.6 [M] Design A Leaderboard [premium]  (38% / 3mo)
- 20.7 [H] Find Median from Data Stream  (38% / 3mo)
- 20.8 [M] Time Based Key-Value Store  (38% / 3mo)
- 20.9 [E] Design an Ordered Stream  (62% / 6mo)
- 20.10 Full Bloomberg question index for this topic (45 questions)

## Part 21 - Concurrency and Python Internals

*The things Bloomberg asks after the algorithm: how does this actually run.*

2 Bloomberg-tagged questions: 0 Tier A, 2 Tier B.

- 21.0 Pattern primer
    - How dict and set really work (hashing, probing, resize) - a frequent follow-up
    - Mutable default arguments, shallow vs deep copy, identity vs equality
    - GIL, threads vs processes vs asyncio
    - Locks, semaphores, condition variables, producer-consumer
    - Generators and memory-bounded stream processing
    - Reference counting, garbage collection, and __slots__

- 21.1 Full Bloomberg question index for this topic (2 questions)

## Part 22 - SQL, Shell and Language-Specific (secondary track)

*Not the new-grad coding round, but tagged for Bloomberg and worth a weekend.*

81 Bloomberg-tagged questions: 8 Tier A, 73 Tier B.

- 22.0 Pattern primer
    - SELECT, JOIN types, and what an interviewer means by 'the second highest'
    - GROUP BY, HAVING, and aggregate gotchas with NULL
    - Window functions: ROW_NUMBER, RANK, DENSE_RANK, LAG/LEAD
    - Self joins and correlated subqueries
    - Writing a query that reads like the question
    - The JavaScript and pandas tagged problems - skim only unless the role asks

- 22.1 [E] Combine Two Tables  (50% / 3mo)
- 22.2 [M] Second Highest Salary  (50% / 3mo)
- 22.3 [E] Duplicate Emails  (50% / 3mo)
- 22.4 [E] Big Countries  (38% / 3mo)
- 22.5 [E] Students and Examinations  (38% / 3mo)
- 22.6 [E] Recyclable and Low Fat Products  (50% / 3mo)
- 22.7 [M] Product Sales Analysis III  (38% / 3mo)
- 22.8 [E] Create Hello World Function  (50% / 6mo)
- 22.9 Full Bloomberg question index for this topic (81 questions)

## Part 23 - Bloomberg Real Interview Bank  [bl]

Questions reported from actual Oct-Dec 2025 rounds. Ordered by how many
separate candidates reported them - the repeat rate is the signal.

- 23.1 [bl] Invalid / potentially fraudulent transactions  (6 reports, R1/R2)
- 23.2 [bl] Collatz steps (3n+1) with memoisation  (6 reports, R1)
- 23.3 [bl] Design Underground System  (6 reports, R1/R2)
- 23.4 [bl] Desert grid with fuel: can the car reach the oasis  (5 reports, R1/R2)
- 23.5 [bl] Repeatedly remove 3+ consecutive identical characters  (4 reports, R1/R2)
- 23.6 [bl] Lottery system: add / remove / draw in O(1)  (4 reports, R1/R2)
- 23.7 [bl] Print all paths between two nodes / flight routes  (4 reports, R1/R2)
- 23.8 [bl] Highway CCTV: record vehicles, top-N brands in a time range  (3 reports, R2)
- 23.9 [bl] Min Stack with top-k minimums  (2 reports, R1)
- 23.10 [bl] Sort words by a custom (multi-character) alphabet  (1 report, R1)
- 23.11 [bl] Browser history: print most-recent-first, deduplicated  (1 report, R1)
- 23.12 [bl] Autocomplete: recommend the next word by frequency  (1 report, R2 (internship))
- 23.13 [bl] Find the process that caused a cascade of aborts  (1 report, R1)
- 23.14 [bl] Can a customer trade during the whole order window  (1 report, R1)
- 23.15 [bl] Tsunami: submerge islands not touching the border  (1 report, R1)
- 23.16 [bl] Count unique index pairs summing to a target  (1 report, R1)
- 23.17 [bl] Two Sum by difference, and how hashing works  (1 report, R1)
- 23.18 [bl] Two City Scheduling with an odd number of people  (1 report, R1)
- 23.19 [bl] Chess board: add a bishop only if no bishop attacks that cell  (1 report, R1)
- 23.20 [bl] Split a string into dictionary words  (1 report, R1)
- 23.21 [bl] Characters in the first string but not the second  (1 report, R2)
- 23.22 [bl] Anagram file ingestion tool, turned into a service  (1 report, R3)
- 23.23 [bl] App Store class redesign (OOP / low-level design round)  (1 report, R3)
- 23.24 [bl] Number of Ships in a Rectangle  (1 report, R1)
- 23.25 [bl] Song recommendation system  (1 report, R1)
- 23.26 [bl] Integer to Roman (1 to 4000)  (1 report, R1)

## Part 24 - OOP and Low-Level Design

*Bloomberg sometimes replaces the distributed-design round with a class-design round in an editor.*

- 24.1 The LLD round: requirements -> entities -> relationships -> API -> code
- 24.2 SOLID in practice, with the refactor each principle implies
- 24.3 The design patterns that come up: strategy, observer, factory, adapter, singleton, decorator
- 24.4 Indexing and denormalisation inside an object model (the App Store question)
- 24.5 Backward-compatible refactoring: keeping an interface while changing storage
- 24.6 Worked: parking lot, elevator, deck of cards, rate limiter, order book
- 24.7 Worked: the App Store question, end to end

## Part 25 - Mock Interview Plan and Spaced Repetition

- 25.1 The 8-week schedule, week by week
- 25.2 Daily loop: 1 new pattern problem + 2 review + 1 timed
- 25.3 Timed mock protocol (45 minutes, talking out loud, no IDE help)
- 25.4 Review log and the 'problems I got wrong' list
- 25.5 The week before: what to do and what to stop doing

## Part 26 - Resources

- 26.1 The source lists and how to regenerate them
- 26.2 Behavioural prep: the questions this loop actually asks
- 26.3 Cross-reference to the system design course

### System design rounds reported in the same chat

Full notes live in `../system-design/` (Part 10). Listed here for cross-reference:

- Custom index (repeated - the single most common Bloomberg design question)
- Top-K / Top-100 most popular news in the past 8 hours
- Note-taking app: create/view/edit/delete, sharing with access levels, offline sync, large files, in-app notification when shared (essentially Dropbox)
- Mobile video app: download videos and resume from where you stopped, no streaming
- Market data: real-time view, data over a defined time range, analytics
- Portfolio system: buy/sell stocks and view history over a period
- Indexed data distribution service: subscribe by index_id, choose columns and format (JSON/CSV/XML), triggered by a daily calculation service
- Bloomberg Terminal subsystem consuming London Stock Exchange data: subscribe to stocks, real-time updates, historical range queries, statistics and analytics
