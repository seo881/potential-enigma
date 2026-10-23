"""queue_rank.py: ruling 12 part 4 (Divit 2026-10-13). The claim order for every hub: feasibility first, then MSV.

    python3 ops/queue_rank.py                    write plan/queue-ranked.txt (committed: rank, hub, url, class, feasibility; no Semrush data)
    python3 ops/queue_rank.py --release-parked   retired (Divit 2026-10-16): feasibility no longer separates parked pages (written questions
                                                 take every page to 10); re-queue by park reason with hubctl release instead

Classes, in this order (MSV high to low inside each):
  ready         has a pull and feasibility >= 10 now
  syn-pending   has a pull, under 10 now, reaches 10 with its tranche's top 2 phrases (Divit has not decided yet): B may claim it
                for the split write (everything but the FAQ; ruling 12 part 5)
  no-pull       no AlsoAsked pull yet (A pulls it; B cannot write it)
  short         under 10 even with the candidates (feasibility high to low). Since Divit 2026-10-16 (item 1) the feasibility count
                includes written slots, so every pulled page reaches 10: shortness no longer demotes a page. Relevance and
                cannibalisation stay with the park reasons and NOT_RELEASED, exactly as before.
Regenerate after every pull wave and every synonym approval. `hubctl claim` takes the first unclaimed ready/syn-pending rows of the hub, top down.
"""
import contextlib, io, json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for d in ("ops", "qc"): sys.path.insert(0, os.path.join(ROOT, d))
import hubctl as H, paa_gate as P, park_rescue as R, pull_wave as W

OUT = os.path.join(ROOT, "plan", "queue-ranked.txt")
ORDER = {"ready": 0, "syn-pending": 1, "no-pull": 2, "short": 3}
# 2026-10-14 05:10 IST (A-coord): --release-parked released these although they were parked for intent mismatch, a rule conflict or a
# library gap, not FAQ supply. Kept out of the claim order until Divit rules (10:00 report); their park notes are in git (status/*.json at 621731fc).
NOT_RELEASED = {"body-type", "body-type-quiz", "change-request", "change-request-form", "fun", "fun-quiz", "grant-application", "grant-application-form", "jurat", "jurat-form", "loan-application", "loan-application-form", "non-compete", "non-compete-form", "pledge", "pledge-form", "product", "product-survey", "questionnaire", "survey-questionnaire", "user-experience", "user-experience-survey"}   # old and migrated slugs (DECISIONS 2026-10-23)

def quiet(f, *a):
    with contextlib.redirect_stdout(io.StringIO()): return f(*a)

def classify(url, syn):
    s = url.rsplit("/", 1)[1]
    if not P.pulls(s): return "no-pull", None
    f = quiet(R.feasibility, url)["total"]
    if f >= 10: return "ready", f
    e = syn.get(s) or {}
    if e.get("pending") and e.get("feasibility_with", 0) >= 10: return "syn-pending", f
    return "short", f

def rows():
    syn = (json.load(open(os.path.join(ROOT, "status", "synonyms.json"))) if os.path.exists(os.path.join(ROOT, "status", "synonyms.json")) else {"pages": {}})["pages"]
    out = []
    for p in W.queued():
        if p["url"].rsplit("/", 1)[1] in NOT_RELEASED: continue
        c, f = classify(p["url"], syn)
        quiz = int("quiz" in p["url"].rsplit("/", 1)[1] or "quiz" in (p.get("primary") or "").lower().split())   # quiz pages stay last (DECISIONS 2026-10-14): non-quiz rows first inside each class
        out.append((ORDER[c], quiz, -(f or 0) if c == "short" else 0, -(p.get("total_msv") or 0), p["hub"], p["url"], c, f))
    return sorted(out)

def ranked():
    """[(rank, hub, url, class, feasibility)] from plan/queue-ranked.txt; None when the file does not exist."""
    if not os.path.exists(OUT): return None
    res = []
    for l in open(OUT):
        if l.startswith("#") or not l.strip(): continue
        r, hub, url, c, f = l.split("\t")
        res.append((int(r), hub, url, c, None if f.strip() == "-" else int(f)))
    return res

def release_parked():
    sys.exit("refused: --release-parked is retired (Divit 2026-10-16): every page now reaches 10 with written questions, so feasibility "
             "would release pages parked for relevance, intent or cannibalisation; re-queue by park reason with hubctl release --note")
    got = []
    for hub in H.WRITER_HUBS:
        for url, e in sorted(H.load_st(hub)["pages"].items()):
            if e.get("state") != "parked" or H.hold_conflict(url): continue
            f = quiet(R.feasibility, url)
            if not f["feasible"]: continue
            subprocess_args = [sys.executable, os.path.join(ROOT, "ops", "hubctl.py"), "release", url, "--by", "A-coord",
                               "--note", f"ruling 12 (Divit 2026-10-13): parked page released to B, feasibility {f['total']}/10"]
            import subprocess; r = subprocess.run(subprocess_args, cwd=ROOT, capture_output=True, text=True)
            got.append((url, f["total"], r.returncode))
    for u, t, rc in got: print(f"released parked {u} ({t}/10)" + ("" if rc == 0 else f": hubctl release exit {rc}"))
    return got

# Dated allowances for B to regenerate the ranking (ruling 12 gave it to A). The overnight lift of 2026-10-15 ended with that run.
B_RERANK = {"2026-10-16": "Divit 2026-10-16 (FULL-THROTTLE WRITING item 2): B re-ranks the queue"}

def main(a):
    import datetime as _dt
    today = _dt.date.today().isoformat()
    if H.clone_account() != "A" and today not in B_RERANK:
        sys.exit("refused: the queue ranking is regenerated by Account A (ruling 12) except on a dated allowance (B_RERANK); B reads plan/queue-ranked.txt")
    if H.clone_account() != "A": print(B_RERANK[today])
    if "--release-parked" in a: release_parked()
    rs = rows()
    with open(OUT, "w") as f:
        f.write("# queue ranked (Divit ruling 12, 2026-10-13): class ready > syn-pending > no-pull > short, quizzes last in each class, then MSV. ops/queue_rank.py; claim from the top only.\n")
        f.write("# rank\thub\turl\tclass\tfeasibility\n")
        for i, r in enumerate(rs, 1): f.write(f"{i}\t{r[4]}\t{r[5]}\t{r[6]}\t{'-' if r[7] is None else r[7]}\n")
    from collections import Counter
    c = Counter((r[4], r[6]) for r in rs)
    for hub in H.CFG["hubs"]: print(f"{hub:10s} " + " ".join(f"{k}={c[(hub, k)]}" for k in ORDER))
    print(f"wrote plan/queue-ranked.txt ({len(rs)} queued pages)")

if __name__ == "__main__":
    main(sys.argv[1:])
