import json
import os
import math

with open(os.path.join(os.path.dirname(__file__), "ga_data.json")) as f:
    d = json.load(f)


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


def total_sessions():
    return sum(int(r[1]) for r in d["channel"]["rows"])


def total_users():
    return sum(int(r[2]) for r in d["channel"]["rows"])


def avg_duration():
    total_s = sum(int(r[1]) for r in d["channel"]["rows"])
    weighted = sum(float(r[4]) * int(r[1]) for r in d["channel"]["rows"])
    return weighted / total_s if total_s else 0


# Build engagement trend
eng_dates = []
eng_users = []
eng_sessions = []
for row in sorted(d["engagement"]["rows"], key=lambda r: r[0]):
    raw = row[0]
    eng_dates.append(f"{raw[6:8]}/{raw[4:6]}/{raw[0:4]}")
    eng_users.append(int(row[1]))
    eng_sessions.append(int(row[2]))

# Channels
ch_labels = [r[0] for r in d["channel"]["rows"]]
ch_sessions = [int(r[1]) for r in d["channel"]["rows"]]
ch_bounce = [fmt_pct(r[3]) for r in d["channel"]["rows"]]
ch_duration = [fmt_duration(r[4]) for r in d["channel"]["rows"]]

# Countries
geo_labels = [r[0] for r in d["geo_country"]["rows"][:10]]
geo_sessions = [int(r[1]) for r in d["geo_country"]["rows"][:10]]
geo_duration = [fmt_duration(r[3]) for r in d["geo_country"]["rows"][:10]]

# Device
dev_labels = [r[0].capitalize() for r in d["device"]["rows"] if r[0] != "(other)"]
dev_sessions = [int(r[1]) for r in d["device"]["rows"] if r[0] != "(other)"]

# OS
os_labels = [r[0] for r in d["os"]["rows"][:8]]
os_sessions = [int(r[1]) for r in d["os"]["rows"][:8]]

# Browser
br_labels = [r[0] for r in d["browser"]["rows"][:8]]
br_sessions = [int(r[1]) for r in d["browser"]["rows"][:8]]

# Age (exclude unknown)
age_rows = [r for r in d["age"]["rows"] if r[0] not in ("unknown", "(not set)")]
age_labels = [r[0] for r in age_rows]
age_users = [int(r[1]) for r in age_rows]

# Gender (exclude unknown)
gen_rows = [r for r in d["gender"]["rows"] if r[0] not in ("unknown", "(not set)")]
gen_labels = [r[0].capitalize() for r in gen_rows]
gen_users = [int(r[1]) for r in gen_rows]

# Sources table
src_rows = [(r[0], r[1], int(r[2]), int(r[3])) for r in d["source"]["rows"][:15]]

# Landing pages table
lp_rows = [(r[0], int(r[1]), fmt_pct(r[3]), fmt_duration(r[4])) for r in d["landing_pages"]["rows"][:15] if r[0] != "(not set)"]

# Search terms table
st_rows = [(r[0], int(r[1])) for r in d["search_terms"]["rows"][:15] if r[0] not in ("", "(not set)")]

