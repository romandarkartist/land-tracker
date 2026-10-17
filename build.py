import json,html,os
d=json.load(open(os.path.join(os.path.dirname(__file__) or '.','data.json')))
e=lambda s:html.escape(str(s if s is not None else ''))
rows=''.join(f"<tr><td>{e(p['name'])}<div class=n>{e(p['notes'])}</div></td><td>{e(p['area'])}</td><td data-v='{p.get('acres') or 0}'>{e(p.get('acres'))}</td><td>{e(p['price'])}</td><td>{e(p['sale_type'])}</td><td>{e(p['deadline'])}</td><td>{e(p['frontage'])}</td><td>{e(p['zoning'])}</td><td>{e(p['status'])}</td><td>{e(p['first_seen'])}</td><td>{e(p['last_checked'])}</td><td>{'<a href=\"'+e(p['url'])+'\">link</a>' if p['url'] else 'unconfirmed'}</td></tr>" for p in d['parcels'])
src=''.join(f"<li><a href='{e(s['url'])}'>{e(s['name'])}</a></li>" for s in d['sources'])
log=''.join(f"<li><b>{e(l['date'])}</b> {e(l['entry'])}</li>" for l in sorted(d['log'],key=lambda x:x['date'],reverse=True))
tot=sum(p.get('acres') or 0 for p in d['parcels'])
out=f"""<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>{e(d['title'])}</title><style>
body{{font-family:system-ui,sans-serif;margin:0;background:#f4f6f3;color:#222}}header{{background:#2f5233;color:#fff;padding:16px}}main{{padding:12px;max-width:1100px;margin:auto}}
.card{{background:#fff;border-radius:10px;padding:12px;margin:10px 0;box-shadow:0 1px 3px #0002}}.wrap{{overflow-x:auto}}table{{border-collapse:collapse;width:100%;font-size:14px}}
th,td{{border-bottom:1px solid #ddd;padding:6px;text-align:left;vertical-align:top}}th{{cursor:pointer;background:#e8efe6;position:sticky;top:0}}.n{{font-size:12px;color:#555;margin-top:4px}}input{{width:100%;padding:8px;font-size:16px;box-sizing:border-box}}a{{color:#2f5233}}</style></head><body>
<header><h2 style=margin:0>{e(d['title'])}</h2><small>Last updated {e(d['last_updated'])}</small></header><main>
<div class=card><b>Summary</b><p>{e(d['criteria'])}</p><p>{len(d['parcels'])} parcels tracked, {tot} acres total.</p></div>
<div class=card><input id=q placeholder="Filter parcels..."><div class=wrap><table id=t><thead><tr><th>Parcel</th><th>Area</th><th>Acres</th><th>Price/Min bid</th><th>Sale type</th><th>Deadline</th><th>Frontage</th><th>Zoning</th><th>Status</th><th>First seen</th><th>Last checked</th><th>Source</th></tr></thead><tbody>{rows}</tbody></table></div><small>Tap a header to sort.</small></div>
<div class=card><b>Sources</b><ul>{src}</ul></div><div class=card><b>Research log</b><ul>{log}</ul></div></main>
<script>q.oninput=()=>{{for(const r of t.tBodies[0].rows)r.style.display=r.innerText.toLowerCase().includes(q.value.toLowerCase())?'':'none'}};
document.querySelectorAll('th').forEach((h,i)=>{{let a=1;h.onclick=()=>{{a=-a;const b=t.tBodies[0];[...b.rows].sort((x,y)=>{{const u=x.cells[i],v=y.cells[i];return(u.dataset.v?u.dataset.v-v.dataset.v:u.innerText.localeCompare(v.innerText))*a}}).forEach(r=>b.appendChild(r))}}}})</script></body></html>"""
open(os.path.join(os.path.dirname(__file__) or '.','index.html'),'w').write(out)
print('built',len(d['parcels']))
