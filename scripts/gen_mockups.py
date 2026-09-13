# -*- coding: utf-8 -*-
"""One-off: generate Phase 5 design mockups (A: Editorial, B: Minimal commerce).
Uses real products/prices/images from mockups_products.json. Not committed to the build."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
prods = json.load(open(os.path.join(ROOT, "mockups_products.json"), encoding="utf-8"))
out = os.path.join(ROOT, "mockups")
os.makedirs(out, exist_ok=True)

CATS = ["lighting", "kitchen", "home-decor", "sport", "fashion"]
LABELS = {"lighting": "Lighting", "kitchen": "Kitchen & Tea", "home-decor": "Home Decor",
          "sport": "Sport", "fashion": "Fashion"}

def slug_cat(c):
    return {"home-decor": "home decor"}.get(c, c.replace("-", " "))

def clean_title(t):
    # strip bot testing suffixes
    for marker in (" \u2014 Deploy test", " \u2013 Deploy test", " (Deploy test)", " - Deploy test"):
        if t.endswith(marker):
            t = t[:-len(marker)]
    return t

def cards_A():
    out = []
    for p in prods:
        out.append(f'''
    <a class="card" href="https://www.amazon.ae/dp/{p['asIn']}" target="_blank" rel="noopener" data-cat="{p['category']}">
      <div class="card-img"><img src="{p['img']}" alt="{p['cover_alt'][:90]}" loading="lazy"></div>
      <div class="card-body">
        <span class="card-cat">{LABELS[p['category']]}</span>
        <h3 class="card-title">{clean_title(p['title'])}</h3>
        <div class="card-row"><span class="price">{p['price']}</span><span class="buy">Buy on Amazon.ae</span></div>
      </div>
    </a>''')
    return "\n".join(out)

def cards_B():
    out = []
    for p in prods:
        out.append(f'''
    <a class="card" href="https://www.amazon.ae/dp/{p['asIn']}" target="_blank" rel="noopener" data-cat="{p['category']}">
      <div class="card-img"><img src="{p['img']}" alt="{p['cover_alt'][:90]}" loading="lazy"></div>
      <div class="card-body">
        <h3 class="card-title">{clean_title(p['title'])}</h3>
        <div class="card-foot">
          <span class="price">{p['price']}</span>
          <span class="buy">Buy on Amazon <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M7 17L17 7M17 7H9M17 7v8"/></svg></span>
        </div>
      </div>
    </a>''')
    return "\n".join(out)

chips_A = "".join(
    f'<button class="chip{" on" if c == "all" else ""}" data-cat="{c}">{"All" if c == "all" else LABELS[c]}</button>'
    for c in ["all"] + CATS)

# hero = cloud light (best single image), featured = teapot
hero = next(p for p in prods if p["asIn"] == "b0clhgcyrn")

MOCKUP_A = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Nillianstore \u00b7 Mockup A \u2014 Editorial</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root {{
  --bg:#faf6f0; --ink:#1d1a16; --muted:#6f675c; --line:#e7e0d4;
  --accent:#b4531f; --accent-soft:#f3e3d3; --card:#ffffff;
  --serif:'Fraunces',Georgia,serif; --sans:'Inter',system-ui,sans-serif;
}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:var(--bg);color:var(--ink);font-family:var(--sans);-webkit-font-smoothing:antialiased}}
a{{color:inherit;text-decoration:none}}
img{{display:block;width:100%;height:100%;object-fit:cover}}
.wrap{{max-width:1200px;margin:0 auto;padding:0 24px}}

.top{{position:sticky;top:0;z-index:50;background:rgba(250,246,240,.94);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}}
.top-in{{display:flex;align-items:center;justify-content:space-between;height:64px}}
.brand{{font-family:var(--serif);font-size:21px;font-weight:600;letter-spacing:.2px;line-height:1.1}}
.brand small{{font-family:var(--sans);font-size:10.5px;color:var(--muted);font-weight:500;display:block;letter-spacing:1.6px;text-transform:uppercase;margin-top:2px}}
nav{{display:flex;gap:28px;font-size:14px;font-weight:500}}
nav a{{color:var(--muted)}}
nav a:hover{{color:var(--ink)}}
@media(max-width:760px){{nav{{display:none}}}}

.hero{{padding:68px 0 52px;display:grid;grid-template-columns:1.05fr .95fr;gap:56px;align-items:center}}
@media(max-width:880px){{.hero{{grid-template-columns:1fr;gap:32px;padding:44px 0 36px}}}}
.eyebrow{{font-size:12px;font-weight:600;letter-spacing:2px;text-transform:uppercase;color:var(--accent);margin-bottom:18px}}
.hero h1{{font-family:var(--serif);font-size:clamp(38px,4.8vw,56px);line-height:1.06;font-weight:500;letter-spacing:-.5px}}
.hero p{{margin-top:20px;font-size:16.5px;line-height:1.65;color:var(--muted);max-width:46ch}}
.hero-cta{{margin-top:30px;display:flex;gap:12px;flex-wrap:wrap}}
.btn{{display:inline-flex;align-items:center;gap:8px;padding:14px 26px;border-radius:999px;font-size:15px;font-weight:600;transition:background .15s,color .15s,border-color .15s}}
.btn-dark{{background:var(--ink);color:#fff}}
.btn-dark:hover{{background:#000}}
.btn-ghost{{border:1px solid var(--line);color:var(--ink);background:var(--card)}}
.btn-ghost:hover{{border-color:var(--ink)}}
.hero-visual{{position:relative;aspect-ratio:4/4.3;border-radius:24px;overflow:hidden;background:var(--accent-soft)}}
.hero-visual img{{object-fit:contain;padding:6%}}
.hero-badge{{position:absolute;left:18px;bottom:18px;background:var(--card);border-radius:14px;padding:13px 17px;box-shadow:0 12px 32px rgba(29,26,22,.14);max-width:260px}}
.hero-badge .t{{font-size:13px;font-weight:600;line-height:1.4}}
.hero-badge .p{{font-size:13px;color:var(--accent);font-weight:600;margin-top:5px}}

.strip{{border-top:1px solid var(--line);border-bottom:1px solid var(--line);margin-top:10px}}
.strip-in{{display:flex;justify-content:space-between;gap:14px;padding:15px 24px;font-size:13px;color:var(--muted);flex-wrap:wrap}}
.strip-in span{{display:flex;gap:8px;align-items:center}}
.dot{{width:6px;height:6px;border-radius:50%;background:var(--accent);display:inline-block}}

.shop{{padding:58px 0 20px}}
.shop-head{{display:flex;align-items:flex-end;justify-content:space-between;gap:24px;flex-wrap:wrap;margin-bottom:26px}}
.shop-head h2{{font-family:var(--serif);font-size:32px;font-weight:500;letter-spacing:-.3px}}
.chips{{display:flex;gap:8px;flex-wrap:wrap}}
.chip{{border:1px solid var(--line);background:var(--card);color:var(--muted);font-family:var(--sans);font-size:13px;font-weight:500;padding:9px 18px;border-radius:999px;cursor:pointer;transition:.15s}}
.chip:hover{{border-color:var(--ink);color:var(--ink)}}
.chip.on{{background:var(--ink);border-color:var(--ink);color:#fff}}

.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:20px}}
@media(max-width:1020px){{.grid{{grid-template-columns:repeat(3,1fr)}}}}
@media(max-width:740px){{.grid{{grid-template-columns:repeat(2,1fr);gap:12px}}}}
@media(max-width:460px){{.grid{{grid-template-columns:1fr}}}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:18px;overflow:hidden;display:flex;flex-direction:column;transition:transform .18s,box-shadow .18s}}
.card:hover{{transform:translateY(-4px);box-shadow:0 16px 40px rgba(29,26,22,.09)}}
.card-img{{aspect-ratio:1/1;background:#f1ebdf}}
.card-body{{padding:16px 18px 18px;display:flex;flex-direction:column;gap:5px;flex:1}}
.card-cat{{font-size:11px;font-weight:600;letter-spacing:1.4px;text-transform:uppercase;color:var(--accent)}}
.card-title{{font-size:14.5px;font-weight:500;line-height:1.45}}
.card-row{{display:flex;justify-content:space-between;align-items:center;margin-top:8px;font-size:13.5px;gap:8px}}
.price{{font-weight:600}}
.buy{{color:var(--accent);font-weight:600;font-size:12.5px;white-space:nowrap}}

.note{{margin:36px 0 0;text-align:center;font-size:13px;color:var(--muted)}}
footer{{border-top:1px solid var(--line);margin-top:52px;padding:38px 0 46px;background:var(--card)}}
.foot-in{{display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap;font-size:13.5px;color:var(--muted)}}
footer .brand{{font-size:19px}}
.mock-tag{{position:fixed;top:12px;right:12px;z-index:99;background:var(--ink);color:#fff;font-size:11px;letter-spacing:1.5px;text-transform:uppercase;padding:8px 14px;border-radius:999px;font-weight:600}}
</style>
</head>
<body>
<div class="mock-tag">Mockup A \u00b7 Editorial</div>
<div class="top"><div class="wrap top-in">
  <a class="brand" href="#">Nillianstore<small>Curated for UAE homes</small></a>
  <nav>
    <a href="#shop">Shop</a><a href="#shop" data-navcat="lighting">Lighting</a><a href="#shop" data-navcat="kitchen">Kitchen &amp; Tea</a><a href="#">About</a><a href="#">Journal</a><a href="#">Contact</a>
  </nav>
</div></div>

<div class="wrap">
  <section class="hero">
    <div>
      <div class="eyebrow">Handpicked \u00b7 Dubai \u00b7 Abu Dhabi \u00b7 Sharjah</div>
      <h1>Everyday objects,<br>chosen for how<br>they actually feel.</h1>
      <p>A small, curated collection of home, tea and lighting pieces \u2014 delivered across the UAE through Amazon.ae. No warehouse of noise. Just things worth keeping.</p>
      <div class="hero-cta">
        <a class="btn btn-dark" href="#shop">Shop the collection</a>
        <a class="btn btn-ghost" href="#">How it works</a>
      </div>
    </div>
    <div class="hero-visual">
      <img src="{hero['img']}" alt="{hero['cover_alt'][:90]}">
      <div class="hero-badge"><div class="t">{clean_title(hero['title'])}</div><div class="p">{hero['price']} \u00b7 via Amazon.ae</div></div>
    </div>
  </section>
</div>

<div class="strip"><div class="wrap strip-in">
  <span><i class="dot"></i> Fast delivery across the UAE</span>
  <span><i class="dot"></i> Secure Amazon.ae checkout</span>
  <span><i class="dot"></i> Easy returns</span>
  <span><i class="dot"></i> Priced in AED</span>
</div></div>

<div class="wrap">
  <section class="shop" id="shop">
    <div class="shop-head">
      <h2>The collection</h2>
      <div class="chips" id="chipsA">{chips_A}</div>
    </div>
    <div class="grid" id="gridA">{cards_A()}</div>
    <p class="note">Purchases complete on Amazon.ae \u2014 Nillianstore curates, Amazon delivers.</p>
  </section>
</div>

<footer><div class="wrap foot-in">
  <a class="brand" href="#">Nillianstore</a>
  <span>Abu Dhabi, UAE \u00b7 +971 58 622 9432 \u00b7 nillianstore@gmail.com</span>
  <span>\u00a9 2026 Nillianstore</span>
</div></footer>

<script>
const chips=[...document.querySelectorAll('#chipsA .chip')];
const cards=[...document.querySelectorAll('#gridA .card')];
function filter(cat){{
  chips.forEach(c=>c.classList.toggle('on',c.dataset.cat===cat));
  cards.forEach(cd=>{{cd.style.display=(cat==='all'||cd.dataset.cat===cat)?'':'none';}});
}}
chips.forEach(ch=>ch.onclick=()=>filter(ch.dataset.cat));
document.querySelectorAll('[data-navcat]').forEach(a=>a.onclick=()=>filter(a.dataset.navcat));
</script>
</body></html>'''

# ---------- Mockup B: Minimal commerce — crisp white, sharp grid, utility nav ----------
MOCKUP_B = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Nillianstore \u00b7 Mockup B \u2014 Minimal Commerce</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root {{
  --bg:#ffffff; --ink:#0f0f10; --muted:#71717a; --line:#e5e5e8;
  --accent:#0f0f10; --amber:#f59e0b; --soft:#f7f7f8;
  --sans:'Manrope',system-ui,sans-serif;
}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:var(--bg);color:var(--ink);font-family:var(--sans);-webkit-font-smoothing:antialiased}}
a{{color:inherit;text-decoration:none}}
img{{display:block;width:100%;height:100%;object-fit:cover}}
.wrap{{max-width:1280px;margin:0 auto;padding:0 24px}}
button{{font-family:var(--sans)}}

.top{{position:sticky;top:0;z-index:50;background:#fff;border-bottom:1px solid var(--line)}}
.top-in{{display:flex;align-items:center;justify-content:space-between;height:60px}}
.brand{{font-size:17px;font-weight:800;letter-spacing:-.4px}}
.brand span{{color:var(--amber)}}
nav{{display:flex;gap:26px;font-size:13.5px;font-weight:600;color:var(--muted)}}
nav a:hover{{color:var(--ink)}}
@media(max-width:760px){{nav{{display:none}}}}

/* hero: banner strip, not centered */
.hero{{border-bottom:1px solid var(--line)}}
.hero-in{{display:grid;grid-template-columns:1fr 1fr;min-height:420px}}
@media(max-width:880px){{.hero-in{{grid-template-columns:1fr}}}}
.hero-copy{{display:flex;flex-direction:column;justify-content:center;padding:56px 48px}}
@media(max-width:880px){{.hero-copy{{padding:40px 24px}}}}
.kicker{{font-size:12px;font-weight:700;letter-spacing:1.8px;text-transform:uppercase;color:var(--muted);margin-bottom:14px}}
.hero-copy h1{{font-size:clamp(32px,3.6vw,44px);font-weight:800;letter-spacing:-1px;line-height:1.08}}
.hero-copy p{{margin-top:16px;font-size:15.5px;line-height:1.6;color:var(--muted);max-width:44ch}}
.hero-cta{{margin-top:26px;display:flex;gap:10px;flex-wrap:wrap}}
.btn{{display:inline-flex;align-items:center;gap:8px;padding:13px 22px;border-radius:10px;font-size:14px;font-weight:700;transition:.15s;border:1px solid var(--ink)}}
.btn-dark{{background:var(--ink);color:#fff}}
.btn-dark:hover{{background:#000}}
.btn-line{{color:var(--ink);background:#fff}}
.btn-line:hover{{background:var(--soft)}}
.hero-img{{background:var(--soft);display:flex;align-items:center;justify-content:center;padding:20px}}
.hero-img img{{max-height:380px;object-fit:contain}}
@media(max-width:880px){{.hero-img{{display:none}}}}

/* category band */
.band{{padding:26px 0;border-bottom:1px solid var(--line)}}
.band-in{{display:flex;gap:10px;flex-wrap:wrap;align-items:center}}
.band-label{{font-size:12px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;color:var(--muted);margin-right:10px}}
.band .chip{{border:1px solid var(--line);background:#fff;color:var(--ink);font-size:13px;font-weight:600;padding:9px 16px;border-radius:8px;cursor:pointer;transition:.12s}}
.band .chip:hover{{border-color:var(--ink)}}
.band .chip.on{{background:var(--ink);color:#fff;border-color:var(--ink)}}

.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;padding:32px 0 40px}}
@media(max-width:1060px){{.grid{{grid-template-columns:repeat(3,1fr)}}}}
@media(max-width:760px){{.grid{{grid-template-columns:repeat(2,1fr)}}}}
@media(max-width:440px){{.grid{{grid-template-columns:1fr}}}}
.card{{border:1px solid var(--line);border-radius:14px;overflow:hidden;background:#fff;display:flex;flex-direction:column;transition:.15s}}
.card:hover{{border-color:var(--ink);box-shadow:0 10px 30px rgba(15,15,16,.08)}}
.card-img{{aspect-ratio:1/1;background:var(--soft)}}
.card-body{{padding:14px 15px 15px;display:flex;flex-direction:column;gap:8px;flex:1}}
.card-title{{font-size:14px;font-weight:600;line-height:1.4;flex:1;letter-spacing:-.1px}}
.card-foot{{display:flex;justify-content:space-between;align-items:center;font-size:13.5px;gap:8px}}
.price{{font-weight:800;letter-spacing:-.2px}}
.buy{{color:var(--muted);font-weight:700;font-size:12.5px;display:inline-flex;align-items:center;gap:5px;white-space:nowrap}}
.card:hover .buy{{color:var(--ink)}}

.note{{text-align:center;font-size:13px;color:var(--muted);padding-bottom:40px}}
footer{{border-top:1px solid var(--line);padding:32px 0 40px;background:var(--soft)}}
.foot-in{{display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap;font-size:13px;color:var(--muted);font-weight:500}}
footer .brand{{color:var(--ink)}}
.mock-tag{{position:fixed;top:12px;right:12px;z-index:99;background:var(--ink);color:#fff;font-size:11px;letter-spacing:1.5px;text-transform:uppercase;padding:8px 14px;border-radius:999px;font-weight:600}}
</style>
</head>
<body>
<div class="mock-tag">Mockup B \u00b7 Minimal Commerce</div>
<div class="top"><div class="wrap top-in">
  <a class="brand" href="#">nillianstore<span>.</span></a>
  <nav>
    <a href="#grid">Shop</a><a href="#grid" data-navcat="lighting">Lighting</a><a href="#grid" data-navcat="kitchen">Kitchen &amp; Tea</a><a href="#">About</a><a href="#">Journal</a><a href="#">Contact</a>
  </nav>
</div></div>

<section class="hero"><div class="hero-in wrap">
  <div class="hero-copy">
    <div class="kicker">Home \u00b7 Tea \u00b7 Lighting \u2014 UAE wide delivery</div>
    <h1>Handpicked pieces for<br>the way you live at home.</h1>
    <p>Twenty-four objects, chosen one by one. Every purchase finishes on Amazon.ae with delivery to Dubai, Abu Dhabi and Sharjah.</p>
    <div class="hero-cta">
      <a class="btn btn-dark" href="#grid">Browse all products</a>
      <a class="btn btn-line" href="#">Gift ideas</a>
    </div>
  </div>
  <div class="hero-img"><img src="{hero['img']}" alt="{hero['cover_alt'][:90]}"></div>
</div></section>

<div class="band"><div class="wrap band-in">
  <span class="band-label">Shop by category</span>
  <div id="chipsB">{"<button class='chip on' data-cat='all'>All</button>" + "".join(f"<button class='chip' data-cat='{c}'>{LABELS[c]}</button>" for c in CATS)}</div>
</div></div>

<div class="wrap">
  <div class="grid" id="gridB">{cards_B()}</div>
  <p class="note">Purchases complete on Amazon.ae \u2014 Nillianstore curates, Amazon delivers.</p>
</div>

<footer><div class="wrap foot-in">
  <a class="brand" href="#">nillianstore.</a>
  <span>Abu Dhabi, UAE \u00b7 +971 58 622 9432 \u00b7 nillianstore@gmail.com</span>
  <span>\u00a9 2026 Nillianstore</span>
</div></footer>

<script>
const chips=[...document.querySelectorAll('#chipsB .chip')];
const cards=[...document.querySelectorAll('#gridB .card')];
function filter(cat){{
  chips.forEach(c=>c.classList.toggle('on',c.dataset.cat===cat));
  cards.forEach(cd=>{{cd.style.display=(cat==='all'||cd.dataset.cat===cat)?'':'none';}});
}}
chips.forEach(ch=>ch.onclick=()=>filter(ch.dataset.cat));
document.querySelectorAll('[data-navcat]').forEach(a=>a.onclick=()=>filter(a.dataset.navcat));
</script>
</body></html>'''

open(os.path.join(out, "Mockup A - Editorial.html"), "w", encoding="utf-8").write(MOCKUP_A)
open(os.path.join(out, "Mockup B - Minimal Commerce.html"), "w", encoding="utf-8").write(MOCKUP_B)
print("A:", len(MOCKUP_A), "B:", len(MOCKUP_B))
print("products embedded:", len(prods))
