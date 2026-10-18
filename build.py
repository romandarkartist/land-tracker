import json,html,os
B=os.path.dirname(__file__) or '.'
d=json.load(open(os.path.join(B,'data.json')))
e=lambda s:html.escape(str(s if s is not None else ''))
F=[('area','Area'),('price','Price / min bid'),('sale_type','Sale type'),('deadline','Deadline'),('frontage','Frontage'),('zoning','Zoning'),('first_seen','First seen'),('last_checked','Last checked')]
def card(p):
    dl=''.join(f"<dt>{l}</dt><dd>{e(p.get(k))}</dd>" for k,l in F)
    ac=p.get('acres')
    link=f"<a class=btn href=\"{e(p['url'])}\" target=_blank rel=noopener>View listing</a>" if p.get('url') else "<span class='btn off'>Source unconfirmed</span>"
    return (f"<article class='card p' data-acres='{ac or 0}' data-name=\"{e(p['name'])}\" data-seen=\"{e(p.get('first_seen'))}\" data-checked=\"{e(p.get('last_checked'))}\">"
      f"<div class=ph><h3>{e(p['name'])}</h3><span class=ac>{e(ac) if ac else '?'} ac</span></div>"
      f"<div class=st>{e(p.get('status'))}</div><dl>{dl}</dl><p class=n>{e(p.get('notes'))}</p>{link}</article>")
cards=''.join(card(p) for p in d['parcels'])
src=''.join(f"<li><a href='{e(s['url'])}' target=_blank rel=noopener>{e(s['name'])}</a></li>" for s in d['sources'])
log=''.join(f"<li><b>{e(l['date'])}</b> {e(l['entry'])}</li>" for l in sorted(d['log'],key=lambda x:x['date'],reverse=True))
tot=round(sum(p.get('acres') or 0 for p in d['parcels']),2)
css="""
:root{--bg:#f4f6f3;--fg:#1d211d;--mut:#555d55;--card:#fff;--line:#dde3db;--acc:#2f5233;--accfg:#fff;--chip:#e8efe6}
@media (prefers-color-scheme:dark){:root{--bg:#121512;--fg:#e8ece6;--mut:#a5ada3;--card:#1d221d;--line:#2f372e;--acc:#8fc79a;--accfg:#0d140e;--chip:#273027}}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{font:16px/1.5 -apple-system,system-ui,sans-serif;margin:0;background:var(--bg);color:var(--fg);overflow-wrap:anywhere}
header{background:#2f5233;color:#fff;padding:calc(16px + env(safe-area-inset-top)) calc(16px + env(safe-area-inset-right)) 16px calc(16px + env(safe-area-inset-left))}
header h1{margin:0;font-size:1.35rem;line-height:1.25}header small{opacity:.85}
main{padding:12px max(12px,env(safe-area-inset-right)) calc(24px + env(safe-area-inset-bottom)) max(12px,env(safe-area-inset-left));max-width:1100px;margin:auto}
.card{background:var(--card);border-radius:12px;padding:14px;margin:12px 0;box-shadow:0 1px 3px #0002}
h2{font-size:1.1rem;margin:0 0 6px}a{color:var(--acc)}
.ctl{display:flex;flex-wrap:wrap;gap:8px;position:sticky;top:0;z-index:2;background:var(--bg);padding:8px 0}
input,select{font-size:16px;min-height:44px;padding:8px 12px;border:1px solid var(--line);border-radius:10px;background:var(--card);color:var(--fg)}
input{flex:1 1 220px;min-width:0}select{flex:0 0 auto}
.grid{display:grid;grid-template-columns:1fr;gap:12px}.grid .card{margin:0}
@media (min-width:760px){.grid{grid-template-columns:repeat(2,1fr)}}
.ph{display:flex;justify-content:space-between;gap:10px;align-items:flex-start}.ph h3{margin:0;font-size:1.05rem;line-height:1.3}
.ac{flex:none;background:var(--acc);color:var(--accfg);border-radius:999px;padding:2px 10px;font-weight:600;font-size:.9rem}
.st{display:inline-block;margin:8px 0 4px;background:var(--chip);border-radius:6px;padding:2px 8px;font-size:.9rem}
dl{display:grid;grid-template-columns:minmax(90px,35%) 1fr;gap:4px 10px;margin:8px 0}dt{color:var(--mut);font-size:.9rem}dd{margin:0}
.n{color:var(--mut);font-size:.95rem;margin:8px 0}
.btn{display:flex;align-items:center;justify-content:center;min-height:44px;border-radius:10px;background:var(--acc);color:var(--accfg);text-decoration:none;font-weight:600}
.btn.off{background:var(--chip);color:var(--mut)}
ul{padding-left:20px;margin:6px 0}li{margin:8px 0}li a{display:inline-block;min-height:44px;padding:10px 0}
"""
out=f"""<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name=color-scheme content="light dark"><meta name=theme-color content="#2f5233"><meta name=apple-mobile-web-app-capable content=yes><title>{e(d['title'])}</title><style>{css}</style></head><body>
<header><h1>{e(d['title'])}</h1><small>Last updated {e(d['last_updated'])}</small></header><main>
<section class=card><h2>Summary</h2><p>{e(d['criteria'])}</p><p>{len(d['parcels'])} parcels tracked, {tot} acres total.</p></section>
<div class=ctl><input id=q type=search placeholder="Filter parcels…" aria-label="Filter parcels"><select id=s aria-label="Sort"><option value="">Default order</option><option value="acres">Acres (most)</option><option value="name">Name</option><option value="seen">First seen (newest)</option><option value="checked">Last checked (newest)</option></select></div>
<div class=grid id=g>{cards}</div>
<section class=card><h2>Sources</h2><ul>{src}</ul></section><section class=card><h2>Research log</h2><ul>{log}</ul></section></main>
<script>const g=document.getElementById('g'),q=document.getElementById('q'),s=document.getElementById('s'),orig=[...g.children];
q.oninput=()=>{{const v=q.value.toLowerCase();for(const c of g.children)c.style.display=c.innerText.toLowerCase().includes(v)?'':'none'}};
s.onchange=()=>{{const k=s.value;let a=[...orig];if(k==='acres')a.sort((x,y)=>y.dataset.acres-x.dataset.acres);else if(k==='name')a.sort((x,y)=>x.dataset.name.localeCompare(y.dataset.name));else if(k)a.sort((x,y)=>(y.dataset[k]||'').localeCompare(x.dataset[k]||''));a.forEach(c=>g.appendChild(c))}};</script></body></html>"""
open(os.path.join(B,'index.html'),'w').write(out)
print('built',len(d['parcels']))
