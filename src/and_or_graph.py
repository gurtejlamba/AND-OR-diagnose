from enum import Enum
from typing import List, Optional, Tuple
import math


class NodeType(Enum):
    OR = "OR"
    AND = "AND"
    LEAF = "LEAF"


class Status(Enum):
    UNSOLVED = "UNSOLVED"
    SOLVED = "SOLVED"
    FAILED = "FAILED"


class Node:
    def __init__(
        self,
        name: str,
        node_type: NodeType,
        cost: float = 0.0,
        h_cost: float = 0.0,
        description: str = "",
        fix_time: int = 0,
    ):
        self.name = name
        self.node_type = node_type
        self.cost = cost            # actual cost for LEAF nodes
        self.h_cost = h_cost        # heuristic estimate for internal nodes
        self.description = description
        self.fix_time = fix_time    # time in minutes
        self.children: List[Tuple["Node", float]] = []   # (child, edge_cost)
        self.f_cost: float = cost if node_type == NodeType.LEAF else h_cost
        self.status: Status = Status.UNSOLVED
        self.best_children: List["Node"] = []
        self.parent: Optional["Node"] = None

    def add_child(self, child: "Node", edge_cost: float = 0.0):
        child.parent = self
        self.children.append((child, edge_cost))

    @property
    def is_leaf(self) -> bool:
        return self.node_type == NodeType.LEAF

    def __repr__(self) -> str:
        return (
            f"Node({self.name!r}, {self.node_type.value}, "
            f"f={self.f_cost:.1f}, {self.status.value})"
        )
