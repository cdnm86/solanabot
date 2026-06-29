# Villa Mukinja — Website

Modern, fast, SEO-ready static website for Villa Mukinja, a boutique hotel at Plitvice Lakes, Croatia.
Built per the Rapid Launch playbooks (Option A: website-first, tracking-ready).

## Run locally

```bash
cd villa-mukinja
python3 -m http.server 4012
# open http://localhost:4012
```

## Structure

```
villa-mukinja/
├── index.html              Home
├── rooms.html              Rooms & suites
├── wellness.html           Sauna & hot tub
├── restaurant.html         Dining
├── activities.html         Things to do
├── contact.html            Location, map, contact form
├── booking.html            Booking (rentl.io slot) — primary conversion
├── privacy.html / terms.html / 404.html
├── sitemap.xml, robots.txt
├── build-tokens.py         Injects shared footer + SVG icons into pages
└── assets/
    ├── css/style.css       Design system (tokens, components, responsive)
    ├── js/main.js          Nav, reveal animations, lightbox, tracking-ready events
    └── images/             Real photos pulled from the live site
```

## Editing shared footer / icons

The footer and inline icons are defined once in `build-tokens.py`. To change them, edit that file
and re-run `python3 build-tokens.py`. (Pages already have resolved HTML; the script is idempotent.)

## Design system

- **Theme:** "Forest & Lake" — deep pine green, lake teal, warm brass on cream.
- **Fonts:** Cormorant Garamond (display) + Inter (body). *Self-host before production per playbook.*
- **Tokens & 8px spacing scale, reusable components, semantic HTML.**

## Performance & SEO (Option A baseline — done)

- LCP hero preloaded with `fetchpriority="high"`; below-fold images lazy-loaded.
- One H1 per page, logical headings, unique titles/metas, canonical + Open Graph.
- Schema: `Hotel` (home) + `BreadcrumbList` (rooms).
- `sitemap.xml` + `robots.txt` prepared.
- Mobile sticky call/book CTA; respects `prefers-reduced-motion`.

## Tracking-ready (for Option B upgrade)

Built so analytics/ads can be layered on **without editing templates**:

- Consistent CTA classes: `.cta-primary`, `.cta-secondary`, `.whatsapp-link`.
- Proper `tel:` / `mailto:` / `wa.me` hrefs and a lead form with `data-form-type`.
- `assets/js/main.js` already pushes events to `window.dataLayer`
  (`phone_click`, `whatsapp_click`, `email_click`, `cta_click`, `form_start`, `form_submit`)
  — GTM/GA4 will pick these up automatically when added.

## Before launch (Option A checklist)

- [ ] Paste rentl.io booking embed into `#booking-widget` on `booking.html`
- [ ] Wire contact & enquiry forms to email
- [ ] Confirm real prices, room details, reviews
- [ ] Finalise privacy/terms; add cookie consent when analytics is added
- [ ] Self-host fonts; convert images to WebP/AVIF
- [ ] Set final domain in canonical/OG/sitemap; remove any noindex
```
