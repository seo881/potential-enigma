"""plan_additions_from_proposals.py: Divit's FINAL keyword list (2026-11-13) -> plan additions.

Reads private/proposals/new-keywords-2026-11-13.md (B-sup-2's markdown tables, one per hub), keeps ONLY the approved slugs listed
below (plus --also SLUG,SLUG for SERP-checked rows Divit allowed), and writes them in keyword-map shape to
private/semrush/plan-additions-2026-11-13.json (git-ignored: Semrush data). Adds their URLs to plan/overrides.json additions.urls
(tracked: URLs only). Prints counts and missing slugs only, never Semrush numbers. Then run: python3 plan/build_map.py --additions-only

    .venv/bin/python3 ops/plan_additions_from_proposals.py [--also help-desk,wedding] [--dry-run]
"""
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "private", "proposals", "new-keywords-2026-11-13.md")
OUT = os.path.join(ROOT, "private", "semrush", "plan-additions-2026-11-13.json")
OV = os.path.join(ROOT, "plan", "overrides.json")
HUBS = {"LP": "/ai-landing-page-builder", "Form": "/ai-form-builder", "Auto": "/ai-automation-builder", "SurveyQuiz": "/ai-survey-and-quiz-builder"}
APPROVED = {
 "LP": "dynamic retargeting competitor-comparison advertorial pay-per-call conversational copywriter home-valuation web-hosting",
 "Form": "medical-consent-for-minor tryout-evaluation donation-request parent-conference-for-teacher bathroom-sign-in-sheet "
         "psychographic-questionnaire seo-client-questionnaire consent-to-treat creative-request boo-basket-questionnaire donation-receipt "
         "supply-request employee-write-up karaoke-sign-up-sheet medical-waiver trunk-or-treat-sign-up-sheet ladder-inspection "
         "customer-information community-service sales-questionnaire chili-cook-off-sign-up-sheet meet-the-teacher-sign-in-sheet "
         "talent-show-sign-up-sheet hvac-inspection delivery-receipt jha pip recruiting-intake scope-of-work trade-show-lead "
         "bake-sale-sign-up-sheet return-authorization white-elephant-sign-up-sheet time-slot-sign-up-sheet meal-train-sign-up-sheet "
         "valentines-day-party-sign-up-sheet dermaplaning-consent spray-tanning-consent bounce-house-waiver agent-open-house-feedback "
         "employee-termination payroll-deduction-authorization trip-report all-about-me-questionnaire forklift-operator-evaluation "
         "sermon-evaluation boat-rental-waiver haunted-house-waiver real-estate-buyer-intake employee-coaching wine-tasting "
         "cookie-exchange-sign-up-sheet fantasy-football-sign-up-sheet mystery-reader-sign-up-sheet",
 "Auto": "finance workflow-for-small-business freight-broker kyc-workflow gym whatsapp gmail artwork-approval-process affiliate "
         "field-service prior-authorization reconciliation tax lead-generation underwriting dsar-workflow",
 "SurveyQuiz": "screening-questions true-and-false slider-scale image airline-questions map game-questions post-meeting-questions "
               "fill-in-the-blank audience-questions learning-and-development-questions scored conjoint questions-for-social-media "
               "flashcard maxdiff automotive lessons-learned hoa-questions matrix-question pre-training-questions drag-and-drop library "
               "retail clothes-questions loyalty-program-questions internal-communications-questions media-consumption-questions "
               "persona-questions yearbook-questions business-travel-questions",
}
SERP_CHECKED = {"help-desk", "data-extraction", "research", "wedding"}   # only via --also, after a clean SERP check

def hub_of_heading(h):
    h = h.lower()
    if "landing" in h or re.search(r"\blp\b", h): return "LP"
    if "survey" in h or "quiz" in h or "surveyquiz" in h: return "SurveyQuiz"
    if "automation" in h or re.search(r"\bauto\b", h): return "Auto"
    if "form" in h: return "Form"
    return None

def num(x):
    m = re.search(r"[\d,]+(?:\.\d+)?", x or ""); return float(m.group(0).replace(",", "")) if m else None

