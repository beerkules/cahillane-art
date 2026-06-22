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
import re
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
<link rel="stylesheet" href="/assets/site.css?v=38">
<link rel="icon" type="image/png" href="/assets/favicon.png?v=24">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png?v=24">
</head>
<body>
<div id="site-header"></div>
"""

FOOT = """<div id="site-footer"></div>
<script src="/assets/include.js?v=41" defer></script>
</body>
</html>
"""


def esc(s):
    return html.escape(str(s), quote=True)


def card(w):
    label = STATUS_LABEL.get(w["status"], "")
    return (
        f'<a class="card" data-cat="original" data-status="{esc(w["status"])}" href="/work/{esc(w["slug"])}.html">'
        f'<div class="card-img"><img src="{esc(w["thumb"])}?v=17" alt="{esc(w["title"])}, {esc(w["year"])}" loading="lazy"></div>'
        f'<div class="card-meta">'
        f'<span class="card-title">{esc(w["title"])}</span>'
        f'<span class="dot {esc(w["status"])}">{esc(label)}</span>'
        f'</div>'
        f'<div class="card-sub">{esc(w["year"])} · {esc(w["dimensions_cm"])}</div>'
        f'</a>'
    )


def build_works(works):
    cards = "\n".join(card(w) for w in works)
    edcards = "\n".join(edition_card(w) for w in works)
    head = HEAD.format(
        title="Works & Editions — Benjamin Cahillane",
        desc="Original works and limited edition prints by contemporary artist Benjamin Cahillane.",
        og_title="Benjamin Cahillane — Works & Editions",
        og_image=f"{DOMAIN}/assets/og.jpg",
        og_url=f"{DOMAIN}/works.html",
    )
    body = f"""<main class="section">
  <div class="wrap center">
    <style>.works-filter .filter-sep{{display:inline-block;width:1px;height:13px;background:rgba(233,231,226,.28);margin:0 12px;vertical-align:middle}}</style>
    <div class="eyebrow">Liminal Dimensions</div>
    <p class="lead">Originals and limited Editions.</p>
    <div class="works-filter"><button data-f="all" class="active">All</button><button data-f="available">Available</button><span class="filter-sep"></span><button data-f="editions">Editions</button></div>
    <div class="grid grid-3" style="text-align:left">
{cards}
{edcards}
    </div>
    <script>(function(){{var b=document.querySelectorAll('.works-filter button'),c=document.querySelectorAll('.grid .card');function apply(f){{c.forEach(function(k){{var cat=k.dataset.cat,st=k.dataset.status,show;if(f==='editions')show=cat==='edition';else if(f==='available')show=cat==='original'&&st==='available';else show=cat==='original';k.style.display=show?'':'none';}});}}b.forEach(function(x){{x.addEventListener('click',function(){{b.forEach(function(y){{y.classList.remove('active')}});x.classList.add('active');apply(x.dataset.f);}})}});if(location.hash==='#editions'){{var e=document.querySelector('.works-filter [data-f=editions]');if(e){{b.forEach(function(y){{y.classList.remove('active')}});e.classList.add('active');apply('editions');return;}}}}apply('all');}})();</script>
    <p class="form-hint" style="margin-top:48px">Be the first to see new work &mdash; <a href="/#private-view" style="color:var(--ink)">join the Private View</a>.</p>
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
            f'&rarr; <a href="/edition/{esc(w["slug"])}.html">View edition</a></p>'
        )

    desc_html = f'<p class="work-desc">{esc(w["description"])}</p>' if w.get("description") else ""
    metal = "gold leaf" if "gold" in w["medium"].lower() else "silver leaf"
    process_html = f'<p class="work-process">Genuine {metal}, dozens of translucent pigment glazes, engraved by hand. Sold with a signed certificate of authenticity.</p>'
    artwork_ld = json.dumps({"@context":"https://schema.org","@type":"VisualArtwork","name":w["title"],"image":f"{DOMAIN}{w['image']}","creator":{"@type":"Person","name":"Benjamin Cahillane"},"artform":"Painting","artMedium":w["medium"],"dateCreated":w["year"],"url":f"{DOMAIN}/work/{w['slug']}.html","creativeWorkStatus":w["status"]},ensure_ascii=False)

    prev_link = f'<a href="/work/{esc(prev_w["slug"])}.html">&larr; {esc(prev_w["title"])}</a>' if prev_w else '<span></span>'
    next_link = f'<a href="/work/{esc(next_w["slug"])}.html">{esc(next_w["title"])} &rarr;</a>' if next_w else '<span></span>'

    body = f"""<main class="work-detail">
  <div class="wrap">
    <div class="work-images">
      <div class="zoom-wrap"><img id="work-main" class="work-main" src="{esc(w["image"])}?v=17" alt="{esc(w["title"])}, {esc(w["year"])}" width="1024" height="1024"></div>
      <div class="work-thumbs">
        <button class="thumb active" data-src="{esc(w["image"])}?v=17" aria-label="Artwork"><img src="{esc(w["image"])}?v=17" alt="" loading="lazy"></button>
        <button class="thumb" data-src="/assets/works/{esc(w["slug"])}-framed.jpg?v=17" aria-label="Framed"><img src="/assets/works/{esc(w["slug"])}-framed.jpg?v=17" alt="{esc(w["title"])} framed" loading="lazy"></button>
        <button class="thumb" data-src="/assets/works/{esc(w["slug"])}-detail.jpg?v=17" aria-label="Detail"><img src="/assets/works/{esc(w["slug"])}-detail.jpg?v=17" alt="{esc(w["title"])} detail" loading="lazy"></button>
      </div>
      <script>(function(){{var m=document.getElementById('work-main'),t=document.querySelectorAll('.work-thumbs .thumb');t.forEach(function(b){{b.addEventListener('click',function(){{m.src=b.dataset.src;t.forEach(function(x){{x.classList.remove('active')}});b.classList.add('active')}})}});var zw=document.querySelector('.zoom-wrap');if(zw){{var zd=false,moved=false,touch=false;var lp=document.createElement('div');lp.className='zoom-loupe';zw.appendChild(lp);function setO(cx,cy){{var r=zw.getBoundingClientRect();var x=Math.min(Math.max(cx-r.left,0),r.width),y=Math.min(Math.max(cy-r.top,0),r.height);lp.style.left=x+'px';lp.style.top=y+'px';m.style.transformOrigin=(x/r.width*100)+'% '+(y/r.height*100)+'%';}}function tog(cx,cy){{zd=!zd;m.style.transform=zd?'scale(2.4)':'';zw.classList.toggle('zoomed',zd);lp.style.display=(touch?(zd?'block':'none'):'block');if(zd&&cx!=null)setO(cx,cy);}}zw.addEventListener('click',function(e){{if(touch)return;tog(e.clientX,e.clientY);}});zw.addEventListener('mousemove',function(e){{if(!touch)setO(e.clientX,e.clientY);}});zw.addEventListener('mouseenter',function(){{if(!touch){{lp.style.display='block';zw.style.cursor='none';}}}});zw.addEventListener('mouseleave',function(){{if(!touch){{lp.style.display='none';zw.style.cursor='';}}}});zw.addEventListener('touchstart',function(e){{touch=true;moved=false;}},{{passive:true}});zw.addEventListener('touchmove',function(e){{if(!zd)return;moved=true;e.preventDefault();var p=e.touches[0];setO(p.clientX,p.clientY);}},{{passive:false}});zw.addEventListener('touchend',function(e){{if(moved)return;var p=e.changedTouches[0];tog(p.clientX,p.clientY);e.preventDefault();}},{{passive:false}});}}}})();</script>
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
      {process_html}
      {cross}
      <form id="inquire" class="ajax-form inquiry-form" action="https://api.web3forms.com/submit" method="POST">
        <input type="hidden" name="access_key" value="80a4ed81-4021-4186-8798-02459c5d3434">
        <input type="hidden" name="subject" value="Inquiry: {esc(w["title"])} — benjamincahillane.com">
        <input type="hidden" name="from_name" value="benjamincahillane.com">
        <input type="hidden" name="work_title" value="{esc(w["title"])}">
        <input type="hidden" name="work_slug" value="{esc(w["slug"])}">
        <input type="checkbox" name="botcheck" style="display:none" tabindex="-1" autocomplete="off">
        <label>Name<input type="text" name="name" required></label>
        <label>Email<input type="email" name="email" required></label>
        <label>Message<textarea name="message" placeholder="I'd like to enquire about this work."></textarea></label>
        <button type="submit" class="btn">Send inquiry</button>
      </form>
      <div class="form-success">Thank you. I'll be in touch shortly.</div>
    </div>
  </div>
</main>
<script type="application/ld+json">{artwork_ld}</script>
"""
    os.makedirs(os.path.join(ROOT, "work"), exist_ok=True)
    with open(os.path.join(ROOT, "work", f'{w["slug"]}.html'), "w") as f:
        f.write(head + body + FOOT)



