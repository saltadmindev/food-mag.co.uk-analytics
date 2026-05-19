import json
import os

with open(os.path.join(os.path.dirname(__file__), "ga_data.json")) as f:
    raw = json.load(f)

COLORS = ["#4f46e5","#7c3aed","#db2777","#d97706","#059669","#2563eb","#dc2626","#0891b2","#ea580c","#9333ea"]


def fmt_duration(seconds):
    try:
        s = float(seconds)
        return f"{s:.0f}s" if s < 60 else f"{s/60:.1f}m"
    except:
        return seconds


def fmt_pct(val):
    try:
        return f"{float(val)*100:.1f}%"
    except:
        return val


def build_period(d):
    ch = d["channel"]["rows"]
    ts = sum(int(r[1]) for r in ch)
    tu = sum(int(r[2]) for r in ch)
    wd = sum(float(r[4]) * int(r[1]) for r in ch)
    avg_dur = fmt_duration(wd / ts if ts else 0)

    eng_rows = sorted(d["engagement"]["rows"], key=lambda r: r[0])
    eng_dates    = [r[0][6:8] + "/" + r[0][4:6] for r in eng_rows]
    eng_sessions = [int(r[2]) for r in eng_rows]
    eng_users    = [int(r[1]) for r in eng_rows]

    geo_rows  = d["geo_country"]["rows"][:10]
    dev_rows  = [r for r in d["device"]["rows"] if r[0] != "(other)"]
    age_rows  = [r for r in d["age"]["rows"] if r[0] not in ("unknown","(not set)")]
    gen_rows  = [r for r in d["gender"]["rows"] if r[0] not in ("unknown","(not set)")]
    src_rows  = d["source"]["rows"][:15]
    lp_rows   = [r for r in d["landing_pages"]["rows"][:15] if r[0] != "(not set)"]
    st_rows   = [r for r in d["search_terms"]["rows"][:15] if r[0] not in ("","(not set)")]

    top_country   = geo_rows[0][0] if geo_rows else "—"
    top_country_s = f"{int(geo_rows[0][1]):,}" if geo_rows else ""
    top_channel   = ch[0][0] if ch else "—"
    top_channel_s = f"{int(ch[0][1]):,}" if ch else ""
    top_device    = dev_rows[0][0].capitalize() if dev_rows else "—"
    top_device_s  = f"{int(dev_rows[0][1]):,}" if dev_rows else ""

    def ch_table_rows():
        out = ""
        for r in ch:
            cls = r[0].lower().replace(" ","").replace("/","")
            out += "<tr><td><span class=\"badge badge-" + cls + "\">" + r[0] + "</span></td>"
            out += "<td>" + f"{int(r[1]):,}" + "</td><td>" + f"{int(r[2]):,}" + "</td>"
            out += "<td>" + fmt_pct(r[3]) + "</td><td>" + fmt_duration(r[4]) + "</td></tr>"
        return out

    def src_table_rows():
        return "".join(
            "<tr><td>" + r[0] + "</td><td>" + r[1] + "</td><td>" + f"{int(r[2]):,}" + "</td><td>" + f"{int(r[3]):,}" + "</td></tr>"
            for r in src_rows
        )

    def lp_table_rows():
        return "".join(
            "<tr><td class=\"truncate\" title=\"" + r[0] + "\">" + r[0] + "</td><td>" + f"{int(r[1]):,}" + "</td><td>" + fmt_pct(r[3]) + "</td><td>" + fmt_duration(r[4]) + "</td></tr>"
            for r in lp_rows
        )

    def st_html():
        if not st_rows:
            return "<p class='note'>No site search terms recorded.</p>"
        rows = "".join("<tr><td>" + r[0] + "</td><td>" + f"{int(r[1]):,}" + "</td></tr>" for r in st_rows)
        return "<table><thead><tr><th>Term</th><th>Sessions</th></tr></thead><tbody>" + rows + "</tbody></table>"

    return {
        "total_sessions": f"{ts:,}",
        "total_users":    f"{tu:,}",
        "avg_duration":   avg_dur,
        "top_country":    top_country,
        "top_country_s":  top_country_s,
        "top_channel":    top_channel,
        "top_channel_s":  top_channel_s,
        "top_device":     top_device,
        "top_device_s":   top_device_s,
        "ch_table":       ch_table_rows(),
        "src_table":      src_table_rows(),
        "lp_table":       lp_table_rows(),
        "st_html":        st_html(),
        "has_age":        bool(age_rows),
        "has_gen":        bool(gen_rows),
        "data": {
            "eng_dates":    eng_dates,
            "eng_sessions": eng_sessions,
            "eng_users":    eng_users,
            "geo_labels":   [r[0] for r in geo_rows],
            "geo_sessions": [int(r[1]) for r in geo_rows],
            "ch_labels":    [r[0] for r in ch],
            "ch_sessions":  [int(r[1]) for r in ch],
            "dev_labels":   [r[0].capitalize() for r in dev_rows],
            "dev_sessions": [int(r[1]) for r in dev_rows],
            "os_labels":    [r[0] for r in d["os"]["rows"][:8]],
            "os_sessions":  [int(r[1]) for r in d["os"]["rows"][:8]],
            "br_labels":    [r[0] for r in d["browser"]["rows"][:8]],
            "br_sessions":  [int(r[1]) for r in d["browser"]["rows"][:8]],
            "age_labels":   [r[0] for r in age_rows],
            "age_users":    [int(r[1]) for r in age_rows],
            "gen_labels":   [r[0].capitalize() for r in gen_rows],
            "gen_users":    [int(r[1]) for r in gen_rows],
        }
    }


