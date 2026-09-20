# 📥 `updates/` — your notes folder (the "temporary folder")

This is where **you** drop changes in plain language — on your phone, any time.
The next agent session (or you at a laptop) turns them into the real manuals, rebuilds the site, and moves the file to `done/`.

## The workflow (4 steps)

```
1. You write      updates/2026-MM-DD-anything.md   ← copy TEMPLATE.md, write freely, any language
2. You (or agent) apply it:
     - words/cards changes  →  cards.json
     - book changes         →  books.json
     - plan changes         →  WEEKLY-PLAN-YEAR1.md / TOY-AND-STUDY-PLAN.md / FRIDGE-CHECKLIST.md
     - buy-list changes     →  SHOPPING-LIST.md
3. Rebuild:       python3 build_docs.py
4. Publish:       git add -A && git commit -m "update from notes" && git push origin main
                  → GitHub Pages updates itself in ~1 minute
```

## Rules

- One note per day (`2026-MM-DD-what.md`). Never delete — after applying, move it into `updates/done/` so you keep a history.
- Write **what you want**, not how to do it. *"Hanzla said mama today!"* or *"remove the horse, we don't keep dog-pictures rule"* is enough.
- Urgent? Title the file `2026-MM-dd-URGENT-....md` so it jumps out.
- Nothing in this folder goes to the printed pages directly — only after step 3–4 does the site change.

## What lives where (cheat sheet)

| You want to change… | Edit this file |
|---|---|
| a flashcard's word / action / age | `cards.json` |
| a mini-book's words or themes | `books.json` |
| the 52-week schedule | `WEEKLY-PLAN-YEAR1.md` |
| toys by age / avoid-list / milestones | `TOY-AND-STUDY-PLAN.md` |
| the one-page fridge sheet | `FRIDGE-CHECKLIST.md` |
| the shopping list (Meesho-style buys) | `SHOPPING-LIST.md` |

Then always: `python3 build_docs.py` → commit → push. The `docs/` folder is generated — **never edit it by hand**.