EDITION = {"medium":"Giclée print","run":"Edition of 25"}
EDITION_PORTRAIT  = [("45 × 60 cm","€ 450"),("60 × 80 cm","€ 650"),("75 × 100 cm","€ 850"),("90 × 120 cm","€ 1050")]
EDITION_LANDSCAPE = [("60 × 45 cm","€ 450"),("80 × 60 cm","€ 650"),("100 × 75 cm","€ 850"),("120 × 90 cm","€ 1050")]
EDITION_SQUARE    = [("50 × 50 cm","€ 450"),("70 × 70 cm","€ 650"),("85 × 85 cm","€ 850"),("100 × 100 cm","€ 1050")]
FROM_PRICE = EDITION_PORTRAIT[0][1]

def edition_sizes_for(w):
    nums = re.findall(r"\d+", w.get("dimensions_cm",""))
    if len(nums) >= 2:
        a, b = int(nums[0]), int(nums[1])
        if a == b: return EDITION_SQUARE
        if a > b:  return EDITION_LANDSCAPE
    return EDITION_PORTRAIT

def edition_card(w):
    return (
        f'<a class="card" data-cat="edition" href="/edition/{esc(w["slug"])}.html">'
        f'<div class="card-img"><img src="{esc(w["image"])}?v=17" alt="{esc(w["title"])} — limited edition print" loading="lazy"></div>'
        f'<div class="card-meta"><span class="card-title">{esc(w["title"])}</span><span class="card-price" style="font-size:13px;letter-spacing:.04em;color:var(--ink-bright);white-space:nowrap">From {FROM_PRICE}</span></div>'
        f'<div class="card-sub">{EDITION["medium"]} · {EDITION["run"]}</div>'
        f'</a>'
    )

