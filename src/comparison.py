"""
Compare AO* (optimal order) vs random-order fixing.

Random simulation: shuffle all LEAF nodes and apply them until one
marks the problem as solved (simulates a user guessing fixes randomly).
"""

import random
import math
import copy
from typing import List

from .and_or_graph import Node, NodeType, Status
from .ao_star import AOStar


def _all_leaves(node: Node) -> List[Node]:
    if node.is_leaf:
        return [node]
    leaves: List[Node] = []
    for child, _ in node.children:
        leaves.extend(_all_leaves(child))
    return leaves


def _reset_tree(node: Node):
    node.status = Status.UNSOLVED
    node.f_cost = node.cost if node.is_leaf else node.h_cost
    node.best_children = []
    for child, _ in node.children:
        _reset_tree(child)


def simulate_random(root_builder, num_trials: int = 2000) -> dict:
    """
    Each trial: try leaf nodes in a random order; stop as soon as one
    is the cheapest fix that actually resolves the root (simplified: stop
    on first free fix, otherwise track until cheapest non-free).
    We measure total cost paid before reaching a working fix.
    """
    costs: List[float] = []
    times: List[int] = []

    for _ in range(num_trials):
        root = root_builder()
        ao = AOStar(root)
        optimal_path = ao.get_solution_path() or []
        # Re-build fresh for simulation
        root = root_builder()
        leaves = _all_leaves(root)
        random.shuffle(leaves)

        trial_cost = 0.0
        trial_time = 0
        solved = False
        for leaf in leaves:
            trial_cost += leaf.cost
            trial_time += leaf.fix_time
            # Simplified success model: leaf is "the fix" with 1/(rank+1) probability
            # We use a deterministic model: stop when we hit a leaf that is in the
            # AO* optimal path (i.e., it's a legitimate fix for this problem).
            if leaf.name in {n.name for n in optimal_path}:
                solved = True
                break
        if not solved:
            trial_cost = sum(l.cost for l in leaves)
            trial_time = sum(l.fix_time for l in leaves)

        costs.append(trial_cost)
        times.append(trial_time)

    return {
        "avg_cost": sum(costs) / len(costs),
        "min_cost": min(costs),
        "max_cost": max(costs),
        "avg_time": sum(times) / len(times),
        "trials": num_trials,
    }


def get_ao_star_stats(root_builder) -> dict:
    root = root_builder()
    ao = AOStar(root)
    path = ao.get_solution_path() or []
    return {
        "cost": sum(n.cost for n in path),
        "time": sum(n.fix_time for n in path),
        "steps": len(path),
        "path": [n.name for n in path],
    }


def run_comparison(name: str, builder):
    print(f"\n{'═'*62}")
    print(f"  COMPARISON REPORT — {name}")
    print(f"{'═'*62}")

    ao = get_ao_star_stats(builder)
    rnd = simulate_random(builder, num_trials=2000)

    print(f"\n  AO* Algorithm (optimal path):")
    print(f"    Steps         : {ao['steps']}")
    print(f"    Total cost    : ${ao['cost']:.0f}")
    print(f"    Total time    : {ao['time']} min")
    print(f"    Path          : {' → '.join(ao['path'])}")

    print(f"\n  Random-order fixing (2 000 simulations):")
    print(f"    Avg cost      : ${rnd['avg_cost']:.0f}")
    print(f"    Best case     : ${rnd['min_cost']:.0f}")
    print(f"    Worst case    : ${rnd['max_cost']:.0f}")
    print(f"    Avg time      : {rnd['avg_time']:.0f} min")

    if rnd["avg_cost"] > 0:
        savings_pct = (rnd["avg_cost"] - ao["cost"]) / rnd["avg_cost"] * 100
        time_saved  = rnd["avg_time"] - ao["time"]
        print(f"\n  AO* saves ~{savings_pct:.0f}% cost and ~{time_saved:.0f} min on average.")
    print()
