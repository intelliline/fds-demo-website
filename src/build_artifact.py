#!/usr/bin/env python3
"""Bundle all five pages into one self-contained, shareable page."""
import base64, pathlib, re, importlib.util

HERE = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("fdsbuild", HERE / "build.py")
B = importlib.util.module_from_spec(spec)
spec.loader.exec_module(B)

# ---- capture each page's body instead of writing files -------------------
PAGES = {}
def collect(fname, title, desc, body, schemas, keywords):
    PAGES[fname] = dict(title=title, desc=desc, body=body, schemas=schemas)
B.page = collect
B.build_home(); B.build_services(); B.build_solutions(); B.build_areas(); B.build_contact()

ROUTES = [("index.html","home"),("services.html","services"),("solutions.html","solutions"),
          ("service-areas.html","areas"),("contact.html","contact")]
SLUG = dict(ROUTES)

def data_uri(p):
    return "data:image/svg+xml;base64," + base64.b64encode((HERE/p).read_bytes()).decode()

def rewrite(html):
    """file links -> hash routes, asset paths -> data URIs"""
    for f, slug in ROUTES:
        html = html.replace(f'href="{f}#', f'href="#{slug}/')
        html = html.replace(f'href="{f}"', f'href="#{slug}"')
    html = html.replace('href="sitemap.xml"', 'href="#home"')
    for img in ["fds-logo.svg", "fds-logo-white.svg", "favicon.svg"]:
        html = html.replace(f"assets/img/{img}", data_uri(f"assets/img/{img}"))
    return html

css = (HERE/"assets/css/style.css").read_text()
js  = (HERE/"assets/js/fds.js").read_text()

home = PAGES["index.html"]
ld = "\n".join('<script type="application/ld+json">' + __import__("json").dumps(s, separators=(",",":")) + '</script>'
               for s in home["schemas"])

sections = []
for f, slug in ROUTES:
    body = PAGES[f]["body"]
    if f == "contact.html":                      # avoid an id clash with the homepage form
        body = body.replace('id="quote"', 'id="contact-quote"')
    sections.append(f'<section class="pg" id="pg-{slug}" data-pg="{slug}">\n{body}\n</section>')

EXTRA_CSS = """
/* ---- shareable bundle: routing + demo band ---- */
.pg{display:none}
.pg.is-on{display:block}
"""

ROUTER_JS = """
/* ---- hash router for the bundled preview ---- */
(function () {
  const pages = [...document.querySelectorAll('.pg')];
  const nav = [...document.querySelectorAll('.nav a')];
  function route() {
    const raw = (location.hash || '#home').replace(/^#/, '');
    const [name, anchor] = raw.split('/');
    const target = document.getElementById('pg-' + name) ? name : 'home';
    pages.forEach(p => p.classList.toggle('is-on', p.dataset.pg === target));
    nav.forEach(a => a.classList.toggle('is-active', a.getAttribute('href') === '#' + target));
    document.querySelector('.nav')?.classList.remove('is-open');
    if (anchor) {
      const el = document.getElementById(anchor);
      if (el) { setTimeout(() => el.scrollIntoView({ behavior: 'smooth', block: 'start' }), 80); return; }
    }
    window.scrollTo({ top: 0 });
  }
  addEventListener('hashchange', route);
  route();
})();
"""

DEMOBAND = """
<div class="demoband">
  <div class="container">
    <span class="tag">DESIGN PREVIEW</span>
    <b>Proposed website for First Digital Surveillance</b>
    <span>Concept only — this is not the live site, and nothing submitted here is sent anywhere.</span>
  </div>
</div>"""

out = f"""<title>First Digital Surveillance</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
{css}
{EXTRA_CSS}
</style>
{ld}
<a class="sr-only" href="#main">Skip to content</a>
{B.header('index.html')}
<main id="main">
{"".join(sections)}
</main>
{B.footer()}
{B.CHAT}
<script>
{js}
{ROUTER_JS}
</script>
"""

out = rewrite(out)
(HERE / "FDS-shareable-preview.html").write_text(out, encoding="utf-8")
print("wrote FDS-shareable-preview.html", len(out), "bytes")
for bad in ("assets/img", "assets/css", "assets/js", "index.html\""):
    print(f"  leftover {bad!r}:", out.count(bad))