def build_editions(works):
    # Editions now live on the Works page under the "Editions" filter.
    # Keep editions.html as a redirect so old links/bookmarks still work.
    redirect = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="0; url=/works.html#editions">
<link rel="canonical" href="https://benjamincahillane.com/works.html#editions">
<title>Editions — Benjamin Cahillane</title>
<meta name="robots" content="noindex">
<script>location.replace('/works.html#editions');</script>
</head>
<body><a href="/works.html#editions">Original works and limited editions</a></body>
</html>
"""
    with open(os.path.join(ROOT,"editions.html"),"w") as f: f.write(redirect)
    print("wrote editions.html")

def build_edition(w, prev_w, next_w):
    size_options = "".join(f'<option data-price="{p}">{sz} — {p}</option>' for sz,p in edition_sizes_for(w))
    head = HEAD.format(title=f'{w["title"]} — Edition — Benjamin Cahillane',
        desc=f'Limited edition print of {w["title"]}. {EDITION["run"]}, signed and numbered.',
        og_title=esc(f'{w["title"]} — Edition'), og_image=f'{DOMAIN}{w["image"]}', og_url=f'{DOMAIN}/edition/{w["slug"]}.html')
    prev_link = f'<a href="/edition/{esc(prev_w["slug"])}.html">&larr; {esc(prev_w["title"])}</a>' if prev_w else '<span></span>'
    next_link = f'<a href="/edition/{esc(next_w["slug"])}.html">{esc(next_w["title"])} &rarr;</a>' if next_w else '<span></span>'
    body = f"""<main class="work-detail">
  <div class="wrap">
    <div class="work-images">
      <div class="zoom-wrap"><img id="work-main" class="work-main" src="{esc(w["image"])}?v=17" alt="{esc(w["title"])} edition" width="1024" height="1024"></div>
      <script>(function(){{var m=document.getElementById('work-main'),zw=document.querySelector('.zoom-wrap');if(zw){{var zd=false;var lp=document.createElement('div');lp.className='zoom-loupe';zw.appendChild(lp);zw.addEventListener('click',function(){{zd=!zd;m.style.transform=zd?'scale(2.4)':'';zw.classList.toggle('zoomed',zd);lp.style.display=zd?'block':'none'}});zw.addEventListener('mousemove',function(e){{var r=zw.getBoundingClientRect();var x=e.clientX-r.left,y=e.clientY-r.top;lp.style.left=x+'px';lp.style.top=y+'px';if(zd)m.style.transformOrigin=(x/r.width*100)+'% '+(y/r.height*100)+'%'}});zw.addEventListener('mouseleave',function(){{lp.style.display='none';zw.style.cursor=''}});zw.addEventListener('mouseenter',function(){{lp.style.display='block';zw.style.cursor='none'}})}}}})();</script>
      <div class="work-nav">{prev_link}{next_link}</div>
    </div>
    <div class="work-info">
      <h1>{esc(w["title"])}</h1>
      <div class="specs">Limited edition<br>{EDITION["medium"]} · {EDITION["run"]}<br>Signed &amp; numbered</div>
      <span class="dot available">Available</span>
      <p class="work-desc">A signed, numbered Giclée print of the original, on archival cotton paper, with a certificate of authenticity.</p>
      <div class="edition-buy">
        <label class="edition-size-label">Size &amp; price
          <select id="edition-size">{size_options}</select>
        </label>
        <a class="btn" id="edition-add" href="#" data-edition="{esc(w["slug"])}">Add to cart</a>
        <p class="form-hint" style="margin-top:14px">Signed &amp; numbered · shipping calculated at checkout.</p>
      </div>
      <p class="work-process"><a href="/work/{esc(w["slug"])}.html" style="color:var(--ink)">View the original work &rarr;</a></p>
    </div>
  </div>
