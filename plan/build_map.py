"""Rebuild the child-page keyword plan from Divit's Semrush workbook.

Source: Emergent_Hub_Child_Pages_Final_v3.xlsx (Project context; NOT in this public repo,
Semrush data cannot be redistributed). Output: plan/keyword_map.json and plan/queue.csv,
both git-ignored. Run from the repo root:
    python3 plan/build_map.py /mnt/project/Emergent_Hub_Child_Pages_Final_v3.xlsx
Overrides (plan/overrides.json) reconcile the sheet with what is live, per Divit's decisions
of 2026-10-06: the 4 existing child pages keep their primaries, slugs and content.
"""
import json, re, sys, csv
import pandas as pd

SRC = sys.argv[1] if len(sys.argv) > 1 else "/mnt/project/Emergent_Hub_Child_Pages_Final_v3.xlsx"
HUB_PATH = {"LP": "/ai-landing-page-builder", "Form": "/ai-form-builder",
            "Auto": "/ai-automation-builder", "SurveyQuiz": "/ai-survey-and-quiz-builder"}  # live paths
SHEET_PATH = {"SurveyQuiz": "/ai-survey-quiz-builder"}  # the sheet's spelling, normalised below

def parse_secs(s):
    if not isinstance(s, str): return []
    out = []
    for part in s.split(";"):
        m = re.match(r"\s*(.+?)\s*\((\d+)\)\s*$", part)
        if m: out.append({"kw": m.group(1).strip(), "msv": int(m.group(2))})
    return out

def norm_url(u):
    u = str(u)
    for hub, sp in SHEET_PATH.items():
        if u.startswith(sp + "/"): u = HUB_PATH[hub] + u[len(sp):]
    return u

fin = pd.read_excel(SRC, "Final - all hubs", header=3)
bp = pd.read_excel(SRC, "Build plan", header=3)
kr = pd.read_excel(SRC, "Keyword report (pass 3)", header=3)
top = pd.read_excel(SRC, "Top ranking URLs", header=3)
amber = pd.read_excel(SRC, "AMBER pages & angles", header=2)
ov = json.load(open("plan/overrides.json"))

kr["url"] = kr["Page URL"].map(norm_url); top["url"] = top["Page URL"].map(norm_url)
bp["url"] = bp["URL"].map(norm_url); amber["url"] = amber["URL"].map(norm_url)
feat = {r.url: {"features": r["SERP features"], "codes": r["SERP feature codes"]}
        for _, r in kr[kr["Role"] == "Primary"].iterrows()}
top10 = {r.url: [r[f"#{i}"] for i in range(1, 11) if isinstance(r[f"#{i}"], str)] for _, r in top.iterrows()}
bpi = {r.url: r for _, r in bp.iterrows()}
ambi = {r.url: r["Evidence and action"] for _, r in amber.iterrows()}

pages = {}
for _, r in fin[fin["Page type"] != "Hub page"].iterrows():
    url = norm_url(r["URL slug"]); b = bpi.get(url)
    secs = parse_secs(r["All secondaries for content (absorbed + Semrush, by MSV)"])
    pages[url] = {
        "hub": r["Hub"], "url": url, "tier": r["Page type"], "display_name": r["Display name"],
        "primary": r["Primary keyword"], "primary_msv": int(r["Primary US MSV"]), "kd": None if pd.isna(r["KD"]) else float(r["KD"]),
        "intent": r["Intent"], "cluster": r["Cluster"], "secondaries": secs,
        "total_msv": int(r["Total MSV targeted by page"]),
        "wave": None if b is None else int(b["Wave"]), "verdict": None if b is None else b["SERP verdict"],
        "top10_mix": None if b is None else b["Top-10 mix (Semrush US, Oct 2026)"],
        "angle": None if b is None else (None if pd.isna(b["Angle and evidence"]) else b["Angle and evidence"]),
        "amber_evidence": ambi.get(url), "serp_features": feat.get(url, {}).get("features"),
        "top10": top10.get(url, []), "pass3_action": None if pd.isna(r["Pass 3 action"]) else r["Pass 3 action"],
        "notes": None if pd.isna(r["Notes"]) else r["Notes"], "status": "planned",
    }

# --- Wave 3 SERP report (Semrush top 10 for the 242 pages the final workbook did not pull) ---
import os as _os
W3 = next((c for c in [_os.environ.get("PE_WAVE3", ""), "/mnt/project/Emergent_Wave3_SERP_Report.xlsx", "private/Emergent_Wave3_SERP_Report.xlsx"] if c and _os.path.exists(c)), None)
if W3:
    v3 = pd.read_excel(W3, "Verdicts"); t3 = pd.read_excel(W3, "Top 10 URLs")
    t3["url"] = t3["URL"].map(norm_url); v3["url"] = v3["URL"].map(norm_url)
    tops3 = {r.url: [r[f"#{i}"] for i in range(1, 11) if isinstance(r[f"#{i}"], str)] for _, r in t3.iterrows()}
    for _, r in v3.iterrows():
        p = pages.get(r.url)
        if not p: continue
        verdict = str(r["Verdict"]); note = None if pd.isna(r["Evidence note"]) else str(r["Evidence note"])
        p["verdict"] = verdict; p["wave3_evidence"] = note
        p["top10_mix"] = f'{int(r["Issuer-owned"])} issuer-owned, {int(r["Builders / e-sign"])} builders/e-sign, {int(r["Template sites"])} template sites, {int(r["Other"])} other' if not pd.isna(r["Issuer-owned"]) else None
        if tops3.get(r.url): p["top10"] = tops3[r.url]
        if verdict.startswith("AMBER") and note: p["angle"] = note
        if verdict.startswith("RED") or verdict.startswith("MERGE"): p["status"] = "needs-decision"
        if verdict.startswith("No Semrush"): p["serp_needed"] = True

