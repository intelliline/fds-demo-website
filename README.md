# fds-demo-website

Proposed website for **First Digital Surveillance** (CCTV installation, Los Angeles).
Static site — no framework, no build step at deploy time. Every page is plain HTML.

## Deploy

Vercel picks this up as a static site with no configuration. `vercel.json` turns on clean URLs
(`/services` instead of `/services.html`), sets long cache headers on `/assets`, and sends
`X-Robots-Tag: noindex` so this preview never competes with the client's live domain in search.

## Local preview

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

## Structure

| Path | What it is |
|---|---|
| `index.html` | Home — live camera wall, speed to lead, services, AI analytics, process, reviews, FAQ |
| `services.html` | Nine services, each with its own live camera view |
| `solutions.html` | Hardware, multi-site camera wall, industry solutions, remote monitoring |
| `service-areas.html` | 24-city service-area hub |
| `contact.html` | Contact, quote form, site-visit booker, coverage map |
| `assets/css/style.css` | Design system — brand tokens at the top |
| `assets/js/fds.js` | All behaviour. `FDS_CONFIG` at the top is the only thing you edit to go live |
| `assets/img/` | Logo and favicon, rebuilt as SVG |
| `FDS-shareable-preview.html` | All five pages bundled into a single self-contained file |
| `src/build.py` | Generator — edit content once, rebuild every page (`python3 src/build.py`) |
| `robots.production.txt` | The robots.txt for the real domain. `robots.txt` here blocks the preview host. |

## Configuration

Everything is in `FDS_CONFIG` at the top of `assets/js/fds.js`:

- `crmWebhookUrl` — where leads go. Blank = demo mode, nothing leaves the browser.
- `callbackSeconds` / `avgResponseSeconds` — the speed-to-lead numbers, used on every page.
- `gtmId` / `ga4Id` — analytics.
- `callTrackingNumber` — swaps every visible phone number for dynamic number insertion.

## Notes

- Brand red `#BF1220` and navy `#1D4F91` are sampled from the client's existing logo.
- The camera views are hand-built SVG/CSS animations, not stock footage. Any `.feed` block accepts a
  `<video autoplay muted loop playsinline>` if real job-site clips become available.
- A "design preview" band sits above the header on every page so this is never mistaken for the
  client's live site. Remove `.demoband` from `build.py` when the site goes into production.
