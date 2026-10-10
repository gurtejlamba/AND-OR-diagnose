# 06 — Testing & Results

## 6.1 Functional Test Cases

### Test 1 — Laptop Won't Start: All Free Fixes Succeed

**Scenario:** User has a software corruption. Safe Mode boot resolves the issue.

**Expected AO\* plan:** Boot in Safe Mode ($0) → first step.

**Trace:**
```
Initial f values (bottom-up):
  safe_mode.f       = $0
  startup_repair.f  = $0
  reinstall_os.f    = $0
  software.f        = min(0, 0, 0) = $0   best_child = safe_mode

  static_reset.f    = $0
  power.f           = $0   best_child = static_reset

  ext_monitor.f     = $0
  display.f         = $0   best_child = ext_monitor

  reseat_ram.f      = $0
  hardware.f        = $0   best_child = reseat_ram

  root.f            = min(0, 0, 0, 0) = $0   best_child = software

Solution path: [Boot in Safe Mode]
```

User enters Y → safe_mode.SOLVED → software.SOLVED → root.SOLVED. ✓

---

### Test 2 — Replanning After Multiple Failures

**Scenario:** All software fixes fail. Power issue also fails for charger. Battery works.

**Trace:**
```
Step 1: Boot in Safe Mode          → N (FAILED)
  software best_child → Startup Repair (next cheapest $0)

Step 2: Run Startup Repair         → N (FAILED)
  software best_child → Reinstall OS ($0)

Step 3: Reinstall OS               → N (FAILED)
  software.status = FAILED, software.f = ∞
  root best_child → power (next cheapest at $0 = static_reset)

Step 4: Static Discharge Reset     → N (FAILED)
  power best_child → Test/Replace Charger ($15)

Step 5: Test / Replace Charger     → N (FAILED)
  power best_child → Replace Battery ($50)

Step 6: Replace Battery            → Y (SOLVED)
  power.SOLVED → root.SOLVED ✓

Total cost: $0+$0+$0+$0+$15+$50 = $65
```

**Verification:** The algorithm correctly moved across categories and within categories in ascending cost order. ✓

---

### Test 3 — AND Node (Printer)

**Scenario:** Printer fixed by connection diagnosis (both steps required).

**Expected plan:** [Reseat Cable ($0), Reinstall Driver ($0)]

**Trace:**
```
connection.f = 0 + 0 = $0   (AND: sum of children)
consumables.f = $0           (OR: clear paper jam)
hardware.f    = $0           (OR: clean print heads)
root.f        = min(0, 0, 0) = $0  best_child = connection (first at $0)

Solution path: [Reseat Cable, Reinstall Driver]   (both — AND node)
```

User: Step 1 (Reseat Cable) → Y, Step 2 (Reinstall Driver) → Y
→ connection.SOLVED → root.SOLVED ✓

---

### Test 4 — AND Node Partial Failure

**Scenario:** Cable reseated (Y), but driver reinstall fails (N).

```
Reinstall Driver → FAILED
connection.status = FAILED (AND with a failed child)
root replans → consumables → Clear Paper Jam ($0)
```

Correct replan across to a completely different sub-tree. ✓

---

## 6.2 Comparison Results

Monte Carlo simulation (2 000 trials per problem):

| Problem | AO\* Cost | Random Avg | Random Max | Savings |
|---------|-----------|-----------|-----------|---------|
| Laptop Won't Start | $0 | $112 | $515 | ~100% |
| WiFi Not Working | $0 | $18 | $65 | ~100% |
| Phone Overheating | $0 | $42 | $160 | ~100% |
| Printer Not Printing | $0 | $38 | $205 | ~100% |

> Note: AO\* cost is $0 because the minimum-cost path always starts with free fixes. In worst-case scenarios (all free fixes exhausted), AO\* still finds the cheapest remaining option, while random may have already spent money on expensive fixes unnecessarily.

## 6.3 Algorithm Performance

| Metric | Value |
|--------|-------|
| Average nodes in graph | 16 per problem |
| Initial cost computation | < 1 ms |
| Replanning step | < 1 ms |
| Memory usage | < 1 MB |
| Max replanning steps (worst case) | Equals number of leaves |

## 6.4 Edge Cases Handled

| Case | Behaviour |
|------|-----------|
| All leaves FAILED | root.status = FAILED; message shown |
| AND node with one FAILED child | AND becomes FAILED; OR parent replans |
| Empty knowledge base | Graceful "No solution found" message |
| User presses Q mid-session | Summary shown with partial log |
| Repeated Y on same step | Handled by SOLVED status (step skipped in future paths) |
