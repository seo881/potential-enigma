import json, re, copy
snap = json.load(open("/home/claude/snapshot_before.json"))
BS = '\\"'   # backslash + quote, as stored in the FAQ embeds

EDITS = {  # page -> field -> list of (old, new) exact substrings
 "lp": {
  "meta-description": [(
   "What a thank you page is, real examples, and templates you can build in minutes. A custom thank you page for WooCommerce, Shopify, or any form, free.",
   "What a thank you page is, four examples by use case, and templates to build in minutes, for WooCommerce, Shopify, or any form. Free to start.")],
  "acrm---key-feature-5-content": [(
   "a Shopify redirect, a WordPress form, or a standalone URL for any form.",
   "a Shopify post-purchase page, a WordPress form, or any standalone URL.")],
  "alpb---how-to-step-6-des": [(
   "It works as a custom thank you page for WooCommerce or Shopify, a WordPress form redirect, or any standalone form.",
   "On Shopify, link it from the order confirmation email, since its own thank you page no longer runs scripts.")],
  "awb---faq-data": [
   ("Yes. Shopify limits what can be changed in the built-in confirmation, so most brands ship a custom Shopify thank you page as a redirect. Emergent builds the page, connects it to the order data, and publishes it on your domain.",
    "Yes, as a linked page rather than a redirect, because Shopify no longer runs custom scripts on its own thank you page. Link an Emergent post-purchase page from the order confirmation email, with the order, a related product, and a next-order code."),
   ("The best examples share five things: a plain confirmation, a clear expectation of what happens next, one next step, delivery of what was promised, and light social proof.",
    "The best examples share five things: a plain confirmation, what happens next, one next step, the promised delivery, and light social proof. The four use cases on this page apply them to a lead magnet, an order, a webinar, and a contact form."),
   ("Load the template, describe what to change, and publish.",
    "Start from the closest one, describe what to change, and publish."),
   ("and the next step you want, and Emergent generates the thank you page,",
    "and the next step you want, and Emergent's <a href=" + BS + "https://emergent.sh/ai-landing-page-builder" + BS + ">AI landing page builder</a> generates the thank you page,"),
  ],
  "awb---mockup-data": [("a database that feeds our email tool.", "a database that feeds my email tool.")],
 },
 "form": {
  "awb---faq-data": [(
   "No. Emergent does not cap responses. By comparison, Typeform's free plan allows 10 responses a month and Jotform's allows 100 submissions.",
   "No. Emergent does not cap responses, so the form keeps collecting through a launch spike. Many form tools cap responses by plan, and some close the form once the cap is reached.")],
 },
 "aab": {
  "alpb---prompt-filter-1": [("Multi-level Routing", "Multi-Level Routing")],
 },
 "sqb": {
  "description": [(
   "Describe what you want to measure and who you are asking. Emergent builds",
   "Describe what you want to measure. Emergent builds")],
  "acrm---key-feature-3-content": [(
   "CSAT and effort scores branch the same way, included from the free tier.",
   "CSAT and effort scores branch the same way, set in one line of the prompt.")],
 },
}

BANNED = [r"[\u2013\u2014]", r"(?i)\bbuilt-in\b", r"&amp;amp;", r"Type II", r"[\u2018\u2019\u201c\u201d]",
          r"(?i)(?<![\w-])(we|our|ours|us)(?![\w-])", r"!"]

def faq_obj(s):
    m = re.search(r"window\.awbFAQ = (\{.*\}); </script>", s, re.S)
    return json.loads(m.group(1))

def p_text(html):
    m = re.search(r"<p[^>]*>(.*?)</p>", html, re.S); return m.group(1)

out, report = {}, []
for page, fields in EDITS.items():
    fd = snap[page]["fieldData"]; out[page] = {}
    for field, pairs in fields.items():
        old_val = fd[field]; new_val = old_val
        for old, new in pairs:
            n = new_val.count(old)
            assert n == 1, f"{page}.{field}: expected 1 occurrence, found {n}: {old[:60]}"
            new_val = new_val.replace(old, new)
        # zero-drift proof: reverting the planned replacements must give back the original byte for byte
        rev = new_val
        for old, new in reversed(pairs):
            assert rev.count(new) == 1, f"{page}.{field}: new text not unique"
            rev = rev.replace(new, old)
        assert rev == old_val, f"{page}.{field}: drift outside planned spans"
        # banned strings: only check the inserted text
        for _, new in pairs:
            plain = re.sub(r"<[^>]+>", "", new.replace(BS, '"'))
            for rx in BANNED:
                assert not re.search(rx, plain), f"{page}.{field}: banned pattern {rx} in new text"
        if field == "awb---faq-data":
            a, b = faq_obj(old_val), faq_obj(new_val)
            assert [i["q"] for i in a["items"]] == [i["q"] for i in b["items"]], "FAQ questions changed"
            assert a["heading"] == b["heading"]
            changed = sum(1 for x, y in zip(a["items"], b["items"]) if x["a"] != y["a"])
            assert changed == len(pairs), f"{page} FAQ: {changed} answers changed, planned {len(pairs)}"
            report.append(f"{page}.{field}: FAQ JSON parses, {len(b['items'])} items, questions identical, {changed} answers changed; hub links: {new_val.count('<a href')}")
        out[page][field] = new_val
        report.append(f"{page}.{field}: {len(pairs)} replacement(s), zero drift")

# band checks
lpf = [len(p_text(out['lp'].get(f'acrm---key-feature-{i}-content', snap['lp']['fieldData'][f'acrm---key-feature-{i}-content']))) for i in range(1,7)]
sqf = [len(p_text(out['sqb'].get(f'acrm---key-feature-{i}-content', snap['sqb']['fieldData'][f'acrm---key-feature-{i}-content']))) for i in range(1,7)]
assert all(165 <= x <= 182 for x in lpf) and max(lpf)-min(lpf) <= 12, lpf
assert all(165 <= x <= 182 for x in sqf) and max(sqf)-min(sqf) <= 12, sqf
report.append(f"LP feature bodies {lpf} spread {max(lpf)-min(lpf)} | SQB feature bodies {sqf} spread {max(sqf)-min(sqf)}")
md = out['lp']['meta-description']; assert 90 <= len(md) <= 155; report.append(f"LP meta description {len(md)} chars")
hd = out['sqb']['description']; report.append(f"SQB hero {len(hd)} chars, {len(hd.split())} words")
json.dump(out, open("/home/claude/work/new_values.json", "w"), indent=1, ensure_ascii=False)
print("\n".join(report)); print("ALL ASSERTIONS PASSED")