p_ww6  = build_period(raw["ww_6m"])
p_ww12 = build_period(raw["ww_12m"])
p_gb6  = build_period(raw["gb_6m"])
p_gb12 = build_period(raw["gb_12m"])


def panel_html(p, pid, active):
    cls = "panel active" if active else "panel"
    age_html = "<canvas id=\"ageChart_" + pid + "\" height=\"160\"></canvas>" if p["has_age"] else "<p class='note'>Insufficient data — enable Google Signals in GA4.</p>"
    gen_html = "<canvas id=\"genderChart_" + pid + "\" height=\"160\"></canvas>" if p["has_gen"] else "<p class='note'>Insufficient data — enable Google Signals in GA4.</p>"
    return (
        "<div class=\"" + cls + "\" id=\"panel_" + pid + "\">"
        "<div class=\"stats\">"
        "<div class=\"stat\"><div class=\"stat-label\">Total Sessions</div><div class=\"stat-value\">" + p["total_sessions"] + "</div></div>"
        "<div class=\"stat\"><div class=\"stat-label\">Active Users</div><div class=\"stat-value\">" + p["total_users"] + "</div></div>"
        "<div class=\"stat\"><div class=\"stat-label\">Avg Session Duration</div><div class=\"stat-value\">" + p["avg_duration"] + "</div></div>"
        "<div class=\"stat\"><div class=\"stat-label\">Top Country</div><div class=\"stat-value sm\">" + p["top_country"] + "</div><div class=\"stat-sub\">" + p["top_country_s"] + " sessions</div></div>"
        "<div class=\"stat\"><div class=\"stat-label\">Top Channel</div><div class=\"stat-value sm\">" + p["top_channel"] + "</div><div class=\"stat-sub\">" + p["top_channel_s"] + " sessions</div></div>"
        "<div class=\"stat\"><div class=\"stat-label\">Top Device</div><div class=\"stat-value sm\">" + p["top_device"] + "</div><div class=\"stat-sub\">" + p["top_device_s"] + " sessions</div></div>"
        "</div>"
        "<div class=\"card full\"><h2>Sessions &amp; Users Over Time</h2><canvas id=\"trendChart_" + pid + "\" height=\"70\"></canvas></div>"
        "<div class=\"grid grid-wide\">"
        "<div class=\"card\"><h2>Sessions by Country</h2><canvas id=\"geoChart_" + pid + "\" height=\"120\"></canvas></div>"
        "<div class=\"card\"><h2>Traffic Channels</h2><canvas id=\"channelChart_" + pid + "\" height=\"120\"></canvas></div>"
        "</div>"
        "<div class=\"grid grid-3\">"
        "<div class=\"card\"><h2>Device Type</h2><canvas id=\"deviceChart_" + pid + "\" height=\"180\"></canvas></div>"
        "<div class=\"card\"><h2>Operating System</h2><canvas id=\"osChart_" + pid + "\" height=\"180\"></canvas></div>"
        "<div class=\"card\"><h2>Browser</h2><canvas id=\"browserChart_" + pid + "\" height=\"180\"></canvas></div>"
        "</div>"
        "<div class=\"grid grid-2\">"
        "<div class=\"card\"><h2>Age Bracket</h2>" + age_html + "</div>"
        "<div class=\"card\"><h2>Gender</h2>" + gen_html + "</div>"
        "</div>"
        "<div class=\"card full\"><h2>Channel Performance</h2>"
        "<table><thead><tr><th>Channel</th><th>Sessions</th><th>Users</th><th>Bounce Rate</th><th>Avg Duration</th></tr></thead>"
        "<tbody>" + p["ch_table"] + "</tbody></table></div>"
        "<div class=\"grid grid-2\">"
        "<div class=\"card\"><h2>Traffic Sources</h2>"
        "<table><thead><tr><th>Source</th><th>Medium</th><th>Sessions</th><th>Users</th></tr></thead>"
        "<tbody>" + p["src_table"] + "</tbody></table></div>"
        "<div class=\"card\"><h2>Top Landing Pages</h2>"
        "<table><thead><tr><th>Page</th><th>Sessions</th><th>Bounce</th><th>Duration</th></tr></thead>"
        "<tbody>" + p["lp_table"] + "</tbody></table></div>"
        "</div>"
        "<div class=\"card full\"><h2>Site Search Terms</h2>" + p["st_html"] + "</div>"
        "</div>"
    )