# --- watch-list and intent flags: attach guidance to every page whose primary the row names ---
wl = pd.read_excel(SRC, "Watch-list & intent flags", header=3)
for _, r in wl.iterrows():
    text = str(r["Keywords"]).lower()
    for p in pages.values():
        if re.search(r"(?<![a-z])" + re.escape(p["primary"].lower()) + r"(?![a-z])", text):
            p.setdefault("watch", []).append(f'{r["Type"]}: {r["Why flagged"]} Guidance: {r["Guidance"]}')

# --- overrides: reconcile with the live pages Divit keeps as-is ---
def kws(p): return {s["kw"].lower() for s in p["secondaries"]} | {p["primary"].lower()}
for o in ov["moves"]:          # move keywords from one URL to another (or create the live page entry)
    src = pages.get(o["from"]); dst = pages.setdefault(o["to"], o.get("create"))
    moved = [s for s in src["secondaries"] if s["kw"].lower() in {k.lower() for k in o["keywords"]}]
    src["secondaries"] = [s for s in src["secondaries"] if s not in moved]
    src["total_msv"] -= sum(s["msv"] for s in moved)
    if dst["primary"].lower() in {k.lower() for k in o["keywords"]}:
        moved = [s for s in moved if s["kw"].lower() != dst["primary"].lower()]
    dst["secondaries"] = sorted(dst["secondaries"] + moved, key=lambda s: -s["msv"])
    dst["total_msv"] = dst["primary_msv"] + sum(s["msv"] for s in dst["secondaries"])
    src.setdefault("overrides", []).append(f"moved {len(moved)+1} keywords to {o['to']} (live page kept as-is)")
    dst.setdefault("overrides", []).append(o["reason"])
for o in ov["swap_primary"]:   # keep the live primary; the sheet's primary becomes the first secondary
    p = pages[o["url"]]
    if p["primary"].lower() != o["live_primary"].lower():
        old = {"kw": p["primary"], "msv": p["primary_msv"]}
        live = next(s for s in p["secondaries"] if s["kw"].lower() == o["live_primary"].lower())
        p["secondaries"] = [old] + [s for s in p["secondaries"] if s is not live]
        p["primary"], p["primary_msv"] = live["kw"], live["msv"]
        p.setdefault("overrides", []).append(o["reason"])
for o in ov["off_plan_live"]:  # live pages the sheet cut; kept per Divit, excluded from the build queue
    pages[o["url"]] = {**o, "status": "live-off-plan", "secondaries": [], "total_msv": o["primary_msv"]}
for u in ov["live_urls"]: pages[u]["status"] = "live-draft"

# --- Wave 3 decisions: cuts and merges ---
for u in ov.get("wave3_cuts", {}).get("urls", []):
    if u in pages: pages[u]["status"] = "cut"; pages[u].setdefault("overrides", []).append("cut: " + ov["wave3_cuts"]["_why"])
for src, dst in ov.get("wave3_merges", {}).get("pairs", []):
    if src in pages and dst in pages:
        s_, d_ = pages[src], pages[dst]; have = {d_["primary"].lower()} | {x["kw"].lower() for x in d_["secondaries"]}
        for kw in [{"kw": s_["primary"], "msv": s_["primary_msv"]}] + s_["secondaries"]:
            if kw["kw"].lower() not in have: d_["secondaries"].append(kw); have.add(kw["kw"].lower())
        d_["secondaries"].sort(key=lambda x: -x["msv"]); d_["total_msv"] = d_["primary_msv"] + sum(x["msv"] for x in d_["secondaries"])
        d_.setdefault("overrides", []).append(f"absorbed {src} (cannibalization merge)")
        s_["status"] = "merged"; s_["merged_into"] = dst

# --- queue: descending volume; Wave 4 (needs a playable quiz) last ---
q = [p for p in pages.values() if p["status"] == "planned"]
q.sort(key=lambda p: (p["wave"] == 4, -p["total_msv"], -p["primary_msv"]))
for i, p in enumerate(q, 1): p["queue_rank"] = i
json.dump(pages, open("plan/keyword_map.json", "w"), indent=1, ensure_ascii=False)
with open("plan/queue.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["rank", "hub", "url", "primary", "primary_msv", "kd", "total_msv", "wave", "verdict", "capability_gap"])
    for p in q:
        mix = p["top10_mix"] if isinstance(p["top10_mix"], str) else ""; m = re.search(r"(\d+) document-template", mix); docs = int(m.group(1)) if m else 0
        txt = ((p["angle"] if isinstance(p["angle"], str) else "") + " " + (p["pass3_action"] if isinstance(p["pass3_action"], str) else "")).lower()
        gap = ("playable quiz" if p["wave"] == 4 else
               "generated document (template SERP)" if docs >= 2 or "doc-template" in txt or "generated output" in txt or "letter" in p["primary"] else "")
        w.writerow([p["queue_rank"], p["hub"], p["url"], p["primary"], p["primary_msv"], p["kd"], p["total_msv"], p["wave"], p["verdict"], gap])
print(f"pages: {len(pages)} | planned queue: {len(q)} | live-draft: {sum(p['status']=='live-draft' for p in pages.values())} | live-off-plan: {sum(p['status']=='live-off-plan' for p in pages.values())} | needs-decision: {sum(p['status']=='needs-decision' for p in pages.values())} | cut: {sum(p['status']=='cut' for p in pages.values())} | merged: {sum(p['status']=='merged' for p in pages.values())} | need a live SERP pull: {sum(1 for p in pages.values() if p.get('serp_needed'))}" + ("" if W3 else " | (Wave 3 report not found)"))
