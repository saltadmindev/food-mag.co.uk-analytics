import json
import os

with open(os.path.join(os.path.dirname(__file__), "ga_data.json")) as f:
    raw = json.load(f)

COLORS = [
    "#6366f1", "#8b5cf6", "#ec4899", "#f59e0b", "#10b981",
    "#3b82f6", "#ef4444", "#14b8a6", "#f97316", "#a855f7"
]


def fmt_duration(seconds):
    try:
        s = float(seconds)
        if s < 60:
            return f"{s:.0f}s"
        return f"{s/60:.1f}m"
    except:
        return seconds


def fmt_pct(val):
    try:
        return f"{float(val)*100:.1f}%"
    except:
        return val


def build_period(d):
    ch = d["channel"]["rows"]

    def total_sessions():
        return sum(int(r[1]) for r in ch)

    def total_users():
        return sum(int(r[2]) for r in ch)

    def avg_duration():
        ts = sum(int(r[1]) for r in ch)
        w = sum(float(r[4]) * int(r[1]) for r in ch)
        return w / ts if ts else 0

    eng_dates, eng_users, eng_sessions = [], [], []
    for row in sorted(d["engagement"]["rows"], key=lambda r: r[0]):
        raw = row[0]
        eng_dates.append(f"{raw[6:8]}/{raw[4:6]}/{raw[0:4]}")
        eng_users.append(int(row[1]))
        eng_sessions.append(int(row[2]))

    ch_labels   = [r[0] for r in ch]
    ch_sessions = [int(r[1]) for r in ch]

    geo_labels   = [r[0] for r in d["geo_country"]["rows"][:10]]
    geo_sessions = [int(r[1]) for r in d["geo_country"]["rows"][:10]]

    dev_rows     = [r for r in d["device"]["rows"] if r[0] != "(other)"]
    dev_labels   = [r[0].capitalize() for r in dev_rows]
    dev_sessions = [int(r[1]) for r in dev_rows]

    os_labels   = [r[0] for r in d["os"]["rows"][:8]]
    os_sessions = [int(r[1]) for r in d["os"]["rows"][:8]]

    br_labels   = [r[0] for r in d["browser"]["rows"][:8]]
    br_sessions = [int(r[1]) for r in d["browser"]["rows"][:8]]

    age_rows  = [r for r in d["age"]["rows"] if r[0] not in ("unknown", "(not set)")]
    gen_rows  = [r for r in d["gender"]["rows"] if r[0] not in ("unknown", "(not set)")]

    src_rows = [(r[0], r[1], int(r[2]), int(r[3])) for r in d["source"]["rows"][:15]]
    lp_rows  = [(r[0], int(r[1]), fmt_pct(r[3]), fmt_duration(r[4])) for r in d["landing_pages"]["rows"][:15] if r[0] != "(not set)"]
    st_rows  = [(r[0], int(r[1])) for r in d["search_terms"]["rows"][:15] if r[0] not in ("", "(not set)")]

    top_country = d["geo_country"]["rows"][0][0] if d["geo_country"]["rows"] else "—"
    top_country_s = f"{int(d['geo_country']['rows'][0][1]):,}" if d["geo_country"]["rows"] else ""
    top_channel = ch[0][0] if ch else "—"
    top_channel_s = f"{int(ch[0][1]):,}" if ch else ""
    top_device = dev_rows[0][0].capitalize() if dev_rows else "—"
    top_device_s = f"{int(dev_rows[0][1]):,}" if dev_rows else ""

    def ch_table():
        rows_html = ""
        for r in d["channel"]["rows"]:
            cls = r[0].lower().replace(" ", "").replace("/", "")
            rows_html += f'<tr><td><span class="badge badge-{cls}">{r[0]}</span></td><td>{int(r[1]):,}</td><td>{int(r[2]):,}</td><td>{fmt_pct(r[3])}</td><td>{fmt_duration(r[4])}</td></tr>'
        return rows_html

    def src_table():
        return "".join(f'<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]:,}</td><td>{r[3]:,}</td></tr>' for r in src_rows)

    def lp_table():
        return "".join(f'<tr><td class="truncate" title="{r[0]}">{r[0]}</td><td>{r[1]:,}</td><td>{r[2]}</td><td>{r[3]}</td></tr>' for r in lp_rows)

    def st_section():
        if not st_rows:
            return "<p class='note'>No site search terms recorded in this period.</p>"
        return "<table><thead><tr><th>Search Term</th><th>Sessions</th></tr></thead><tbody>" + "".join(f'<tr><td>{r[0]}</td><td>{r[1]:,}</td></tr>' for r in st_rows) + "</tbody></table>"

    age_chart = ""
    if age_rows:
        age_labels_js = json.dumps([r[0] for r in age_rows])
        age_users_js  = json.dumps([int(r[1]) for r in age_rows])
        age_chart = f"new Chart(document.getElementById('ageChart_{{ID}}'), {{ type: 'bar', data: {{ labels: {age_labels_js}, datasets: [{{ label: 'Users', data: {age_users_js}, backgroundColor: COLORS, borderRadius: 4 }}] }}, options: {{ plugins: {{ legend: {{ display: false }} }}, scales: {{ x: {{ ticks: {{ color: '#94a3b8' }}, grid: {{ display: false }} }}, y: {{ ticks: {{ color: '#64748b' }}, grid: {{ color: '#1e2a3a' }} }} }} }} }});"

    gen_chart = ""
    if gen_rows:
        gen_labels_js = json.dumps([r[0].capitalize() for r in gen_rows])
        gen_users_js  = json.dumps([int(r[1]) for r in gen_rows])
        gen_chart = f"new Chart(document.getElementById('genderChart_{{ID}}'), {{ type: 'doughnut', data: {{ labels: {gen_labels_js}, datasets: [{{ data: {gen_users_js}, backgroundColor: ['#ec4899','#6366f1','#10b981'], borderWidth: 0, hoverOffset: 4 }}] }}, options: {{ plugins: {{ legend: {{ position: 'bottom', labels: {{ color: '#94a3b8', padding: 10, font: {{ size: 12 }} }} }} }} }} }});"

    return {
        "total_sessions": f"{total_sessions():,}",
        "total_users":    f"{total_users():,}",
        "avg_duration":   fmt_duration(avg_duration()),
        "top_country":    top_country,
        "top_country_s":  top_country_s,
        "top_channel":    top_channel,
        "top_channel_s":  top_channel_s,
        "top_device":     top_device,
        "top_device_s":   top_device_s,
        "eng_dates":      json.dumps(eng_dates),
        "eng_sessions":   json.dumps(eng_sessions),
        "eng_users":      json.dumps(eng_users),
        "ch_labels":      json.dumps(ch_labels),
        "ch_sessions":    json.dumps(ch_sessions),
        "geo_labels":     json.dumps(geo_labels),
        "geo_sessions":   json.dumps(geo_sessions),
        "dev_labels":     json.dumps(dev_labels),
        "dev_sessions":   json.dumps(dev_sessions),
        "os_labels":      json.dumps(os_labels),
        "os_sessions":    json.dumps(os_sessions),
        "br_labels":      json.dumps(br_labels),
        "br_sessions":    json.dumps(br_sessions),
        "ch_table":       ch_table(),
        "src_table":      src_table(),
        "lp_table":       lp_table(),
        "st_section":     st_section(),
        "age_chart":      age_chart,
        "gen_chart":      gen_chart,
        "has_age":        bool(age_rows),
        "has_gen":        bool(gen_rows),
    }


