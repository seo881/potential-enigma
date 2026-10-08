"""alsoasked_schema.py: describe a saved AlsoAsked pull without printing its body.

  .venv/bin/python3 ops/alsoasked_schema.py private/alsoasked/<slug>.json

Prints every key path (list indices collapsed to []) with its JSON types, question-node counts per depth,
and one sample node with long strings truncated to 60 chars. The parser in qc/paa_gate.py is built from this output.
"""
import json, sys

def paths(o, p="", out=None):
    out = {} if out is None else out
    t = type(o).__name__
    out.setdefault(p or "$", set()).add(t)
    if isinstance(o, dict):
        for k, v in o.items(): paths(v, f"{p}.{k}" if p else k, out)
    elif isinstance(o, list):
        for v in o: paths(v, p + "[]", out)
    return out

def nodes(o, d=0, out=None):
    out = [] if out is None else out
    if isinstance(o, dict):
        isq = isinstance(o.get("question"), str)
        if isq: out.append((d + 1, o))
        for v in o.values(): nodes(v, d + 1 if isq else d, out)
    elif isinstance(o, list):
        for v in o: nodes(v, d, out)
    return out

def trunc(o):
    if isinstance(o, str): return o[:60]
    if isinstance(o, dict): return {k: ("[%d items]" % len(v) if isinstance(v, list) else trunc(v)) for k, v in o.items()}
    return o

if __name__ == "__main__":
    d = json.load(open(sys.argv[1]))
    for p, ts in sorted(paths(d).items()): print(f"{p:70s} {'|'.join(sorted(ts))}")
    ns = nodes(d); counts = {}
    for dep, _ in ns: counts[dep] = counts.get(dep, 0) + 1
    print("question nodes per depth:", ", ".join(f"d{k}={v}" for k, v in sorted(counts.items())) or "none")
    if ns: print("sample node:", json.dumps(trunc(ns[0][1]), ensure_ascii=False))
