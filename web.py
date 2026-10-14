#!/usr/bin/env python3
"""Web front end: serves web/index.html and a small JSON API over the AO* engine."""
import json
import math
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from src.ao_star import AOStar
from src.and_or_graph import Status
from src.comparison import simulate_random, get_ao_star_stats
from src.knowledge_base import DEVICE_PROBLEMS


def _index(node, nodes):
    """Depth-first ids so the client can refer to nodes across requests."""
    nodes.append(node)
    for child, _ in node.children:
        _index(child, nodes)
    return nodes


def build_state(problem, events):
    """Rebuild the tree, replay [(node_id, 'Y'|'N'), ...], return the full view."""
    root = DEVICE_PROBLEMS[problem][1]()
    ao = AOStar(root)
    nodes = _index(root, [])
    ids = {id(n): i for i, n in enumerate(nodes)}
    for node_id, result in events:
        leaf = nodes[node_id]
        if not leaf.is_leaf or leaf.status != Status.UNSOLVED:
            continue
        (ao.mark_solved if result == "Y" else ao.mark_failed)(leaf)

    path = ao.get_solution_path()
    on_plan = set()

    def mark_plan(n):
        if n.status == Status.SOLVED:
            return
        on_plan.add(id(n))
        for c in n.best_children:
            mark_plan(c)

    if not ao.is_failed:
        mark_plan(root)

    def ser(n, edge=0):
        return {
            "id": ids[id(n)], "name": n.name, "type": n.node_type.value,
            "cost": n.cost, "time": n.fix_time, "desc": n.description, "edge": edge,
            "f": None if math.isinf(n.f_cost) else n.f_cost,
            "status": n.status.value, "onPlan": id(n) in on_plan,
            "children": [ser(c, e) for c, e in n.children],
        }

    return {
        "tree": ser(root),
        "path": [ids[id(n)] for n in path],
        "solved": ao.is_solved,
        "failed": ao.is_failed,
    }


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=os.path.join(ROOT, "web"), **kw)

    def _json(self, obj, code=200):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/api/problems":
            return self._json([{"key": k, "name": v[0]} for k, v in DEVICE_PROBLEMS.items()])
        if url.path == "/api/compare":
            key = parse_qs(url.query).get("problem", [""])[0]
            if key not in DEVICE_PROBLEMS:
                return self._json({"error": "unknown problem"}, 400)
            builder = DEVICE_PROBLEMS[key][1]
            return self._json({"ao": get_ao_star_stats(builder),
                               "random": simulate_random(builder, num_trials=2000)})
        return super().do_GET()

    def do_POST(self):
        if urlparse(self.path).path != "/api/state":
            return self._json({"error": "not found"}, 404)
        try:
            req = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
            key = req["problem"]
            if key not in DEVICE_PROBLEMS:
                raise ValueError("unknown problem")
            events = [(int(i), r) for i, r in req.get("events", [])]
            return self._json(build_state(key, events))
        except (ValueError, KeyError, IndexError, TypeError) as e:
            return self._json({"error": str(e)}, 400)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Open http://localhost:{port}")
    HTTPServer(("127.0.0.1", port), Handler).serve_forever()
