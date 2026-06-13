# CAHILLANE — Site Plan

Decisions locked (2026-06-13): **fully hand-coded static** (GitHub Pages, no platform/backend), **English only**, **no content produced yet** — so this is a structure-first plan with placeholders + a content checklist.

Design language carried from `circle.html`: dark restrained palette (`#0a0a0c` bg, `#e9e7e2`/`#f2f0ea` text, `#8e8c85` muted), League Spartan / Avenir Next for the wordmark, DM Sans for body, wide letter-spacing, image-first, quiet type. Mobile-first throughout.

---

## 0. Foundations (build once, used everywhere)

**File structure**
```
/index.html            Home (stays coming-soon until launch, then swapped)
/works.html            Originals grid
/work.html             Single-work template (reads ?id= from works.json)  [or generated pages]
/about.html            About
/view.html             The Private View (rename of circle.html)
/contact.html          Contact (or fold into footer)
/editions.html         DEFERRED — prints, priced, cart
/assets/
  site.css             shared design system (extract the CSS out of circle.html)
  works.json           the data model for all works
  /works/<slug>/...    per-work images (full + thumb)
```

**Shared components**
- Extract the inline CSS into `assets/site.css` so every page shares one system (currently it's locked inside `circle.html`).
- **Header** (all pages except coming-soon home): centered wordmark + minimal nav. Mobile = hamburger → full-screen slide-out (mmcgrath pattern). Nav: **Works · About · The Private View · Contact**.
- **Footer** (all pages): wordmark, Instagram, `info@cahillane.de`, © year, one quiet Private View signup link.
- Header/footer markup duplicated per page (simplest for static) OR injected via a tiny `include.js`. Recommend a small include.js to avoid drift.

**Motion / interaction principles**: minimal. Slow fades on image hover, smooth scroll, no carousels-for-the-sake-of-it. Restraint is the brand.

---

## 1. Data & content model

**`works.json`** — single source of truth; the grid and detail pages both render from it.
```json
{
  "slug": "untitled-threshold",
  "title": "Untitled (Threshold)",
  "year": 2026,
  "medium": "Acrylic & engraved silver on canvas",
  "dimensions_cm": "150 × 100 cm",
  "dimensions_in": "59 × 39¼ in",
  "status": "available",          // available | reserved | sold
  "price": null,                   // null = inquiry only (originals)
  "edition_slug": null,            // link to an Editions item if a print exists
  "images": ["assets/works/untitled-threshold/full.jpg"],
  "thumb": "assets/works/untitled-threshold/thumb.jpg",
  "description": "",
  "featured": true,
  "order": 1
}
```

**Availability dots** (the Kuznetsov mechanic): `available` = green, `reserved` = amber, `sold` = red. Small dot + label, on both grid and detail.

**Inquiry mechanism (originals)**: each work's "Inquire" opens a Web3Forms form pre-filled with hidden `work_title` + `work_slug`, so the inbox shows exactly which piece. Reuses the existing access key. No price ever shown on originals.

**Image pipeline**: you provide high-res; a small script (PIL/ImageMagick) generates two sizes per work — `thumb.jpg` (~800px, grid) and `full.jpg` (~1600px, detail) — progressive JPEG, q≈82. Avoids shipping 6 MB originals (the mistake we already corrected once).

---

## 2. Per-page plans

### A. Home — `index.html`
**Job:** 5-second impression → route to Works or The Private View.
**Phasing:** stays the current *coming-soon* page (wordmark + Private View capture) until you have ~6+ photographed works. Then swap to the full home below.
**Full-home sections (top→bottom):**
1. Full-bleed hero work + wordmark + one-line hook.
2. **Featured strip** — 3–6 strongest pieces (pulls `featured:true` from works.json) → click into Works.
3. One quiet line of statement (1 sentence, not a paragraph).
4. **The Private View** capture (single field + Request access).
5. Footer.
**Needs from you:** 1 hero image, 3–6 featured works, 1 sentence of positioning.

### B. Works — `works.html`  ← the heart
**Job:** present the originals as a gallery; make scarcity visible.
**Layout:** responsive grid — 1 col (mobile) → 2 (tablet) → 2–3 (desktop), generous gaps, images do the talking. Each card: image, title · year, **availability dot**. No prices.
**Interactions:** subtle hover (slight zoom / saturation lift), lazy-load, fixed aspect handling to prevent layout shift.
**Filter (optional, v1.1):** All / Available / Sold — the Sold view is social proof, don't hide it.
**Empty/低 state:** if few works, center the grid and let them breathe rather than stretch.
**Needs from you:** photographed works + the works.json fields per piece.

### C. Work detail — `work.html?id=<slug>`  (or generated static pages)
**Job:** sell one piece; convert to inquiry.
**Layout (mobile-first, single column):**
- Large image (tap to zoom / lightbox), multiple shots if available (incl. one in-situ for scale).
- Meta block: Title · Year / medium / dimensions (cm + in) / **availability dot + label**.
- **"Inquire"** button → pre-filled Web3Forms (price on request). Never a number.
- Short description (optional, 1–3 sentences).
- Quiet cross-sell *only if* an edition exists: "A limited edition print of this work is available →".
- Prev / Next work navigation.
**Important technical note:** a JSON+JS template (`work.html?id=`) is easiest to maintain but **social/SEO crawlers don't run JS** — shared links won't get per-work preview images. If sharing individual works on Instagram/links matters (it will), the better path is a tiny **generator script** that reads works.json and emits a real static HTML file per work with correct OG tags. Recommend: author in JSON, generate static pages. (Decision flagged in Open Questions.)
**Needs from you:** per-work photos (straight-on + ideally in-situ), medium, dimensions, status.

### D. About — `about.html`
**Job:** credibility — collectors buy the person as much as the painting.
**Sections:** portrait or studio photo → short bio (2–3 short paras) → artist statement (about the work / first collection) → optional studio image → **Selected exhibitions / collaborations** (when they exist) → quiet CTA into The Private View.
**Needs from you:** portrait/studio photo, bio, statement. Exhibitions deferred until real.

### E. The Private View — `view.html` (rename of `circle.html`, already built)
**Job:** convert — both the permanent "join" page and the paid-traffic landing page.
**Status:** done; just rename the file and link it from nav. Keep `noindex` while it doubles as the ad LP, or split into two files if you want it indexed as a normal page later.

### F. Contact — `contact.html` (or footer-only)
**Job:** inquiries, press, representation.
**Content:** `info@cahillane.de`, a short inquiry form (Web3Forms), Instagram, location/studio (optional), a line for gallery/representation enquiries.
**Needs from you:** Instagram handle, whether to list a location.

### G. Editions — `editions.html`  **(DEFERRED)**
**Job:** sell prints with visible prices + checkout. Build only when a real edition line exists.
**Plan:** separate grid (never mixed with originals), listed prices, edition/stock count, **Shopify Buy Button or Stripe Payment Link embedded** into the static page (keeps us hand-coded, adds checkout without a platform). Adds "Editions" to nav at that point.

---

## 3. Cross-cutting

**SEO / OG:** per-page `<title>`, description, and OG image. Per-work OG needs the generator approach (see C). Add a `sitemap.xml` + `robots.txt` at launch (keep `view.html` noindex while it's the ad LP).

**Analytics + GDPR (you're on .de — this matters):**
- **Meta Pixel** requires consent → needs a cookie-consent banner under GDPR/ePrivacy.
- Recommend **Plausible or similar cookieless analytics** for general traffic (no banner needed) + load the Pixel only after consent for ad campaigns. Keeps the site clean and compliant.
- Add a short **Impressum + Privacy** page (legally required in Germany).

**Performance:** compressed responsive images, `width`/`height` on every img (no layout shift), lazy-load below the fold, preconnect fonts, minimal JS.

**Accessibility:** real alt text per work, visible focus states, AA contrast (our palette passes), semantic headings, keyboard-navigable menu/lightbox.

---

## 4. Content you need to produce (nothing exists yet)

**Photography (highest priority — the site is empty without it):**
- Each work: **straight-on shot**, even/neutral light, true color, square-on (no keystoning), high-res (long edge ≥ 2500px).
- At least one **in-situ shot** (a work on a wall, with furniture/scale) — single biggest lift to perceived value.
- One **portrait or studio shot** of you for About.
- One **hero image** for Home (can be a detail crop of a strong work).

**Writing:**
- 1-sentence positioning line (Home).
- Short bio (2–3 paragraphs) + artist statement (About).
- Optional 1–3 sentence note per work.

**Facts per work:** title, year, medium, dimensions, status (available/reserved/sold).

**Misc:** Instagram handle, whether to show a location, German Impressum details.

---

## 5. Build roadmap (suggested order)

1. **Foundations** — extract `site.css`, build shared header/footer (include.js), nav + slide-out menu. *(buildable now, no content needed)*
2. **Works + Work detail** — works.json schema, grid with dots, detail template + inquiry form, image pipeline. *(scaffold now with placeholders; fill when photos arrive)*
3. **About** — layout with placeholder bio/portrait.
4. **Rename `circle.html` → `view.html`**, wire into nav.
5. **Contact** + footer everywhere.
6. **Launch swap** — replace coming-soon `index.html` with full Home, reveal nav, add sitemap/robots, Impressum/Privacy, analytics.
7. **Later:** Editions (cart), exhibitions on About, German translation, per-work OG generator.

---

## 6. Open questions for Ben
1. **Work detail pages:** JSON+JS template (easy, weak link-sharing) vs a small generator that emits static per-work pages (best for SEO/sharing). Recommend generator — confirm.
2. **Collection size** for v1 (sizes the grid + decides if filtering is worth it).
3. **Instagram handle** + whether to show a studio location.
4. **Rename** `circle.html` → `view.html` now (URL is cost-free to change pre-launch)?
5. **Analytics:** OK to go cookieless (Plausible) + consent-gated Pixel, plus add Impressum/Privacy?
