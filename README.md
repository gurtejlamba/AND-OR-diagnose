# AI Device Troubleshooting Assistant
## AO* Algorithm on AND-OR Fault Graphs

### Quick Start
```bash
python web.py
# → open http://localhost:8000
```
The server uses only the standard library (`requirements.txt` is for the PDF/PPT generators).

### Generate Presentation PDF
```bash
python presentation/generate_pdf.py
# → presentation/5min_presentation_script.pdf
```

### Project Structure
```
aiscp/
├── web.py                       ← entry point: HTTP server + JSON API
├── web/index.html               ← interactive fault-tree UI
├── requirements.txt
├── src/
│   ├── and_or_graph.py          ← Node, NodeType, Status
│   ├── ao_star.py               ← AO* engine (cost propagation + replanning)
│   ├── knowledge_base.py        ← 4 device problem trees
│   └── comparison.py            ← Monte Carlo vs AO* comparison
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

### Using the web app
- Pick a device problem; the tree animates AO* costs flowing up and highlights the cheapest plan.
- Answer each step with **It worked (Y)** / **It didn't (N)**; AO* propagates the result and replans.
- **Run 2,000 random repairs** compares the AO* plan against trying fixes in random order.

### Device Problems Included
1. Laptop Won't Start
2. WiFi Not Working
3. Phone Overheating
4. Printer Not Printing
