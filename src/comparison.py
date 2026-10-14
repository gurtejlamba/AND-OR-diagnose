"""
Compare AO* (optimal order) vs random-order fixing.

Random simulation: shuffle all LEAF nodes and pay for each one until every
step of the AO* plan has been tried (simulates a user guessing fixes randomly).
"""

import random
from typing import List

from .and_or_graph import Node
from .ao_star import AOStar


def _all_leaves(node: Node) -> List[Node]:
    if node.is_leaf:
        return [node]
    return [leaf for child, _ in node.children for leaf in _all_leaves(child)]


def get_ao_star_stats(root_builder) -> dict:
    path = AOStar(root_builder()).get_solution_path()
    return {
        "cost": sum(n.cost for n in path),
        "time": sum(n.fix_time for n in path),
        "steps": len(path),
        "path": [n.name for n in path],
    }


def simulate_random(root_builder, num_trials: int = 2000) -> dict:
    # ponytail: assumes the AO* plan is the fix that actually works; real success odds would need repair data
    needed = set(get_ao_star_stats(root_builder)["path"])
    leaves = _all_leaves(root_builder())
    costs: List[float] = []
    times: List[int] = []

    for _ in range(num_trials):
        random.shuffle(leaves)
        cost, time, left = 0.0, 0, set(needed)
        for leaf in leaves:
            cost += leaf.cost
            time += leaf.fix_time
            left.discard(leaf.name)
            if not left:  # an AND plan needs all of its steps, not just one
                break
        costs.append(cost)
        times.append(time)

    return {
        "avg_cost": sum(costs) / num_trials,
        "min_cost": min(costs),
        "max_cost": max(costs),
        "avg_time": sum(times) / num_trials,
        "trials": num_trials,
    }
