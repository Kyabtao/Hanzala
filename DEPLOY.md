# Deploy this site to GitHub Pages

Two options. **Option A takes 30 seconds; Option B is automatic forever.**

## Option A — the manual switch (recommended first)
1. Open **https://github.com/Kyabtao/Hanzala/settings/pages**
2. **Source:** `Deploy from a branch`
3. **Branch:** `main` · **Folder:** `/docs` → **Save**
4. Wait ~1 minute, then open **https://kyabtao.github.io/Hanzala/**

That's all. `docs/` already contains a finished static site — no build, no dependencies, no `node_modules`.

## Option B — auto-deploy on every push (Actions)
The workflow is written to **`ops/pages-workflow.yml.example`** — copy it yourself (agents are not permitted to add files under `.github/`):

```bash
mkdir -p .github/workflows
cp ops/pages-workflow.yml.example .github/workflows/pages.yml
git add .github/workflows/pages.yml
git commit -m "ci: auto-deploy docs/ to Pages"
git push origin main
```
Then set **Settings → Pages → Build and deployment → Source: `GitHub Actions`**. It re-runs `python3 build_docs.py` on every push to `main`, so the published site can never drift from the `.md` sources. Use Option A **or** Option B, not both.
After pushing it once, set **Settings → Pages → Build and deployment → Source: `GitHub Actions`**.
(If the workflow fails with a permissions error: Settings → Actions → General → Workflow permissions → **Read and write**.)

## Verify it is live
| Check | Expected |
|---|---|
| `https://kyabtao.github.io/Hanzala/` | the site, **Home** tab, green header |
| `.../Hanzala/data.js` | JavaScript starting `window.SITE = {` (if this 404s, the folder is wrong) |
| `.../Hanzala/print/tracker.html` | printable tracker; press **Print / Save as PDF** |
| `.../Hanzala/print/cards.html` | 56 cards; print **A4 landscape** |
| `.../Hanzala/print/books.html` | 📖 **8 mini-books**; print **A4 portrait**, cut & staple |

## If it shows 404
- **Folder must be `/docs`** — not `/ (root)`. This is the #1 cause.
- Branch must be the one that contains `docs/` (currently `main`).
- First deploy can take 1–2 minutes; hard-refresh with `Ctrl`+`Shift`+`R`.
- No `.nojekyll` needed? It is there — `docs/.nojekyll` exists, so nothing is filtered out.

## Update the content later
1. Edit `WEEKLY-PLAN-YEAR1.md`, `TOY-AND-STUDY-PLAN.md`, `FRIDGE-CHECKLIST.md`, `SHOPPING-LIST.md`, `cards.json` or `books.json`
   (or just drop a dated note into `updates/` and apply it later — see `updates/README.md`)
2. `python3 build_docs.py`
3. `git add -A && git commit -m "update plan" && git push origin main` → Pages updates itself (Option A) or Actions updates it (Option B)

## Phone / offline tips
- On Android/iOS: open the site in Chrome → **Add to Home screen** → it behaves like an app and works from cache.
- To hand relatives a PDF: open `print/tracker.html` → **Print** → **Save as PDF** → A4.
- The tick-boxes save inside the browser on the device you tick them on (they are not shared between phone and laptop — that is deliberate: no account, no server, nothing leaves the device).
