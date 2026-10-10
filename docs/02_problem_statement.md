# 02 — Problem Statement

## The Core Problem
Diagnosing a faulty device is hard because:

1. **One symptom, many causes.** A laptop that won't start could have a dead battery, corrupted OS, failed RAM, or cracked screen — the external symptom is identical.
2. **Fixes are interdependent.** Some causes require a sequence of ordered steps (AND relationship); others are alternatives where only one needs to work (OR relationship).
3. **Random fixing is expensive.** Users typically try fixes in arbitrary order. If a $280 motherboard replacement is attempted before a free static-discharge reset, money is lost permanently.
4. **No replanning.** Traditional guides give a static checklist. If step 3 fails, the user has no structured guidance for what to do next.

## Formal Problem Definition
Given:
- A fault `F` (root node) with a set of possible causes `C = {c₁, c₂, …, cₙ}`.
- Each cause `cᵢ` may require a single repair action (LEAF) or a sub-tree of actions (AND-OR subtree).
- Each repair action `aⱼ` has a known cost `cost(aⱼ) ≥ 0`.

Find:
- A **solution subgraph** `S` rooted at `F` such that executing the actions in `S` resolves `F`.
- Among all valid solution subgraphs, `S` must minimise `∑ cost(aⱼ)` for all `aⱼ ∈ S`.

When a repair action `aⱼ ∈ S` **fails at runtime**, find the new minimum-cost solution subgraph `S'` that excludes `aⱼ`.

## Why AND-OR Graphs?
Standard graphs support only OR decomposition (pick any path). AND-OR graphs add the AND connector, which captures the idea that some faults require **all** of a set of steps to be resolved before the parent problem is considered fixed. This is essential for realistic repair scenarios:

- **OR example:** "WiFi not working" — either update the driver **or** restart the router (one is enough).
- **AND example:** "Printer not printing (connection)" — must verify the cable **and** reinstall the driver (both are required).

## Why AO\*?
AO\* is the natural algorithm for AND-OR graphs because:
- It propagates costs correctly through both AND and OR connectors.
- It is **optimal**: the first solution it finds has minimum cost.
- It is **complete**: it will find a solution if one exists.
- It supports **replanning** by simply marking a failed node and re-running cost propagation.

## Illustrative Example
```
Laptop Won't Start  [OR]
├── Software Issue  [OR]        ← h = $5
│   ├── Boot in Safe Mode       $0   (try first)
│   ├── Run Startup Repair      $0
│   └── Reinstall OS            $0
├── Power Issue     [OR]        ← h = $20
│   ├── Static Discharge Reset  $0
│   ├── Test / Replace Charger  $15
│   └── Replace Battery         $50
├── Display Issue   [OR]        ← h = $30
│   ├── Test External Monitor   $0
│   ├── Reseat Display Cable    $0
│   └── Replace Screen          $120
└── Hardware Issue  [OR]        ← h = $80
    ├── Reseat RAM              $0
    ├── Replace SSD             $70
    └── Replace Motherboard     $280
```

AO\* initial recommendation: **"Boot in Safe Mode" ($0)**. If that fails → **"Run Startup Repair" ($0)**. After all software options exhausted → **"Static Discharge Reset" ($0)**. And so on — always cheapest next.
