# AI Device Troubleshooting Assistant
## AO* Algorithm on AND-OR Fault Graphs

### Quick Start
```bash
pip install -r requirements.txt
python run.py
```

### Generate Presentation PDF
```bash
python presentation/generate_pdf.py
# → presentation/5min_presentation_script.pdf
```

### Project Structure
```
aiscp/
├── run.py                       ← entry point
├── requirements.txt
├── src/
│   ├── and_or_graph.py          ← Node, NodeType, Status
│   ├── ao_star.py               ← AO* engine (cost propagation + replanning)
│   ├── knowledge_base.py        ← 4 device problem trees
│   ├── troubleshooter.py        ← CLI session manager
│   ├── visualizer.py            ← ASCII tree renderer
│   ├── comparison.py            ← Monte Carlo vs AO* comparison
│   └── main.py                  ← menu controller
├── docs/
│   ├── 01_introduction.md
│   ├── 02_problem_statement.md
│   ├── 03_algorithm_theory.md
│   ├── 04_system_design.md
│   ├── 05_implementation.md
│   ├── 06_testing_results.md
│   └── 07_conclusion.md
├── viva/
│   └── 100_viva_questions.md    ← 100 Q&A across 7 topics
└── presentation/
    ├── 5min_script.md           ← 2-person script (markdown)
    └── generate_pdf.py          ← run to produce PDF
```

### Menu Options
| Option | Description |
|--------|-------------|
| 1 | View AO* optimal fix plan (read-only) |
| 2 | Interactive session — attempt steps, trigger replanning |
| 3 | Monte Carlo comparison: AO* vs random fixing |
| 4 | Show full AND-OR tree with cost annotations |

### Device Problems Included
1. Laptop Won't Start
2. WiFi Not Working
3. Phone Overheating
4. Printer Not Printing
