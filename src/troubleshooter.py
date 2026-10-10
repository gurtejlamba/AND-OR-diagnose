from typing import List, Optional, Tuple
from .and_or_graph import Node, Status
from .ao_star import AOStar
from .visualizer import print_tree, print_solution_path


class Troubleshooter:
    """High-level wrapper: runs AO*, displays plans, drives interactive sessions."""

    def __init__(self, root: Node, verbose: bool = False):
        self.root = root
        self.verbose = verbose
        self.ao = AOStar(root)
        self.total_cost: float = 0.0
        self.total_time: int = 0
        self.log: List[Tuple[str, str, float]] = []  # (name, result, cost)

    # ──────────────────────────────────────────────────────────────────
    # Auto / plan mode
    # ──────────────────────────────────────────────────────────────────

    def show_plan(self):
        print(f"\n{'═'*62}")
        print(f"  DIAGNOSIS: {self.root.name}")
        print(f"{'═'*62}")
        if self.verbose:
            print("\n  AND-OR Problem Tree:\n")
            print_tree(self.root)
        path = self.ao.get_solution_path()
        if path:
            print("\n  AO* Optimal Fix Plan:")
            print_solution_path(path)
        else:
            print("  No solution found in knowledge base.")

    # ──────────────────────────────────────────────────────────────────
    # Interactive mode
    # ──────────────────────────────────────────────────────────────────

    def run_interactive(self):
        print(f"\n{'═'*62}")
        print(f"  INTERACTIVE TROUBLESHOOTING — {self.root.name}")
        print(f"{'═'*62}")
        print("  For each step: Y = fixed  |  N = didn't work  |  Q = quit\n")

        path = self.ao.get_solution_path()
        if not path:
            print("  No solution found in knowledge base.")
            return

        print("  Initial AO* plan:")
        print_solution_path(path)

        while path:
            step = path[0]
            print(f"  {'─'*58}")
            print(f"  NEXT STEP : {step.name}")
            print(f"  Cost      : ${step.cost:.0f}   Time: {step.fix_time} min")
            print(f"  Action    : {step.description}")
            print(f"  {'─'*58}")
            ans = input("  Result (Y/N/Q): ").strip().upper()

            if ans == "Q":
                print("\n  Session ended.")
                break

            elif ans == "Y":
                self.total_cost += step.cost
                self.total_time += step.fix_time
                self.log.append((step.name, "SUCCESS", step.cost))
                self.ao.mark_solved(step)
                print(f"  ✓ Step succeeded.  Running cost: ${self.total_cost:.0f}\n")

                if self.ao.is_solved:
                    print(f"  ✓✓ PROBLEM SOLVED! ✓✓")
                    break
                path = self.ao.get_solution_path() or []

            elif ans == "N":
                self.total_cost += step.cost
                self.total_time += step.fix_time
                self.log.append((step.name, "FAILED", step.cost))
                self.ao.mark_failed(step)
                print(f"  ✗ Step failed.  Replanning…\n")

                path = self.ao.get_solution_path()
                if path:
                    print("  New plan:")
                    print_solution_path(path)
                else:
                    print("  No more solution paths available.")
                    print("  Recommendation: seek professional repair service.")
                    break

        self._print_summary()

    # ──────────────────────────────────────────────────────────────────
    # Summary
    # ──────────────────────────────────────────────────────────────────

    def _print_summary(self):
        if not self.log:
            return
        print(f"\n{'═'*62}")
        print("  SESSION SUMMARY")
        print(f"{'═'*62}")
        print(f"  {'Step':<38} {'Result':<10} {'Cost':>6}")
        print(f"  {'─'*38} {'─'*10} {'─'*6}")
        for name, result, cost in self.log:
            print(f"  {name:<38} {result:<10} ${cost:>5.0f}")
        print(f"  {'─'*38} {'─'*10} {'─'*6}")
        print(f"  {'TOTAL':<38} {'':<10} ${self.total_cost:>5.0f}")
        print(f"  {'TIME SPENT':<38} {'':<10} {self.total_time:>4} min\n")
