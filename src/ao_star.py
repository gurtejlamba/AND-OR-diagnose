import math
from typing import List, Optional
from .and_or_graph import Node, NodeType, Status


class AOStar:
    """
    AO* search on a pre-built AND-OR graph.

    Cost rules
    ----------
    LEAF  : f = actual repair cost
    OR    : f = min over non-failed children of (edge_cost + f(child))
    AND   : f = sum over all non-failed unsolved children of (edge_cost + f(child))
             → FAILED if any child is FAILED
    """

    def __init__(self, root: Node):
        self.root = root
        self._compute_all_costs(root)

    # ------------------------------------------------------------------
    # Internal cost propagation
    # ------------------------------------------------------------------

    def _compute_all_costs(self, node: Node):
        """Bottom-up initialisation of all f values."""
        if node.is_leaf:
            node.f_cost = node.cost
            return
        for child, _ in node.children:
            self._compute_all_costs(child)
        self._update_node(node)

    def _update_node(self, node: Node):
        """Recompute f_cost and best_children for one internal node."""
        if node.is_leaf:
            return

        if node.node_type == NodeType.OR:
            best_cost = math.inf
            best_child: Optional[Node] = None
            for child, edge_cost in node.children:
                if child.status == Status.FAILED:
                    continue
                total = edge_cost + child.f_cost
                if total < best_cost:
                    best_cost = total
                    best_child = child

            if best_child is None:
                node.status = Status.FAILED
                node.f_cost = math.inf
                node.best_children = []
            else:
                node.f_cost = best_cost
                node.best_children = [best_child]
                if best_child.status == Status.SOLVED:
                    node.status = Status.SOLVED

        elif node.node_type == NodeType.AND:
            total = 0.0
            all_solved = True
            for child, edge_cost in node.children:
                if child.status == Status.FAILED:
                    node.status = Status.FAILED
                    node.f_cost = math.inf
                    node.best_children = []
                    return
                total += edge_cost + child.f_cost
                if child.status != Status.SOLVED:
                    all_solved = False
            node.f_cost = total
            node.best_children = [c for c, _ in node.children]
            if all_solved:
                node.status = Status.SOLVED

    def _propagate_up(self, node: Node):
        """Walk up to root, recomputing each ancestor."""
        current = node.parent
        while current is not None:
            self._update_node(current)
            current = current.parent

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def get_solution_path(self) -> List[Node]:
        """
        Return the ordered list of LEAF nodes in the current best plan,
        excluding any already SOLVED (already executed) leaves.
        Empty if the root is SOLVED or FAILED.
        """
        if self.root.status == Status.FAILED:
            return []
        return self._extract_path(self.root)

    def _extract_path(self, node: Node) -> List[Node]:
        if node.status == Status.SOLVED:
            return []
        if node.is_leaf:
            return [node]
        result: List[Node] = []
        for child in node.best_children:
            result.extend(self._extract_path(child))
        return result

    def mark_solved(self, node: Node):
        """Call when a fix step succeeds."""
        node.status = Status.SOLVED
        self._propagate_up(node)

    def mark_failed(self, node: Node):
        """Call when a fix step fails; triggers replanning."""
        node.status = Status.FAILED
        node.f_cost = math.inf
        self._propagate_up(node)

    @property
    def is_solved(self) -> bool:
        return self.root.status == Status.SOLVED

    @property
    def is_failed(self) -> bool:
        return self.root.status == Status.FAILED