COLORS = [
    "#6366f1", "#8b5cf6", "#ec4899", "#f59e0b", "#10b981",
    "#3b82f6", "#ef4444", "#14b8a6", "#f97316", "#a855f7"
]

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GA4 Analytics Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #0f1117; color: #e2e8f0; min-height: 100vh; }}
  .header {{ background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%); padding: 32px 40px; border-bottom: 1px solid #2d2d4e; }}
  .header h1 {{ font-size: 28px; font-weight: 700; color: #fff; }}
  .header p {{ color: #a5b4fc; margin-top: 4px; font-size: 14px; }}
  .container {{ max-width: 1400px; margin: 0 auto; padding: 32px 40px; }}
  .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; margin-bottom: 32px; }}
  .stat {{ background: #1e2030; border: 1px solid #2d2d4e; border-radius: 12px; padding: 20px; }}
  .stat-label {{ font-size: 12px; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; }}
  .stat-value {{ font-size: 32px; font-weight: 700; color: #fff; margin-top: 4px; }}
  .stat-sub {{ font-size: 12px; color: #94a3b8; margin-top: 4px; }}
  .grid {{ display: grid; gap: 24px; margin-bottom: 24px; }}
  .grid-2 {{ grid-template-columns: 1fr 1fr; }}
  .grid-3 {{ grid-template-columns: 1fr 1fr 1fr; }}
  .grid-wide {{ grid-template-columns: 2fr 1fr; }}
  .card {{ background: #1e2030; border: 1px solid #2d2d4e; border-radius: 12px; padding: 24px; }}
  .card h2 {{ font-size: 15px; font-weight: 600; color: #c7d2fe; margin-bottom: 20px; display: flex; align-items: center; gap: 8px; }}
  .card h2::before {{ content: ""; display: block; width: 3px; height: 16px; background: #6366f1; border-radius: 2px; }}
  .chart-wrap {{ position: relative; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  th {{ text-align: left; padding: 8px 12px; color: #64748b; font-weight: 500; border-bottom: 1px solid #2d2d4e; font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; }}
  td {{ padding: 10px 12px; border-bottom: 1px solid #1a1a2e; color: #cbd5e1; }}
  tr:last-child td {{ border-bottom: none; }}
  tr:hover td {{ background: #252840; }}
  .badge {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; }}
  .badge-direct {{ background: #1e3a5f; color: #60a5fa; }}
  .badge-organic {{ background: #14302a; color: #34d399; }}
  .badge-referral {{ background: #2d1b4e; color: #a78bfa; }}
  .badge-email {{ background: #3b2000; color: #fbbf24; }}
  .badge-paid {{ background: #3b0000; color: #f87171; }}
  .note {{ font-size: 12px; color: #475569; margin-top: 16px; font-style: italic; }}
  @media (max-width: 900px) {{ .grid-2, .grid-3, .grid-wide {{ grid-template-columns: 1fr; }} .container {{ padding: 20px; }} }}
</style>
</head>
<body>
<div class="header">
  <h1>GA4 Analytics Dashboard</h1>
  <p>Last 30 days &nbsp;·&nbsp; Generated {d["generated"]} &nbsp;·&nbsp; Property {275227762}</p>
</div>
<div class="container">

  <!-- Summary stats -->
  <div class="stats">
    <div class="stat">
      <div class="stat-label">Total Sessions</div>
      <div class="stat-value">{total_sessions():,}</div>
    </div>
    <div class="stat">
      <div class="stat-label">Active Users</div>
      <div class="stat-value">{total_users():,}</div>
    </div>
    <div class="stat">
      <div class="stat-label">Avg Session Duration</div>
      <div class="stat-value">{fmt_duration(avg_duration())}</div>
    </div>
    <div class="stat">
      <div class="stat-label">Top Country</div>
      <div class="stat-value" style="font-size:20px">{d["geo_country"]["rows"][0][0] if d["geo_country"]["rows"] else "—"}</div>
      <div class="stat-sub">{int(d["geo_country"]["rows"][0][2]):,} sessions</div>
    </div>
    <div class="stat">
      <div class="stat-label">Top Channel</div>
      <div class="stat-value" style="font-size:18px">{d["channel"]["rows"][0][0] if d["channel"]["rows"] else "—"}</div>
      <div class="stat-sub">{int(d["channel"]["rows"][0][2]):,} sessions</div>
    </div>
    <div class="stat">
      <div class="stat-label">Top Device</div>
      <div class="stat-value" style="font-size:20px">{d["device"]["rows"][0][0].capitalize() if d["device"]["rows"] else "—"}</div>
      <div class="stat-sub">{int(d["device"]["rows"][0][2]):,} sessions</div>
    </div>
  </div>

  <!-- Engagement trend -->
  <div class="grid" style="margin-bottom:24px;">
    <div class="card">
      <h2>Sessions &amp; Users Over Time</h2>
      <div class="chart-wrap"><canvas id="trendChart" height="80"></canvas></div>
    </div>
  </div>

  <!-- Channels + Geo -->
  <div class="grid grid-wide">
    <div class="card">
      <h2>Sessions by Country</h2>
      <div class="chart-wrap"><canvas id="geoChart" height="120"></canvas></div>
    </div>
    <div class="card">
      <h2>Traffic Channels</h2>
      <div class="chart-wrap"><canvas id="channelChart" height="120"></canvas></div>
    </div>
  </div>

  <!-- Device + OS + Browser -->
  <div class="grid grid-3" style="margin-top:24px;">
    <div class="card">
      <h2>Device Type</h2>
      <div class="chart-wrap"><canvas id="deviceChart" height="180"></canvas></div>
    </div>
    <div class="card">
      <h2>Operating System</h2>
      <div class="chart-wrap"><canvas id="osChart" height="180"></canvas></div>
    </div>
    <div class="card">
      <h2>Browser</h2>
      <div class="chart-wrap"><canvas id="browserChart" height="180"></canvas></div>
    </div>
  </div>

  <!-- Age + Gender -->
  <div class="grid grid-2" style="margin-top:24px;">
    <div class="card">
      <h2>Age Bracket</h2>
      {"<div class='chart-wrap'><canvas id='ageChart' height='160'></canvas></div>" if age_rows else "<p class='note'>Insufficient data — enable Google Signals in GA4 and ensure traffic thresholds are met.</p>"}
    </div>
    <div class="card">
      <h2>Gender</h2>
      {"<div class='chart-wrap'><canvas id='genderChart' height='160'></canvas></div>" if gen_rows else "<p class='note'>Insufficient data — enable Google Signals in GA4 and ensure traffic thresholds are met.</p>"}
    </div>
  </div>

  <!-- Channel table -->
  <div class="grid" style="margin-top:24px;">
    <div class="card">
      <h2>Channel Performance</h2>
      <table>
        <thead><tr><th>Channel</th><th>Sessions</th><th>Users</th><th>Bounce Rate</th><th>Avg Duration</th></tr></thead>
        <tbody>
          {"".join(f'<tr><td><span class="badge badge-{r[0].lower().replace(" ","")}">{r[0]}</span></td><td>{int(r[1]):,}</td><td>{int(r[2]):,}</td><td>{fmt_pct(r[3])}</td><td>{fmt_duration(r[4])}</td></tr>' for r in d["channel"]["rows"])}
        </tbody>
      </table>
    </div>
  </div>

  <!-- Sources + Landing pages -->
  <div class="grid grid-2" style="margin-top:24px;">
    <div class="card">
      <h2>Traffic Sources</h2>
      <table>
        <thead><tr><th>Source</th><th>Medium</th><th>Sessions</th><th>Users</th></tr></thead>
        <tbody>
          {"".join(f'<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]:,}</td><td>{r[3]:,}</td></tr>' for r in src_rows)}
        </tbody>
      </table>
    </div>
    <div class="card">
      <h2>Top Landing Pages</h2>
      <table>
        <thead><tr><th>Page</th><th>Sessions</th><th>Bounce</th><th>Duration</th></tr></thead>
        <tbody>
          {"".join(f'<tr><td style="max-width:200px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap" title="{r[0]}">{r[0]}</td><td>{r[1]:,}</td><td>{r[2]}</td><td>{r[3]}</td></tr>' for r in lp_rows)}
        </tbody>
      </table>
    </div>
  </div>

  <!-- Search terms -->
  <div class="grid" style="margin-top:24px;">
    <div class="card">
      <h2>Site Search Terms</h2>
      {"<table><thead><tr><th>Search Term</th><th>Sessions</th></tr></thead><tbody>" + "".join(f'<tr><td>{r[0]}</td><td>{r[1]:,}</td></tr>' for r in st_rows) + "</tbody></table>" if st_rows else "<p class='note'>No site search terms recorded in this period.</p>"}
    </div>
  </div>

</div>

<script>
const COLORS = {json.dumps(COLORS)};

// Trend chart
new Chart(document.getElementById("trendChart"), {{
  type: "line",
  data: {{
    labels: {json.dumps(eng_dates)},
    datasets: [
      {{ label: "Sessions", data: {json.dumps(eng_sessions)}, borderColor: "#6366f1", backgroundColor: "rgba(99,102,241,0.1)", fill: true, tension: 0.3, pointRadius: 2 }},
      {{ label: "Users", data: {json.dumps(eng_users)}, borderColor: "#10b981", backgroundColor: "rgba(16,185,129,0.1)", fill: true, tension: 0.3, pointRadius: 2 }}
    ]
  }},
  options: {{ plugins: {{ legend: {{ labels: {{ color: "#94a3b8" }} }} }}, scales: {{ x: {{ ticks: {{ color: "#64748b", maxTicksLimit: 10 }}, grid: {{ color: "#1e2a3a" }} }}, y: {{ ticks: {{ color: "#64748b" }}, grid: {{ color: "#1e2a3a" }} }} }} }}
}});

// Geo chart
new Chart(document.getElementById("geoChart"), {{
  type: "bar",
  data: {{
    labels: {json.dumps(geo_labels)},
    datasets: [{{ label: "Sessions", data: {json.dumps(geo_sessions)}, backgroundColor: COLORS, borderRadius: 4 }}]
  }},
  options: {{ indexAxis: "y", plugins: {{ legend: {{ display: false }} }}, scales: {{ x: {{ ticks: {{ color: "#64748b" }}, grid: {{ color: "#1e2a3a" }} }}, y: {{ ticks: {{ color: "#94a3b8" }} }}, grid: {{ display: false }} }} }}
}});

// Channel doughnut
new Chart(document.getElementById("channelChart"), {{
  type: "doughnut",
  data: {{
    labels: {json.dumps(ch_labels)},
    datasets: [{{ data: {json.dumps(ch_sessions)}, backgroundColor: COLORS, borderWidth: 0, hoverOffset: 6 }}]
  }},
  options: {{ plugins: {{ legend: {{ position: "right", labels: {{ color: "#94a3b8", padding: 12, font: {{ size: 12 }} }} }} }} }}
}});

// Device doughnut
new Chart(document.getElementById("deviceChart"), {{
  type: "doughnut",
  data: {{
    labels: {json.dumps(dev_labels)},
    datasets: [{{ data: {json.dumps(dev_sessions)}, backgroundColor: ["#6366f1","#10b981","#f59e0b"], borderWidth: 0, hoverOffset: 4 }}]
  }},
  options: {{ plugins: {{ legend: {{ position: "bottom", labels: {{ color: "#94a3b8", padding: 10, font: {{ size: 12 }} }} }} }} }}
}});

// OS bar
new Chart(document.getElementById("osChart"), {{
  type: "bar",
  data: {{
    labels: {json.dumps(os_labels)},
    datasets: [{{ label: "Sessions", data: {json.dumps(os_sessions)}, backgroundColor: COLORS, borderRadius: 4 }}]
  }},
  options: {{ indexAxis: "y", plugins: {{ legend: {{ display: false }} }}, scales: {{ x: {{ ticks: {{ color: "#64748b" }}, grid: {{ color: "#1e2a3a" }} }}, y: {{ ticks: {{ color: "#94a3b8" }}, grid: {{ display: false }} }} }} }}
}});

// Browser bar
new Chart(document.getElementById("browserChart"), {{
  type: "bar",
  data: {{
    labels: {json.dumps(br_labels)},
    datasets: [{{ label: "Sessions", data: {json.dumps(br_sessions)}, backgroundColor: COLORS, borderRadius: 4 }}]
  }},
  options: {{ indexAxis: "y", plugins: {{ legend: {{ display: false }} }}, scales: {{ x: {{ ticks: {{ color: "#64748b" }}, grid: {{ color: "#1e2a3a" }} }}, y: {{ ticks: {{ color: "#94a3b8" }}, grid: {{ display: false }} }} }} }}
}});

{"// Age chart" if age_rows else ""}
{"new Chart(document.getElementById('ageChart'), { type: 'bar', data: { labels: " + json.dumps(age_labels) + ", datasets: [{ label: 'Users', data: " + json.dumps(age_users) + ", backgroundColor: COLORS, borderRadius: 4 }] }, options: { plugins: { legend: { display: false } }, scales: { x: { ticks: { color: '#94a3b8' }, grid: { display: false } }, y: { ticks: { color: '#64748b' }, grid: { color: '#1e2a3a' } } } } });" if age_rows else ""}

{"// Gender chart" if gen_rows else ""}
{"new Chart(document.getElementById('genderChart'), { type: 'doughnut', data: { labels: " + json.dumps(gen_labels) + ", datasets: [{ data: " + json.dumps(gen_users) + ", backgroundColor: ['#ec4899','#6366f1','#10b981'], borderWidth: 0, hoverOffset: 4 }] }, options: { plugins: { legend: { position: 'bottom', labels: { color: '#94a3b8', padding: 10, font: { size: 12 } } } } } });" if gen_rows else ""}
</script>
</body>
</html>"""

out = os.path.join(os.path.dirname(__file__), "dashboard.html")
with open(out, "w") as f:
    f.write(html)

print(f"Dashboard written to {out}")
