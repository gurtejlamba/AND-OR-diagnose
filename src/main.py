"""Entry point — device troubleshooting assistant CLI."""

from .knowledge_base import DEVICE_PROBLEMS
from .troubleshooter import Troubleshooter
from .comparison import run_comparison


def _pick_problem():
    print("\n  Select device problem:")
    for key, (name, _) in DEVICE_PROBLEMS.items():
        print(f"    {key}. {name}")
    return input("\n  Choice: ").strip()


def main():
    print("\n" + "═" * 62)
    print("   AI DEVICE TROUBLESHOOTING ASSISTANT")
    print("   AO* Algorithm on AND-OR Fault Graphs")
    print("═" * 62)

    while True:
        print("\n  MENU")
        print("  ────")
        print("  1  View optimal fix plan  (auto mode)")
        print("  2  Interactive session    (step-by-step with replanning)")
        print("  3  Compare AO* vs random  (cost analysis)")
        print("  4  Show AND-OR tree       (verbose plan)")
        print("  Q  Quit")

        choice = input("\n  Enter option: ").strip().upper()

        if choice == "Q":
            print("\n  Goodbye!\n")
            break

        elif choice in ("1", "2", "4"):
            key = _pick_problem()
            if key not in DEVICE_PROBLEMS:
                print("  Invalid problem number.")
                continue
            name, builder = DEVICE_PROBLEMS[key]
            t = Troubleshooter(builder(), verbose=(choice == "4"))
            if choice in ("1", "4"):
                t.show_plan()
            else:
                t.run_interactive()

        elif choice == "3":
            key = _pick_problem()
            if key not in DEVICE_PROBLEMS:
                print("  Invalid problem number.")
                continue
            name, builder = DEVICE_PROBLEMS[key]
            run_comparison(name, builder)

        else:
            print("  Unknown option — please try again.")
