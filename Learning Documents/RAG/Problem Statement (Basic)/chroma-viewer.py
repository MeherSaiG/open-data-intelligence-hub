"""
Read-only web viewer for a local Chroma database.

Needs only chromadb (already installed for the demo) and the standard library.

Run:
    python 04-chroma_viewer.py chroma_db
    python 04-chroma_viewer.py chroma_db --port 8001

Then open http://127.0.0.1:8000 in your browser. Press Ctrl+C to stop.
It only reads data; nothing is changed or deleted.
"""
import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

import chromadb

PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Chroma viewer</title>
<style>
:root{--bg:#F2F5F7;--ink:#16212B;--mut:#5B6B78;--card:#fff;--line:#D3DCE3;--ok:#0E7C86;--bad:#B4531A}
@media(prefers-color-scheme:dark){:root{--bg:#10171D;--ink:#E6EDF2;--mut:#93A4B1;--card:#18222A;--line:#2B3944;--ok:#4FC3CE;--bad:#F09A63}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}
main{max-width:1100px;margin:0 auto;padding:22px 16px 50px}h1{font-size:1.4rem;margin:0 0 12px}
.row{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:8px 0}
select,input,button{font:inherit;color:var(--ink);background:var(--card);border:1px solid var(--line);border-radius:6px;padding:6px 10px}
input[type=text]{flex:1;min-width:200px}button{cursor:pointer}button[aria-pressed=true]{background:var(--ink);color:var(--bg)}
button:focus-visible,input:focus-visible,select:focus-visible{outline:3px solid var(--ok);outline-offset:2px}
.wrap{overflow-x:auto;border:1px solid var(--line);border-radius:6px;background:var(--card)}
table{border-collapse:collapse;width:100%}th,td{text-align:left;vertical-align:top;padding:7px 10px;border-bottom:1px solid var(--line)}
th{color:var(--mut);font-weight:600;white-space:nowrap}td.mono,td.id{font:12.5px/1.4 ui-monospace,Menlo,Consolas,monospace}
td.doc{min-width:260px}.mut{color:var(--mut)}.err{color:var(--bad);font-weight:600}
</style></head><body><main>
<h1>Chroma viewer <span class="mut" id="path"></span></h1>
<div class="row"><label>Collection <select id="col"></select></label><span class="mut" id="info"></span></div>
<div class="row"><button id="tb" aria-pressed="true">Browse</button><button id="ts" aria-pressed="false">Search</button>
<label><input type="checkbox" id="emb"> show embedding preview</label></div>
<div class="row"><input type="text" id="q" placeholder="Search text (Search tab only)">
<input type="text" id="where" placeholder='Metadata filter as JSON, e.g. {"status": "current"}'>
<button id="go">Run</button></div>
<div class="row"><button id="prev">Previous</button><button id="next">Next</button><span class="mut" id="range"></span></div>
<div id="msg"></div><div class="wrap"><table><thead id="head"></thead><tbody id="body"></tbody></table></div>
</main><script>
const $=s=>document.querySelector(s);let tab="browse",offset=0,limit=25,total=0;
const api=async(p,o)=>(await fetch(p+"?"+new URLSearchParams(o))).json();
function td(text,cls){const e=document.createElement("td");e.textContent=text;if(cls)e.className=cls;return e}
function render(rows,cols){
  const h=$("#head");h.replaceChildren();const tr=document.createElement("tr");
  cols.forEach(c=>{const t=document.createElement("th");t.textContent=c;tr.append(t)});h.append(tr);
  const b=$("#body");b.replaceChildren();
  rows.forEach(r=>{const t=document.createElement("tr");
    t.append(td(r.id,"id"));
    if(tab==="search")t.append(td(r.distance.toFixed(4),"mono"));
    t.append(td(r.document||"","doc"),td(JSON.stringify(r.metadata||{}),"mono"));
    if($("#emb").checked)t.append(td(r.embedding?"["+r.embedding.join(", ")+", ...]":"","mono"));
    b.append(t)});
}
function cols(){const c=["id"];if(tab==="search")c.push("distance");c.push("document","metadata");if($("#emb").checked)c.push("embedding (first 8)");return c}
async function run(){
  const c=$("#col").value;if(!c)return;$("#msg").textContent="";
  const o={c,where:$("#where").value.trim(),emb:$("#emb").checked?1:0};
  let d;
  if(tab==="browse"){d=await api("/api/items",{...o,offset,limit})}
  else{if(!$("#q").value.trim()){$("#msg").textContent="Type a search text first.";return}d=await api("/api/search",{...o,q:$("#q").value,n:limit})}
  if(d.error){$("#msg").innerHTML="";const s=document.createElement("span");s.className="err";s.textContent=d.error;$("#msg").append(s);render([],cols());return}
  render(d.rows,cols());
  $("#range").textContent=tab==="browse"?`${d.rows.length?offset+1:0}-${offset+d.rows.length} of ${d.total} (matching filter)`:`${d.rows.length} nearest (lower distance = closer)`;
  total=d.total||0;$("#prev").disabled=tab!=="browse"||offset===0;$("#next").disabled=tab!=="browse"||offset+limit>=total;
}
function setTab(t){tab=t;offset=0;$("#tb").setAttribute("aria-pressed",t==="browse");$("#ts").setAttribute("aria-pressed",t==="search");run()}
async function init(){
  const d=await api("/api/collections",{});$("#path").textContent=d.path;
  const s=$("#col");d.collections.forEach(c=>{const o=document.createElement("option");o.value=c.name;o.textContent=`${c.name} (${c.count})`;s.append(o)});
  if(!d.collections.length)$("#msg").textContent="No collections found at this path.";run();
}
$("#tb").onclick=()=>setTab("browse");$("#ts").onclick=()=>setTab("search");$("#go").onclick=()=>{offset=0;run()};
$("#col").onchange=()=>{offset=0;run()};$("#emb").onchange=run;
$("#prev").onclick=()=>{offset=Math.max(0,offset-limit);run()};$("#next").onclick=()=>{offset+=limit;run()};
["q","where"].forEach(i=>$("#"+i).addEventListener("keydown",e=>{if(e.key==="Enter"){offset=0;run()}}));
init();
</script></body></html>"""


def make_handler(client, path):
    def names():
        return [c if isinstance(c, str) else c.name for c in client.list_collections()]

    def parse_where(raw):
        raw = (raw or "").strip()
        return json.loads(raw) if raw else None

    def preview(emb):
        return None if emb is None else [round(float(x), 3) for x in list(emb)[:8]]

    def collections(_):
        out = []
        for n in names():
            c = client.get_collection(n)
            out.append({"name": n, "count": c.count(), "metadata": c.metadata})
        return {"path": path, "collections": out}

    def items(p):
        col = client.get_collection(p["c"][0])
        where = parse_where(p.get("where", [""])[0])
        offset, limit = int(p.get("offset", ["0"])[0]), int(p.get("limit", ["25"])[0])
        inc = ["documents", "metadatas"] + (["embeddings"] if p.get("emb", ["0"])[0] == "1" else [])
        got = col.get(where=where, limit=limit, offset=offset, include=inc)
        total = len(col.get(where=where, include=[])["ids"]) if where else col.count()
        embs = got.get("embeddings")
        rows = [{"id": i, "document": got["documents"][k], "metadata": got["metadatas"][k],
                 "embedding": preview(embs[k]) if embs is not None else None}
                for k, i in enumerate(got["ids"])]
        return {"rows": rows, "total": total}

    def search(p):
        col = client.get_collection(p["c"][0])
        where = parse_where(p.get("where", [""])[0])
        inc = ["documents", "metadatas", "distances"] + (["embeddings"] if p.get("emb", ["0"])[0] == "1" else [])
        r = col.query(query_texts=[p["q"][0]], n_results=int(p.get("n", ["5"])[0]), where=where, include=inc)
        embs = r.get("embeddings")
        rows = [{"id": i, "document": r["documents"][0][k], "metadata": r["metadatas"][0][k],
                 "distance": r["distances"][0][k],
                 "embedding": preview(embs[0][k]) if embs is not None else None}
                for k, i in enumerate(r["ids"][0])]
        return {"rows": rows, "total": len(rows)}

    routes = {"/api/collections": collections, "/api/items": items, "/api/search": search}

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            u = urlparse(self.path)
            if u.path == "/":
                return self.send(200, PAGE.encode(), "text/html; charset=utf-8")
            fn = routes.get(u.path)
            if not fn:
                return self.send(404, b"Not found", "text/plain")
            try:
                body, code = json.dumps(fn(parse_qs(u.query))), 200
            except Exception as e:  # show problems in the page instead of crashing
                body, code = json.dumps({"error": f"{type(e).__name__}: {e}"}), 400
            self.send(code, body.encode(), "application/json")

        def send(self, code, data, ctype):
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def log_message(self, *a):  # keep the terminal quiet
            pass

    return Handler


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Read-only Chroma viewer")
    ap.add_argument("path", nargs="?", default="chroma_db", help="Chroma folder (default: chroma_db)")
    ap.add_argument("--port", type=int, default=8000)
    a = ap.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", a.port), make_handler(chromadb.PersistentClient(path=a.path), a.path))
    print(f"Viewing '{a.path}' at http://127.0.0.1:{a.port}  (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
