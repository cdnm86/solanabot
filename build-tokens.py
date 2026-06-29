#!/usr/bin/env python3
"""Inject shared footer + inline SVG icons into all HTML files.
Run once after editing pages: python3 build-tokens.py
Idempotent — only replaces ${TOKENS}, leaves resolved HTML untouched."""
import glob, re

ICON = {
"CHECK": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>',
"INFO": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg>',
"ICON_SAUNA": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M6 13c0-2 1-3 1-4.5S6 6 6 6m4 7c0-2 1-3 1-4.5S10 6 10 6m4 7c0-2 1-3 1-4.5S14 6 14 6"/><path d="M3 21h18M5 21v-4h14v4"/></svg>',
"ICON_COFFEE": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M17 8h1a4 4 0 1 1 0 8h-1"/><path d="M3 8h14v9a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4Z"/><path d="M6 2v2M10 2v2M14 2v2"/></svg>',
"ICON_WIFI": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.55a11 11 0 0 1 14 0M8.5 16.1a6 6 0 0 1 7 0M2 8.82a15 15 0 0 1 20 0"/><path d="M12 20h.01"/></svg>',
"ICON_PARKING": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="3"/><path d="M9 17V7h4a3 3 0 0 1 0 6H9"/></svg>',
"ICON_PIN": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>',
"ICON_PHONE": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92Z"/></svg>',
"ICON_MAIL": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg>',
"ICON_WALK": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="13" cy="4" r="2"/><path d="m9 20 2-5 2 2v3m-2-9 3-2 2 3 2 1m-7-2-2 4"/></svg>',
}

FB = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M22 12a10 10 0 1 0-11.56 9.88v-6.99H7.9V12h2.54V9.8c0-2.5 1.49-3.89 3.78-3.89 1.09 0 2.24.2 2.24.2v2.46h-1.26c-1.24 0-1.63.77-1.63 1.56V12h2.78l-.45 2.89h-2.33v6.99A10 10 0 0 0 22 12Z"/></svg>'
IG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><path d="M17.5 6.5h.01"/></svg>'

FOOTER = f'''<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <a class="brand" href="index.html" style="margin-bottom:var(--s3)"><span class="name">Villa Mukinja</span><span class="sub">Plitvice Lakes · Croatia</span></a>
        <p>A family-run boutique hotel and wellness retreat, a ten-minute walk from Plitvice Lakes National Park. Comfortable beds, a sauna and hot tub, and a breakfast to die for.</p>
        <div class="socials">
          <a href="https://www.facebook.com/villa.mukinja/" target="_blank" rel="noopener" aria-label="Facebook">{FB}</a>
          <a href="https://www.instagram.com/villamukinja" target="_blank" rel="noopener" aria-label="Instagram">{IG}</a>
          <a href="https://wa.me/385997877479" target="_blank" rel="noopener" aria-label="WhatsApp" class="whatsapp-link">{ICON["ICON_PHONE"]}</a>
        </div>
      </div>
      <div>
        <h4>Explore</h4>
        <ul>
          <li><a href="rooms.html">Rooms &amp; Suites</a></li>
          <li><a href="wellness.html">Wellness &amp; Spa</a></li>
          <li><a href="restaurant.html">Restaurant</a></li>
          <li><a href="activities.html">Activities</a></li>
        </ul>
      </div>
      <div>
        <h4>Visit</h4>
        <ul>
          <li><a href="contact.html">Location</a></li>
          <li><a href="booking.html" data-book>Book a Stay</a></li>
          <li><a href="contact.html">Contact Us</a></li>
        </ul>
      </div>
      <div>
        <h4>Get in touch</h4>
        <div class="contact-row">{ICON["ICON_PIN"]}<span>Mukinje 47, 53231<br>Plitvička Jezera, Croatia</span></div>
        <div class="contact-row">{ICON["ICON_PHONE"]}<a href="tel:+385997877479">+385 99 7877 479</a></div>
        <div class="contact-row">{ICON["ICON_MAIL"]}<a href="mailto:villa.mukinja@gmail.com">villa.mukinja@gmail.com</a></div>
        <a class="btn btn-primary cta-primary" href="booking.html" data-book style="margin-top:var(--s2)">Book Now</a>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span id="year">2026</span> Villa Mukinja. All rights reserved.</span>
      <span><a href="privacy.html">Privacy</a> · <a href="terms.html">Terms</a> · Crafted with care in Croatia</span>
    </div>
  </div>
</footer>'''

tokens = {"FOOTER": FOOTER}
tokens.update(ICON)

count = 0
for path in glob.glob("*.html"):
    html = open(path, encoding="utf-8").read()
    orig = html
    for name, val in tokens.items():
        html = html.replace("${" + name + "}", val)
    if html != orig:
        open(path, "w", encoding="utf-8").write(html)
        count += 1
        print(f"  resolved tokens in {path}")
# warn on any leftover tokens
leftover = set()
for path in glob.glob("*.html"):
    for m in re.findall(r"\$\{([A-Z_]+)\}", open(path, encoding="utf-8").read()):
        leftover.add(m)
print(f"Done. Updated {count} files.")
if leftover:
    print("WARNING leftover tokens:", leftover)
