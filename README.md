# CloudyMind Oy

Bilingual static portfolio website for CloudyMind Oy, presenting Azure cloud architecture, governance, security, and FinOps services in English and Finnish.

## Features
- Built with semantic HTML, CSS, and vanilla JavaScript.
- Responsive layout with a soft colour palette, system-based dark theme, and manual theme toggle.
- English pages are at the site root; Finnish pages are under `fi/`. Each page links to its counterpart in the other language.
- Published to GitHub Pages using GitHub Actions (`.github/workflows/deploy.yml`).
- Includes a sitemap and robots policy for search engines.

## Site structure
- `index.html`, `services/index.html`, `about.html`, `contact.html`, `privacy.html` – English site
- `fi/index.html`, `fi/services/index.html`, `fi/about.html`, `fi/contact.html`, `fi/privacy.html` – Finnish site
- `css/style.css` – Site styling and theme tokens
- `js/main.js` – Theme toggle and mobile navigation
- `css/style.css` – CSS-tyylit ja muuttujat (Design tokens)
- `js/main.js` – Teemakytkimen ja mobiilivalikon logiikka

## Availability badge animation

The English and Finnish homepages share a CSS-only availability badge. Its halo
animates `transform` and `opacity` instead of repainting a `box-shadow` every
frame. The solid dot stays the same size and follows the current theme.
With `prefers-reduced-motion: reduce`, the halo is disabled and the dot stays visible.

### Optional browser regression tests

These development-only tests cover both languages, light/dark themes, mobile and
desktop sizes, live reduced-motion changes, and the badge without JavaScript.
They do not add a production build step or runtime dependency.

```powershell
python -m pip install -r tests\requirements.txt
python -m playwright install chromium
python tests\test_pulse_animation.py -v
```

To use an already-installed Microsoft Edge instead of downloading Chromium,
skip the browser installation and set `$env:BROWSER_CHANNEL = 'msedge'` before
running the tests.
