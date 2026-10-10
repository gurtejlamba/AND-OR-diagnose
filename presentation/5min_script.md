# 5-Minute Presentation Script
## AI Device Troubleshooting Assistant using AO* on AND-OR Graphs
### Two-Person Script — Person A & Person B

---

**[SLIDE 1 — Title Slide]**

**Person A:**
Good morning, everyone. We are presenting our project titled "AI-Powered Device Troubleshooting Assistant using the AO Star Algorithm on AND-OR Graphs."

**Person B:**
My name is [Name], and this is [Name]. Our project applies a classical AI search technique to a very practical, everyday problem: figuring out why your device broke — and fixing it as cheaply as possible.

---

**[SLIDE 2 — The Problem]**

**Person A:**
Think about the last time your laptop refused to start. What did you do? You probably tried a few things at random — maybe you charged it, restarted it, or panicked. That random approach is the core problem we are solving.

One symptom like "laptop won't start" can have dozens of causes: a dead battery, a corrupted operating system, a loose RAM stick, or even a failed screen. And these fixes are not equal — a static discharge reset costs nothing and takes two minutes, while replacing the motherboard costs two hundred and eighty dollars.

**Person B:**
Choosing the expensive fix first when a free one would have worked wastes money. Our goal was to build a system that always recommends the minimum-cost repair path first and automatically replans if a step doesn't work.

---

**[SLIDE 3 — AI Approach: AND-OR Graphs]**

**Person B:**
We modelled each device fault as an AND-OR graph. Here is how it works.

An OR node means the fault can be caused by ANY ONE of its children — you fix whichever one is the actual cause. An AND node means ALL children must be addressed — both steps are required together.

For example: "Laptop Won't Start" is an OR node at the root — it could be a software issue, a power issue, a display issue, or a hardware issue.

**Person A:**
Each of those is itself an OR node with concrete repair actions as leaf nodes. "Software Issue" has three children: boot in safe mode at zero dollars, run startup repair at zero dollars, or reinstall the OS at zero dollars. "Hardware Issue" has children ranging from zero dollars to reseat the RAM all the way to two-hundred-eighty dollars to replace the motherboard.

Our Printer problem demonstrates AND nodes: diagnosing the connection requires you to reseat the cable AND reinstall the driver — both are mandatory, so both are children of an AND node.

---

**[SLIDE 4 — AO* Algorithm]**

**Person A:**
We search this AND-OR graph using the AO Star algorithm. AO Star assigns each node a cost estimate called f of n.

For leaf nodes, f equals the actual repair cost. For OR nodes, f equals the minimum cost among all children. For AND nodes, f equals the sum of all children's costs.

**Person B:**
The algorithm computes these values bottom-up — children first, parents after. The result is an optimal fix plan: a ranked list of repair actions starting with the cheapest.

When the user attempts a fix and it fails, we mark that leaf with infinite cost and propagate the change upward in O-of-depth time. The OR parent automatically picks its next-best child. This is replanning — instant, with no full restart needed.

---

**[SLIDE 5 — Live Example Trace]**

**Person B:**
Let us trace through a quick example. The root is "Laptop Won't Start." AO Star computes that the Software category has the lowest f value, so it recommends "Boot in Safe Mode" — cost zero, time ten minutes.

If the user tries it and it doesn't work, we mark it failed. Now the Software category tries "Run Startup Repair" — also zero dollars.

**Person A:**
If that also fails, and then Reinstall OS fails too, the entire Software category is marked failed. AO Star then moves to the Power category and recommends "Static Discharge Reset" — still zero dollars. Only after exhausting all free options does it suggest paid repairs, starting with the cheapest: Replace Charger at fifteen dollars, then Replace Battery at fifty dollars.

Throughout this entire process, the system has guided the user from free to expensive — not the other way around.

---

**[SLIDE 6 — Results and Comparison]**

**Person A:**
We ran a Monte Carlo simulation with two thousand trials to measure how much AO Star saves versus random-order fixing.

On the "Laptop Won't Start" problem, random users spent an average of one hundred and twelve dollars before finding the correct fix. The worst case was five hundred and fifteen dollars. AO Star's minimum-cost path starts at zero.

**Person B:**
Across all four device categories — laptop, WiFi, phone overheating, and printer — AO Star consistently delivers the minimum-cost fix path first. The simulation shows an average saving of over ninety percent compared to random trial-and-error.

---

**[SLIDE 7 — Conclusion]**

**Person B:**
To summarise: we built a complete AI troubleshooting assistant with an AND-OR graph knowledge base covering four device types, a correct AO Star implementation with dynamic replanning, an interactive CLI session, and a statistical comparison module.

**Person A:**
Future work includes adding success probabilities for a probabilistic model, a web frontend, and learning heuristics from repair history.

AO Star is a sixty-year-old algorithm — but it solves a very modern, very real problem better than most users solve it on their own. Thank you.

**[Both]:**
We welcome your questions.

---

> **Timing guide:**
> Slide 1 — 0:00–0:25  
> Slide 2 — 0:25–1:10  
> Slide 3 — 1:10–2:00  
> Slide 4 — 2:00–2:50  
> Slide 5 — 2:50–3:45  
> Slide 6 — 3:45–4:30  
> Slide 7 — 4:30–5:00  