p6  = build_period(raw["6m"])
p12 = build_period(raw["12m"])


def panel(p, pid):
    age_html = f'<canvas id="ageChart_{pid}" height="160"></canvas>' if p["has_age"] else "<p class='note'>Insufficient data — enable Google Signals in GA4.</p>"
    gen_html = f'<canvas id="genderChart_{pid}" height="160"></canvas>' if p["has_gen"] else "<p class='note'>Insufficient data — enable Google Signals in GA4.</p>"
    age_js   = p["age_chart"].replace("{ID}", pid)
    gen_js   = p["gen_chart"].replace("{ID}", pid)

    return f"""
<div class="panel" id="panel_{pid}">
  <div class="stats">
    <div class="stat"><div class="stat-label">Total Sessions</div><div class="stat-value">{p["total_sessions"]}</div></div>
    <div class="stat"><div class="stat-label">Active Users</div><div class="stat-value">{p["total_users"]}</div></div>
    <div class="stat"><div class="stat-label">Avg Session Duration</div><div class="stat-value">{p["avg_duration"]}</div></div>
    <div class="stat"><div class="stat-label">Top Country</div><div class="stat-value sm">{p["top_country"]}</div><div class="stat-sub">{p["top_country_s"]} sessions</div></div>
    <div class="stat"><div class="stat-label">Top Channel</div><div class="stat-value sm">{p["top_channel"]}</div><div class="stat-sub">{p["top_channel_s"]} sessions</div></div>
    <div class="stat"><div class="stat-label">Top Device</div><div class="stat-value sm">{p["top_device"]}</div><div class="stat-sub">{p["top_device_s"]} sessions</div></div>
  </div>

  <div class="card full">
    <h2>Sessions &amp; Users Over Time</h2>
    <canvas id="trendChart_{pid}" height="70"></canvas>
  </div>

  <div class="grid grid-wide">
    <div class="card"><h2>Sessions by Country</h2><canvas id="geoChart_{pid}" height="120"></canvas></div>
    <div class="card"><h2>Traffic Channels</h2><canvas id="channelChart_{pid}" height="120"></canvas></div>
  </div>

  <div class="grid grid-3">
    <div class="card"><h2>Device Type</h2><canvas id="deviceChart_{pid}" height="180"></canvas></div>
    <div class="card"><h2>Operating System</h2><canvas id="osChart_{pid}" height="180"></canvas></div>
    <div class="card"><h2>Browser</h2><canvas id="browserChart_{pid}" height="180"></canvas></div>
  </div>

  <div class="grid grid-2">
    <div class="card"><h2>Age Bracket</h2>{age_html}</div>
    <div class="card"><h2>Gender</h2>{gen_html}</div>
  </div>

  <div class="card full">
    <h2>Channel Performance</h2>
    <table><thead><tr><th>Channel</th><th>Sessions</th><th>Users</th><th>Bounce Rate</th><th>Avg Duration</th></tr></thead>
    <tbody>{p["ch_table"]}</tbody></table>
  </div>

  <div class="grid grid-2">
    <div class="card"><h2>Traffic Sources</h2>
      <table><thead><tr><th>Source</th><th>Medium</th><th>Sessions</th><th>Users</th></tr></thead>
      <tbody>{p["src_table"]}</tbody></table>
    </div>
    <div class="card"><h2>Top Landing Pages</h2>
      <table><thead><tr><th>Page</th><th>Sessions</th><th>Bounce</th><th>Duration</th></tr></thead>
      <tbody>{p["lp_table"]}</tbody></table>
    </div>
  </div>

  <div class="card full"><h2>Site Search Terms</h2>{p["st_section"]}</div>
</div>

<script>
(function() {{
  const COLORS = {json.dumps(COLORS)};
  new Chart(document.getElementById("trendChart_{pid}"), {{
    type:"line", data:{{ labels:{p["eng_dates"]}, datasets:[
      {{label:"Sessions",data:{p["eng_sessions"]},borderColor:"#6366f1",backgroundColor:"rgba(99,102,241,0.1)",fill:true,tension:0.3,pointRadius:2}},
      {{label:"Users",data:{p["eng_users"]},borderColor:"#10b981",backgroundColor:"rgba(16,185,129,0.1)",fill:true,tension:0.3,pointRadius:2}}
    ]}}, options:{{plugins:{{legend:{{labels:{{color:"#94a3b8"}}}}}},scales:{{x:{{ticks:{{color:"#64748b",maxTicksLimit:12}},grid:{{color:"#1e2a3a"}}}},y:{{ticks:{{color:"#64748b"}},grid:{{color:"#1e2a3a"}}}}}}}}
  }});
  new Chart(document.getElementById("geoChart_{pid}"), {{
    type:"bar", data:{{labels:{p["geo_labels"]},datasets:[{{label:"Sessions",data:{p["geo_sessions"]},backgroundColor:COLORS,borderRadius:4}}]}},
    options:{{indexAxis:"y",plugins:{{legend:{{display:false}}}},scales:{{x:{{ticks:{{color:"#64748b"}},grid:{{color:"#1e2a3a"}}}},y:{{ticks:{{color:"#94a3b8"}},grid:{{display:false}}}}}}}}
  }});
  new Chart(document.getElementById("channelChart_{pid}"), {{
    type:"doughnut", data:{{labels:{p["ch_labels"]},datasets:[{{data:{p["ch_sessions"]},backgroundColor:COLORS,borderWidth:0,hoverOffset:6}}]}},
    options:{{plugins:{{legend:{{position:"right",labels:{{color:"#94a3b8",padding:12,font:{{size:12}}}}}}}}}}
  }});
  new Chart(document.getElementById("deviceChart_{pid}"), {{
    type:"doughnut", data:{{labels:{p["dev_labels"]},datasets:[{{data:{p["dev_sessions"]},backgroundColor:["#6366f1","#10b981","#f59e0b"],borderWidth:0,hoverOffset:4}}]}},
    options:{{plugins:{{legend:{{position:"bottom",labels:{{color:"#94a3b8",padding:10,font:{{size:12}}}}}}}}}}
  }});
  new Chart(document.getElementById("osChart_{pid}"), {{
    type:"bar", data:{{labels:{p["os_labels"]},datasets:[{{label:"Sessions",data:{p["os_sessions"]},backgroundColor:COLORS,borderRadius:4}}]}},
    options:{{indexAxis:"y",plugins:{{legend:{{display:false}}}},scales:{{x:{{ticks:{{color:"#64748b"}},grid:{{color:"#1e2a3a"}}}},y:{{ticks:{{color:"#94a3b8"}},grid:{{display:false}}}}}}}}
  }});
  new Chart(document.getElementById("browserChart_{pid}"), {{
    type:"bar", data:{{labels:{p["br_labels"]},datasets:[{{label:"Sessions",data:{p["br_sessions"]},backgroundColor:COLORS,borderRadius:4}}]}},
    options:{{indexAxis:"y",plugins:{{legend:{{display:false}}}},scales:{{x:{{ticks:{{color:"#64748b"}},grid:{{color:"#1e2a3a"}}}},y:{{ticks:{{color:"#94a3b8"}},grid:{{display:false}}}}}}}}
  }});
  {age_js}
  {gen_js}
}})();
</script>
"""


