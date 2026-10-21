# CloudyMind Solutions – Freelancer-kotisivut & Blogi

CloudyMind Oy:n / Jyrki Heinosen verkkosivusto ja asiantuntijablogi. 

Sivusto esittelee freelancerina tarjotut Azure-pilviarkkitehtuuripalvelut, tuotteistetun Azure-terveystarkastuksen, FinOps-kustannusoptimoinnin sekä julkaisee blogikirjoituksia ja teknisiä löydöksiä.

## Ominaisuudet
- **Staattinen ja salamannopea:** Puhdasta HTML5, CSS3 ja kevyttä JavaScriptiä ilman raskaat riippuvuudet.
- **Pehmeä väripaletti & teematuki:** Sisäänrakennettu tuki järjestelmän oletuksen mukaiselle tummalle teemalle (`prefers-color-scheme: dark`) sekä manuaalinen teemakytkin (Light / Dark mode tallennettuna selaimen muistiin).
- **GitHub Pages & Actions:** Täysin automatisoitu julkaisu GitHub Actions -työnkululla (`.github/workflows/deploy.yml`).
- **Valmius omalle domainille:** Sivusto toimii GitHub Pages -osoitteessa sekä tukee suoraan omaa domainia (esim. `cloudymind.fi`) lisäämällä `CNAME`-tiedoston.
- **SEO & saavutettavuus:** Responsiivinen ulkoasu, semanttinen HTML, `sitemap.xml` ja `robots.txt`.

## Sivurakenne
- `index.html` – Etusivu (arvolupaus, palvelukortit, uusimmat blogikirjoitukset, yhteenveto minusta ja CTA)
- `palvelut/index.html` – Palvelut (Azure-terveystarkastus, Landing Zonet, FinOps-kustannushallinta, Governance & tietoturva)
- `blog/index.html` – Blogin etusivu ja artikkelilistaus
  - `blog/azure-cost-quick-wins.html` – Azure Cost Quick Wins: 10 säästökohdetta
  - `blog/expiring-entra-id-secrets.html` – Vanhenevat Entra ID -sovellussalaisuudet
  - `blog/palkkatyosta-freelanceriksi-tuntihinta.html` – Palkkatyöstä freelanceriksi: Minimituntihinnan laskenta
- `minusta.html` – Esittely ja tausta (Azure-pilviarkkitehtuuri, SaaS-kokemus, tiimileadius, sertifikaatit)
- `yhteys.html` – Yhteystiedot, sähköposti, LinkedIn, GitHub ja CloudyMind Oy:n yritystiedot
- `tietosuoja.html` – Evästeetön ja kevyt tietosuojaseloste
- `css/style.css` – CSS-tyylit ja muuttujat (Design tokens)
- `js/main.js` – Teemakytkimen ja mobiilivalikon logiikka

## Sivun lataus ja selaintestit

Jokaisen HTML-sivun `<head>` palauttaa tallennetun teeman pienellä
inline-skriptillä ennen tyylitiedostoa. Ilman tallennettua valintaa CSS käyttää
järjestelmän teemaa. `js/main.js` ladataan `defer`-attribuutilla, jotta sen
lataaminen ei estä sivun sisällön näyttämistä. Säilytä tämä järjestys myös uusilla
sivuilla: teeman palautus, tyylitiedosto, viivästetty vuorovaikutusskripti.

Sivusto ei tarvitse ajonaikaisia riippuvuuksia tai koontivaihetta. Valinnaiset
Python-selaintestit käyttävät Playwrightia:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r tests\requirements.txt
.\.venv\Scripts\python.exe -m playwright install chromium
.\.venv\Scripts\python.exe tests\test_page_loading.py
```

Asennettua Microsoft Edgeä voi käyttää Chromium-latauksen sijaan asettamalla
`$env:BROWSER_CHANNEL = 'msedge'` ennen testien ajamista.

Testit pitävät `main.js`-pyynnön odottamassa ja varmistavat, että kaikki HTML-sivut
piirtyvät oikealla teemalla jo ennen sen valmistumista. Lisäksi testataan
teemavalinnan tallennus, järjestelmän teeman muutokset, mobiilivalikko ja sisällön
näkyminen ilman JavaScriptiä.
