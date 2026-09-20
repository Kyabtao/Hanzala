#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild the GitHub Pages site in docs/ from the .md files + cards.json + books.json.
   Usage:  python3 build_docs.py   →  docs/index.html, docs/data.js, docs/cards.js,
           docs/print/tracker.html, docs/print/cards.html, docs/print/books.html
   Edit TOY-AND-STUDY-PLAN.md / WEEKLY-PLAN-YEAR1.md / FRIDGE-CHECKLIST.md /
   SHOPPING-LIST.md / cards.json / books.json, run this, commit, push → Pages updates.
"""
import json, os, re, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
def read(p): return open(os.path.join(ROOT, p), encoding='utf-8').read()

def md2html(md):
    md = md.replace('\r', '')
    lines = md.split('\n'); out = []; i = 0
    esc = lambda s: s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    def inline(s):
        s = esc(s)
        s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
        s = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', s)
        s = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<i>\1</i>', s)
        return s
    while i < len(lines):
        ln = lines[i]
        if ln.startswith('|') and i + 1 < len(lines) and re.match(r'^\|[\s:|-]+\|$', lines[i + 1].strip()):
            hdr = [c.strip() for c in ln.strip().strip('|').split('|')]; i += 2; rows = []
            while i < len(lines) and lines[i].startswith('|'):
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')]); i += 1
            t = '<div class="tw"><table><thead><tr>' + ''.join(f'<th>{inline(c)}</th>' for c in hdr) + '</tr></thead><tbody>'
            for r in rows:
                r = (r + [''] * len(hdr))[:len(hdr)]
                t += '<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>'
            out.append(t + '</tbody></table></div>'); continue
        if ln.startswith('#'):
            lv = min(len(ln) - len(ln.lstrip('#')), 4)
            out.append(f'<h{lv} class="h{lv}">{inline(ln[lv:].strip())}</h{lv}>')
        elif ln.strip().startswith('>'):
            buf = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                buf.append(lines[i].strip().lstrip('>').strip()); i += 1
            i -= 1; out.append('<blockquote>' + inline(' '.join(buf)) + '</blockquote>')
        elif re.match(r'^\s*[-*☐]\s+', ln):
            buf = []
            while i < len(lines) and re.match(r'^\s*[-*☐]\s+', lines[i]):
                raw = lines[i]; item = re.sub(r'^\s*[-*☐]\s+', '', raw)
                box = '<span class="tick"></span> ' if raw.lstrip().startswith('☐') else ''
                buf.append(f'<li>{box}{inline(item)}</li>'); i += 1
            i -= 1; out.append('<ul>' + ''.join(buf) + '</ul>')
        elif ln.strip() in ('---', '***'): out.append('<hr>')
        elif not ln.strip(): pass
        elif ln.startswith('```'):
            buf = []; i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                buf.append(lines[i]); i += 1
            out.append('<pre>' + esc('\n'.join(buf)) + '</pre>')
        else:
            buf = [ln]
            while i + 1 < len(lines):
                nx = lines[i + 1]
                if (not nx.strip()) or nx.startswith('#') or nx.startswith('|') or nx.strip().startswith('>') \
                   or nx.startswith('```') or nx.strip() == '---' or re.match(r'^\s*[-*☐]\s+', nx): break
                buf.append(nx); i += 1
            out.append('<p>' + inline(' '.join(x.strip() for x in buf)) + '</p>')
        i += 1
    return '\n'.join(out)

def safe(html_text):
    """Never let an embedded string close our script tag."""
    return html_text.replace('</', '<\\/')


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def gen_books(books):
    """docs/print/books.html — printable First-Words mini-book collection.
    Each book = cover + 6 word pages + back page = 8 quarter-pages = 2 A4 sheets.
    """
    total_words = sum(len(b['words']) for b in books)
    chips = ''.join('<button class="chip" data-b="%s">%s %s</button>' % (b['id'], b['emoji'], esc(b['title'].split(' · ')[-1])) for b in books)
    secs = ''
    pageno = 0
    for b in books:
        pgs = []
        # cover
        pgs.append('<div class="pg cover"><div class="c-emoji">%s</div><div class="c-collection">Ḥanzalā — My First Words · My First Books</div>'
                   '<div class="c-title">%s</div><div class="c-sub">%s</div><div class="c-name">for Ḥanzalā · b. 11 Jan 2026</div></div>'
                   % (b['emoji'], esc(b['title']), esc(b['sub'])))
        for w in b['words']:
            pageno += 1
            pgs.append('<div class="pg"><div class="emoji">%s</div><div class="ar">%s</div><div class="ur">%s</div>'
                       '<div class="en">%s</div><div class="say">%s</div><div class="foot"><span>%s</span><span>page %d</span></div></div>'
                       % (w['emoji'], esc(w['ar']), esc(w['ur']), esc(w['en']), esc(w['say']), esc(b['title']), pageno))
        pgs.append('<div class="pg back"><div class="b-head">How to read this book</div><ul>'
                   '<li>Hold him facing the page — his eye on the picture, your voice at his ear.</li>'
                   '<li>One page a day is enough. Say the word <b>5 times</b> while pointing.</li>'
                   '<li>Add the sentence: <i>"%s."</i> Then wait — count to five silently.</li>'
                   '<li>Never quiz. Reading is cuddle-time, not a test.</li>'
                   '<li>End every book the same way: <span class="ar-inline">اَلْحَمْدُ لِلّٰهِ</span> — done!</li>'
                   '</ul><div class="b-foot">%s · %s</div></div>'
                   % (esc(b['words'][0]['en']), esc(b['title']), esc(b['sub'])))
        sheets = ''
        for i in (0, 1):
            sheets += '<div class="sheet">%s</div>' % ''.join(pgs[i * 4:(i + 1) * 4])
        secs += ('<section class="book" id="bk-%s"><div class="bhead noprint"><h2>%s %s</h2>'
                 '<button class="btn" onclick="onlyBook(\'%s\')">🖨 Print just this book</button></div>%s</section>'
                 % (b['id'], b['emoji'], esc(b['title']), b['id'], sheets))
    css = read('docs_src/books_print.css')
    head = ('<!DOCTYPE html>\n<html lang="en"><head><meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
            '<title>Ḥanzalā — My First Words · %d printable mini-books</title>\n'
            '<link href="https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Noto+Nastaliq+Urdu:wght@400;700&family=Inter:wght@400;600;800&display=swap" rel="stylesheet">\n'
            '<style>') % len(books)
    head += css + '</style></head><body>\n'
    toolbar = ('<div class="toolbar noprint"><div><h1>📖 Ḥanzalā — My First Words · %d printable mini-books</h1>'
               '<p class="sub">%d word pages, Arabic + Urdu + English. Each book prints on 2 A4 sheets → cut → staple = a board book like the shop ones, for free.</p></div>'
               '<div class="tbtns"><button class="btn big" onclick="onlyBook(\'\')">🖨 Print all %d books</button>'
               '<button class="btn gh" onclick="onlyBook(\'__cover__\')">Print only the covers</button></div></div>\n'
               '<div class="howto noprint"><b>Make each book in 4 steps:</b> '
               '① Print the book\'s 2 A4 sheets (plain paper is fine; 160–200 gsm card feels like a real board book). '
               '② Cut along the <b>dashed lines</b> → 8 quarter-pages. ③ Stack in page order (cover first, "How to read" page last). '
               '④ Staple the left edge — or glue each quarter onto a cut cereal box before stacking and cover with wide tape = a wipe-clean "board book".</div>\n'
               '<div class="chips noprint"><button class="chip on" data-b="">All %d books</button>%s</div>\n') % (
        len(books), total_words, len(books), len(books), chips)
    js = ('<script>\n'
          'function onlyBook(id){\n'
          '  document.body.classList.toggle("coversonly", id==="__cover__");\n'
          '  var secs=document.querySelectorAll(".book"), one=!!(id&&id!=="__cover__");\n'
          '  for(var i=0;i<secs.length;i++){secs[i].style.display=(!one||secs[i].id==="bk-"+id)?"":"none";}\n'
          '  var chips=document.querySelectorAll(".chip");\n'
          '  for(var j=0;j<chips.length;j++){chips[j].classList.toggle("on",chips[j].getAttribute("data-b")===(id||""));}\n'
          '  setTimeout(function(){window.print();},60);\n'
          '}\n</script>\n')
    page = head + toolbar + secs + '\n' + js + '</body></html>'
    open(os.path.join(ROOT, 'docs', 'print', 'books.html'), 'w', encoding='utf-8').write(page)
    shutil.copyfile(os.path.join(ROOT, 'docs', 'print', 'books.html'), os.path.join(ROOT, 'printable', 'books.html'))
    return total_words

def main():
    cards = json.loads(read('cards.json'))
    books = json.loads(read('books.json'))
    site = {
        'dob': '2026-01-11',
        'name': 'Ḥanzalā',
        'weeks': md2html(read('WEEKLY-PLAN-YEAR1.md')),
        'plan':  md2html(read('TOY-AND-STUDY-PLAN.md')),
        'fridge': md2html(read('FRIDGE-CHECKLIST.md')),
        'shop':  md2html(read('SHOPPING-LIST.md')),
    }
    os.makedirs(os.path.join(ROOT, 'docs', 'print'), exist_ok=True)
    open(os.path.join(ROOT, 'docs', 'data.js'), 'w', encoding='utf-8').write(
        '/* generated by build_docs.py — edit the .md files instead */\nwindow.SITE = ' + safe(json.dumps(site, ensure_ascii=False)) + ';\n')
    open(os.path.join(ROOT, 'docs', 'cards.js'), 'w', encoding='utf-8').write(
        '/* generated by build_docs.py — edit cards.json instead */\nwindow.CARDS = ' + safe(json.dumps(cards, ensure_ascii=False)) + ';\n')

    tpl = read('docs_src/index.html')
    open(os.path.join(ROOT, 'docs', 'index.html'), 'w', encoding='utf-8').write(tpl)
    for f in ('tracker.html', 'index.html'):
        shutil.copyfile(os.path.join(ROOT, 'printable', f), os.path.join(ROOT, 'docs', 'print', f))

    # print/cards.html from cards.json (single source of truth)
    body = ''
    for n, c in enumerate(cards, 1):
        body += ('  <div class="card"><div class="top"><span class="cat">%s</span><span class="age">from %s</span></div>'
                 '<div class="ttl">%s</div><div class="ar">%s</div><div class="ur">%s</div><div class="en">%s</div>'
                 '<div class="act"><b>Do:</b> %s</div><div class="foot">Ḥanzalā · b. 11 Jan 2026 · card %d/%d</div></div>\n') % (
            c['cat'], c['age'], c['title'], c['ar'], c['ur'], c['en'], c['act'], n, len(cards))
    css = read('docs_src/cards_print.css')
    page = ('<!DOCTYPE html>\n<html lang="en"><head><meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
            '<title>Ḥanzalā — Āyah &amp; Word Cards</title>\n'
            '<link href="https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Noto+Nastaliq+Urdu&display=swap" rel="stylesheet">\n'
            '<style>' + css + '</style></head><body>\n'
            '<div class="toolbar"><h1>Ḥanzalā — %d printable cards · Āyah · Words · Duʿāʾ · Asmāʾ al-Ḥusnā</h1>'
            '<button onclick="window.print()">🖨 Print / Save as PDF</button>'
            '<button class="g" onclick="document.querySelector(\'.grid\').classList.toggle(\'two\')">6 per page (bigger)</button></div>\n'
            '<div class="sheet"><p class="note"><b>Print:</b> A4 <b>landscape</b>, margins "None" → 8 cards per sheet, then cut. '
            '<b>Use:</b> 3–5 cards out at a time at his eye level; duʿāʾ cards on the fridge. <b>Do not quiz a baby</b> — hold the card up, '
            'say it aloud while doing the action, 5–10× a day, one card per week.</p><div class="grid">\n%s</div></div></body></html>' % (len(cards), body))
    open(os.path.join(ROOT, 'docs', 'print', 'cards.html'), 'w', encoding='utf-8').write(page)
    shutil.copyfile(os.path.join(ROOT, 'docs', 'print', 'cards.html'), os.path.join(ROOT, 'printable', 'cards.html'))
    words = gen_books(books)
    open(os.path.join(ROOT, 'docs', '.nojekyll'), 'w').write('')
    print('docs/ rebuilt · cards: %d · books: %d (%d word pages) · data.js: %d KB' % (
        len(cards), len(books), words, os.path.getsize(os.path.join(ROOT, 'docs', 'data.js')) // 1024))

if __name__ == '__main__':
    main()
