"""paa_phase2.py: AlsoAsked Phase 2 over every pulled written page (Divit, 2026-10-08). No API calls.

  .venv/bin/python3 ops/paa_phase2.py

Order: paa-resource (provenance, reclassify; text byte-identical) -> gate on the pull -> synonym candidates ->
gate on the FAQ strict and with SAFE candidates -> QC re-run (must stay TOTAL 0) -> audit/paa/summary.md and
.cache/review/paa.csv (one row per page). No question text in either output.
"""
import csv, json, os, re, subprocess, sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "ops")); sys.path.insert(0, os.path.join(ROOT, "qc"))
import guards as G, paa_gate as P

WRITTEN = {"images", "reviewed", "challenged", "approved", "rework", "cms_draft", "published"}
VD = os.path.join(ROOT, "private", "alsoasked", "verdicts")
# risk tags from handover 3.5-3.6 and logs/writers-2026-10-07.md, plus detection in the copy
LEGAL_MEDICAL = {"surgery-consent-form", "photo-release-form", "tattoo-consent-form", "esthetician-intake-form", "drug-test-consent-form",
                 "sublease-form", "tenant-screening-form", "personal-injury-intake-form", "telemedicine-consent-form", "car-rental-form",
                 "rental-history-form", "anesthesia-consent-form", "copyright-release-form", "permanent-makeup-consent-form", "cobra-election-form",
                 "nda-form", "rental-agreement-form", "advance-directive-form", "liability-waiver-form", "consent-form", "dental-intake-form"}
LM_WORDS = ["consent", "waiver", "release", "agreement", "contract", "nda", "lease", "sublease", "directive", "hipaa", "medical", "patient",
            "dental", "surgery", "anesthesia", "telemedicine", "injury", "legal", "attorney", "affidavit", "notary", "cobra", "intake", "health", "will"]
ROLLING = {"mileage-reimbursement-form", "travel-reimbursement-form", "cobra-election-form", "payroll-change-form", "overtime-request-form",
           "telemedicine-consent-form", "food-bank-application-form", "tenant-screening-form"}

def sh(*a): return subprocess.run([sys.executable, os.path.join(ROOT, "ops", "hubctl.py"), *a], capture_output=True, text=True)

def page_metrics(slug, suffix):
    v = json.load(open(os.path.join(VD, slug + suffix + ".json")))
    on = [i for i in v["items"] if i["verdict"] != "reject"]
    rej = Counter(r["rule"] for i in v["items"] if i["verdict"] == "reject" for r in i["reasons"] if r["kind"] == "reject")
    pa7 = sum(any(r["rule"] == "PA7" and r["kind"] == "flag" for r in i["reasons"]) for i in v["items"])
    return {"on": len(on), "replace": len(v["items"]) - len(on), "park": len(on) < P.MIN_ON_TOPIC, "pa7": pa7, "rej": rej, "flags": v["counts"]["flag"]}

def risk(s):
    slug = s["url"].rsplit("/", 1)[1]; prim = (s.get("keywords") or {}).get("primary", "")
    text = " ".join(v for v in (s.get("fields") or {}).values() if isinstance(v, str))
    tags = []
    if slug in LEGAL_MEDICAL or any(re.search(r"\b" + w + r"\b", prim) for w in LM_WORDS): tags.append("legal/medical")
    if slug in ROLLING or re.search(r"\b(FY ?20\d\d|202[6-9] (rate|limit|wage|rule|per diem))\b", text, re.I): tags.append("rolling-figures")
    live = {x["url"] for x in G.all_specs() if x.get("status") in ("live-draft", "published")}
    hubs = tuple(h["path"] + "/" for h in json.load(open(os.path.join(ROOT, "config", "collections.json")))["hubs"].values())
    links = {m for m in re.findall(r"href=\\?[\"'](?:https?://(?:www\.)?emergent\.sh)?(/[a-z0-9/-]+)", text) if m.startswith(hubs) and m != s["url"]}
    unpub = sorted(l for l in links if l not in live)
    if unpub: tags.append(f"unpublished-links:{len(unpub)}")
    return tags