def parse():
    rows, hub, cols = [], None, None
    for line in open(SRC, encoding="utf-8"):
        s = line.strip()
        if s.startswith("#"):
            hub = hub_of_heading(s) or hub; cols = None; continue
        if not s.startswith("|"): cols = None if not s else cols; continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c): continue
        low = [c.lower() for c in cells]
        if any("slug" in c for c in low) and any("primary" in c or "keyword" in c for c in low): cols = low; continue
        if cols and hub and len(cells) >= len(cols) - 1:
            r = dict(zip(cols, cells)); r["_hub"] = hub; rows.append(r)
    return rows

def col(r, *names):
    for k, v in r.items():
        if any(n in k for n in names): return v
    return ""

def main(argv):
    also = set(); dry = "--dry-run" in argv
    if "--also" in argv: also = {x.strip() for x in argv[argv.index("--also") + 1].split(",") if x.strip()}
    bad = also - SERP_CHECKED
    if bad: sys.exit(f"refused: --also takes only the SERP-check rows {sorted(SERP_CHECKED)}; got {sorted(bad)}")
    want = {h: set(v.split()) for h, v in APPROVED.items()}
    rows = parse(); found, out = set(), {}
    for r in rows:
        slug = re.sub(r"[`\s]", "", col(r, "slug")).strip("/").split("/")[-1]
        h = r["_hub"]
        if not slug or not (slug in want.get(h, set()) or slug in also): continue
        primary = re.sub(r"[`*]", "", col(r, "primary", "keyword")).strip()
        secs = []
        for part in re.split(r";|\n", col(r, "secondar")):
            m = re.match(r"\s*(.+?)\s*\((\d[\d,]*)\)\s*$", part)
            if m: secs.append({"kw": m.group(1), "msv": int(m.group(2).replace(",", ""))})
            elif part.strip(): secs.append({"kw": part.strip(), "msv": None})
        pm = num(col(r, "msv", "volume")); kd = num(col(r, "kd"))
        url = f"{HUBS[h]}/{slug}"
        out[url] = {"hub": h, "url": url, "tier": "Addition 2026-11-13", "display_name": primary[:1].upper() + primary[1:],
                    "primary": primary, "primary_msv": int(pm) if pm is not None else 0, "kd": kd, "intent": "Commercial",
                    "cluster": "Divit 2026-11-13 final list", "secondaries": secs,
                    "total_msv": int((pm or 0) + sum(s["msv"] or 0 for s in secs)), "wave": 4 if (h == "SurveyQuiz" and "quiz" in primary) else 5,
                    "verdict": "Approved (advisor cannibalisation + intent analysis 2026-11-13)", "top10_mix": None, "angle": None,
                    "amber_evidence": None, "serp_features": None, "top10": [], "pass3_action": None,
                    "notes": "YMYL: " + col(r, "ymyl") if col(r, "ymyl") else None, "status": "planned"}
        found.add((h, slug))
    missing = sorted(f"{h}:{s}" for h, ss in want.items() for s in ss if (h, s) not in found) + sorted(f"?:{s}" for s in also if not any(s == f[1] for f in found))
    print(f"rows parsed {len(rows)}; approved found {len(out)} of {sum(len(v) for v in want.values()) + len(also)}; per hub: "
          + ", ".join(f"{h} {sum(1 for p in out.values() if p['hub'] == h)}" for h in HUBS))
    if missing: print("MISSING (not found in the proposals tables, check slug/heading): " + ", ".join(missing))
    if dry: print("dry run: nothing written"); return 0
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    prev = json.load(open(OUT)) if os.path.exists(OUT) else {}
    prev.update(out); json.dump(prev, open(OUT, "w"), indent=1, ensure_ascii=False)
    ov = json.load(open(OV)); a = ov.setdefault("additions", {}); urls = a.setdefault("urls", [])
    n = 0
    for u in out:
        if u not in urls: urls.append(u); n += 1
    json.dump(ov, open(OV, "w"), indent=1, ensure_ascii=False)
    print(f"wrote {len(out)} addition(s) to the private plan-additions file; overrides.json additions.urls +{n}. Next: python3 plan/build_map.py --additions-only")
    return 0

if __name__ == "__main__": sys.exit(main(sys.argv[1:]))