html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>GA4 Dashboard — food-mag.co.uk</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
  *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
  body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:#0f1117;color:#e2e8f0;min-height:100vh}}
  .header{{background:linear-gradient(135deg,#1e1b4b 0%,#312e81 100%);padding:28px 40px;border-bottom:1px solid #2d2d4e;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px}}
  .header h1{{font-size:24px;font-weight:700;color:#fff}}
  .header p{{color:#a5b4fc;font-size:13px;margin-top:2px}}
  .tabs{{display:flex;gap:8px}}
  .tab{{padding:8px 20px;border-radius:8px;border:1px solid #4338ca;background:transparent;color:#a5b4fc;font-size:14px;font-weight:600;cursor:pointer;transition:all 0.15s}}
  .tab.active{{background:#4338ca;color:#fff;border-color:#4338ca}}
  .tab:hover:not(.active){{background:#2d2d4e}}
  .container{{max-width:1400px;margin:0 auto;padding:32px 40px}}
  .panel{{display:none}}.panel.active{{display:block}}
  .stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:16px;margin-bottom:24px}}
  .stat{{background:#1e2030;border:1px solid #2d2d4e;border-radius:12px;padding:20px}}
  .stat-label{{font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:0.05em}}
  .stat-value{{font-size:30px;font-weight:700;color:#fff;margin-top:4px}}
  .stat-value.sm{{font-size:18px}}
  .stat-sub{{font-size:12px;color:#94a3b8;margin-top:4px}}
  .grid{{display:grid;gap:20px;margin-bottom:20px}}
  .grid-2{{grid-template-columns:1fr 1fr}}
  .grid-3{{grid-template-columns:1fr 1fr 1fr}}
  .grid-wide{{grid-template-columns:2fr 1fr}}
  .card{{background:#1e2030;border:1px solid #2d2d4e;border-radius:12px;padding:24px;margin-bottom:0}}
  .card.full{{margin-bottom:20px}}
  h2{{font-size:14px;font-weight:600;color:#c7d2fe;margin-bottom:18px;display:flex;align-items:center;gap:8px}}
  h2::before{{content:"";display:block;width:3px;height:14px;background:#6366f1;border-radius:2px;flex-shrink:0}}
  table{{width:100%;border-collapse:collapse;font-size:13px}}
  th{{text-align:left;padding:8px 10px;color:#64748b;font-weight:500;border-bottom:1px solid #2d2d4e;font-size:11px;text-transform:uppercase;letter-spacing:0.05em}}
  td{{padding:9px 10px;border-bottom:1px solid #1a1a2e;color:#cbd5e1}}
  tr:last-child td{{border-bottom:none}}
  tr:hover td{{background:#252840}}
  .truncate{{max-width:220px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
  .badge{{display:inline-block;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:600}}
  .badge-direct{{background:#1e3a5f;color:#60a5fa}}
  .badge-organicsearch{{background:#14302a;color:#34d399}}
  .badge-referral{{background:#2d1b4e;color:#a78bfa}}
  .badge-email{{background:#3b2000;color:#fbbf24}}
  .badge-paidsearch{{background:#3b0000;color:#f87171}}
  .badge-organicsocial{{background:#1a2040;color:#818cf8}}
  .badge-unassigned{{background:#1e2030;color:#64748b}}
  .note{{font-size:12px;color:#475569;font-style:italic}}
  @media(max-width:900px){{.grid-2,.grid-3,.grid-wide{{grid-template-columns:1fr}}.container{{padding:16px}}.header{{padding:20px}}}}
</style>
</head>
<body>
<div class="header">
  <div>
    <h1>GA4 Analytics — food-mag.co.uk</h1>
    <p>Generated {raw["generated"]}</p>
  </div>
  <div class="tabs">
    <button class="tab active" onclick="switchTab('6m',this)">Last 6 Months</button>
    <button class="tab" onclick="switchTab('12m',this)">Last 12 Months</button>
  </div>
</div>
<div class="container">
  {panel(p6, "6m")}
  {panel(p12, "12m")}
</div>
<script>
function switchTab(id, btn) {{
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.getElementById('panel_' + id).classList.add('active');
  btn.classList.add('active');
}}
document.getElementById('panel_6m').classList.add('active');
</script>
</body>
</html>"""

out = os.path.join(os.path.dirname(__file__), "index.html")
with open(out, "w") as f:
    f.write(html)

print(f"Dashboard written to {out}")
