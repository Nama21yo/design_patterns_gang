"""Real Bloomberg interview questions reported by candidates, Oct 2025 - Dec 2025.

Source: an exported group chat of candidates going through the Bloomberg new-grad /
internship loop. These are the questions that were ACTUALLY asked, with the follow-ups
the interviewers actually used. Prompts are kept close to verbatim - that wording is
itself a study aid, because the interviewers phrase things loosely on purpose.

Each entry:
  slug        stable id, used for the Notion page and the notes/ filename
  title       page title
  dates       reported dates (all 2025 unless stated)
  rounds      which round(s) it showed up in
  reports     how many separate people reported it - the repeat-rate is the signal
  prompt      near-verbatim problem statement
  lc          related LeetCode problems (may be empty - several are not on LeetCode)
  followups   follow-ups the interviewers actually asked
  pattern     the topics.py part slug this drills
"""

BANK = [
    dict(slug="bl-fuel-grid", title="Desert grid with fuel: can the car reach the oasis",
         dates=["2025-10-08", "2025-11-04", "2025-11-05"], rounds=["R1", "R2"], reports=5,
         pattern="graphs",
         prompt=(
             "You are given a grid and two points (a starting point and an ending point) and you "
             "have a fuel amount. Check whether it is possible to reach the ending point without "
             "running out of fuel. You may only travel horizontally and vertically.\n\n"
             "A later retelling of the same question: you are on a desert given by an m x n matrix "
             "containing the characters '.', 'c' and 'o'. 'c' is your car's position and 'o' is the "
             "oasis you want to reach with the fuel you are given. Can you make it to the oasis?\n\n"
             "    [ ['.','.','c'],\n"
             "      ['.','r','r'],\n"
             "      ['.','.','o'] ]"),
         lc=[("Shortest Path in Binary Matrix", "https://leetcode.com/problems/shortest-path-in-binary-matrix/"),
             ("Shortest Path in a Grid with Obstacles Elimination", "https://leetcode.com/problems/shortest-path-in-a-grid-with-obstacles-elimination/")],
         followups=[
             "Some cells have a gas station, so you can refill the tank and continue.",
             "Only ONE gas station exists somewhere in the desert.",
             "Multiple gas stations, with edge cases around refilling on the same cell twice.",
             "Obstacles are added to the matrix, given by 'r'.",
             "What if refuelling is partial, or the station has a capacity?"]),

    dict(slug="bl-invalid-transactions", title="Invalid / potentially fraudulent transactions",
         dates=["2025-10-13", "2025-10-21", "2025-10-23", "2025-10-28"], rounds=["R1", "R2"], reports=6,
         pattern="arrays-hashing",
         prompt=(
             "Given a list of transactions, each with a trader name, amount, time and location:\n"
             "A transaction is invalid if\n"
             "  1. its amount is greater than 1000, or\n"
             "  2. it happens within 60 minutes (before OR after) of another transaction by the "
             "same person in a DIFFERENT city.\n"
             "Return all invalid transactions, sorted by time.\n\n"
             "    example_input = [\n"
             "      {'trader_name':'Matt','amount':1001,'time':10,'location':'NYSE'},\n"
             "      {'trader_name':'Matt','amount':1500,'time':1100,'location':'London SE'},\n"
             "      {'trader_name':'sss','amount':1500,'time':102,'location':'NYSE'},\n"
             "      {'trader_name':'Matt','amount':1050,'time':1003,'location':'London SE'}]"),
         lc=[("Invalid Transactions", "https://leetcode.com/problems/invalid-transactions/")],
         followups=[
             "The interviewer specifically wanted the O(n) solution, not the O(n^2) pairwise scan.",
             "Read carefully: some interviewers only want you to compare against the PREVIOUS and "
             "NEXT transaction of the same name, which is NOT the LeetCode 1169 semantics.",
             "Input arrives as a CSV file - parse it first.",
             "What if the transactions are not sorted by time?",
             "What if this is a stream and you cannot hold all transactions in memory?"]),

    dict(slug="bl-collatz", title="Collatz steps (3n+1) with memoisation",
         dates=["2025-10-09", "2025-10-17", "2025-10-20", "2025-10-28", "2025-11-10"], rounds=["R1"], reports=6,
         pattern="dp",
         prompt=(
             "If x is even then x = x / 2. If x is odd then x = 3 * x + 1.\n"
             "Calculate the number of steps taken to reach 1.\n"
             "For example x = 3 takes 7 steps (3 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1)."),
         lc=[("Sort Integers by The Power Value", "https://leetcode.com/problems/sort-integers-by-the-power-value/")],
         followups=[
             "What are the drawbacks of the recursive solution? Convert it to iterative "
             "(one interviewer FORCED the iterative version).",
             "How would you optimise it if there are multiple calls? (memoise)",
             "Store every number reached along the way, not just the input: for 10 -> 5 -> 16 -> 8 "
             "-> 4 -> 2 -> 1 the cache should end up {10:6, 5:4, 16:7, 8:3, 4:2, 2:1, 1:0}.",
             "Wrap it as Sort Integers by The Power Value: sort a range by step count, tie-break by value.",
             "Is termination guaranteed? (open problem - say so, it is a good signal)"]),

    dict(slug="bl-underground-system", title="Design Underground System",
         dates=["2025-10-23", "2025-10-28", "2025-11-06", "2025-11-18"], rounds=["R1", "R2"], reports=6,
         pattern="design",
         prompt=(
             "Implement an underground railway system that tracks customer travel times between "
             "stations: checkIn(id, stationName, t), checkOut(id, stationName, t), and "
             "getAverageTime(startStation, endStation) returning the average travel time for all "
             "customers who travelled from start to end."),
         lc=[("Design Underground System", "https://leetcode.com/problems/design-underground-system/")],
         followups=[
             "Give the edge cases (asked repeatedly, in almost every report).",
             "A person checks in today, skips the checkout, and checks out the next morning - "
             "how do you handle it?",
             "Intervals that cross midnight, e.g. 22:00 - 02:00.",
             "What if a customer checks in twice without checking out?",
             "How would you expire stale check-ins?",
             "Make getAverageTime O(1)."]),

    dict(slug="bl-cctv-top-n", title="Highway CCTV: record vehicles, top-N brands in a time range",
         dates=["2025-10-22", "2025-10-30"], rounds=["R2"], reports=3,
         pattern="heap",
         prompt=(
             "Implement a module for a CCTV camera by a highway. It logs traffic events (a car "
             "passes by) and provides aggregate on-demand statistics about the traffic so far.\n\n"
             "  record(brand)               - log the brand of a vehicle passing under the camera\n"
             "  printStatistics(n, start_time, end_time)\n"
             "        - print the top n most frequently detected brands in [start_time, end_time]\n"
             "          together with their counts.\n\n"
             "E.g. if between 9:00 and 10:00 there were 500 Sedans, 5 motorcycles, 200 SUVs and "
             "50 trucks, then for N=2 the output is 'Sedan: 500' then 'SUV: 200'."),
         lc=[("Top K Frequent Elements", "https://leetcode.com/problems/top-k-frequent-elements/"),
             ("Design Hit Counter", "https://leetcode.com/problems/design-hit-counter/")],
         followups=[
             "Use a min-heap to get the top N instead of sorting the whole frequency list.",
             "Use binary search (bisect_left / bisect_right) to find the time range instead of scanning.",
             "How can you guarantee binary search is valid? (events arrive sequentially, so the "
             "list is already sorted by time - say this explicitly)",
             "What if the log does not fit in memory?",
             "What if you need statistics continuously, not on demand?"]),

    dict(slug="bl-remove-three-consecutive", title="Repeatedly remove 3+ consecutive identical characters",
         dates=["2025-10-18", "2025-10-29", "2025-10-30"], rounds=["R1", "R2"], reports=4,
         pattern="stack-queue",
         prompt=(
             "You are given a string s. Repeatedly remove any substring that contains three or "
             "more consecutive identical characters. After each removal the remaining parts are "
             "concatenated and the process continues until no such substring exists. Return the "
             "final string.\n\n"
             "  s = 'aabbbbc'  -> 'aac'\n"
             "  s = 'aabbbbac' -> 'c'"),
         lc=[("Remove All Adjacent Duplicates in String II", "https://leetcode.com/problems/remove-all-adjacent-duplicates-in-string-ii/")],
         followups=[
             "What if we can start at any index instead of scanning left to right? "
             "e.g. s = 'aaabbbbaa' -> ''  (does the answer depend on the order of removals?)",
             "What if the threshold k is a parameter instead of 3?",
             "Can you do it in one pass without rebuilding the string each time?"]),

    dict(slug="bl-lottery-system", title="Lottery system: add / remove / draw in O(1)",
         dates=["2025-10-28", "2025-11-10", "2025-11-26"], rounds=["R1", "R2"], reports=4,
         pattern="design",
         prompt=(
             "Implement a lottery system with three functions:\n"
             "  addParticipant(name)\n"
             "  removeParticipant(name)\n"
             "  pick() / draw()  - return a uniformly random participant\n"
             "Each must be O(1) on average."),
         lc=[("Insert Delete GetRandom O(1)", "https://leetcode.com/problems/insert-delete-getrandom-o1/"),
             ("Insert Delete GetRandom O(1) - Duplicates allowed", "https://leetcode.com/problems/insert-delete-getrandom-o1-duplicates-allowed/")],
         followups=[
             "What if there are duplicate names?",
             "How can you increase a participant's chance of being selected based on their "
             "frequency (weighted random)?",
             "How would you do weighted sampling if weights are arbitrary floats?",
             "How does random.choice actually pick uniformly?"]),

    dict(slug="bl-min-stack", title="Min Stack with top-k minimums",
         dates=["2025-10-20", "2025-11-07"], rounds=["R1"], reports=2,
         pattern="stack-queue",
         prompt=(
             "Design a stack that supports push, pop, top and retrieving the minimum element in "
             "constant time."),
         lc=[("Min Stack", "https://leetcode.com/problems/min-stack/")],
         followups=[
             "Add a function that returns the top k minimums, optimally.",
             "What if there are duplicates?",
             "What happens if you use `raise` instead of `return` on an empty stack? "
             "(a Python-semantics probe - know your exception types)",
             "Can you do it with O(1) extra space instead of a second stack?"]),

    dict(slug="bl-all-paths", title="Print all paths between two nodes / flight routes",
         dates=["2025-10-17", "2025-10-22"], rounds=["R1", "R2"], reports=4,
         pattern="backtracking",
         prompt=(
             "Design a class to represent direct flight routes between cities:\n"
             "  addRoute(start, destination)      - add a direct route\n"
             "  printAllRoutes(start, destination) - print ALL possible routes\n\n"
             "  addRoute('A','B'); addRoute('A','C'); addRoute('B','D'); addRoute('C','D')\n"
             "  printAllRoutes('A','D') -> [[A,B,D], [A,C,D]]\n\n"
             "A variant given as a plain graph DFS:\n"
             "  A->B, B->A, A->C, C->A, A->D, D->A, B->C, C->B, B->D, D->B\n"
             "  print_all_paths(C, D) -> C,A,B,D / C,A,D / C,B,A,D / C,B,D"),
         lc=[("All Paths From Source to Target", "https://leetcode.com/problems/all-paths-from-source-to-target/"),
             ("Find if Path Exists in Graph", "https://leetcode.com/problems/find-if-path-exists-in-graph/")],
         followups=[
             "The graph has cycles - the visited set must be per-path, not global.",
             "What if no route exists? (return a message, not an empty list - read the spec)",
             "Shortest route instead of all routes.",
             "What if the graph is huge - would you still enumerate all paths?",
             "Add a layover/hop limit."]),

    dict(slug="bl-welsh-dictionary", title="Sort words by a custom (multi-character) alphabet",
         dates=["2025-10-10"], rounds=["R1"], reports=1,
         pattern="sorting",
         prompt=(
             "There is a Welsh dictionary whose alphabet is\n"
             "  ['a','b','c','ch','d','dd','e','f','ff','g','ng','h','i','l','ll','m','n','o',\n"
             "   'p','ph','r','rhe','s','t','th','u','w','y']\n"
             "Characters are either a single English character or a double one. When you tokenise "
             "a word, give priority to the LONGER characters: in 'ddb' the letters are 'dd' and 'b', "
             "not 'd','d','b'.\n"
             "Given a list of words, e.g. ['ddr','nah','dea','dd','ngah'], sort them by this "
             "alphabet and return the sorted list."),
         lc=[("Verifying an Alien Dictionary", "https://leetcode.com/problems/verifying-an-alien-dictionary/"),
             ("Alien Dictionary", "https://leetcode.com/problems/alien-dictionary/")],
         followups=[
             "What if the alphabet has letters longer than two characters, e.g. 'beeee', 'phe', 'rhe'? "
             "(greedy longest-match tokenisation, or a trie over the alphabet)",
             "What if a word contains a character not in the alphabet?",
             "Can you avoid re-tokenising a word on every comparison? (decorate-sort-undecorate)"]),

    dict(slug="bl-browser-history", title="Browser history: print most-recent-first, deduplicated",
         dates=["2025-10-14"], rounds=["R1"], reports=1,
         pattern="design",
         prompt=(
             "Whenever you visit a website you save it in your History. When asked for the history "
             "you print it from most recently visited to least recently visited.\n\n"
             "  visits: bbc.com, bloomberg.com, msn.com, bloomberg.com\n"
             "  history: bloomberg.com, msn.com, bbc.com\n\n"
             "For duplicates you print only the most recent occurrence. It is like an LRU cache, "
             "but with no size limit."),
         lc=[("LRU Cache", "https://leetcode.com/problems/lru-cache/"),
             ("Design Browser History", "https://leetcode.com/problems/design-browser-history/")],
         followups=[
             "Now add a capacity - it becomes a true LRU.",
             "Support back() and forward().",
             "Support search by prefix over the history (trie).",
             "How would you persist this across sessions?"]),

    dict(slug="bl-autocomplete-next-word", title="Autocomplete: recommend the next word by frequency",
         dates=["2025-10-17"], rounds=["R2 (internship)"], reports=1,
         pattern="trie",
         prompt=(
             "Design an autocomplete system. You are given raw data such as\n"
             "  data = [['i','am','lost'], ['lost','i','am'], ['i','gain','weight']]\n"
             "Train a model so that when the user types one word you recommend the next one, "
             "choosing the highest-frequency successor. For 'i' the successors are (am,2) and "
             "(gain,1), so you recommend 'am'."),
         lc=[("Design Search Autocomplete System", "https://leetcode.com/problems/design-search-autocomplete-system/")],
         followups=[
             "Recommend the top-k successors rather than one.",
             "Extend to n-grams (condition on the last two words).",
             "Prefix autocomplete rather than next-word (trie with cached top-k per node).",
             "How do you update the model online as new sentences arrive?",
             "The interviewer spent most of the time on the SYSTEM, not the code - be ready to "
             "talk storage, training and serving."]),

    dict(slug="bl-process-abort", title="Find the process that caused a cascade of aborts",
         dates=["2025-11-04"], rounds=["R1"], reports=1,
         pattern="graphs",
         prompt=(
             "Assume an operating system. Processes can have children, grandchildren and so on. "
             "Every process has a parent except one root process. A process knows its children but "
             "NOT its parent. When a process is aborted all of its descendants are aborted with it. "
             "A log records every aborted process. Find the initial process that caused all the "
             "aborts.\n\n"
             "  log = [{id:1, children:[2,3]}, {id:2, children:[4]}, {id:3, children:[]}, "
             "{id:4, children:[]}]\n"
             "  answer = 1"),
         lc=[("Find the Town Judge", "https://leetcode.com/problems/find-the-town-judge/"),
             ("Minimum Number of Vertices to Reach All Nodes", "https://leetcode.com/problems/minimum-number-of-vertices-to-reach-all-nodes/")],
         followups=[
             "What if a process has multiple parents, or there are cycles? Return None / stop the "
             "computation.",
             "What if several independent roots aborted? Return all of them.",
             "What if the log is incomplete?"]),

    dict(slug="bl-bank-trading-hours", title="Can a customer trade during the whole order window",
         dates=["2025-10-20"], rounds=["R1"], reports=1,
         pattern="intervals",
         prompt=(
             "Your trading platform aggregates multiple banks, each with its own trading hours. "
             "Customers can place trades anytime during the day, but trades can only be executed "
             "when AT LEAST ONE bank is open. Given the operating hours of the banks, verify "
             "whether a customer can trade at every minute of the given order window.\n\n"
             "  order1 = 15:00 - 20:00\n"
             "  Banks: 03:30-09:30 JP Morgan, 08:00-12:00 Bank of America, 10:00-15:00 National,\n"
             "         14:00-18:30 HSBC, 16:00-20:00 Citi, 19:00-23:00 Deutsche\n"
             "  canTrade(banks, order1) = True"),
         lc=[("Merge Intervals", "https://leetcode.com/problems/merge-intervals/")],
         followups=[
             "The reported failure mode: the candidate read 'at least one bank open' as 'one single "
             "bank covers the whole window'. Restate the requirement back to the interviewer.",
             "Many orders against the same bank set - preprocess once, answer each in O(log n).",
             "Banks whose hours wrap past midnight.",
             "Return the gaps where trading is impossible, not just a boolean."]),

    dict(slug="bl-tsunami-islands", title="Tsunami: submerge islands not touching the border",
         dates=["2025-10-20"], rounds=["R1"], reports=1,
         pattern="graphs",
         prompt=(
             "You are given a 2D binary array representing land (1) and water (0). A tsunami has "
             "occurred and all islands that are completely surrounded by water will be submerged. "
             "Return the map after the tsunami. (Islands touching the border survive.)"),
         lc=[("Number of Closed Islands", "https://leetcode.com/problems/number-of-closed-islands/"),
             ("Surrounded Regions", "https://leetcode.com/problems/surrounded-regions/")],
         followups=[
             "Do it in place.",
             "What if the map wraps horizontally (a cylinder) or in both directions (a torus)?",
             "Count the submerged islands as well as returning the map.",
             "Diagonal connectivity instead of 4-directional."]),

    dict(slug="bl-count-pairs-target", title="Count unique index pairs summing to a target",
         dates=["2025-10-20"], rounds=["R1"], reports=1,
         pattern="arrays-hashing",
         prompt=(
             "Given an array of numbers and a target, count the number of unique pairs that sum to "
             "the target, where uniqueness is by INDEX.\n"
             "  arr = [0,1,2,3,4,5,5], target = 5  ->  4   (indices (0,5),(0,6),(1,4),(2,3))"),
         lc=[("Two Sum", "https://leetcode.com/problems/two-sum/"),
             ("Count Number of Pairs With Absolute Difference K", "https://leetcode.com/problems/count-number-of-pairs-with-absolute-difference-k/")],
         followups=[
             "Unique by VALUE instead of by index - how does the answer change?",
             "Count pairs whose DIFFERENCE is the target (asked separately, see bl-two-sum-difference).",
             "Count triplets instead of pairs.",
             "How does hashing work in a Python set and dict? (asked verbatim)"]),

    dict(slug="bl-two-sum-difference", title="Two Sum by difference, and how hashing works",
         dates=["2025-10-31"], rounds=["R1"], reports=1,
         pattern="arrays-hashing",
         prompt=(
             "Two Sum, but instead of a sum find two numbers whose DIFFERENCE equals the target."),
         lc=[("Two Sum", "https://leetcode.com/problems/two-sum/"),
             ("Find K-Diff Pairs in an Array", "https://leetcode.com/problems/k-diff-pairs-in-an-array/")],
         followups=[
             "Does reordering the array matter? (it does - a - b != b - a)",
             "How does hashing work in a set and a hash map? (collisions, load factor, resize)",
             "What if the array is already sorted? (two pointers, O(1) space)",
             "What about duplicates and target = 0?"]),

    dict(slug="bl-two-city-scheduling", title="Two City Scheduling with an odd number of people",
         dates=["2025-10-17"], rounds=["R1"], reports=1,
         pattern="greedy",
         prompt=(
             "There are two cities NY and SF and we want to send n participants to the two cities. "
             "Both cities have a capacity of half the total. The cost of flying one person is given "
             "as (costNY, costSF). What is the minimum cost to fly all participants?"),
         lc=[("Two City Scheduling", "https://leetcode.com/problems/two-city-scheduling/")],
         followups=[
             "The number of people may be ODD, and the interviewer will not mention it - you have "
             "to ask. One city then gets half + 1, and the middle person after sorting must be checked.",
             "Prove the greedy (exchange argument on the cost difference).",
             "Arbitrary capacities rather than half/half (min-cost flow or DP).",
             "More than two cities."]),

    dict(slug="bl-bishop-board", title="Chess board: add a bishop only if no bishop attacks that cell",
         dates=["2025-11-18"], rounds=["R1"], reports=1,
         pattern="matrix",
         prompt=(
             "You are given a chess board and add_bishop(row, col) is called on it. You add a bishop "
             "on that cell, but you must return False if there is already another bishop along "
             "either of the two diagonals passing through that cell."),
         lc=[("N-Queens", "https://leetcode.com/problems/n-queens/")],
         followups=[
             "Instead of returning a boolean, return the cell of the existing bishop.",
             "Make add_bishop O(1) (index by the two diagonal keys r+c and r-c).",
             "Support remove_bishop.",
             "Extend to rooks and queens."]),

    dict(slug="bl-word-break-sentence", title="Split a string into dictionary words",
         dates=["2025-11-26"], rounds=["R1"], reports=1,
         pattern="dp",
         prompt=(
             "  input1 = 'bloombergisfun'\n"
             "  input2 = ['bloom','bloomberg','is','fun']\n"
             "Split input1 with spaces so that every word exists in input2, and return the sentence.\n"
             "  answer = 'bloomberg is fun'"),
         lc=[("Word Break", "https://leetcode.com/problems/word-break/"),
             ("Word Break II", "https://leetcode.com/problems/word-break-ii/")],
         followups=[
             "Return ALL valid sentences, not just one.",
             "The dictionary is huge - use a trie instead of a set.",
             "Prefer the segmentation with the fewest words, or with the longest first word.",
             "What if no valid segmentation exists?"]),

    dict(slug="bl-chars-in-first-not-second", title="Characters in the first string but not the second",
         dates=["2025-10-30"], rounds=["R2"], reports=1,
         pattern="strings",
         prompt=(
             "Given two strings first and second, return the characters that appear in first but "
             "do not appear in second.\n"
             "  first = 'abcdef', second = 'bdf' -> 'ace'"),
         lc=[("Find the Difference", "https://leetcode.com/problems/find-the-difference/"),
             ("Minimum Number of Steps to Make Two Strings Anagram", "https://leetcode.com/problems/minimum-number-of-steps-to-make-two-strings-anagram/")],
         followups=[
             "What about multiplicities - is 'aab' vs 'ab' leaving 'a'?",
             "Preserve the order of first, or return sorted?",
             "Unicode rather than lowercase ASCII - does your 26-slot array still work?",
             "Do it with O(1) extra space using a bitmask."]),

    dict(slug="bl-anagram-file-service", title="Anagram file ingestion tool, turned into a service",
         dates=["2025-11-05"], rounds=["R3"], reports=1,
         pattern="strings",
         prompt=(
             "An analyst has written a tool that helps with a step in a data ingestion pipeline. "
             "It has greatly increased their productivity and they have been sharing it around. "
             "You, as a Bloomberg engineer, have been asked to formalise this tool into a service. "
             "(The interviewer plays your colleague and mentor on the team.)\n\n"
             "Data files arrive by email from many external providers, as text files with one word "
             "per line and anagrams grouped onto consecutive lines. The file name is a unique "
             "provider id plus a date, e.g. GS1234.20230525.txt. If the content is not correct an "
             "error alert email goes to the data analysts, who repair the file and give feedback to "
             "the provider. Corrected files land in a network folder monitored by the pipeline. "
             "Files vary in size and priority. Throughput is limited by the number of analysts and "
             "the backlog is growing fast.\n\n"
             "The analyst's tool takes a file of words, one per line, and writes a file where "
             "anagrams are grouped on consecutive lines. Their logic: read each line, hash it to a "
             "key, append to a hashmap of key -> list of words, then write every list out.\n\n"
             "    C:> python convertfile.py in.txt out.txt\n"
             "    C:> cp out.txt z:\\next_stage\\input_files\\"),
         lc=[("Group Anagrams", "https://leetcode.com/problems/group-anagrams/")],
         followups=[
             "What IS the hash key? (sorted letters, or a 26-count tuple - and the trade-off)",
             "Find the bug/limitation in the analyst's pseudocode.",
             "Memory: the file does not fit in RAM. Stream it, or shard by key.",
             "Priorities and varying file sizes - this becomes a work queue design question.",
             "Validation, error alerting, and feedback to the provider.",
             "This is a hybrid coding + design + 'work with a colleague' round - narrate constantly."]),

    dict(slug="bl-appstore-ood", title="App Store class redesign (OOP / low-level design round)",
         dates=["2025-11-21"], rounds=["R3"], reports=1,
         pattern="design",
         prompt=(
             "You have an AppStore where applications are listed, like Google Play or the App Store. "
             "It works fine today, but as the user base grew its performance started degrading. "
             "Find the bottleneck in the class design and improve it. There are also new features to "
             "implement. The interface must stay backward compatible, because many users rely on the "
             "current architecture.\n\n"
             "  class AppEntry:  app_id, app_name, publisher_id, publisher_name  (+ getters/setters)\n"
             "  class AppStore:  inventory = {app_id: AppEntry}                  (+ getters/setters)\n\n"
             "The bottleneck: AppStore.get_publisher_name(pub_id) scans every app in the inventory. "
             "AppEntry.get_publisher_name() is the method that causes the design trouble.\n\n"
             "New functionality to add:\n"
             "  get_all_published_app(pub_id) - all apps by a publisher\n"
             "  rename_publisher(pub_id, new_name)"),
         lc=[],
         followups=[
             "Normalise: a Publisher object, referenced by id, so rename is O(1) instead of O(n).",
             "Add secondary indexes: publisher_id -> set of app_ids.",
             "Keep AppEntry.get_publisher_name() working by delegating to the Publisher - backward "
             "compatibility without duplicated state.",
             "Thread safety if the store is shared.",
             "This round is NOT the usual distributed system design round - expect to write classes "
             "in an editor."]),

    dict(slug="bl-ships-in-rectangle", title="Number of Ships in a Rectangle",
         dates=["2025-10-24"], rounds=["R1"], reports=1,
         pattern="backtracking",
         prompt=(
             "You have a rectangle on a 2D plane and an API hasShips(topRight, bottomLeft) that "
             "returns True if there is at least one ship in that rectangle. Count the ships in the "
             "given rectangle with at most 400 API calls."),
         lc=[("Number of Ships in a Rectangle", "https://leetcode.ca/2019-05-27-1274-Number-of-Ships-in-a-Rectangle/")],
         followups=[
             "Why is divide and conquer bounded by the API call budget?",
             "What if ships could be at non-integer coordinates?",
             "Generalise to 3D."]),

    dict(slug="bl-song-recommendation", title="Song recommendation system",
         dates=["2025-12-12"], rounds=["R1"], reports=1,
         pattern="heap",
         prompt=(
             "A song recommendation problem: given users' listening histories, recommend songs. "
             "(Reported via a LeetCode discuss post; treat it as a design-flavoured coding question "
             "about co-occurrence counting and top-k selection.)"),
         lc=[],
         followups=[
             "Top-k recommendations per user.",
             "How do you break ties?",
             "How does this scale to millions of users?",
             "Cold start for a new user."]),

    dict(slug="bl-roman-numerals", title="Integer to Roman (1 to 4000)",
         dates=["2025-11-10"], rounds=["R1"], reports=1,
         pattern="math",
         prompt="Convert a number from 1 to 4000 into Roman numerals.",
         lc=[("Integer to Roman", "https://leetcode.com/problems/integer-to-roman/"),
             ("Roman to Integer", "https://leetcode.com/problems/roman-to-integer/")],
         followups=[
             "Roman to integer (the reverse).",
             "Validate a Roman numeral string.",
             "Why does the greedy value table work, and why does it need the subtractive pairs?"]),
]

