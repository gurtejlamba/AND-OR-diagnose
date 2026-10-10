# 100 Viva Questions — AI Device Troubleshooting with AO*

---

## Section A — Basics of AI and Problem Solving (Q1–15)

**Q1. What is Artificial Intelligence?**
A. AI is the branch of computer science that designs systems capable of performing tasks that normally require human intelligence, such as reasoning, learning, problem-solving, and decision-making.

**Q2. What is a search problem in AI?**
A. A search problem consists of an initial state, a set of possible actions, a goal test, and a path/step cost function. The goal is to find a sequence of actions (a path) leading from the initial state to a goal state.

**Q3. What is a state space?**
A. The state space is the set of all possible states reachable from the initial state by applying any sequence of actions. It is typically represented as a graph.

**Q4. What is the difference between uninformed and informed search?**
A. Uninformed (blind) search algorithms (BFS, DFS, UCS) use no problem-specific knowledge beyond the problem definition. Informed (heuristic) search algorithms (A\*, AO\*) use a heuristic function `h(n)` to estimate the cost from a node to the goal, guiding the search more efficiently.

**Q5. What is a heuristic function?**
A. A heuristic function `h(n)` is an estimate of the cost from node `n` to the nearest goal. It is computed from information about the problem domain without exploring the state space.

**Q6. What makes a heuristic admissible?**
A. A heuristic is admissible if it never overestimates the true cost to reach the goal — i.e., `h(n) ≤ h*(n)` for all nodes `n`, where `h*(n)` is the true optimal cost.

**Q7. What is the difference between optimality and completeness in search?**
A. **Completeness** means the algorithm is guaranteed to find a solution if one exists. **Optimality** means it finds the lowest-cost solution. An algorithm can be complete but not optimal (e.g., DFS).

**Q8. What is a cost function in the context of repair?**
A. In device troubleshooting, the cost function assigns a non-negative dollar value to each repair action (LEAF node). The total cost of a repair plan is the sum of costs of all actions executed.

**Q9. What is problem decomposition?**
A. Problem decomposition is the strategy of breaking a complex problem into simpler sub-problems, solving each independently or in combination, then combining solutions. AND-OR graphs are the formal structure for this.

**Q10. How does problem decomposition apply to device troubleshooting?**
A. A device fault (e.g., "laptop won't start") is decomposed into possible causes (power, display, software, hardware). Each cause is further decomposed into specific repair actions. AO\* then searches this decomposed structure.

**Q11. What is a knowledge base in AI?**
A. A knowledge base is a structured repository of domain facts and rules. In this project, it is the collection of AND-OR graphs encoding device faults, their causes, and repair actions with costs.

**Q12. What is an expert system?**
A. An expert system is an AI program that uses a knowledge base and inference rules to solve problems in a specific domain — similar to how a human expert would reason. This project is a lightweight expert system for device repair.

**Q13. What is the difference between forward and backward chaining?**
A. Forward chaining starts from known facts and applies rules to derive new facts until the goal is reached. Backward chaining starts from the goal and works backward to find supporting facts. AO\* search is a form of backward chaining from the fault to the fix.

**Q14. What role does domain knowledge play in AO\*?**
A. Domain knowledge provides the AND-OR graph structure and the heuristic values `h(n)`. Without domain knowledge, AO\* degenerates to an uninformed search. Good heuristics make the algorithm fast and accurate.

