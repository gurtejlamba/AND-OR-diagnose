# 05 — Implementation Guide

## 5.1 Project Setup

```bash
# Clone / enter project
cd aiscp

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate          # macOS / Linux
venv\Scripts\activate             # Windows

# Install dependencies
pip install -r requirements.txt

# Run the assistant
python run.py
```

## 5.2 Core Algorithm — Step-by-Step

### Step 1 — Build the AND-OR Graph

Each device problem is built by a `build_*` function in `knowledge_base.py`. Nodes are instantiated as `Node` objects and linked via `add_child()`:

```python
root = Node("Laptop Won't Start", NodeType.OR, h_cost=50)
software = Node("Software Issue", NodeType.OR, h_cost=5)
safe_mode = Node("Boot in Safe Mode", NodeType.LEAF, cost=0, fix_time=10)

software.add_child(safe_mode)          # edge_cost defaults to 0
root.add_child(software)
```

`add_child()` also sets `child.parent = self`, establishing the upward links needed for propagation.

### Step 2 — Initialise AO\*

```python
ao = AOStar(root)
```

The constructor calls `_compute_all_costs(root)`, which does a **post-order (bottom-up) DFS**:

```
_compute_all_costs(node):
  if LEAF: node.f_cost = node.cost; return
  for each child: _compute_all_costs(child)   ← recurse first
  _update_node(node)                          ← then compute parent
```

After this, every node has a valid `f_cost` and every OR node has a valid `best_children`.

### Step 3 — Extract Solution Path

```python
path = ao.get_solution_path()
```

`_extract_path(node)` is a recursive descent that:
- Returns `[]` if node is SOLVED (already done).
- Returns `[node]` if node is a LEAF.
- Otherwise follows `node.best_children` and concatenates results.

### Step 4 — Execute and Replan

**On success:**
```python
ao.mark_solved(leaf)
# → leaf.status = SOLVED
# → propagate_up: OR parent may become SOLVED if leaf was best_child
```

**On failure:**
```python
ao.mark_failed(leaf)
# → leaf.status = FAILED, leaf.f_cost = ∞
# → propagate_up: OR parent picks next-best child
#                 AND parent becomes FAILED
```

## 5.3 Key Design Decisions

### Pre-built vs Lazy Graph Expansion
We pre-build the entire problem graph at startup rather than expanding nodes lazily. This is appropriate because:
- The knowledge base is finite and small (< 30 nodes per problem).
- Pre-building enables immediate visualisation of the full tree.
- Lazy expansion would add complexity without any practical benefit.

### Edge Costs vs Node Costs
All repair costs are stored on LEAF nodes (`node.cost`), not on edges. Edges have weight 0 unless a diagnostic step itself has a cost. This simplifies the model while remaining general.

### Heuristic Values
`h_cost` on internal (OR/AND) nodes is a conservative lower-bound estimate of the cheapest fix in that sub-tree. Example: "Hardware Issue" has `h_cost = 80` because the cheapest hardware fix (RAM reseating) costs $0 but the category on average costs ~$80. This guides AO\* to try software fixes first.

### Comparison Module
The comparison uses a Monte Carlo simulation (2 000 trials). In each trial:
- All LEAF nodes are shuffled into a random order.
- Steps are applied until a leaf that is in the AO\* optimal path is reached (i.e., a legitimate fix).
- The total cost up to that point is recorded.

The average across trials represents the expected cost of random-order fixing.

## 5.4 Extending the Knowledge Base

To add a new device problem:

1. Write a `build_my_problem()` function in `knowledge_base.py`.
2. Populate the tree with `Node` objects and `add_child()` calls.
3. Register it in `DEVICE_PROBLEMS`:
   ```python
   "5": ("My New Problem", build_my_problem),
   ```

No changes to `ao_star.py` or `troubleshooter.py` are needed.

## 5.5 File Reference

```
aiscp/
├── run.py                  ← launch here: python run.py
├── requirements.txt        ← fpdf2 for PDF generation
├── src/
│   ├── __init__.py
│   ├── and_or_graph.py     ← Node, NodeType, Status
│   ├── ao_star.py          ← AO* engine
│   ├── knowledge_base.py   ← 4 device problem trees
│   ├── troubleshooter.py   ← CLI session manager
│   ├── visualizer.py       ← ASCII rendering
│   ├── comparison.py       ← Monte Carlo comparison
│   └── main.py             ← menu controller
├── docs/                   ← project documentation (7 files)
├── viva/                   ← 100 viva Q&A
└── presentation/           ← 5-min script + PDF generator
```
