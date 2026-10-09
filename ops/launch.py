"""launch.py: the launch set (Divit, 2026-10-09: 20 pages; contact-form held). Pre-flight, publish payload and rollback. Nothing here calls Webflow.

  .venv/bin/python3 ops/launch.py pages                       the launch set in publish order (batch-1 ledger, held pages excluded)
  .venv/bin/python3 ops/launch.py preflight READBACK.json     read-only checks against a stored read of the child collections
                                                               -> status/launch-checklist.md (IDs and pass/fail only)
  .venv/bin/python3 ops/launch.py prepare                     ops/out/launch/publish.json (isDraft false on exactly the launch item IDs)
                                                               + ops/out/launch/rollback/<slug>.json (unpublish that one item)

Run order on Divit's "publish batch 1": fresh read of the collections -> preflight (all pass) -> send publish.json ->
staging publish -> `node ops/verify_launch.mjs --base https://<site>.webflow.io` -> emergent.sh publish -> `node ops/verify_launch.mjs` -> `hubctl verify-live` per URL -> `hubctl links --relink`.
"""
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "ops"))
import hubctl as H, ship as S

BATCH = os.path.join(ROOT, "plan", "batches", "batch-1.txt")
OUT = os.path.join(ROOT, "ops", "out", "launch")

def pages():
    L = S.load_ledger(BATCH)
    return [u for u in S.batch_urls(BATCH) if not L["pages"][u].get("stopped")]

def preflight(rb):
    items = H._items_from_readback(rb); rows = []; ok_all = True
    for url in pages():
        hub = H.hub_of(url); h = H.CFG["hubs"][hub]; s = json.load(open(H.spath(url))); slug = url.rsplit("/", 1)[1]
        mine = [it for it in items if (it.get("fieldData") or {}).get("slug") == slug and it.get("_collection", h["collection_id"]) == h["collection_id"]]
        it = next((x for x in mine if x["id"] == s.get("item_id")), mine[0] if mine else None)
        r = {"draft": bool(it) and it.get("isDraft") is True and it["id"] == s.get("item_id")}
        diff = []
        if it:
            fd = it["fieldData"]
            for k, v in H.export_fields(url, s)[0].items():
                if v in (None, "") and k in H.CFG["optional_fields"]: continue
                if fd.get(h["fields"][k]) != v: diff.append(k)
            imgs = [fd.get(h["fields"][k]) or {} for k in H.CFG["image_fields"]]
            r["images"] = all(i.get("fileId") and "website-files.com/" in (i.get("url") or "") for i in imgs)
            r["awbPrompt"] = "window.awbPrompt" in (fd.get(h["fields"]["hero_prompt"]) or "")
            r["awbFAQ"] = "window.awbFAQ" in (fd.get(h["fields"]["faq"]) or "") and len(re.findall(r'"q":', fd.get(h["fields"]["faq"]) or "")) == 10
        else:
            r.update(images=False, awbPrompt=False, awbFAQ=False)
        r["verify"] = bool(it) and not diff
        r["slug_unique"] = len(mine) == 1
        ok = all(r.values()); ok_all &= ok
        rows.append((url, it["id"] if it else "-", r, ok, diff))
    hdr = ["#", "Page", "CMS item", "Draft exists", "Bulk-verify (0 mismatches)", "awbPrompt", "awbFAQ (10 items)", "Images resolve to Webflow files", "Slug unique", "Result"]
    L = ["# Launch pre-flight checklist", "", f"Generated {H.now()} by `ops/launch.py preflight` from a read-only read of the child collections (`{os.path.relpath(rb, ROOT)}`, not committed). IDs and pass/fail only.", "",
         "| " + " | ".join(hdr) + " |", "|" + "---|" * len(hdr)]
    pf = lambda b: "pass" if b else "FAIL"
    for n, (url, iid, r, ok, diff) in enumerate(rows, 1):
        L.append(f"| {n} | {url} | {iid} | {pf(r['draft'])} | {pf(r['verify'])}{' (' + ', '.join(diff) + ')' if diff else ''} | {pf(r['awbPrompt'])} | {pf(r['awbFAQ'])} | {pf(r['images'])} | {pf(r['slug_unique'])} | **{pf(ok)}** |")
    L += ["", f"**{sum(r[3] for r in rows)} of {len(rows)} pages pass every check.**"]
    open(os.path.join(ROOT, "status", "launch-checklist.md"), "w").write("\n".join(L) + "\n")
    print(f"status/launch-checklist.md: {sum(r[3] for r in rows)} of {len(rows)} pass"); return 0 if ok_all else 1

def prepare():
    os.makedirs(os.path.join(OUT, "rollback"), exist_ok=True); by = {}; ids = []
    for url in pages():
        s = json.load(open(H.spath(url))); h = H.CFG["hubs"][H.hub_of(url)]
        if not s.get("item_id"): sys.exit(f"{url}: no CMS item yet; create and verify the draft first")
        by.setdefault(h["collection_id"], []).append({"id": s["item_id"], "isDraft": False, "fieldData": {}}); ids.append((url, s["item_id"]))
        json.dump([{"label": f"ROLLBACK unpublish {url}", "unpublish_collection_items": {"collection_id": h["collection_id"], "request": {"items": [{"id": s["item_id"]}]}}}],
                  open(os.path.join(OUT, "rollback", url.rsplit("/", 1)[1] + ".json"), "w"), indent=1)
    man = []
    for url in pages():
        s = json.load(open(H.spath(url))); F = s["fields"]; hub = H.hub_of(url)
        fq = json.loads(re.search(r"window\.awbFAQ\s*=\s*(\{.*\})\s*;\s*</script>", F["faq"], re.S).group(1))
        txt = lambda v: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", v or "")).strip()
        man.append({"url": url, "hub": H.CFG["hubs"][hub]["path"], "h1": txt(F["h1"]), "meta_title": F["meta_title"], "meta_description": F["meta_description"],
                    "faq": [i["q"] for i in fq["items"]], "default_prompt": txt(F["hero_prompt"]), "chips": s.get("chip_prompts") or [],
                    "uc_images": [(s["images"].get(f"tab_image_{i}") or {}).get("cdn_url") for i in range(1, 5)],
                    "tab_labels": [txt(F.get(f"tab_label_{i}")) for i in range(1, 5)],
                    "pending_links": [p["target"] for p in s.get("pending_links") or []]})
    json.dump({"pages": man, "hubs": sorted({m["hub"] for m in man})}, open(os.path.join(OUT, "manifest.json"), "w"), indent=1, ensure_ascii=False)
    acts = [{"label": f"launch: isDraft false on {len(v)} item(s) in {c}", "update_collection_items": {"collection_id": c, "request": {"items": v}}} for c, v in by.items()]
    json.dump(acts, open(os.path.join(OUT, "publish.json"), "w"), indent=1)
    print(f"ops/out/launch/publish.json: {len(ids)} item IDs in {len(acts)} action(s) (NOT sent); rollback files: {len(ids)}")

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a: print(__doc__); sys.exit(0)
    if a[0] == "pages": print("\n".join(pages())); print(len(pages()), "pages")
    elif a[0] == "preflight": sys.exit(preflight(a[1]))
    elif a[0] == "prepare": prepare()
