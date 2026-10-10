from .and_or_graph import Node, NodeType, Status

_TYPE_LABEL = {NodeType.OR: "[OR] ", NodeType.AND: "[AND]", NodeType.LEAF: "[FIX]"}
_STATUS_SYM = {Status.SOLVED: "✓", Status.FAILED: "✗", Status.UNSOLVED: " "}


def print_tree(node: Node, prefix: str = "", is_last: bool = True):
    """Render the AND-OR graph as an ASCII tree to stdout."""
    connector = "└── " if is_last else "├── "
    tl = _TYPE_LABEL[node.node_type]
    ss = _STATUS_SYM[node.status]

    if node.is_leaf:
        cost_str = f"  ${node.cost:.0f}  {node.fix_time} min"
    else:
        cost_str = f"  f=${node.f_cost:.0f}" if node.f_cost < 1e8 else "  f=∞"

    print(f"{prefix}{connector}{tl} {node.name}{cost_str}  [{ss}]")

    child_prefix = prefix + ("    " if is_last else "│   ")
    children = node.children
    for i, (child, _) in enumerate(children):
        print_tree(child, child_prefix, is_last=(i == len(children) - 1))


def print_solution_path(path):
    """Print the ordered fix steps with total cost."""
    if not path:
        print("  (no solution path)")
        return
    total_cost = sum(n.cost for n in path)
    total_time = sum(n.fix_time for n in path)
    print(f"\n  {'Step':<4} {'Fix Action':<38} {'Cost':>6}  {'Time':>6}")
    print(f"  {'─'*4} {'─'*38} {'─'*6}  {'─'*6}")
    for i, node in enumerate(path, 1):
        print(f"  {i:<4} {node.name:<38} ${node.cost:>5.0f}  {node.fix_time:>4} min")
    print(f"  {'─'*4} {'─'*38} {'─'*6}  {'─'*6}")
    print(f"  {'TOTAL':<43} ${total_cost:>5.0f}  {total_time:>4} min\n")
