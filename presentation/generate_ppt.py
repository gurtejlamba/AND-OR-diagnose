#!/usr/bin/env python3
"""
Generate a PowerPoint presentation for the AO* Troubleshooting project.
Run:    python presentation/generate_ppt.py
Output: presentation/AO_Star_Troubleshooting.pptx
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

# ── Colour palette ───────────────────────────────────────────────────
NAVY    = RGBColor(0x0F, 0x28, 0x50)
BLUE    = RGBColor(0x1A, 0x5C, 0xA8)
ACCENT  = RGBColor(0x00, 0xB0, 0xF0)
WHITE   = RGBColor(0xFF, 0xFF, 0xFF)
DARK    = RGBColor(0x1E, 0x1E, 0x1E)
GRAY    = RGBColor(0x60, 0x60, 0x60)
GREEN   = RGBColor(0x00, 0x7A, 0x3D)
RED     = RGBColor(0xC0, 0x20, 0x20)
LGRAY   = RGBColor(0xF0, 0xF3, 0xF7)
YELLOW  = RGBColor(0xFF, 0xC0, 0x00)

W = Inches(13.33)   # widescreen width
H = Inches(7.5)     # widescreen height


# ── Helpers ──────────────────────────────────────────────────────────

def add_rect(slide, l, t, w, h, fill=NAVY, alpha=None):
    shape = slide.shapes.add_shape(1, Inches(l), Inches(t), Inches(w), Inches(h))
    shape.line.fill.background()
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    return shape


def add_text(slide, text, l, t, w, h,
             size=24, bold=False, color=WHITE, align=PP_ALIGN.LEFT,
             italic=False, wrap=True):
    txb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    txb.word_wrap = wrap
    tf = txb.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return txb


def add_bullet_box(slide, items, l, t, w, h,
                   size=20, color=DARK, title=None, title_color=NAVY):
    txb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    txb.word_wrap = True
    tf = txb.text_frame
    tf.word_wrap = True

    first = True
    if title:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.alignment = PP_ALIGN.LEFT
        run = p.add_run()
        run.text = title
        run.font.size = Pt(size + 2)
        run.font.bold = True
        run.font.color.rgb = title_color

    for item in items:
        p = tf.paragraphs[0] if (first and not title) else tf.add_paragraph()
        first = False
        p.alignment = PP_ALIGN.LEFT
        p.level = 0
        run = p.add_run()
        run.text = item
        run.font.size = Pt(size)
        run.font.color.rgb = color
    return txb


def slide_bg(slide, fill=LGRAY):
    bg = slide.background
    fill_obj = bg.fill
    fill_obj.solid()
    fill_obj.fore_color.rgb = fill


def header_bar(slide, title, subtitle=None):
    add_rect(slide, 0, 0, 13.33, 1.4, fill=NAVY)
    add_text(slide, title, 0.4, 0.12, 12, 0.7,
             size=32, bold=True, color=WHITE)
    if subtitle:
        add_text(slide, subtitle, 0.4, 0.8, 12, 0.5,
                 size=16, color=ACCENT, bold=False)
    add_rect(slide, 0, 1.4, 13.33, 0.06, fill=ACCENT)


def footer_bar(slide, text="AI Device Troubleshooting Assistant  |  AO* on AND-OR Graphs"):
    add_rect(slide, 0, 7.2, 13.33, 0.3, fill=NAVY)
    add_text(slide, text, 0.3, 7.22, 12, 0.26,
             size=10, color=ACCENT, align=PP_ALIGN.LEFT)


# ── Slide builders ───────────────────────────────────────────────────

def slide_title(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    # Full navy background
    add_rect(slide, 0, 0, 13.33, 7.5, fill=NAVY)
    # Accent stripe
    add_rect(slide, 0, 5.5, 13.33, 0.12, fill=ACCENT)
    # Decorative circle
    from pptx.util import Inches as I
    shape = slide.shapes.add_shape(9, I(10.5), I(0.3), I(2.8), I(2.8))
    shape.fill.solid(); shape.fill.fore_color.rgb = BLUE
    shape.line.fill.background()

    add_text(slide, "AI Device Troubleshooting", 0.6, 1.2, 10, 1.0,
             size=44, bold=True, color=WHITE)
    add_text(slide, "Assistant", 0.6, 2.1, 10, 0.9,
             size=44, bold=True, color=ACCENT)
    add_text(slide, "Using AO* Algorithm on AND-OR Fault Graphs",
             0.6, 3.1, 10, 0.6, size=22, color=RGBColor(0xCC, 0xDD, 0xFF))
    add_rect(slide, 0.6, 3.85, 4.5, 0.05, fill=ACCENT)
    add_text(slide, "AISC Project Presentation  |  2026",
             0.6, 4.0, 8, 0.5, size=16, color=GRAY)
    add_text(slide, "Member 1  &  Member 2",
             0.6, 4.6, 8, 0.5, size=18, color=WHITE, bold=True)


def slide_problem(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide_bg(slide)
    header_bar(slide, "The Problem", "Why random fixing is expensive and unreliable")
    footer_bar(slide)

    # Left column
    add_rect(slide, 0.4, 1.6, 5.8, 4.8, fill=WHITE)
    add_bullet_box(slide, [
        "One symptom = many possible causes",
        "",
        "Laptop won't start could be:",
        "   - Corrupted OS  ($0 to fix)",
        "   - Dead battery   ($50 to fix)",
        "   - Cracked screen ($120 to fix)",
        "   - Failed board   ($280 to fix)",
        "",
        "Fixes are also inter-dependent:",
        "   - Some are alternatives (OR)",
        "   - Some are sequential steps (AND)",
    ], 0.6, 1.7, 5.4, 4.5, size=17, color=DARK,
       title="The Diagnosis Challenge", title_color=NAVY)

    # Right column
    add_rect(slide, 6.9, 1.6, 6.0, 4.8, fill=WHITE)
    add_bullet_box(slide, [
        "Users try fixes in random order",
        "",
        "Random avg cost:   $272",
        "Random worst case: $535",
        "Random avg time:   223 min",
        "",
        "AO* optimal cost:  $0",
        "AO* time:          10 min",
        "",
        "Savings:  ~100% cost",
        "           ~213 minutes",
    ], 7.1, 1.7, 5.6, 4.5, size=17, color=DARK,
       title="The Cost of Random Fixing", title_color=RED)

    add_text(slide, "VS", 6.05, 3.6, 0.9, 0.9,
             size=28, bold=True, color=NAVY, align=PP_ALIGN.CENTER)


def slide_approach(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide_bg(slide)
    header_bar(slide, "AI Approach: AND-OR Graphs",
               "Encoding device faults as a structured search problem")
    footer_bar(slide)

    # OR box
    add_rect(slide, 0.4, 1.7, 3.9, 2.2, fill=BLUE)
    add_text(slide, "OR Node", 0.6, 1.8, 3.5, 0.5,
             size=20, bold=True, color=WHITE)
    add_text(slide,
             "Problem solved when ANY ONE\nchild is resolved.\n\n"
             "Example: 'Laptop Won't Start'\ncould be power OR software\nOR display OR hardware.",
             0.6, 2.3, 3.5, 1.5, size=14, color=WHITE)

    # AND box
    add_rect(slide, 4.7, 1.7, 3.9, 2.2, fill=GREEN)
    add_text(slide, "AND Node", 4.9, 1.8, 3.5, 0.5,
             size=20, bold=True, color=WHITE)
    add_text(slide,
             "Problem solved only when ALL\nchildren are resolved.\n\n"
             "Example: 'Printer Connection'\nneeds cable reseated AND\ndriver reinstalled.",
             4.9, 2.3, 3.5, 1.5, size=14, color=WHITE)

    # LEAF box
    add_rect(slide, 9.0, 1.7, 3.9, 2.2, fill=RGBColor(0x7B, 0x2D, 0x8B))
    add_text(slide, "LEAF Node", 9.2, 1.8, 3.5, 0.5,
             size=20, bold=True, color=WHITE)
    add_text(slide,
             "A concrete repair action\nwith a known cost and time.\n\n"
             "Example: 'Replace Battery'\n  Cost: $50\n  Time: 30 min",
             9.2, 2.3, 3.5, 1.5, size=14, color=WHITE)

    # Tree diagram
    add_rect(slide, 0.4, 4.1, 12.5, 2.8, fill=WHITE)
    add_text(slide, "Example Tree: Laptop Won't Start", 0.6, 4.15, 12, 0.4,
             size=14, bold=True, color=NAVY)
    tree = (
        "[OR]  Laptop Won't Start\n"
        "   [OR]  Software Issue   -> Boot Safe Mode $0  |  Startup Repair $0  |  Reinstall OS $0\n"
        "   [OR]  Power Issue      -> Static Reset $0    |  Charger $15        |  Battery $50\n"
        "   [OR]  Display Issue    -> Ext. Monitor $0    |  Reseat Cable $0    |  Screen $120\n"
        "   [OR]  Hardware Issue   -> Reseat RAM $0      |  Replace SSD $70    |  Motherboard $280"
    )
    add_text(slide, tree, 0.6, 4.55, 12.5, 2.3, size=13,
             color=DARK)


def slide_algorithm(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide_bg(slide)
    header_bar(slide, "AO* Algorithm",
               "Heuristic search that finds the minimum-cost solution subgraph")
    footer_bar(slide)

    # Cost formulas
    add_rect(slide, 0.4, 1.6, 5.9, 3.5, fill=NAVY)
    add_text(slide, "Cost Propagation Rules", 0.65, 1.7, 5.4, 0.5,
             size=18, bold=True, color=ACCENT)
    formulas = [
        "LEAF node:",
        "  f(n) = actual repair cost",
        "",
        "OR node:",
        "  f(n) = MIN over children c of",
        "         [ edge_cost + f(c) ]",
        "",
        "AND node:",
        "  f(n) = SUM over all children c of",
        "         [ edge_cost + f(c) ]",
    ]
    add_bullet_box(slide, formulas, 0.65, 2.2, 5.5, 2.7,
                   size=15, color=WHITE)

    # Steps
    add_rect(slide, 6.7, 1.6, 6.2, 3.5, fill=WHITE)
    add_text(slide, "Algorithm Steps", 6.95, 1.7, 5.7, 0.5,
             size=18, bold=True, color=NAVY)
    steps = [
        "1.  Build the AND-OR graph (knowledge base)",
        "2.  Compute all f(n) values bottom-up",
        "     (leaves first, root last)",
        "3.  Extract solution path following",
        "     best_child at each OR node,",
        "     all children at each AND node",
        "4.  User attempts each step (Y / N)",
        "5.  On FAIL: mark node f = infinity,",
        "     propagate up in O(depth) time",
        "6.  Re-extract path -> instant replan",
    ]
    add_bullet_box(slide, steps, 6.95, 2.2, 5.7, 2.7,
                   size=14, color=DARK)

    # Properties bar
    add_rect(slide, 0.4, 5.3, 12.5, 1.5, fill=BLUE)
    props = [
        ("Complete", "Finds solution if one exists"),
        ("Optimal", "Minimum cost guaranteed (admissible h)"),
        ("Replan", "O(depth) per failed step"),
        ("Practical", "< 1ms per operation"),
    ]
    for i, (label, desc) in enumerate(props):
        x = 0.6 + i * 3.1
        add_text(slide, label, x, 5.38, 2.9, 0.45,
                 size=15, bold=True, color=YELLOW)
        add_text(slide, desc, x, 5.8, 2.9, 0.9,
                 size=12, color=WHITE)


def slide_example(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide_bg(slide)
    header_bar(slide, "Live Example: Laptop Won't Start",
               "AO* guides from free fixes to paid — never the other way")
    footer_bar(slide)

    steps = [
        ("Step 1", "Boot in Safe Mode",         "$0",   "10 min", GREEN,  "AO* initial recommendation"),
        ("Step 2", "Run Startup Repair",         "$0",   "30 min", GREEN,  "After Step 1 fails -> replan"),
        ("Step 3", "Reinstall OS",               "$0",   "90 min", GREEN,  "After Step 2 fails -> replan"),
        ("Step 4", "Static Discharge Reset",     "$0",   "3 min",  BLUE,   "Software exhausted -> move to Power"),
        ("Step 5", "Test / Replace Charger",     "$15",  "5 min",  BLUE,   "After Step 4 fails -> replan"),
        ("Step 6", "Replace Battery",            "$50",  "30 min", BLUE,   "After Step 5 fails -> replan"),
        ("Step 7", "Reseat RAM",                 "$0",   "15 min", RGBColor(0x7B,0x2D,0x8B), "Power exhausted -> Hardware"),
        ("Step 8", "Replace Motherboard",        "$280", "120 min",RED,    "Absolute last resort"),
    ]

    # Header row
    add_rect(slide, 0.4, 1.55, 12.5, 0.45, fill=NAVY)
    for label, cw, cx in [
        ("Step", 0.7, 0.5), ("Fix Action", 2.0, 4.5),
        ("Cost", 0.8, 8.0), ("Time", 1.0, 9.2), ("Note", 3.5, 10.3)
    ]:
        add_text(slide, label, cx, 1.58, cw, 0.38,
                 size=13, bold=True, color=WHITE)

    for i, (step, name, cost, time, color, note) in enumerate(steps):
        y = 2.05 + i * 0.6
        bg = LGRAY if i % 2 == 0 else WHITE
        add_rect(slide, 0.4, y, 12.5, 0.57, fill=bg)
        add_rect(slide, 0.4, y, 1.5, 0.57, fill=color)
        add_text(slide, step, 0.45, y + 0.07, 1.4, 0.45,
                 size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        add_text(slide, name,  2.05, y + 0.07, 5.8, 0.45, size=13, color=DARK)
        add_text(slide, cost,  8.05, y + 0.07, 0.9, 0.45, size=13, color=DARK, align=PP_ALIGN.CENTER)
        add_text(slide, time,  9.25, y + 0.07, 1.0, 0.45, size=13, color=DARK, align=PP_ALIGN.CENTER)
        add_text(slide, note, 10.35, y + 0.07, 2.5, 0.45, size=11, color=GRAY)


def slide_replan(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide_bg(slide)
    header_bar(slide, "Dynamic Replanning",
               "AO* instantly adapts when a repair step fails")
    footer_bar(slide)

    stages = [
        ("Initial Plan", NAVY, [
            "AO* computes f values bottom-up",
            "Recommends: Boot in Safe Mode ($0)",
            "All free software fixes tried first",
        ]),
        ("Step Fails (N)", RED, [
            "User marks step as FAILED",
            "f(leaf) = infinity",
            "Propagate up in O(depth) steps",
        ]),
        ("OR Node Updates", BLUE, [
            "OR parent skips failed child",
            "Selects next-best child",
            "f(parent) automatically updated",
        ]),
        ("New Plan Ready", GREEN, [
            "Re-extract path from root",
            "Next cheapest fix shown",
            "No full restart needed",
        ]),
    ]

    for i, (title, color, bullets) in enumerate(stages):
        x = 0.4 + i * 3.2
        add_rect(slide, x, 1.6, 3.0, 1.0, fill=color)
        add_text(slide, title, x + 0.1, 1.7, 2.8, 0.8,
                 size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        add_rect(slide, x, 2.6, 3.0, 2.8, fill=WHITE)
        add_bullet_box(slide, bullets, x + 0.1, 2.7, 2.8, 2.6,
                       size=14, color=DARK)
        if i < 3:
            add_text(slide, "->", x + 3.0, 2.8, 0.2, 0.6,
                     size=22, bold=True, color=NAVY, align=PP_ALIGN.CENTER)

    # AND node callout
    add_rect(slide, 0.4, 5.6, 12.5, 1.4, fill=NAVY)
    add_text(slide, "AND Node Behaviour on Failure:", 0.7, 5.68, 4, 0.5,
             size=15, bold=True, color=ACCENT)
    add_text(slide,
             "If ANY child of an AND node fails -> entire AND node is marked FAILED.\n"
             "Its OR parent then looks for the next alternative sub-tree. "
             "This correctly models mandatory sequential steps.",
             0.7, 6.1, 12, 0.8, size=14, color=WHITE)


def slide_results(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide_bg(slide)
    header_bar(slide, "Results: AO* vs Random Fixing",
               "Monte Carlo simulation — 2,000 trials per device problem")
    footer_bar(slide)

    data = [
        ("Laptop Won't Start",   "$0",  "$272", "$535", "~100%"),
        ("WiFi Not Working",     "$0",  "$18",  "$65",  "~100%"),
        ("Phone Overheating",    "$0",  "$42",  "$160", "~100%"),
        ("Printer Not Printing", "$0",  "$38",  "$205", "~100%"),
    ]

    # Table header
    add_rect(slide, 0.4, 1.6, 12.5, 0.55, fill=NAVY)
    cols = [
        ("Device Problem",     3.5, 0.5),
        ("AO* Cost",           1.5, 4.1),
        ("Random Avg",         1.5, 5.7),
        ("Random Worst",       1.8, 7.3),
        ("Cost Saved",         1.8, 9.2),
    ]
    for label, w, x in cols:
        add_text(slide, label, x, 1.65, w, 0.45,
                 size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

    for i, (prob, ao, avg, worst, saved) in enumerate(data):
        y = 2.2 + i * 0.72
        bg = LGRAY if i % 2 == 0 else WHITE
        add_rect(slide, 0.4, y, 12.5, 0.68, fill=bg)
        add_text(slide, prob, 0.55, y + 0.1, 3.4, 0.5, size=14, color=DARK, bold=True)
        add_text(slide, ao,    4.1, y + 0.1, 1.5, 0.5, size=14, color=GREEN,
                 bold=True, align=PP_ALIGN.CENTER)
        add_text(slide, avg,   5.7, y + 0.1, 1.5, 0.5, size=14, color=DARK,
                 align=PP_ALIGN.CENTER)
        add_text(slide, worst, 7.3, y + 0.1, 1.8, 0.5, size=14, color=RED,
                 align=PP_ALIGN.CENTER)
        add_text(slide, saved, 9.2, y + 0.1, 1.8, 0.5, size=14, color=GREEN,
                 bold=True, align=PP_ALIGN.CENTER)

    # Key insight
    add_rect(slide, 0.4, 5.15, 12.5, 1.65, fill=BLUE)
    add_text(slide, "Key Insight", 0.7, 5.25, 3, 0.5,
             size=16, bold=True, color=YELLOW)
    add_text(slide,
             "AO* always starts with the cheapest available fix (often free). "
             "Random users may attempt a $280 motherboard replacement before trying a free "
             "static discharge reset. AO* eliminates this by construction — "
             "the minimum-cost path is guaranteed optimal by the admissible heuristic.",
             0.7, 5.7, 12, 1.0, size=14, color=WHITE)


def slide_architecture(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide_bg(slide)
    header_bar(slide, "System Architecture",
               "Modular Python design — knowledge base is independent of the algorithm")
    footer_bar(slide)

    modules = [
        ("and_or_graph.py",  0.4,  1.7, "Data Structures\nNode, NodeType, Status",             NAVY),
        ("ao_star.py",       0.4,  3.2, "AO* Engine\nCost propagation + replanning",           BLUE),
        ("knowledge_base.py",4.6,  1.7, "Domain Knowledge\n4 device problem trees",             GREEN),
        ("troubleshooter.py",4.6,  3.2, "CLI Session\nInteractive Y/N + summary",              RGBColor(0x7B,0x2D,0x8B)),
        ("comparison.py",    8.8,  1.7, "Monte Carlo\nAO* vs random simulation",               RGBColor(0xC0,0x60,0x00)),
        ("visualizer.py",    8.8,  3.2, "Rendering\nASCII tree + solution table",              GRAY),
        ("main.py",          4.6,  4.7, "Menu Controller\nTop-level flow control",             NAVY),
    ]

    for name, x, y, desc, color in modules:
        add_rect(slide, x, y, 3.8, 1.25, fill=color)
        add_text(slide, name, x + 0.15, y + 0.08, 3.5, 0.45,
                 size=14, bold=True, color=WHITE)
        add_text(slide, desc, x + 0.15, y + 0.55, 3.5, 0.65,
                 size=12, color=WHITE)

    add_rect(slide, 0.4, 5.9, 12.5, 1.1, fill=WHITE)
    add_text(slide, "run.py", 0.6, 5.97, 1.5, 0.4,
             size=14, bold=True, color=NAVY)
    add_text(slide,
             "Entry point:  python run.py\n"
             "Presentation PDF:  python presentation/generate_pdf.py",
             2.2, 5.97, 10.5, 0.9, size=14, color=DARK)


def slide_conclusion(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide_bg(slide)
    header_bar(slide, "Conclusion & Future Work",
               "AO* delivers optimal, adaptive device troubleshooting")
    footer_bar(slide)

    # Achievements
    add_rect(slide, 0.4, 1.6, 6.0, 4.8, fill=WHITE)
    add_bullet_box(slide, [
        "AND-OR graph knowledge base",
        "  covering 4 device categories",
        "",
        "AO* with dynamic replanning",
        "  O(depth) per failed step",
        "",
        "Interactive CLI session",
        "  Y / N / Q per step + summary",
        "",
        "Monte Carlo comparison",
        "  ~100% cost savings vs random",
        "",
        "100 viva Q&A + PDF script",
    ], 0.6, 1.7, 5.6, 4.6, size=16, color=DARK,
       title="Achievements", title_color=NAVY)

    # Future work
    add_rect(slide, 6.9, 1.6, 6.0, 4.8, fill=NAVY)
    add_bullet_box(slide, [
        "Probabilistic AO* (PAO*)",
        "  Add success probability per fix",
        "  Minimise expected cost",
        "",
        "Web / Mobile Frontend",
        "  Replace CLI with React / Flutter",
        "",
        "NLP Symptom Input",
        "  Natural language -> graph node",
        "",
        "Learned Heuristics",
        "  Update h(n) from session logs",
        "",
        "Expanded Knowledge Base",
        "  20+ device categories",
    ], 7.1, 1.7, 5.6, 4.6, size=15, color=WHITE,
       title="Future Work", title_color=ACCENT)


def slide_thankyou(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_rect(slide, 0, 0, 13.33, 7.5, fill=NAVY)
    add_rect(slide, 0, 6.0, 13.33, 0.12, fill=ACCENT)

    add_text(slide, "Thank You", 0, 1.5, 13.33, 1.5,
             size=60, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_text(slide, "We welcome your questions.",
             0, 3.1, 13.33, 0.8, size=24, color=ACCENT, align=PP_ALIGN.CENTER)
    add_rect(slide, 4.0, 4.1, 5.33, 0.06, fill=ACCENT)
    add_text(slide,
             "github.com/gurtejlamba/AND-OR-diagnose\n"
             "python run.py  ->  try it live",
             0, 4.4, 13.33, 1.0, size=18,
             color=RGBColor(0xCC, 0xDD, 0xFF), align=PP_ALIGN.CENTER)


# ── Main ─────────────────────────────────────────────────────────────

def build_ppt(out_path: str):
    prs = Presentation()
    prs.slide_width  = Inches(13.33)
    prs.slide_height = Inches(7.5)

    slide_title(prs)
    slide_problem(prs)
    slide_approach(prs)
    slide_algorithm(prs)
    slide_example(prs)
    slide_replan(prs)
    slide_results(prs)
    slide_architecture(prs)
    slide_conclusion(prs)
    slide_thankyou(prs)

    prs.save(out_path)
    print(f"PPT created: {out_path}  ({len(prs.slides)} slides)")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(script_dir, "AO_Star_Troubleshooting.pptx")
    build_ppt(out)
