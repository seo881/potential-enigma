# Top rework causes (from the 2026-10-16 sprint reviews; Divit 2026-10-21 item 7b)

Writers: clear every line before requesting review. Reviewers: check every line first.

1. **Unsourced fact stated as fact** (HUB_RULES 8): any statement about how a third-party system, law, standard or group of people behaves needs a quoted domain_sources span, or must be rewritten as advice ("map each field...", "ask your district..."). Most common blocker.
2. **Source scope dropped**: a rule quoted without its own limits (FAR "except commercial products", "competitive acquisitions", Reg Z "not more conspicuously"). Keep the source's conditions in the copy.
3. **Image contradicts copy** (CONTENT_DEFECTS #20/#25): a person-addressed message drawn as a "#" channel (message heroes ignore `dm`: use a card addressed to the person); a staff-only screen shown to a customer; a rate shown more prominently than the APR; numbers that do not add up.
4. **Comparison table**: single-vendor library entries only. Never the grouped "Landingi / Leadpages / Instapage" entry; never one vendor in two columns.
5. **Internal contradiction**: two answers giving different numbers for the same thing (question counts, deadlines, minimums).
6. **Off-intent FAQ sense**: insurance-sense "proposal form", construction "board survey", state-specific programs. Builder intent only; no state-specific content.
7. **Claims about "the examples above"** must be true of every tab.
8. **Before review**: QC 0, `hubctl paa --spec` 0 rejects and 0 flags, `hubctl learn-check`, hero prompt rule (QC L10), `render_changed.py` so render.json is current.
