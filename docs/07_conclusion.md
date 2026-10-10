# 07 — Conclusion

## 7.1 Summary of Achievements

This project successfully built an AI-powered device troubleshooting assistant that demonstrates the practical value of heuristic AND-OR search in a real-world domain.

| Objective | Status |
|-----------|--------|
| Model device faults as AND-OR graphs | ✓ Complete — 4 problems, 16+ nodes each |
| Implement AO\* with correct cost propagation | ✓ Complete — bottom-up init + upward propagation |
| Support OR and AND decompositions | ✓ Complete — validated on Printer problem |
| Dynamic replanning on step failure | ✓ Complete — O(depth) per replan |
| Statistical comparison with random fixing | ✓ Complete — 2 000-trial Monte Carlo |
| Interactive CLI with session logging | ✓ Complete — Y/N/Q interface + summary |

## 7.2 Key Findings

1. **AO\* always recommends the cheapest fix first.** In all four device scenarios, the initial recommendation costs $0. This is not a coincidence — it is a guarantee of the algorithm's optimality.

2. **Replanning is seamless.** When a step fails, the system identifies the next minimum-cost path in O(depth) time without restarting from scratch. In a graph of depth 3, this is at most 3 node updates.

3. **Random fixing is significantly more expensive.** Across 2 000 simulations, users who try fixes randomly pay between $18 and $112 on average before finding the correct fix, versus $0 with AO\*.

4. **AND nodes are essential for realistic problems.** The printer problem demonstrated that purely OR-based models fail to capture scenarios where multiple diagnostic steps are mandatory.

## 7.3 Limitations

- **Knowledge base is static.** New device models or failure modes require manual graph updates.
- **Binary success/failure model.** Real repairs often have partial outcomes (e.g., "charger works for 30 min then stops"). The current model does not support probabilistic outcomes.
- **No learning.** The system does not update its heuristics based on past repair sessions.
- **Single fault assumption.** The system diagnoses one fault at a time. Compound faults (e.g., laptop with both a cracked screen and corrupted OS) are not modelled.

## 7.4 Future Work

| Enhancement | Description |
|-------------|-------------|
| Probabilistic AO\* (PAO\*) | Add success probabilities to each fix; minimise expected cost |
| Learning heuristics | Update `h_cost` values from historical session data |
| Web / mobile UI | Replace CLI with a React/Flutter frontend |
| NLP symptom input | Let users describe faults in natural language; map to graph nodes |
| Multi-fault diagnosis | Support AND-connected root problems |
| Expanded knowledge base | Add 20+ device categories via crowdsourced repair guides |

## 7.5 Learning Outcomes

This project reinforced the following AI concepts:
- **Problem decomposition** using AND-OR trees
- **Admissible heuristics** and their role in guaranteeing optimality
- **Cost back-propagation** as the mechanism for both planning and replanning
- **The difference between A\* and AO\***: A\* works on linear paths; AO\* handles branching AND/OR structures
- **Empirical evaluation**: Monte Carlo simulation as a way to compare algorithm performance against a baseline

## 7.6 References

1. Nilsson, N.J. (1980). *Principles of Artificial Intelligence*. Tioga Publishing. (Original AO\* formulation)
2. Russell, S. & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach*, 4th Ed. Pearson.
3. Martelli, A. & Montanari, U. (1978). "Optimizing decision trees through heuristically guided search." *Communications of the ACM*, 21(12), 1025-1039.
4. iFixit Repair Guides — https://www.ifixit.com (domain knowledge for repair costs and steps)
