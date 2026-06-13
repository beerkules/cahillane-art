#!/usr/bin/env python3
"""CAHILLANE static site generator.

Reads assets/works.json and emits:
  - works.html              (the originals grid)
  - work/<slug>.html        (one static page per work, with per-work OG tags)

Per-work static pages mean shared links (Instagram, etc.) get a real preview
image — which a client-side JSON+JS approach can't give.

Run after editing works.json:   python3 build.py
"""
import json
import os
import html

ROOT = os.path.dirname(os.path.abspath(__file__))
DOMAIN = "https://benjamincahillane.com"
STATUS_LABEL = {"available": "Available", "reserved": "Reserved", "sold": "Sold"}

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{og_image}">
<meta property="og:url" content="{og_url}">
<meta property="og:type" content="website">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=League+Spartan:wght@500;600&family=DM+Sans:ital,wght@0,300;0,400;1,300&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css?v=16">
<link rel="icon" type="image/png" href="/assets/favicon.png?v=5">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png?v=5">
</head>
<body>
<div id="site-header"></div>
"""

FOOT = """<div id="site-footer"></div>
<script src="/assets/include.js?v=16" defer></script>
</body>
</html>
"""


def esc(s):
    return html.escape(str(s), quote=True)


def card(w):
    label = STATUS_LABEL.get(w["status"], "")
    return (
        f'<a class="card" data-status="{esc(w["status"])}" href="/work/{esc(w["slug"])}.html">'
        f'<div class="card-img"><img src="{esc(w["thumb"])}?v=5" alt="{esc(w["title"])}, {esc(w["year"])}" loading="lazy"></div>'
        f'<div class="card-meta">'
        f'<span class="card-title">{esc(w["title"])}</span>'
        f'<span class="dot {esc(w["status"])}">{esc(label)}</span>'
        f'</div>'
        f'<div class="card-sub">{esc(w["year"])} · {esc(w["dimensions_cm"])}</div>'
        f'</a>'
    )


def build_works(works):
    cards = "\n".join(card(w) for w in works)
    head = HEAD.format(
        title="Works — Benjamin Cahillane",
        desc="Original works by contemporary artist Benjamin Cahillane.",
        og_title="Benjamin Cahillane — Works",
        og_image=f"{DOMAIN}/assets/og.jpg",
        og_url=f"{DOMAIN}/works.html",
    )
    body = f"""<main class="section">
  <div class="wrap center">
    <div class="eyebrow">Liminal Dimensions</div>
    <p class="lead">Original works. Enquire for availability and price.</p>
    <div class="works-filter"><button data-f="all" class="active">All</button><button data-f="available">Available</button></div>
    <div class="grid grid-3" style="text-align:left">
{cards}
    </div>
    <script>(function(){{var b=document.querySelectorAll('.works-filter button'),c=document.querySelectorAll('.grid .card');b.forEach(function(x){{x.addEventListener('click',function(){{b.forEach(function(y){{y.classList.remove('active')}});x.classList.add('active');var f=x.dataset.f;c.forEach(function(k){{k.style.display=(f==='all'||k.dataset.status==='available')?'':'none'}})}})}})}})();</script>
    <p class="form-hint" style="margin-top:48px">Selected works are also available as limited edition prints &mdash; <a href="/editions.html" style="color:var(--ink)">view editions</a>.</p>
  </div>
