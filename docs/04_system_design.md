# 04 — System Design

## 4.1 Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                   run.py  (CLI entry)               │
└────────────────────────┬────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────┐
│               src/main.py  (menu controller)        │
└──────┬─────────────────┬──────────────────┬─────────┘
       │                 │                  │
┌──────▼──────┐  ┌───────▼──────┐  ┌───────▼──────┐
│troubleshooter│  │  comparison  │  │  visualizer  │
│    .py       │  │    .py       │  │    .py       │
└──────┬───────┘  └───────┬──────┘  └──────────────┘
       │                  │
┌──────▼──────────────────▼──────┐
│          src/ao_star.py        │
│   (AO* algorithm engine)       │
└──────────────┬─────────────────┘
               │
┌──────────────▼─────────────────┐
│       src/and_or_graph.py      │
│   (Node, NodeType, Status)     │
└──────────────┬─────────────────┘
               │ (graph instances)
┌──────────────▼─────────────────┐
│      src/knowledge_base.py     │
│  (device-specific problem      │
│   trees: 4 problems)           │
└────────────────────────────────┘
```

## 4.2 Data Model

### Node
```
Node
├── name         : str           — human-readable label
├── node_type    : NodeType      — OR | AND | LEAF
├── cost         : float         — actual repair cost (LEAF only)
├── h_cost       : float         — heuristic estimate (internal nodes)
├── description  : str           — step instructions shown to user
├── fix_time     : int           — estimated minutes to complete
├── children     : [(Node, float)]  — (child, edge_cost) list
├── f_cost       : float         — current estimated total cost
├── status       : Status        — UNSOLVED | SOLVED | FAILED
├── best_children: [Node]        — selected children in current plan
└── parent       : Node | None   — upward link for propagation
```

### NodeType
```
OR   → at least one child must be solved (try alternatives)
AND  → all children must be solved (all steps required)
LEAF → no children; represents a concrete repair action
```

### Status
```
UNSOLVED → not yet attempted or incomplete
SOLVED   → fix confirmed successful by user
FAILED   → fix attempted and confirmed not working
```

## 4.3 AND-OR Graph Structure per Problem

### Laptop Won't Start
```
Root [OR]
 ├── Software Issue [OR]    h=$5
 │    ├── Safe Mode         $0
 │    ├── Startup Repair    $0
 │    └── Reinstall OS      $0
 ├── Power Issue [OR]       h=$20
 │    ├── Static Reset      $0
 │    ├── Replace Charger   $15
 │    └── Replace Battery   $50
 ├── Display Issue [OR]     h=$30
 │    ├── Ext. Monitor      $0
 │    ├── Reseat Cable      $0
 │    └── Replace Screen    $120
 └── Hardware Issue [OR]    h=$80
      ├── Reseat RAM        $0
      ├── Replace SSD       $70
      └── Replace MB        $280
```

### Printer Not Printing (AND node example)
```
Root [OR]
 ├── Connection Diag. [AND]  ← both steps mandatory
 │    ├── Reseat Cable       $0
 │    └── Reinstall Driver   $0
 ├── Consumables [OR]
 │    ├── Clear Paper Jam    $0
 │    └── Replace Cartridge  $30
 └── Hardware Fault [OR]
      ├── Clean Print Heads  $0
      ├── Replace Head Asm.  $55
      └── Replace Printer    $120
```

## 4.4 Replanning Flow

```
User says step FAILED
       │
       ▼
ao.mark_failed(leaf)
 → leaf.f_cost = ∞
 → leaf.status = FAILED
       │
       ▼
_propagate_up(leaf)
 → walk up tree to root
 → at each OR parent:
     recompute best_child (skip FAILED children)
 → at each AND parent:
     if any child FAILED → AND becomes FAILED
       │
       ▼
ao.get_solution_path()
 → traverse root → best_children → leaves
 → skip SOLVED leaves (already done)
 → return new ordered list of LEAF steps
       │
       ▼
Display new plan to user
```

## 4.5 Module Responsibilities

| Module | Responsibility |
|--------|---------------|
| `and_or_graph.py` | Data structures only — no logic |
| `ao_star.py` | Cost computation, propagation, path extraction |
| `knowledge_base.py` | Domain-specific graph builders |
| `troubleshooter.py` | UI layer — wraps AO\*, handles I/O |
| `visualizer.py` | ASCII tree and solution table rendering |
| `comparison.py` | Monte Carlo simulation vs AO\* |
| `main.py` | Top-level menu and flow control |