**Q15. Why is device troubleshooting a good application for AI search?**
A. It has a well-defined problem structure (symptom → causes → fixes), quantifiable costs (repair prices), binary outcomes (fix worked / didn't work), and clear benefit from optimisation (minimising cost). All these properties make it ideal for AO\* search.

---

## Section B — AND-OR Graphs (Q16–35)

**Q16. What is an AND-OR graph?**
A. An AND-OR graph is a directed graph where each node is either an OR node (problem solved by resolving any ONE child) or an AND node (problem solved only by resolving ALL children). Leaf nodes represent base cases (solvable directly).

**Q17. What does an OR node represent in device troubleshooting?**
A. An OR node represents a fault that can be caused by any one of several sub-problems. For example, "Laptop Won't Start" is an OR node because it could be a power issue OR a display issue OR a software issue.

**Q18. What does an AND node represent in device troubleshooting?**
A. An AND node represents a diagnostic or repair procedure that requires ALL its children to be completed. For example, "Connection Diagnosis" for a printer is an AND node: you must reseat the cable AND reinstall the driver.

**Q19. What is a LEAF node?**
A. A LEAF node is a terminal node with no children. It represents an atomic, concrete repair action (e.g., "Replace Battery") with a known cost and time.

**Q20. What is a solution subgraph?**
A. A solution subgraph is a sub-tree rooted at the problem node that represents a complete, valid repair plan. For OR nodes, it includes exactly one child's subtree. For AND nodes, it includes all children's subtrees.

**Q21. How is the cost of a solution subgraph computed?**
A. It is the sum of all LEAF node costs in the subgraph. Internal node costs are heuristic estimates; only LEAFs have true costs counted in the total.

**Q22. Can AND-OR graphs have cycles?**
A. In theory yes, but in practical troubleshooting trees, the graph is a tree (acyclic). Cycles would imply circular dependencies (fix A requires fix B which requires fix A), which don't occur in hardware repair.

**Q23. What is the difference between an AND-OR graph and a standard graph?**
A. In a standard graph, every node is implicitly an OR node (we need to satisfy just one path). AND-OR graphs add AND nodes that require all children to be satisfied simultaneously, enabling richer problem structure.

**Q24. How do you represent the structure "fix A or fix B, but either way also do fix C"?**
A. Use an AND node as the root of that sub-problem, with two children: (1) an OR node {fix A, fix B} and (2) a LEAF node {fix C}. The AND forces both the choice and fix C.

**Q25. What is the branching factor of the AND-OR graph in this project?**
A. The average branching factor is 3–4 (each OR/AND node has 3–4 children). The depth is 2–3 (root → category → fix). So the total graph size is small: ~12–20 nodes per problem.

**Q26. Why is the "Laptop Won't Start" root an OR node rather than an AND node?**
A. Because the laptop fails for exactly one reason (not all reasons simultaneously). You don't need to fix the power AND the display AND the software — only one fix is usually needed. Hence OR.

**Q27. Give a real-world example of an AND node in device troubleshooting.**
A. Printer connectivity diagnosis: you must BOTH reseat the USB cable AND reinstall the printer driver to verify the connection. Neither alone is sufficient — both are required (AND).

**Q28. What happens to the solution subgraph when an OR node's best child fails?**
A. The failed child gets `f = ∞` and is excluded from future consideration. The OR node picks its next-best (second cheapest) child as the new best_child. The solution subgraph is updated accordingly.

**Q29. What happens when an AND node's child fails?**
A. The AND node immediately becomes FAILED (f = ∞) because not all required steps can be completed. Its parent (an OR node) then looks for an alternative sub-tree.

**Q30. How is depth defined for an AND-OR graph?**
A. The depth of a node is its distance from the root. In troubleshooting graphs: root at depth 0, category nodes at depth 1, repair actions (leaves) at depth 2 (or 3 for deeper trees).

**Q31. What is the difference between a proof tree and a solution subgraph?**
A. They are equivalent concepts in different contexts. A "proof tree" is used in theorem proving; a "solution subgraph" is used in search. Both represent a complete, valid decomposition from a root to base cases.

**Q32. How does the AND-OR graph encode the "try cheapest first" strategy?**
A. By assigning lower costs to cheaper repair actions. When AO\* computes `f(OR node) = min(edge + f(child))`, the minimum naturally selects the cheapest child. No explicit "sort by cost" step is needed.

**Q33. What is an edge cost in this project, and why are most edges weighted 0?**
A. Edge costs represent transition costs (e.g., diagnostic testing fees). In most cases, determining which sub-category a fault belongs to costs nothing — the user just describes the symptom. Hence edge costs are 0, and all true costs sit on LEAF nodes.

**Q34. Can the same LEAF node appear in multiple branches of the tree?**
A. In a tree structure (our implementation), no — each node has exactly one parent. In a graph (DAG) structure, yes — a repair action could apply to multiple fault categories. We use trees for simplicity.

**Q35. What is the difference between a complete solution and a partial solution in AND-OR graphs?**
A. A complete solution resolves all pending sub-problems. A partial solution is an in-progress subgraph where some AND branches are still being executed. During an interactive session, the system tracks the partial solution as steps are completed.

---

## Section C — AO\* Algorithm (Q36–60)

**Q36. Who invented AO\*, and when?**
A. AO\* was formulated by Nils Nilsson in 1980 in *Principles of Artificial Intelligence*. It was later refined by Martelli and Montanari (1978) in the context of optimising decision trees.

**Q37. What is the key difference between A\* and AO\*?**
A. A\* searches standard (OR-only) graphs and finds the minimum-cost path. AO\* searches AND-OR graphs and finds the minimum-cost solution subgraph. AO\* handles both conjunctive (AND) and disjunctive (OR) problem structures.

**Q38. What is the f(n) formula for an OR node?**
A. `f(n) = min over non-failed children c of [w(n,c) + f(c)]` where `w(n,c)` is the edge weight.

**Q39. What is the f(n) formula for an AND node?**
A. `f(n) = sum over all children c of [w(n,c) + f(c)]`  (if any child is FAILED, f(n) = ∞).

**Q40. What is the f(n) formula for a LEAF node?**
A. `f(n) = n.cost` — the actual known repair cost.

**Q41. Why is bottom-up initialisation used instead of top-down?**
A. Because f(n) for internal nodes depends on the f values of their children. Children must be computed before parents — hence post-order (bottom-up) traversal.

**Q42. What is the `best_child` of an OR node?**
A. It is the child `c` that minimises `w(n,c) + f(c)`. The OR node's solution subgraph uses only this child's sub-tree.

**Q43. What are the `best_children` of an AND node?**
A. All children — because all must be included in the solution subgraph. The AND node's f cost is the sum of all children's f costs.

**Q44. Describe the replanning procedure when a LEAF is marked FAILED.**
A. (1) Set leaf.status = FAILED, leaf.f_cost = ∞. (2) Walk up the parent chain, recomputing `_update_node(parent)` at each level. (3) OR parents automatically select the next-best child. AND parents become FAILED if any child failed. (4) Call `get_solution_path()` to extract the new plan.

**Q45. What is the time complexity of replanning?**
A. O(depth) — one `_update_node` call per ancestor. In our trees (depth ≤ 3), this is effectively O(1).

**Q46. What does `propagate_up` do in the code?**
A. It walks from a node to the root, calling `_update_node` at each ancestor. This ensures all f values and best_children pointers are consistent after a status change.

**Q47. When does AO\* terminate successfully?**
A. When `root.status == SOLVED`, meaning all required fix steps have been confirmed as successful.

**Q48. When does AO\* terminate with failure?**
A. When `root.status == FAILED`, meaning every path in the AND-OR graph has been exhausted (all alternatives failed).

**Q49. Is AO\* complete?**
A. Yes — for finite AND-OR graphs with non-negative costs, AO\* will always find a solution if one exists, or correctly determine that no solution exists.

**Q50. Is AO\* optimal?**
A. Yes — provided the heuristic `h(n)` is admissible (never overestimates). AO\* is guaranteed to find the minimum-cost solution subgraph.

**Q51. How is AO\* different from Best-First Search?**
A. Best-First Search (on standard graphs) selects the single globally-best open node. AO\* selects the best node in the **marked subgraph** (current partial solution) to expand — a more targeted strategy that respects the AND-OR structure.

**Q52. What is the "marked subgraph" in AO\*?**
A. It is the current best partial solution — the subgraph that would be the solution if all unexpanded nodes turn out to be solvable. AO\* only expands nodes in this marked subgraph.

**Q53. Why doesn't AO\* need an explicit OPEN list in our implementation?**
A. Because the entire graph is pre-built. The "expansion" in classic AO\* generates children lazily; in our system, all children are pre-assigned. We replace expansion with cost computation and path extraction.

**Q54. What would happen if h(n) = 0 for all nodes?**
A. AO\* degenerates to a form of Uniform Cost Search on AND-OR graphs. It is still correct and optimal but may explore more nodes than necessary before identifying the best solution.

**Q55. What would happen if h(n) > h*(n) for some node (inadmissible heuristic)?**
A. AO\* may return a suboptimal solution — the first plan found might not be the cheapest. An inadmissible heuristic can cause the algorithm to over-prune branches that actually contain the optimal solution.

**Q56. How is the initial h_cost for "Hardware Issue" node set to $80?**
A. It is set conservatively as the expected average cost of a hardware repair ($80). Since the cheapest hardware fix (RAM reseating) costs $0, h=$80 is actually slightly overestimated for that sub-problem — but since it is the h_cost of the category node, not a leaf, and the actual minimum is driven by child f values, it still guides correctly.

**Q57. Can AO\* handle graphs where AND and OR nodes are mixed at multiple levels?**
A. Yes — AO\* handles arbitrary depth AND-OR trees. The recursion in `_compute_all_costs` and `_extract_path` handles any combination of node types at any depth.

**Q58. What is the space complexity of AO\*?**
A. O(|V|) where |V| is the total number of nodes. Every node must be stored and its f value maintained. In our system, |V| ≤ 20 per problem, so memory is trivial.

**Q59. How does AO\* handle tie-breaking when two children have equal f costs?**
A. In our implementation, the first child encountered with the minimum cost becomes the best_child. This is deterministic but could be randomised or broken by a secondary criterion (e.g., fix_time).

**Q60. What is the difference between `get_solution_path()` returning `None` vs returning `[]`?**
A. `None` means the root is FAILED (no solution exists). `[]` (empty list) means the root is SOLVED (all steps done — no more actions needed). Both signal the end of the session, but for different reasons.

---

## Section D — Heuristics (Q61–70)

**Q61. Why are heuristics important in AO\*?**
A. Without heuristics (h=0 for all), AO\* explores the cheapest subgraph uniformly. With good heuristics, it focuses on the most promising branch first, reducing the number of fix attempts before finding the solution.

**Q62. What is a consistent (monotone) heuristic?**
A. A heuristic is consistent if `h(n) ≤ w(n,c) + h(c)` for every edge (n,c). Consistency implies admissibility. In our problem, heuristics on parent nodes are set lower than the actual minimum child cost, ensuring consistency.

**Q63. How would you design a heuristic for a new device fault category?**
A. Set `h(category_node)` to the cheapest possible repair cost in that category. For example, if a "Display Issue" category has fixes ranging from $0 to $120, set h=0 (since $0 is achievable). This ensures admissibility.

**Q64. What is an inadmissible heuristic, and when might you intentionally use one?**
A. An inadmissible heuristic overestimates cost. You might use one to make the search faster (explore fewer nodes) at the cost of optimality — acceptable when approximate solutions are good enough.

**Q65. Can heuristics be learned rather than hand-crafted?**
A. Yes — from historical repair data, one can train a model to predict repair costs given fault descriptions. These learned costs then serve as heuristics. This is the basis for "learning heuristics" in AI.

**Q66. Why is `h(LEAF) = actual_cost` not a heuristic?**
A. For LEAF nodes, the cost is known exactly — it is the true `h*(n)`. A heuristic is an estimate; for LEAFs there is nothing to estimate since the action and its cost are fully defined.

**Q67. What is the relationship between heuristic quality and algorithm performance?**
A. Better heuristics (closer to h\*) mean AO\* explores fewer branches before finding the optimal path. Poor heuristics (close to 0) mean more exploration. The algorithm's correctness is unaffected as long as h ≤ h\*.

**Q68. How do heuristic values influence the order in which repair categories are tried?**
A. AO\* sets `f(root) = min over children of [h(child)]`. Children with lower h values are tried first. Setting h(software) = 5 and h(hardware) = 80 ensures software fixes are explored before hardware — which is the correct strategy.

**Q69. What is the "null heuristic" and how does AO\* behave with it?**
A. The null heuristic sets h(n) = 0 for all internal nodes. AO\* then uses only the leaf costs to guide search. It is still optimal but may not prioritise categories well (e.g., might explore a hardware category before exhausting free software fixes).

**Q70. If a repair technician provides historical cost data, how would you improve the heuristics?**
A. Compute the expected cost of each sub-tree from historical data: `h(n) = avg cost paid across all repairs rooted at n`. Use these as heuristic values. This creates a data-driven heuristic that is more accurate than hand-set values.

---

## Section E — Project-Specific Questions (Q71–85)

**Q71. Why did you choose Python for this project?**
A. Python has excellent support for object-oriented design (classes for Node, Status, NodeType), is fast to prototype in, and has a rich ecosystem (fpdf2 for PDF generation, built-in random for Monte Carlo simulation).

**Q72. What are the four device problems in your knowledge base?**
A. (1) Laptop Won't Start, (2) WiFi Not Working, (3) Phone Overheating, (4) Printer Not Printing.

**Q73. How did you validate that your AO\* implementation is correct?**
A. By tracing manual examples (e.g., Test Case 2 in docs/06) step by step, verifying that failed nodes cause the correct replanning, and that the extracted path always contains the minimum-cost remaining steps.

**Q74. What is the purpose of the `comparison.py` module?**
A. To quantitatively show that AO\* outperforms random-order fixing. It runs 2 000 Monte Carlo trials where leaves are applied in random order and measures the average cost, comparing it to AO\*'s optimal cost.

**Q75. How is the Monte Carlo simulation designed?**
A. All LEAF nodes are collected and shuffled randomly. Steps are applied until a leaf that belongs to the AO\* optimal path is encountered (simulating a correct fix found by chance). The total cost paid before that point is the trial cost. Average across 2 000 trials gives the random baseline.

**Q76. Why is the `parent` pointer stored in each Node?**
A. To enable O(depth) upward propagation. When a leaf's status changes, we need to update all ancestors without re-traversing the entire graph. The parent pointer chain provides a direct path from leaf to root.

**Q77. What happens in the interactive session when the user types Q?**
A. The session terminates gracefully. The partial session log (steps attempted, results, costs) is displayed as a summary. No further steps are executed.

**Q78. How does the visualizer display AND vs OR nodes differently?**
A. OR nodes show `[OR]`, AND nodes show `[AND]`, and LEAFs show `[FIX]` as a prefix in the ASCII tree. Solved nodes show `[✓]` and failed nodes show `[✗]` at the end of their line.

**Q79. What would you change to add a "Phone Won't Charge" fault?**
A. Write `build_phone_wont_charge()` in `knowledge_base.py`, create a tree with OR children (cable issue, port issue, software issue, battery issue), and register it as `"5": ("Phone Won't Charge", build_phone_wont_charge)` in `DEVICE_PROBLEMS`.

**Q80. Why does the Printer problem use an AND node but the Laptop problem uses all OR nodes?**
A. Printer connectivity requires BOTH a physical check (cable) AND a logical check (driver reinstall) — you cannot confirm connectivity with just one. Laptop faults are genuinely alternative causes — if the OS is corrupted, the hardware is fine; only one fix is needed.

**Q81. What is `fix_time` used for?**
A. It records the estimated time in minutes for each repair step. It is displayed to the user and summed in the session summary, helping users plan their time as well as their budget.

**Q82. What does `h_cost` represent on an OR node in the code?**
A. It is the initial estimate of the cost to solve that sub-problem before the bottom-up computation runs. After `_compute_all_costs()` runs, `f_cost` replaces it with the accurate computed value based on actual child costs.

**Q83. Could this project be extended to use a probabilistic model?**
A. Yes — PAO\* (Probabilistic AO\*) assigns a success probability to each fix action. The objective changes to minimising expected cost rather than worst-case cost. This would make the system more realistic.

**Q84. What is the difference between `show_plan()` and `run_interactive()` in `troubleshooter.py`?**
A. `show_plan()` prints the full AND-OR tree and optimal plan without executing any steps — it is a read-only view. `run_interactive()` drives a full session where the user attempts each step and the system replans as needed.

**Q85. What is the output of `get_solution_path()` for the Printer problem initially?**
A. `[Reseat Cable, Reinstall Driver]` — both AND children of the "Connection Diagnosis" node, since the AND node's `best_children` includes all children, and both are UNSOLVED LEAF nodes.

---

## Section F — Implementation Details (Q86–93)

**Q86. What Python data type is used for `children` in the Node class?**
A. `List[Tuple[Node, float]]` — a list of `(child_node, edge_cost)` pairs. This allows each edge to carry a weight while maintaining ordered children.

**Q87. Why is `math.inf` used for failed node costs?**
A. Because `math.inf` is larger than any finite cost. When a parent computes `min(w + f(child))` and the child has f=∞, it is automatically excluded from the minimum without any special case code.

**Q88. What does `_compute_all_costs` do and when is it called?**
A. It performs a bottom-up DFS to initialise all `f_cost` values and `best_children` pointers. It is called once in `AOStar.__init__()`. Subsequent updates are done incrementally via `_propagate_up`.

**Q89. How does `_extract_path` handle a SOLVED leaf node?**
A. It returns `[]` (empty list) because a SOLVED node has already been fixed and needs no further action. The parent's remaining UNSOLVED siblings are returned instead.

**Q90. What is the role of `Status.UNSOLVED` vs `Status.SOLVED` vs `Status.FAILED`?**
A. `UNSOLVED`: default state — not yet attempted. `SOLVED`: user confirmed this fix worked. `FAILED`: user confirmed this fix did not work. These three states drive all branching logic in AO\*.

**Q91. Why is `NodeType` an `Enum` rather than a string?**
A. Enums prevent typos (`NodeType.OR` vs `"OR"`), enable IDE autocomplete, and make `if node.node_type == NodeType.OR` checks more readable and refactor-safe than string comparisons.

**Q92. How does the project prevent the same fix from being suggested again after it fails?**
A. `mark_failed(leaf)` sets `leaf.status = FAILED` and `leaf.f_cost = ∞`. In `_update_node(OR parent)`, failed children are skipped: `if child.status == Status.FAILED: continue`. The leaf is permanently excluded from future paths.

**Q93. What would happen if `parent` pointers were not set in `add_child()`?**
A. `_propagate_up` would immediately stop (current = None) after the first update. Cost changes would never reach the root, meaning OR nodes would never update their best_child after a failure — replanning would break entirely.

---

## Section G — Analysis and Broader AI (Q94–100)

**Q94. How does this project relate to expert systems?**
A. It is a lightweight rule-based expert system for device repair. The knowledge base (AND-OR graphs) plays the role of the rule base, and AO\* search plays the role of the inference engine.

**Q95. Compare AO\* to Minimax in game trees.**
A. Minimax alternates between MAX (maximise score) and MIN (minimise score) levels. AO\* alternates between OR (minimise cost — pick cheapest) and AND (sum costs — do all). Both are recursive algorithms on structured trees; AO\* targets cost minimisation, Minimax targets payoff optimisation.

**Q96. How would you adapt this system to use machine learning?**
A. Train a classifier on symptom descriptions to predict the most likely fault category (replacing the static menu). Train a regression model on historical repair data to predict fix success probability and cost, improving heuristics.

**Q97. What is the relationship between AO\* and SAT solving?**
A. Boolean SAT can be encoded as an AND-OR graph where clauses are OR nodes and conjunctions are AND nodes. AO\* search is analogous to unit propagation and DPLL search in SAT solvers. Both search for a satisfying assignment (solution) in a conjunctive/disjunctive structure.

**Q98. Why is the comparison module important from a scientific perspective?**
A. It provides an empirical baseline. Without comparison to random fixing, the claim that "AO\* saves money" is unsupported. The Monte Carlo simulation quantifies the improvement with statistical confidence across 2 000 trials.

**Q99. What is the ethical implication of a fault diagnosis system giving wrong advice?**
A. A wrong recommendation could cause a user to perform an unnecessary expensive repair (financial harm) or, in extreme cases, damage other components (e.g., improper motherboard handling). The system should always recommend professional diagnosis when all paths are exhausted, which is implemented in `run_interactive()`.

**Q100. If you had to re-implement this project in one week, what would you do differently?**
A. (1) Add a probabilistic success model to each LEAF (using repair statistics). (2) Use a graph (DAG) instead of a tree to allow shared repair actions. (3) Add a web frontend for non-technical users. (4) Automatically learn h_cost values from session logs rather than hard-coding them.
