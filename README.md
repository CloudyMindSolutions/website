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