def main():
    st = G.all_status()
    pages = [s for s in G.all_specs() if s.get("status") != "live-draft" and st.get(s["url"], {}).get("state") in WRITTEN
             and os.path.exists(P.pull_path(s["url"].rsplit("/", 1)[1]))]
    unpulled = [s["url"] for s in G.all_specs() if s.get("status") != "live-draft" and st.get(s["url"], {}).get("state") in WRITTEN
                and not os.path.exists(P.pull_path(s["url"].rsplit("/", 1)[1]))]
    print(f"{len(pages)} pulled written pages; {len(unpulled)} written pages without a pull", flush=True)
    errs = []
    for s in pages:
        r = sh("paa-resource", s["url"])
        if r.returncode: errs.append((s["url"], "paa-resource", r.stderr.strip()[-160:]))
    for s in pages: sh("paa", s["url"], "--quiet")
    P.synonym_candidates([s["url"] for s in pages])
    for s in pages: sh("paa", s["url"], "--spec", "--quiet"); sh("paa", s["url"], "--spec", "--cand", "--quiet")
    qcfail = []
    for s in G.all_specs():
        if s["url"] in {p["url"] for p in pages}:
            r = subprocess.run([sys.executable, os.path.join(ROOT, "qc", "qc_hub.py"), s["_path"]], capture_output=True, text=True)
            if r.returncode: qcfail.append((s["url"], sorted({m.group(2) for m in re.finditer(r"^  (P0|P1) (\S+)", r.stdout, re.M)})))
    rows = []
    for s in G.all_specs():
        if s["url"] not in {p["url"] for p in pages}: continue
        slug = s["url"].rsplit("/", 1)[1]; a, b = page_metrics(slug, ".faq"), page_metrics(slug, ".faq.cand")
        pull = json.load(open(os.path.join(VD, slug + ".json")))["counts"]
        rows.append({"hub": P.hub_of(s["url"])[0], "url": s["url"], "state": st[s["url"]]["state"],
                     "pull_pass": pull["pass"], "pull_reject": pull["reject"], "pull_flag": pull["flag"],
                     "on_topic_strict": a["on"], "replace_strict": a["replace"], "park_strict": a["park"],
                     "on_topic_cand": b["on"], "replace_cand": b["replace"], "park_cand": b["park"],
                     "pa7_flags": a["pa7"], "flags_strict": a["flags"],
                     "rejects_by_rule_strict": " ".join(f"{k}:{v}" for k, v in sorted(a["rej"].items())),
                     "risk_tags": "; ".join(risk(s))})
    os.makedirs(os.path.join(ROOT, ".cache", "review"), exist_ok=True)
    with open(os.path.join(ROOT, ".cache", "review", "paa.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(sorted(rows, key=lambda r: (r["hub"], r["url"])))
    sp = os.path.join(ROOT, "audit", "paa", "summary.md")
    with open(sp, "w") as f:
        f.write("# PAA gate summary (qc/paa_gate.py)\n\nPhase 2 (DECISIONS 2026-10-08): one line per page, no question text. Per-question verdicts stay in "
                "private/alsoasked/verdicts/; the full table is .cache/review/paa.csv. STRICT = head phrase only; CAND = plus SAFE synonym "
                "candidates (rules/paa_synonym_candidates.json, not yet approved). PA10 covers every child spec in the hub, including the 4 original "
                "live children; the 4 hub pages' FAQs are not in the repo, so they are not covered.\n\n")
        for r in sorted(rows, key=lambda r: (r["hub"], r["url"])):
            f.write(f"- {r['url']} [{r['state']}]: pull pass {r['pull_pass']}/reject {r['pull_reject']}/flag {r['pull_flag']}; FAQ on-topic "
                    f"strict {r['on_topic_strict']}/10 (replace {r['replace_strict']}{', PARKS' if r['park_strict'] else ''}), cand {r['on_topic_cand']}/10 "
                    f"(replace {r['replace_cand']}{', PARKS' if r['park_cand'] else ''}); PA7 flags {r['pa7_flags']}; rejects {r['rejects_by_rule_strict'] or 'none'}"
                    f"{'; risk: ' + r['risk_tags'] if r['risk_tags'] else ''}\n")
    json.dump({"rows": rows, "errors": errs, "qc_fail": qcfail, "unpulled": unpulled},
              open(os.path.join(ROOT, ".cache", "review", "paa_phase2.json"), "w"), indent=1)
    print(f"rows {len(rows)}; paa-resource errors {len(errs)}; QC failures after resource {len(qcfail)}")
    for u, ids in qcfail[:10]: print("  QC FAIL", u, ",".join(ids))
    for u, k, e in errs[:5]: print("  ERR", u, k, e)

if __name__ == "__main__":
    main()
