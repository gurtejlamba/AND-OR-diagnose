# 03 — Algorithm Theory

## 3.1 AND-OR Graphs — Formal Definition

An **AND-OR graph** `G = (V, E, type)` where:
- `V` is the set of nodes (problems / sub-problems / repair actions).
- `E ⊆ V × V` is the set of directed edges (decomposition relationships).
- `type : V → {OR, AND, LEAF}` labels each node.

**Terminal (LEAF) nodes** have no children and represent atomic repair actions with a known cost.

**OR nodes** model *alternative decompositions*: the problem is solved if **any one** child sub-problem is solved. They represent the choice between different potential causes.

**AND nodes** model *conjunctive decompositions*: the problem is solved only when **all** child sub-problems are solved. They represent compound diagnosis steps that must all succeed.

## 3.2 Solution Subgraph

A **solution subgraph** `S` rooted at node `n` is defined recursively:
- If `n` is a LEAF: `S = {n}`.
- If `n` is an OR node with children `c₁…cₖ`: `S = {n} ∪ S(cᵢ)` for exactly one `i`.
- If `n` is an AND node with children `c₁…cₖ`: `S = {n} ∪ S(c₁) ∪ … ∪ S(cₖ)`.

The **cost of a solution subgraph** is the sum of costs of all LEAF nodes in `S`.

The objective is to find the solution subgraph `S*` with minimum total cost.

## 3.3 AO\* Algorithm

AO\* is a best-first heuristic search algorithm for AND-OR graphs, analogous to A\* for standard graphs.

### Node Cost Definitions

Each node `n` has an estimated cost-to-solve `f(n)`:

```
f(n) = n.cost                                            if n is LEAF
f(n) = min over non-failed children c of [w(n,c) + f(c)]  if n is OR
f(n) = sum over all children c of [w(n,c) + f(c)]         if n is AND
```

where `w(n,c)` is the edge weight between `n` and child `c`.

### Algorithm Steps

```
PROCEDURE AO*(root):
  1. Compute f(n) for all nodes bottom-up (post-order traversal).
  2. At each OR node, record best_child = argmin[w(n,c) + f(c)].
  3. At each AND node, record best_children = all children.
  4. Extract solution path: from root, follow best_children recursively
     to collect all LEAF nodes — this is the ordered fix plan.
  5. Execute the fix steps one by one.
  6. If a fix SUCCEEDS:
       Mark leaf as SOLVED; propagate upward.
       If root is SOLVED → stop.
       Else re-extract path (next steps from remaining AND branches).
  7. If a fix FAILS:
       Mark leaf as FAILED (f = ∞); propagate upward.
       OR parent picks next-best child (automatically via f update).
       Re-extract path → replan.
  8. If root is FAILED (all paths exhausted) → no solution.
```

### Cost Propagation (Back-Propagation)

When a node's status changes, costs propagate upward:

```
PROPAGATE_UP(node n):
  parent ← n.parent
  while parent ≠ null:
    recompute f(parent) using updated children
    update best_children(parent)
    update status(parent)
    parent ← parent.parent
```

This is O(depth) per replanning step.

## 3.4 Admissibility and Optimality

AO\* is **admissible** (guaranteed to find the minimum-cost solution) if and only if the heuristic `h(n)` satisfies:

```
h(n) ≤ h*(n)   for all n
```

where `h*(n)` is the true minimum cost to solve `n`.

In our implementation, the heuristic `h_cost` values assigned to OR/AND nodes are conservative lower bounds derived from domain knowledge (e.g., the cheapest possible fix in a category). This ensures optimality.

## 3.5 Complexity Analysis

| Metric | Value |
|--------|-------|
| Space | O(b^d) — must store entire graph |
| Time (best case) | O(d) — straight path, no replanning |
| Time (worst case) | O(b^d) — exhaustive search |
| Replanning step | O(depth) — propagate up from failed node |

Where `b` = branching factor, `d` = depth of the solution.

In practice, device troubleshooting graphs are shallow (d ≤ 3) and narrow (b ≤ 5), so the algorithm runs in constant time for all practical inputs.

## 3.6 Comparison with A\*

| Feature | A\* | AO\* |
|---------|-----|------|
| Graph type | Standard (OR only) | AND-OR |
| Node type | Single type | OR, AND, LEAF |
| Cost model | Path cost | Subgraph cost |
| Supports conjunctions | No | Yes |
| Replanning | Requires full re-run | Incremental (propagate up) |
| Used for | Pathfinding, planning | Problem decomposition, repair |