# Questions asked as plain LeetCode problems in real rounds - these get their notes under the
# pattern Parts, but are flagged here so the "reported" list stays complete.
REPORTED_LEETCODE = [
    ("palindrome-number", "R1", ["2025-10-08"]),
    ("longest-substring-without-repeating-characters", "R2", ["2025-11-06", "2025-11-26"]),
    ("meeting-rooms-ii", "R2", ["2025-11-03"]),
    ("decode-string", "R1", ["2025-11-06"]),
    ("minimum-number-of-steps-to-make-two-strings-anagram", "R1", ["2025-11-08"]),
    ("word-search", "R1", ["2025-11-13"]),
    ("number-of-islands", "R1", ["2025-11-28"]),
    ("remove-letter-to-equalize-frequency", "R1", ["2025-10-21"]),
    ("merge-intervals", "R1", ["2025-10-20"]),
    ("insert-delete-getrandom-o1", "R2", ["2025-10-28"]),
    ("min-stack", "R1", ["2025-10-20", "2025-11-07"]),
    ("two-sum", "R1", ["2025-10-31"]),
    ("sort-integers-by-the-power-value", "R1", ["2025-10-09"]),
    ("invalid-transactions", "R1", ["2025-10-13", "2025-10-21", "2025-10-23"]),
    ("design-underground-system", "R2", ["2025-10-23", "2025-10-28", "2025-11-06", "2025-11-18"]),
    ("two-city-scheduling", "R1", ["2025-10-17"]),
]

# System design rounds reported in the same chat. Full notes live in ../system-design;
# listed here so the DSA course cross-references the right page.
SYSTEM_DESIGN_ROUNDS = [
    "Custom index (repeated - the single most common Bloomberg design question)",
    "Top-K / Top-100 most popular news in the past 8 hours",
    "Note-taking app: create/view/edit/delete, sharing with access levels, offline sync, "
    "large files, in-app notification when shared (essentially Dropbox)",
    "Mobile video app: download videos and resume from where you stopped, no streaming",
    "Market data: real-time view, data over a defined time range, analytics",
    "Portfolio system: buy/sell stocks and view history over a period",
    "Indexed data distribution service: subscribe by index_id, choose columns and format "
    "(JSON/CSV/XML), triggered by a daily calculation service",
    "Bloomberg Terminal subsystem consuming London Stock Exchange data: subscribe to stocks, "
    "real-time updates, historical range queries, statistics and analytics",
]