</main>
"""
    os.makedirs(os.path.join(ROOT,"edition"),exist_ok=True)
    with open(os.path.join(ROOT,"edition",f'{w["slug"]}.html'),"w") as f: f.write(head+body+FOOT)


def main():
    with open(os.path.join(ROOT, "assets", "works.json")) as f:
        data = json.load(f)
    works = sorted(data["works"], key=lambda w: w.get("order", 0))
    build_works(works)
    build_editions(works)
    for i, w in enumerate(works):
        prev_w = works[i - 1] if i > 0 else None
        next_w = works[i + 1] if i < len(works) - 1 else None
        build_work(w, prev_w, next_w)
        build_edition(w, prev_w, next_w)
    # sitemap + robots
    pages=["","works.html","editions.html","studio.html","about.html","contact.html","view.html","legal.html","privacy.html"]+[f"work/{w['slug']}.html" for w in works]+[f"edition/{w['slug']}.html" for w in works]
    urls="".join(f"<url><loc>{DOMAIN}/{p}</loc></url>" for p in pages)
    with open(os.path.join(ROOT,"sitemap.xml"),"w") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    with open(os.path.join(ROOT,"robots.txt"),"w") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
    print(f"wrote {len(works)} work pages + sitemap + robots")


if __name__ == "__main__":
    main()
