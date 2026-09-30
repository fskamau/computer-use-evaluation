#!/usr/bin/env python3
import html, json
from pathlib import Path
ev=json.loads(Path("data/evaluations.json").read_text())
tasks={x["task_id"]:x for x in json.loads(Path("data/tasks.json").read_text())}
cards=[]
for e in ev:
    t=tasks[e["task_id"]]
    issues=e.get("errors",[])
    issue_html="<p class='muted'>No recorded errors.</p>" if not issues else "<ul>"+"".join("<li><strong>{}</strong> — step {}: {}</li>".format(html.escape(x["category"]),x["step"],html.escape(x["description"])) for x in issues)+"</ul>"
    cards.append("<article class='card'><div class='eyebrow'>{}</div><h2>{}</h2><p>{}</p><dl><div><dt>Trajectory</dt><dd>{}</dd></div><div><dt>Task completion</dt><dd>{}</dd></div><div><dt>Tool use</dt><dd>{}</dd></div></dl><h3>Observed issues</h3>{}</article>".format(html.escape(e["overall"]["final_rating"]),html.escape(t["title"]),html.escape(t["instruction"]),html.escape(e["trajectory_id"]),html.escape(e["overall"]["task_completion"]),html.escape(e["overall"]["tool_use"]),issue_html))
style=":root{--bg:#0d0f12;--surface:#15181d;--text:#f3f4f6;--muted:#9ca3af;--border:#2a2f36;--accent:#60a5fa}*{box-sizing:border-box}body{margin:0;font-family:Inter,ui-sans-serif,system-ui,sans-serif;background:var(--bg);color:var(--text)}main{width:min(1050px,calc(100% - 32px));margin:auto;padding:72px 0}header{max-width:760px;margin-bottom:48px}.eyebrow{color:var(--accent);font-size:12px;text-transform:uppercase;letter-spacing:.08em}h1{font-size:clamp(40px,7vw,72px);line-height:1;letter-spacing:-.045em;margin:12px 0 20px}header p,.card p,li{color:var(--muted);line-height:1.65}.grid{display:grid;gap:18px}.card{border:1px solid var(--border);background:var(--surface);border-radius:14px;padding:28px}.card h2{margin:8px 0 10px}dl{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:26px 0}dl div{border-top:1px solid var(--border);padding-top:12px}dt{color:var(--muted);font-size:12px}dd{margin:6px 0 0}@media(max-width:700px){dl{grid-template-columns:1fr}}"
doc="<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Computer-Use Evaluation Lab</title><style>"+style+"</style></head><body><main><header><div class='eyebrow'>Synthetic evaluation dataset</div><h1>Computer-Use Evaluation Lab</h1><p>Structured computer-use trajectory evaluation, error analysis, and QA using synthetic tasks.</p></header><section class='grid'>"+"".join(cards)+"</section></main></body></html>"
Path("report.html").write_text(doc,encoding="utf-8")
print("Wrote report.html")
