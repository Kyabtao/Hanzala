# Audit — 20 September 2026

Full audit of the repo and the generated site, run after adding the **printable mini-books**
(`books.json` → `printable/books.html`) and the **shopping list** (`SHOPPING-LIST.md`).

## Verdict: 🟢 healthy — 3 bugs found & fixed, all checks pass

| # | Check | Result |
|---|---|---|
| 1 | `python3 build_docs.py` runs clean | ✅ 56 cards · 8 books (48 word pages) · data.js 65 KB |
| 2 | `books.json` / `cards.json` schema (every word has emoji/en/ar/ur/say/deen, 6 words per book, unique ids) | ✅ |
| 3 | JS syntax of generated `docs/data.js`, `docs/cards.js`, inline script of `books.html` (`node --check` / `vm`) | ✅ |
| 4 | Local-link check in 6 shipped HTML files (`docs/index.html`, `printable/index.html`, `docs/print/*`) | ✅ all resolve |
| 5 | HTML tag-balance parse of all 6 shipped pages | ✅ |
| 6 | `books.html` structure: 16 A4 sheets, 64 quarter-pages (8 covers + 48 words + 8 back pages) | ✅ |
| 7 | `cards.html`: exactly 56 cards | ✅ |
| 8 | `.nojekyll`, `docs/print/index.html` present for Pages | ✅ |
| 9 | GitHub Actions workflow example (`ops/pages-workflow.yml.example`) — valid YAML, correct permissions, runs `build_docs.py` before upload | ✅ (owner must copy it to `.github/workflows/` — agents may not) |

## Bugs found & fixed

1. **Week counter off by one** — the Home tab showed week *N+1* (today 20 Sep 2026 is week 3, it said 4).
   `docs_src/index.html`: display `wk` (which is already `floor(days/7)+1`), not `wk+1`. ✅ fixed
2. **"You are here" month pill wrong** — it derived the month from age (months − 6) instead of the plan's weeks,
   so on 20 Sep it highlighted *Month 2* instead of *Month 1*. Now `Math.ceil(wk/4)` (Month 1 = weeks 1–4). ✅ fixed
3. **"357 tick-boxes" claim wrong** — the real count in the tracker is **≈400** (milestones 89 + deen & adab 69 +
   ḥifẓ 81 + duʿāʾ 18 + 14-day routine grid 120 + revision/daily 16). Wording changed to "~400 auto-saving tick-boxes". ✅ fixed
4. *(Caught before release)* **print-CSS bug in the new books page** — the print sheet height clipped the second
   row of quarter-pages; replaced fixed height with `grid-template-rows:132.5mm` and added
   `.book:last-child .sheet:last-child{page-break-after:auto}` so no trailing blank page prints. ✅ fixed

## Known limitations (by design, not bugs)

- **Google Fonts** (Amiri, Noto Nastaliq Urdu, Inter) load from the internet; offline, system fallbacks are used
  and Arabic/Urdu still render via the fallback stack in the CSS variables.
- Ticks/typed notes live in **localStorage per device** — deliberate: no account, no server, nothing leaves the device.
- `docs/` and `printable/cards.html` / `printable/books.html` are **generated** (build_docs.py). Edit the sources
  (`.md`, `cards.json`, `books.json`), never the generated files — they are committed only so Pages Option A works.
- Emoji pictures print from the device's emoji font — they vary slightly between Windows/Android/iPhone. A photo
  or sticker glued on each page is the upgrade path when he is older.

## Recommended next actions (owner)

1. Deploy: follow `DEPLOY.md` — Option A (30 seconds, Settings → Pages → `/docs`) or Option B (Actions auto-deploy,
   copy `ops/pages-workflow.yml.example` → `.github/workflows/pages.yml`).
2. Print a test book from `printable/books.html` (start with **My Dīn**) on plain A4 to check your printer's margins.
3. Drop future manual changes into `updates/` (see `updates/README.md`).
