# 01 — Introduction

## Project Title
**AI-Powered Device Troubleshooting Assistant using AO\* on AND-OR Graphs**

## Team
| Role | Responsibility |
|------|---------------|
| Gurtej Singh Lamba (2427030405) | Algorithm design, AO\* implementation, AND-OR graph construction |
| Abhiyansh Bhansali (2427030437) | Knowledge base, interactive session engine, comparison module, documentation |

## Motivation
Every user who owns a laptop, smartphone, or peripheral device will eventually face a hardware or software fault. The standard response is to search online or visit a repair shop. Both approaches share a critical flaw: **the fix is chosen without knowing its cost or likelihood of success**, leading to wasted time and money.

This project replaces random trial-and-error with a principled AI search strategy. By encoding domain knowledge into an **AND-OR graph** and searching it with the **AO\* algorithm**, the system always recommends the minimum-cost repair path first, replans instantly when a step fails, and can quantifiably show how much cost it saves over random fixing.

## Goals
1. Model device faults as AND-OR graphs where nodes represent sub-problems and leaves represent concrete repair actions.
2. Implement the AO\* algorithm to find the minimum-cost solution subgraph.
3. Support dynamic replanning when a suggested fix fails.
4. Demonstrate cost savings through statistical comparison with random-order fixing.

## Scope
The system currently covers four device categories:
- Laptop won't start
- WiFi not working
- Phone overheating
- Printer not printing

Each category is backed by a hand-curated knowledge base that can be extended without modifying the core algorithm.

## Technologies Used
| Component | Technology |
|-----------|-----------|
| Language | Python 3.10+ |
| Algorithm | AO\* (heuristic AND-OR search) |
| Graph model | Custom AND-OR graph library |
| PDF generation | fpdf2 |
| Interface | Terminal CLI |