def data_vars(p, pid):
    d = p["data"]
    lines = []
    for key, val in d.items():
        lines.append("const " + key + "_" + pid + " = " + json.dumps(val) + ";")
    return "\n".join(lines)


CHART_OPTS = {
    "line_scales": '{"x":{"ticks":{"color":"#9ca3af","maxTicksLimit":12},"grid":{"color":"#f3f4f6"}},"y":{"ticks":{"color":"#9ca3af"},"grid":{"color":"#f3f4f6"}}}',
    "bar_scales_h": '{"x":{"ticks":{"color":"#9ca3af"},"grid":{"color":"#f3f4f6"}},"y":{"ticks":{"color":"#374151"},"grid":{"display":false}}}',
}


def init_js(pid):
    return """
  IC('trendChart_{p}',{type:'line',data:{labels:eng_dates_{p},datasets:[
    {label:'Sessions',data:eng_sessions_{p},borderColor:'#4f46e5',backgroundColor:'rgba(79,70,229,0.08)',fill:true,tension:0.3,pointRadius:2},
    {label:'Users',data:eng_users_{p},borderColor:'#059669',backgroundColor:'rgba(5,150,105,0.08)',fill:true,tension:0.3,pointRadius:2}
  ]},options:{plugins:{legend:{labels:{color:'#374151'}}},scales:{x:{ticks:{color:'#9ca3af',maxTicksLimit:12},grid:{color:'#f3f4f6'}},y:{ticks:{color:'#9ca3af'},grid:{color:'#f3f4f6'}}}}});
  IC('geoChart_{p}',{type:'bar',data:{labels:geo_labels_{p},datasets:[{label:'Sessions',data:geo_sessions_{p},backgroundColor:COLORS,borderRadius:4}]},options:{indexAxis:'y',plugins:{legend:{display:false}},scales:{x:{ticks:{color:'#9ca3af'},grid:{color:'#f3f4f6'}},y:{ticks:{color:'#374151'},grid:{display:false}}}}});
  IC('channelChart_{p}',{type:'doughnut',data:{labels:ch_labels_{p},datasets:[{data:ch_sessions_{p},backgroundColor:COLORS,borderWidth:0,hoverOffset:6}]},options:{plugins:{legend:{position:'right',labels:{color:'#374151',padding:12,font:{size:12}}}}}});
  IC('deviceChart_{p}',{type:'doughnut',data:{labels:dev_labels_{p},datasets:[{data:dev_sessions_{p},backgroundColor:['#4f46e5','#059669','#d97706'],borderWidth:0,hoverOffset:4}]},options:{plugins:{legend:{position:'bottom',labels:{color:'#374151',padding:10,font:{size:12}}}}}});
  IC('osChart_{p}',{type:'bar',data:{labels:os_labels_{p},datasets:[{label:'Sessions',data:os_sessions_{p},backgroundColor:COLORS,borderRadius:4}]},options:{indexAxis:'y',plugins:{legend:{display:false}},scales:{x:{ticks:{color:'#9ca3af'},grid:{color:'#f3f4f6'}},y:{ticks:{color:'#374151'},grid:{display:false}}}}});
  IC('browserChart_{p}',{type:'bar',data:{labels:br_labels_{p},datasets:[{label:'Sessions',data:br_sessions_{p},backgroundColor:COLORS,borderRadius:4}]},options:{indexAxis:'y',plugins:{legend:{display:false}},scales:{x:{ticks:{color:'#9ca3af'},grid:{color:'#f3f4f6'}},y:{ticks:{color:'#374151'},grid:{display:false}}}}});
  if(typeof age_labels_{p}!=='undefined'&&age_labels_{p}.length) IC('ageChart_{p}',{type:'bar',data:{labels:age_labels_{p},datasets:[{label:'Users',data:age_users_{p},backgroundColor:COLORS,borderRadius:4}]},options:{plugins:{legend:{display:false}},scales:{x:{ticks:{color:'#374151'},grid:{display:false}},y:{ticks:{color:'#9ca3af'},grid:{color:'#f3f4f6'}}}}});
  if(typeof gen_labels_{p}!=='undefined'&&gen_labels_{p}.length) IC('genderChart_{p}',{type:'doughnut',data:{labels:gen_labels_{p},datasets:[{data:gen_users_{p},backgroundColor:['#db2777','#4f46e5','#059669'],borderWidth:0,hoverOffset:4}]},options:{plugins:{legend:{position:'bottom',labels:{color:'#374151',padding:10,font:{size:12}}}}}});
""".replace("{p}", pid)


