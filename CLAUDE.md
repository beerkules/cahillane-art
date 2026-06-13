# CLAUDE.md — project memory for Benjamin Cahillane

Read this first. It is the single source of truth for any session (loaded automatically by Claude Code). Deep detail lives in **`SITE-PLAN.md`** (per-page plan) and **`DESIGN-NOTES.md`** (decisions + inspiration).

## What this is
Marketing + portfolio website for **Benjamin Cahillane**, contemporary artist. Goal: build a collector audience ("The Private View" email list), then sell originals (inquiry) and editions (priced) direct — feeding an Instagram → link-in-bio → site → sale funnel.

## Tech & conventions
- **Fully hand-coded static site.** No framework, no backend. Hosted on **GitHub Pages**, custom domain **benjamincahillane.com**.
- **Work on the `main` branch** — pushing to `main` publishes live. (User directive: "always work on live." The branch `claude/mobile-design-inspiration-iwxp6j` is stale; ignore it.)
- **English only.**
- Shared design system: `assets/site.css`. Shared header/footer/mobile-menu + form handler: `assets/include.js` (pages include `<div id="site-header"></div>` / `<div id="site-footer"></div>`).
- **Works are data-driven:** edit `assets/works.json`, then run **`python3 build.py`** to regenerate `works.html` and `work/<slug>.html` (static per-work pages with their own OG tags). Don't hand-edit generated files.
- Internal links/assets use root-absolute paths (`/assets/...`, `/work/...`).
- Forms post to **Web3Forms** (access key already in the HTML). Web3Forms blocks server-side POSTs, so forms can only be tested from a real browser.
- Palette: bg `#0a0a0c`, ink `#e9e7e2`/`#f2f0ea`, muted `#8e8c85`. Fonts: League Spartan/Avenir Next (display), DM Sans (body). Dark, restrained, image-first, mobile-first.

## Page map
- `index.html` — LIVE coming-soon (wordmark + Private View capture). Swap for `home.html` at launch.
- `home.html` — full home (hero, selected works, statement, capture). Not yet the live page.
- `works.html` — originals grid (generated). `work/*.html` — per-work pages (generated).
- `editions.html` — prints, priced, Add-to-cart placeholders (wire Stripe/Shopify later).
- `about.html`, `contact.html` — scaffolds.
- `view.html` — The Private View (also the paid-traffic landing page; `noindex`). `circle.html` redirects here.
- `privacy.html`, `legal.html` — Swiss legal pages (placeholders to fill).
- `positioning-preview.html` — throwaway preview page for copy review.

## Brand decisions (locked)
- **Name/wordmark:** "Benjamin Cahillane" everywhere; logo lockup is `BENJAMIN` / `CAHILLANE` stacked, wide tracking.
- **Tagline:** "Silence in space."
- **Mailing list:** "The Private View" · CTA "Request access" · success "You'll see it first."
- **Pricing (tiered):** originals = inquiry only, no public price; editions = priced + checkout.
- **IA:** Works (originals) and Editions (prints) are separate sections, never one grid. Launch nav: Works · About · The Private View · Contact. Add Editions when a real print line exists.
- **Availability dots:** green=available, amber=reserved, red=sold (from `works.json` `status`).

## Legal / privacy
- Operator is in **Switzerland**; governing law **revFADP (nDSG)**. GDPR still applies to EU ad traffic.
- `privacy.html` + `legal.html` exist with `[bracketed]` placeholders — fill legal name + Swiss address before selling. Not legal advice; have reviewed.
- **No analytics enabled** (decision). Future: Plausible (cookieless) + consent-gated Meta Pixel for campaigns.

## Marketing context
- Plan: ~€5k/mo Meta ads, optimized for collector **emails** over vanity followers. Funnel lands on `view.html`.
- Inspiration: fabianutta.com, mmcgrath.com (mobile/gallery feel), alexkuznetsov.org (sold/available dots). See `DESIGN-NOTES.md`.

## Outstanding / TODO
1. **HTTPS cert** (blocker) — GitHub Pages custom-domain certificate not provisioned; site shows "connection not private." Fix in repo Settings → Pages + DNS (A records 185.199.108–111.153; `www` CNAME → beerkules.github.io). Cannot be done via API/this tooling — user action.
2. **Real photos + bio** — replace placeholder images (currently reuse `assets/hero.jpg`/`og.jpg`) and About copy. Target first collection ~10–12 works, mostly vertical + a few landscape.
3. **Fill legal placeholders** in `privacy.html` / `legal.html`.
4. At launch: swap `index.html` → home content, add `sitemap.xml` + `robots.txt`, reveal nav.
5. Later: Editions checkout (Stripe/Shopify), exhibitions on About, analytics + Pixel.