</main>
"""
    with open(os.path.join(ROOT, "works.html"), "w") as f:
        f.write(head + body + FOOT)
    print("wrote works.html")


def build_work(w, prev_w, next_w):
    label = STATUS_LABEL.get(w["status"], "")
    desc = w.get("description") or f'{w["title"]}, {w["year"]} — {w["medium"]}, {w["dimensions_cm"]}.'
    head = HEAD.format(
        title=f'{w["title"]} — Benjamin Cahillane',
        desc=esc(desc),
        og_title=esc(f'{w["title"]} — Benjamin Cahillane'),
        og_image=f'{DOMAIN}{w["image"]}',
        og_url=f'{DOMAIN}/work/{w["slug"]}.html',
    )

    cross = ""
    if w.get("edition_slug"):
        cross = (
            f'<p class="cross-sell">A limited edition print of this work is available '
            f'&rarr; <a href="/editions.html#{esc(w["edition_slug"])}">View edition</a></p>'
        )

    desc_html = f'<p class="work-desc">{esc(w["description"])}</p>' if w.get("description") else ""

    prev_link = f'<a href="/work/{esc(prev_w["slug"])}.html">&larr; {esc(prev_w["title"])}</a>' if prev_w else '<span></span>'
    next_link = f'<a href="/work/{esc(next_w["slug"])}.html">{esc(next_w["title"])} &rarr;</a>' if next_w else '<span></span>'

    body = f"""<main class="work-detail">
  <div class="wrap">
    <div class="work-images">
      <img id="work-main" class="work-main" src="{esc(w["image"])}?v=5" alt="{esc(w["title"])}, {esc(w["year"])}" width="1024" height="1024">
      <div class="work-thumbs">
        <button class="thumb active" data-src="{esc(w["image"])}?v=5" aria-label="Artwork"><img src="{esc(w["image"])}?v=5" alt="" loading="lazy"></button>
        <button class="thumb" data-src="/assets/works/{esc(w["slug"])}-room.jpg?v=5" aria-label="In situ"><img src="/assets/works/{esc(w["slug"])}-room.jpg?v=5" alt="{esc(w["title"])} in situ" loading="lazy"></button>
        <button class="thumb" data-src="/assets/works/{esc(w["slug"])}-detail.jpg?v=5" aria-label="Detail"><img src="/assets/works/{esc(w["slug"])}-detail.jpg?v=5" alt="{esc(w["title"])} detail" loading="lazy"></button>
      </div>
      <script>(function(){{var m=document.getElementById('work-main'),t=document.querySelectorAll('.work-thumbs .thumb');t.forEach(function(b){{b.addEventListener('click',function(){{m.src=b.dataset.src;t.forEach(function(x){{x.classList.remove('active')}});b.classList.add('active')}})}})}})();</script>
      <div class="work-nav">{prev_link}{next_link}</div>
    </div>
    <div class="work-info">
      <h1>{esc(w["title"])}</h1>
      <div class="specs">
        {esc(w["year"])}<br>
        {esc(w["medium"])}<br>
        {esc(w["dimensions_cm"])} &nbsp;/&nbsp; {esc(w["dimensions_in"])}
      </div>
      <span class="dot {esc(w["status"])}">{esc(label)}</span>
      {desc_html}
      {cross}
      <form id="inquire" class="ajax-form inquiry-form" action="https://api.web3forms.com/submit" method="POST" style="margin-top:34px">
        <input type="hidden" name="access_key" value="80a4ed81-4021-4186-8798-02459c5d3434">
        <input type="hidden" name="subject" value="Inquiry: {esc(w["title"])} — cahillane.art">
        <input type="hidden" name="from_name" value="cahillane.art">
        <input type="hidden" name="work_title" value="{esc(w["title"])}">
        <input type="hidden" name="work_slug" value="{esc(w["slug"])}">
        <input type="checkbox" name="botcheck" style="display:none" tabindex="-1" autocomplete="off">
        <label>Name<input type="text" name="name" required></label>
        <label>Email<input type="email" name="email" required></label>
        <label>Message<textarea name="message" placeholder="I'd like to enquire about this work."></textarea></label>
        <button type="submit" class="btn">Send inquiry</button>
      </form>
      <div class="form-success">Thank you — we'll be in touch shortly.</div>
    </div>
  </div>
</main>
"""
    os.makedirs(os.path.join(ROOT, "work"), exist_ok=True)
    with open(os.path.join(ROOT, "work", f'{w["slug"]}.html'), "w") as f:
        f.write(head + body + FOOT)


def main():
    with open(os.path.join(ROOT, "assets", "works.json")) as f:
        data = json.load(f)
    works = sorted(data["works"], key=lambda w: w.get("order", 0))
    build_works(works)
    for i, w in enumerate(works):
        prev_w = works[i - 1] if i > 0 else None
        next_w = works[i + 1] if i < len(works) - 1 else None
        build_work(w, prev_w, next_w)
    print(f"wrote {len(works)} work pages -> /work/")


if __name__ == "__main__":
    main()