html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>GA4 Dashboard — food-mag.co.uk</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
  *,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
  body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:#f9fafb;color:#111827;min-height:100vh}
  .header{background:#fff;border-bottom:1px solid #e5e7eb;padding:24px 40px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px}
  .header h1{font-size:20px;font-weight:700;color:#111827}
  .header p{color:#6b7280;font-size:13px;margin-top:2px}
  .top-tabs{display:flex;gap:6px}
  .top-tab{padding:8px 22px;border-radius:6px;border:1px solid #e5e7eb;background:#fff;color:#6b7280;font-size:14px;font-weight:700;cursor:pointer;transition:all 0.15s}
  .top-tab.active{background:#111827;color:#fff;border-color:#111827}
  .top-tab:hover:not(.active){background:#f3f4f6;color:#111827}
  .sub-bar{background:#fff;border-bottom:1px solid #e5e7eb;padding:12px 40px;display:flex;gap:6px}
  .sub-tab{padding:6px 16px;border-radius:6px;border:1px solid #e5e7eb;background:#fff;color:#6b7280;font-size:13px;font-weight:600;cursor:pointer;transition:all 0.15s}
  .sub-tab.active{background:#4f46e5;color:#fff;border-color:#4f46e5}
  .sub-tab:hover:not(.active){background:#f3f4f6;color:#111827}
  .section{display:none}.section.active{display:block}
  .container{max-width:1400px;margin:0 auto;padding:28px 40px}
  .panel{display:none}.panel.active{display:block}
  .stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:14px;margin-bottom:20px}
  .stat{background:#fff;border:1px solid #e5e7eb;border-radius:10px;padding:18px}
  .stat-label{font-size:11px;color:#9ca3af;text-transform:uppercase;letter-spacing:0.05em;font-weight:500}
  .stat-value{font-size:28px;font-weight:700;color:#111827;margin-top:4px;line-height:1}
  .stat-value.sm{font-size:17px;margin-top:6px}
  .stat-sub{font-size:12px;color:#9ca3af;margin-top:4px}
  .grid{display:grid;gap:16px;margin-bottom:16px}
  .grid-2{grid-template-columns:1fr 1fr}
  .grid-3{grid-template-columns:1fr 1fr 1fr}
  .grid-wide{grid-template-columns:2fr 1fr}
  .card{background:#fff;border:1px solid #e5e7eb;border-radius:10px;padding:22px}
  .card.full{margin-bottom:16px}
  h2{font-size:11px;font-weight:600;color:#9ca3af;margin-bottom:16px;text-transform:uppercase;letter-spacing:0.06em}
  table{width:100%;border-collapse:collapse;font-size:13px}
  th{text-align:left;padding:7px 10px;color:#9ca3af;font-weight:500;border-bottom:1px solid #f3f4f6;font-size:11px;text-transform:uppercase;letter-spacing:0.04em}
  td{padding:9px 10px;border-bottom:1px solid #f9fafb;color:#374151}
  tr:last-child td{border-bottom:none}
  tr:hover td{background:#fafafa}
  .truncate{max-width:220px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .badge{display:inline-block;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:600}
  .badge-direct{background:#eff6ff;color:#2563eb}
  .badge-organicsearch{background:#f0fdf4;color:#16a34a}
  .badge-referral{background:#faf5ff;color:#7c3aed}
  .badge-email{background:#fffbeb;color:#d97706}
  .badge-paidsearch{background:#fef2f2;color:#dc2626}
  .badge-organicsocial{background:#f0f9ff;color:#0284c7}
  .badge-unassigned{background:#f9fafb;color:#9ca3af}
  .note{font-size:12px;color:#9ca3af;font-style:italic}
  @media(max-width:900px){.grid-2,.grid-3,.grid-wide{grid-template-columns:1fr}.container{padding:16px}.header{padding:16px 20px}.sub-bar{padding:10px 16px}}
</style>
</head>
<body>
<div class="header">
  <div>
    <h1>food-mag.co.uk — Analytics</h1>
    <p>Generated """ + raw["generated"] + """</p>
  </div>
  <div class="top-tabs">
    <button class="top-tab active" onclick="switchSection('ww',this)">Worldwide</button>
    <button class="top-tab" onclick="switchSection('gb',this)">GB Only</button>
  </div>
</div>

<div class="section active" id="section_ww">
  <div class="sub-bar">
    <button class="sub-tab active" onclick="switchPanel('ww_6m',this,'ww')">Last 6 Months</button>
    <button class="sub-tab" onclick="switchPanel('ww_12m',this,'ww')">Last 12 Months</button>
  </div>
  <div class="container">
""" + panel_html(p_ww6, "ww_6m", True) + panel_html(p_ww12, "ww_12m", False) + """
  </div>
</div>

<div class="section" id="section_gb">
  <div class="sub-bar">
    <button class="sub-tab active" onclick="switchPanel('gb_6m',this,'gb')">Last 6 Months</button>
    <button class="sub-tab" onclick="switchPanel('gb_12m',this,'gb')">Last 12 Months</button>
  </div>
  <div class="container">
""" + panel_html(p_gb6, "gb_6m", True) + panel_html(p_gb12, "gb_12m", False) + """
  </div>
</div>

<script>
const COLORS = """ + json.dumps(COLORS) + """;
""" + data_vars(p_ww6, "ww_6m") + """
""" + data_vars(p_ww12, "ww_12m") + """
""" + data_vars(p_gb6, "gb_6m") + """
""" + data_vars(p_gb12, "gb_12m") + """
const _done = {};
function IC(id, cfg) { if (!_done[id]) { const el = document.getElementById(id); if (el) { new Chart(el, cfg); _done[id] = 1; } } }
function initww_6m() {""" + init_js("ww_6m") + """}
function initww_12m() {""" + init_js("ww_12m") + """}
function initgb_6m() {""" + init_js("gb_6m") + """}
function initgb_12m() {""" + init_js("gb_12m") + """}

function switchSection(id, btn) {
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  document.querySelectorAll('.top-tab').forEach(t => t.classList.remove('active'));
  document.getElementById('section_' + id).classList.add('active');
  btn.classList.add('active');
  if (id === 'gb') initgb_6m();
}

function switchPanel(id, btn, section) {
  const sec = document.getElementById('section_' + section);
  sec.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  btn.parentElement.querySelectorAll('.sub-tab').forEach(t => t.classList.remove('active'));
  document.getElementById('panel_' + id).classList.add('active');
  btn.classList.add('active');
  window['init' + id]();
}

window.addEventListener('DOMContentLoaded', initww_6m);
</script>
</body>
</html>"""

out = os.path.join(os.path.dirname(__file__), "index.html")
with open(out, "w") as f:
    f.write(html)

print("Dashboard written.")
