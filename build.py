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


CITY_COORDS = {
    "London":[51.5074,-0.1278],"Birmingham":[52.4862,-1.8904],"Manchester":[53.4808,-2.2426],
    "Leeds":[53.8008,-1.5491],"Sheffield":[53.3811,-1.4701],"Bristol":[51.4545,-2.5879],
    "Liverpool":[53.4084,-2.9916],"Plymouth":[50.3755,-4.1427],"Edinburgh":[55.9533,-3.1883],
    "Glasgow":[55.8642,-4.2518],"Cardiff":[51.4816,-3.1791],"Belfast":[54.5973,-5.9301],
    "Nottingham":[52.9548,-1.1581],"Leicester":[52.6369,-1.1398],"Coventry":[52.4068,-1.5197],
    "Bradford":[53.796,-1.7594],"Stoke-on-Trent":[53.0027,-2.1794],"Wolverhampton":[52.5862,-2.1265],
    "Derby":[52.9225,-1.4746],"Southampton":[50.9097,-1.4044],"Portsmouth":[50.8198,-1.088],
    "Oxford":[51.752,-1.2577],"Cambridge":[52.2053,0.1218],"Norwich":[52.6309,1.2974],
    "Exeter":[50.7236,-3.5275],"Bath":[51.3758,-2.3599],"York":[53.9591,-1.0815],
    "Hull":[53.7676,-0.3274],"Kingston upon Hull":[53.7676,-0.3274],
    "Sunderland":[54.9069,-1.3838],"Newcastle upon Tyne":[54.9783,-1.6178],"Newcastle":[54.9783,-1.6178],
    "Aberdeen":[57.1497,-2.0943],"Dundee":[56.462,-2.9707],"Swansea":[51.6214,-3.9436],
    "Brighton":[50.8225,-0.1372],"Brighton and Hove":[50.8225,-0.1372],
    "Bournemouth":[50.7192,-1.8808],"Reading":[51.4543,-0.9781],"Luton":[51.8787,-0.42],
    "Northampton":[52.2405,-0.9027],"Milton Keynes":[52.0406,-0.7594],"Peterborough":[52.5695,-0.2405],
    "Ipswich":[52.0567,1.1482],"Gloucester":[51.8642,-2.2382],"Blackpool":[53.8175,-3.0357],
    "Middlesbrough":[54.5742,-1.235],"Huddersfield":[53.6458,-1.7853],"Wigan":[53.5454,-2.6322],
    "Stockport":[53.4083,-2.1494],"Telford":[52.6766,-2.4469],"Doncaster":[53.5228,-1.1286],
    "Barnsley":[53.5526,-1.4797],"Wakefield":[53.683,-1.4977],"Rotherham":[53.43,-1.3563],
    "Salford":[53.4875,-2.2901],"Bolton":[53.5779,-2.4282],"Oldham":[53.54,-2.1183],
    "Rochdale":[53.6156,-2.1553],"Blackburn":[53.7481,-2.4847],"Preston":[53.7632,-2.7031],
    "Chester":[53.1905,-2.891],"Warrington":[53.39,-2.597],"Guildford":[51.2362,-0.5704],
    "Chelmsford":[51.7356,0.4685],"Colchester":[51.8957,0.8919],"Shrewsbury":[52.7075,-2.754],
    "Worcester":[52.192,-2.22],"Hereford":[52.0565,-2.716],"Carlisle":[54.8951,-2.9382],
    "Lancaster":[54.0466,-2.8007],"Durham":[54.7761,-1.5733],"Inverness":[57.4778,-4.2247],
    "Perth":[56.3958,-3.4311],"Stirling":[56.1165,-3.9369],"Newport":[51.5842,-2.9977],
    "Wrexham":[53.047,-2.9924],"Derry":[54.9966,-7.3086],"Londonderry":[54.9966,-7.3086],
    "Lisburn":[54.5162,-6.058],"Cheltenham":[51.8994,-2.0783],"Swindon":[51.5558,-1.7797],
    "Slough":[51.5105,-0.595],"Watford":[51.6565,-0.3969],"Basildon":[51.577,0.49],
    "Southend-on-Sea":[51.5461,0.7077],"Worthing":[50.812,-0.372],"Crawley":[51.1091,-0.1872],
    "Eastbourne":[50.7692,0.2799],"Hastings":[50.8549,0.5714],"Canterbury":[51.2802,1.0789],
    "Maidstone":[51.272,0.529],"Medway":[51.3898,0.543],"Aldershot":[51.248,-0.7616],
    "Basingstoke":[51.2665,-1.0875],"Salisbury":[51.0688,-1.7945],"Weston-super-Mare":[51.3462,-2.9776],
    "Taunton":[51.0158,-3.0973],"Torquay":[50.4619,-3.5253],"Truro":[50.2632,-5.051],
    "Newquay":[50.413,-5.0757],"Aylesbury":[51.814,-0.8078],"High Wycombe":[51.6288,-0.7478],
    "Banbury":[52.0629,-1.3398],"Dundee":[56.462,-2.9707],"Kilmarnock":[55.6111,-4.4961],
    "Ayr":[55.4595,-4.629],"Paisley":[55.8459,-4.423],"Motherwell":[55.7861,-3.9898],
    "Dunfermline":[56.0719,-3.4536],"Falkirk":[56.0019,-3.7839],"Kirkcaldy":[56.1107,-3.1628],
    "Barry":[51.4051,-3.284],"Bridgend":[51.5048,-3.5772],"Neath":[51.6614,-3.8069],
    "Llanelli":[51.684,-4.1632],"Carmarthen":[51.8579,-4.312],"Merthyr Tydfil":[51.7462,-3.3783],
    "Newry":[54.1762,-6.3451],"Antrim":[54.7195,-6.2036],"Ballymena":[54.8631,-6.2764],
    "Coleraine":[55.133,-6.668],"Omagh":[54.5976,-7.3038],"Enniskillen":[54.3449,-7.6351],
    "Bury St Edmunds":[52.2437,0.7152],"St Albans":[51.7454,-0.3366],"Stevenage":[51.9017,-0.2046],
    "Harlow":[51.7754,0.1003],"Bedford":[52.1356,-0.4666],"Dunstable":[51.886,-0.5218],
    "Lowestoft":[52.48,1.75],"Great Yarmouth":[52.6075,1.7291],"Wokingham":[51.4113,-0.8348],
    "Bracknell":[51.4162,-0.7478],"Windsor":[51.4839,-0.6044],"Maidenhead":[51.5221,-0.7228],
    "Hemel Hempstead":[51.7526,-0.4427],"Hitchin":[51.9463,-0.2799],"Trowbridge":[51.3199,-2.2085],
    "Yeovil":[50.9421,-2.6364],"Bridgwater":[51.128,-3.0003],"Crediton":[50.7908,-3.6524],
    "Tavistock":[50.5482,-4.1448],"Exmouth":[50.6214,-3.4136],"Newton Abbot":[50.5268,-3.6066],
    "Brixham":[50.3975,-3.5148],"Honiton":[50.7987,-3.1883],"Sidmouth":[50.6832,-3.2395],
    "Cirencester":[51.7219,-1.9674],"Stroud":[51.7458,-2.218],"Chippenham":[51.4584,-2.1196],
    "Frome":[51.2303,-2.3223],"Wisbech":[52.663,0.1595],"Huntingdon":[52.3319,-0.18],
    "St Neots":[52.2296,-0.277],"Newmarket":[52.2439,0.4078],"Haverhill":[52.0845,0.44],
    "Letchworth":[51.9779,-0.2283],"Welwyn Garden City":[51.7981,-0.1895],"Hatfield":[51.7632,-0.2285],
    "Bicester":[51.9001,-1.1531],"Witney":[51.7843,-1.4863],"Abingdon":[51.6708,-1.282],
    "Winchester":[51.0632,-1.3077],"Andover":[51.2082,-1.4822],"Newbury":[51.4013,-1.3221],
    "Farnham":[51.2146,-0.7985],"Woking":[51.3188,-0.5564],"Guildford":[51.2362,-0.5704],
    "Aberdeen":[57.1497,-2.0943],"Fort William":[56.8198,-5.106],"Oban":[56.4117,-5.472],
    "Dumfries":[55.0713,-3.605],"Hamilton":[55.777,-4.0388],"Livingston":[55.8894,-3.5223],
    "Aberystwyth":[52.4153,-4.0829],"Llandudno":[53.3236,-3.8272],"Rhyl":[53.3197,-3.4893],
    "Colwyn Bay":[53.2934,-3.726],"Pontypridd":[51.5968,-3.3432],"Caerphilly":[51.5788,-3.2189],
    "Cwmbran":[51.6539,-3.0228]
}

CITY_TO_COUNTY = {
    # London — GA4 reports all London as "London"; handled as special case in JS map
    "London":"London",
    # West Midlands metro LADs
    "Birmingham":"Birmingham","Wolverhampton":"Wolverhampton","Coventry":"Coventry",
    "Walsall":"Walsall","Sandwell":"Sandwell","Dudley":"Dudley","Solihull":"Solihull",
    # Greater Manchester LADs
    "Manchester":"Manchester","Salford":"Salford","Bolton":"Bolton",
    "Oldham":"Oldham","Rochdale":"Rochdale","Stockport":"Stockport","Wigan":"Wigan",
    "Bury":"Bury","Tameside":"Tameside","Trafford":"Trafford",
    # West Yorkshire LADs
    "Leeds":"Leeds","Bradford":"Bradford","Huddersfield":"Kirklees","Wakefield":"Wakefield","Halifax":"Calderdale",
    # South Yorkshire LADs
    "Sheffield":"Sheffield","Doncaster":"Doncaster","Barnsley":"Barnsley","Rotherham":"Rotherham",
    # Merseyside LADs
    "Liverpool":"Liverpool","Birkenhead":"Wirral","Southport":"Sefton","St Helens":"St. Helens","Knowsley":"Knowsley",
    # Devon LADs
    "Plymouth":"Plymouth","Exeter":"Exeter","Torquay":"Torbay","Brixham":"Torbay",
    "Barnstaple":"North Devon","Tavistock":"West Devon","Newton Abbot":"Teignbridge",
    "Exmouth":"East Devon","Honiton":"East Devon","Sidmouth":"East Devon","Crediton":"Mid Devon",
    # Bristol / South West LADs
    "Bristol":"Bristol, City of","Bath":"Bath and North East Somerset","Weston-super-Mare":"North Somerset",
    "Taunton":"Taunton Deane","Yeovil":"South Somerset","Bridgwater":"Sedgemoor","Frome":"Mendip",
    "Gloucester":"Gloucester","Cheltenham":"Cheltenham","Cirencester":"Cotswold","Stroud":"Stroud",
    "Swindon":"Swindon","Salisbury":"Wiltshire","Chippenham":"Wiltshire","Trowbridge":"Wiltshire",
    "Truro":"Cornwall","Newquay":"Cornwall",
    # Norfolk / Suffolk / Essex LADs
    "Norwich":"Norwich","Great Yarmouth":"Great Yarmouth",
    "Ipswich":"Ipswich","Bury St Edmunds":"St Edmundsbury","Lowestoft":"Waveney",
    "Newmarket":"Forest Heath","Haverhill":"St Edmundsbury",
    "Colchester":"Colchester","Chelmsford":"Chelmsford","Basildon":"Basildon",
    "Southend-on-Sea":"Southend-on-Sea","Harlow":"Harlow",
    # Tyne & Wear LADs
    "Newcastle upon Tyne":"Newcastle upon Tyne","Newcastle":"Newcastle upon Tyne",
    "Sunderland":"Sunderland","Gateshead":"Gateshead",
    # East Midlands LADs
    "Nottingham":"Nottingham","Leicester":"Leicester","Derby":"Derby",
    "Northampton":"Northampton","Peterborough":"Peterborough","Cambridge":"Cambridge",
    "Lincoln":"Lincoln",
    # Yorkshire
    "York":"York","Middlesbrough":"Middlesbrough",
    "Hull":"Kingston upon Hull, City of","Kingston upon Hull":"Kingston upon Hull, City of",
    # Lancashire LADs
    "Preston":"Preston","Blackpool":"Blackpool","Blackburn":"Blackburn with Darwen","Lancaster":"Lancaster",
    # Cheshire
    "Chester":"Cheshire West and Chester","Warrington":"Warrington",
    # North East
    "Durham":"County Durham","Carlisle":"Carlisle",
    # Beds / Herts / Bucks LADs
    "Luton":"Luton","Bedford":"Bedford","Dunstable":"Central Bedfordshire",
    "Watford":"Watford","St Albans":"St Albans","Stevenage":"Stevenage",
    "Hemel Hempstead":"Dacorum","Hatfield":"Welwyn Hatfield","Welwyn Garden City":"Welwyn Hatfield",
    "Letchworth":"North Hertfordshire","Hitchin":"North Hertfordshire",
    "Milton Keynes":"Milton Keynes","Aylesbury":"Aylesbury Vale","High Wycombe":"Wycombe",
    # Berkshire / Oxfordshire LADs
    "Reading":"Reading","Slough":"Slough","Windsor":"Windsor and Maidenhead","Maidenhead":"Windsor and Maidenhead",
    "Wokingham":"Wokingham","Bracknell":"Bracknell Forest","Newbury":"West Berkshire",
    "Oxford":"Oxford","Banbury":"Cherwell","Bicester":"Cherwell","Witney":"West Oxfordshire","Abingdon":"Vale of White Horse",
    # Hampshire / Surrey / Kent / Sussex LADs
    "Southampton":"Southampton","Portsmouth":"Portsmouth","Basingstoke":"Basingstoke and Deane",
    "Winchester":"Winchester","Aldershot":"Rushmoor","Andover":"Test Valley",
    "Guildford":"Guildford","Woking":"Woking","Crawley":"Crawley","Worthing":"Worthing",
    "Brighton":"Brighton and Hove","Brighton and Hove":"Brighton and Hove","Eastbourne":"Eastbourne","Hastings":"Hastings",
    "Canterbury":"Canterbury","Maidstone":"Maidstone","Medway":"Medway","Folkestone":"Shepway",
    # West Midlands non-metro LADs
    "Worcester":"Worcester","Hereford":"Herefordshire, County of","Shrewsbury":"Shropshire","Telford":"Telford and Wrekin",
    "Stoke-on-Trent":"Stoke-on-Trent","Burton upon Trent":"East Staffordshire","Stafford":"Stafford",
    # Scotland LADs
    "Edinburgh":"City of Edinburgh","Glasgow":"Glasgow City","Aberdeen":"Aberdeen City",
    "Dundee":"Dundee City","Perth":"Perth and Kinross","Stirling":"Stirling","Inverness":"Highland",
    "Kilmarnock":"East Ayrshire","Ayr":"South Ayrshire","Paisley":"Renfrewshire",
    "Motherwell":"North Lanarkshire","Hamilton":"South Lanarkshire","Livingston":"West Lothian",
    "Falkirk":"Falkirk","Dunfermline":"Fife","Kirkcaldy":"Fife","Glenrothes":"Fife",
    "Dumfries":"Dumfries and Galloway","Oban":"Argyll and Bute","Fort William":"Highland",
    # Wales LADs
    "Cardiff":"Cardiff","Swansea":"Swansea","Newport":"Newport","Wrexham":"Wrexham",
    "Barry":"Vale of Glamorgan","Bridgend":"Bridgend","Neath":"Neath Port Talbot",
    "Llanelli":"Carmarthenshire","Carmarthen":"Carmarthenshire","Merthyr Tydfil":"Merthyr Tydfil",
    "Pontypridd":"Rhondda Cynon Taf","Caerphilly":"Caerphilly","Cwmbran":"Torfaen",
    "Aberystwyth":"Ceredigion","Llandudno":"Conwy","Rhyl":"Denbighshire","Colwyn Bay":"Conwy",
    # Northern Ireland council areas
    "Belfast":"Belfast","Derry":"Derry City and Strabane","Londonderry":"Derry City and Strabane",
    "Lisburn":"Lisburn and Castlereagh","Newry":"Newry Mourne and Down","Armagh":"Armagh City Banbridge and Craigavon",
    "Antrim":"Antrim and Newtownabbey","Ballymena":"Mid and East Antrim","Coleraine":"Causeway Coast and Glens",
    "Omagh":"Derry City and Strabane","Enniskillen":"Fermanagh and Omagh",
}


def build_gb_location(d):
    if "gb_region" not in d:
        return None
    reg_rows    = [r for r in d["gb_region"]["rows"] if r[0] not in ("(not set)","")]
    city_rows   = [r for r in d["gb_city"]["rows"] if r[0] not in ("(not set)","")]
    cr_rows     = [r for r in d["gb_city_region"]["rows"] if r[0] not in ("(not set)","")]

    # Aggregate sessions by county
    county_sessions = {}
    for r in city_rows:
        county = CITY_TO_COUNTY.get(r[0])
        if county:
            county_sessions[county] = county_sessions.get(county, 0) + int(r[1])
    county_sorted = sorted(county_sessions.items(), key=lambda x: x[1], reverse=True)

    city_map_data = []
    for r in city_rows:
        name = r[0]
        coords = CITY_COORDS.get(name)
        if coords:
            city_map_data.append({
                "name": name,
                "lat": coords[0],
                "lng": coords[1],
                "sessions": int(r[1]),
                "users": int(r[2]),
                "duration": fmt_duration(r[3]),
                "bounce": fmt_pct(r[4]),
                "county": CITY_TO_COUNTY.get(name, ""),
            })

    def region_table():
        return "".join(
            "<tr><td><strong>" + r[0] + "</strong></td><td>" + f"{int(r[1]):,}" + "</td><td>" + f"{int(r[2]):,}" + "</td><td>" + fmt_duration(r[3]) + "</td><td>" + fmt_pct(r[4]) + "</td></tr>"
            for r in reg_rows
        )

    def city_table():
        return "".join(
            "<tr><td>" + r[0] + "</td><td>" + f"{int(r[1]):,}" + "</td><td>" + f"{int(r[2]):,}" + "</td><td>" + fmt_duration(r[3]) + "</td><td>" + fmt_pct(r[4]) + "</td></tr>"
            for r in city_rows[:50]
        )

    def city_region_table():
        return "".join(
            "<tr><td>" + r[0] + "</td><td>" + r[1] + "</td><td>" + f"{int(r[2]):,}" + "</td><td>" + f"{int(r[3]):,}" + "</td><td>" + fmt_duration(r[4]) + "</td></tr>"
            for r in cr_rows[:100]
        )

    def county_table():
        return "".join(
            "<tr><td>" + c[0] + "</td><td>" + f"{c[1]:,}" + "</td></tr>"
            for c in county_sorted
        )

    return {
        "region_table":      region_table(),
        "city_table":        city_table(),
        "city_region_table": city_region_table(),
        "county_table":      county_table(),
        "reg_labels":        [r[0] for r in reg_rows],
        "reg_sessions":      [int(r[1]) for r in reg_rows],
        "city_labels":       [r[0] for r in city_rows[:20]],
        "city_sessions":     [int(r[1]) for r in city_rows[:20]],
        "county_labels":     [c[0] for c in county_sorted[:30]],
        "county_sessions":   [c[1] for c in county_sorted[:30]],
        "county_map":        dict(county_sorted),
        "city_map_data":     city_map_data,
    }


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
        "gb_location":    build_gb_location(d),
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


def gb_location_html(p, pid):
    loc = p.get("gb_location")
    if not loc:
        return ""
    return (
        "<div class=\"section-divider\"><span>GB Location Breakdown</span></div>"
        "<div class=\"card full map-card\"><h2>Interactive Map — Sessions by Location (City Bubbles)</h2>"
        "<div id=\"gbMap_" + pid + "\" class=\"gb-map\"></div>"
        "<div class=\"map-legend\" id=\"legend_" + pid + "\"></div>"
        "</div>"
        "<div class=\"card full map-card\"><h2>Interactive Map — Sessions by County (Choropleth)</h2>"
        "<div id=\"gbCountyMap_" + pid + "\" class=\"gb-map\"></div>"
        "<div class=\"map-legend\" id=\"countyLegend_" + pid + "\"></div>"
        "</div>"
        "<div class=\"grid grid-2\">"
        "<div class=\"card\"><h2>Sessions by Region</h2><canvas id=\"regChart_" + pid + "\" height=\"160\"></canvas></div>"
        "<div class=\"card\"><h2>Top 20 Cities</h2><canvas id=\"cityChart_" + pid + "\" height=\"160\"></canvas></div>"
        "</div>"
        "<div class=\"card full\"><h2>Sessions by County (Top 30)</h2><canvas id=\"countyChart_" + pid + "\" height=\"200\"></canvas></div>"
        "<div class=\"card full\"><h2>UK Regions</h2>"
        "<table><thead><tr><th>Region</th><th>Sessions</th><th>Users</th><th>Avg Duration</th><th>Bounce Rate</th></tr></thead>"
        "<tbody>" + loc["region_table"] + "</tbody></table></div>"
        "<div class=\"card full\"><h2>Cities (Top 50)</h2>"
        "<table><thead><tr><th>City</th><th>Sessions</th><th>Users</th><th>Avg Duration</th><th>Bounce Rate</th></tr></thead>"
        "<tbody>" + loc["city_table"] + "</tbody></table></div>"
        "<div class=\"card full\"><h2>City + Region (Top 100)</h2>"
        "<table><thead><tr><th>City</th><th>Region</th><th>Sessions</th><th>Users</th><th>Avg Duration</th></tr></thead>"
        "<tbody>" + loc["city_region_table"] + "</tbody></table></div>"
        "<div class=\"card full\"><h2>Sessions by County</h2>"
        "<table><thead><tr><th>County / Area</th><th>Sessions</th></tr></thead>"
        "<tbody>" + loc["county_table"] + "</tbody></table></div>"
    )


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
        + gb_location_html(p, pid) +
        "</div>"
    )


def data_vars(p, pid):
    lines = []
    for key, val in p["data"].items():
        lines.append("const " + key + "_" + pid + " = " + json.dumps(val) + ";")
    loc = p.get("gb_location")
    if loc:
        lines.append("const reg_labels_" + pid + " = " + json.dumps(loc["reg_labels"]) + ";")
        lines.append("const reg_sessions_" + pid + " = " + json.dumps(loc["reg_sessions"]) + ";")
        lines.append("const city_labels_" + pid + " = " + json.dumps(loc["city_labels"]) + ";")
        lines.append("const city_sessions_" + pid + " = " + json.dumps(loc["city_sessions"]) + ";")
        lines.append("const city_map_data_" + pid + " = " + json.dumps(loc["city_map_data"]) + ";")
        lines.append("const county_labels_" + pid + " = " + json.dumps(loc["county_labels"]) + ";")
        lines.append("const county_sessions_" + pid + " = " + json.dumps(loc["county_sessions"]) + ";")
        lines.append("const county_map_" + pid + " = " + json.dumps(loc["county_map"]) + ";")
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
  if(typeof reg_labels_{p}!=='undefined'&&reg_labels_{p}.length) IC('regChart_{p}',{type:'bar',data:{labels:reg_labels_{p},datasets:[{label:'Sessions',data:reg_sessions_{p},backgroundColor:COLORS,borderRadius:4}]},options:{indexAxis:'y',plugins:{legend:{display:false}},scales:{x:{ticks:{color:'#9ca3af'},grid:{color:'#f3f4f6'}},y:{ticks:{color:'#374151'},grid:{display:false}}}}});
  if(typeof city_labels_{p}!=='undefined'&&city_labels_{p}.length) IC('cityChart_{p}',{type:'bar',data:{labels:city_labels_{p},datasets:[{label:'Sessions',data:city_sessions_{p},backgroundColor:COLORS,borderRadius:4}]},options:{indexAxis:'y',plugins:{legend:{display:false}},scales:{x:{ticks:{color:'#9ca3af'},grid:{color:'#f3f4f6'}},y:{ticks:{color:'#374151'},grid:{display:false}}}}});
  if(typeof county_labels_{p}!=='undefined'&&county_labels_{p}.length) IC('countyChart_{p}',{type:'bar',data:{labels:county_labels_{p},datasets:[{label:'Sessions',data:county_sessions_{p},backgroundColor:COLORS.concat(COLORS).concat(COLORS),borderRadius:4}]},options:{indexAxis:'y',plugins:{legend:{display:false}},scales:{x:{ticks:{color:'#9ca3af'},grid:{color:'#f3f4f6'}},y:{ticks:{color:'#374151',font:{size:11}},grid:{display:false}}}}});
  if(typeof city_map_data_{p}!=='undefined') initGBMap('{p}', city_map_data_{p}, typeof county_map_{p}!=='undefined'?county_map_{p}:{});
  if(typeof county_map_{p}!=='undefined') initCountyMap('{p}', county_map_{p});
""".replace("{p}", pid)


html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>GA4 Dashboard — food-mag.co.uk</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
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
  .section-divider{display:flex;align-items:center;gap:12px;margin:28px 0 16px;color:#6b7280;font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:0.06em}
  .section-divider::before,.section-divider::after{content:'';flex:1;height:1px;background:#e5e7eb}
  .gb-map{height:580px;border-radius:8px;overflow:hidden;border:1px solid #e5e7eb}
  .map-legend{display:flex;flex-wrap:wrap;gap:12px;margin-top:12px;font-size:12px;color:#6b7280;align-items:center}
  .map-legend-item{display:flex;align-items:center;gap:6px}
  .map-legend-dot{border-radius:50%;display:inline-block}
  .county-tip{background:#fff;border:1px solid #e5e7eb;border-radius:6px;padding:6px 10px;font-size:12px;color:#374151;box-shadow:0 2px 8px rgba(0,0,0,0.08)}
  .leaflet-popup-content-wrapper{border-radius:8px!important;box-shadow:0 4px 16px rgba(0,0,0,0.12)!important;border:1px solid #e5e7eb!important}
  .leaflet-popup-content{margin:12px 16px!important;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif!important;font-size:13px!important}
  .map-popup-title{font-weight:700;font-size:14px;color:#111827;margin-bottom:8px}
  .map-popup-grid{display:grid;grid-template-columns:1fr 1fr;gap:4px 16px}
  .map-popup-label{color:#9ca3af;font-size:11px;text-transform:uppercase;letter-spacing:0.04em}
  .map-popup-val{color:#111827;font-weight:600}
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

const _maps = {};
function initGBMap(pid, cityData, countyData) {
  if (_maps[pid]) return;
  const el = document.getElementById('gbMap_' + pid);
  if (!el) return;

  const map = L.map('gbMap_' + pid, {zoomControl:true, scrollWheelZoom:false}).setView([54.4, -3.2], 6);
  _maps[pid] = map;

  L.tileLayer('https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png', {
    attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/">CARTO</a>',
    maxZoom:13
  }).addTo(map);

  const maxCounty = Math.max(1, ...Object.values(countyData));
  function countyColor(name) {
    const s = countyData[name] || 0;
    const t = s / maxCounty;
    if (t > 0.6) return '#312e81';
    if (t > 0.3) return '#4338ca';
    if (t > 0.1) return '#6366f1';
    if (t > 0.03) return '#a5b4fc';
    if (s > 0) return '#e0e7ff';
    return '#f8fafc';
  }
  function countyOpacity(name) { return countyData[name] ? 0.75 : 0.15; }

  function normName(s) { return s ? s.toLowerCase().replace(/[^a-z0-9]/g,'') : ''; }
  function ladDisplayName(props) {
    return props['LAD13NM'] || props['LGDNAME'] || Object.values(props||{})[0] || '';
  }
  function findCountySessions(props) {
    // London boroughs: LAD13CD starts E09 — attribute all to "London" entry
    if (props['LAD13CD'] && props['LAD13CD'].startsWith('E09') && countyData['London']) {
      return {name:'London', sessions:countyData['London']};
    }
    const keys = ['LAD13NM','LGDNAME','CTY17NM','ctyua19nm','ctyua22nm','LAD17NM','lad17nm','lgdname','lad_name','name','NAME'];
    for (const k of keys) { if (props[k]) { const n = props[k]; const v = countyData[n]; if (v) return {name:n,sessions:v}; } }
    for (const k of keys) {
      if (props[k]) {
        const pn = normName(props[k]);
        for (const [cn, cs] of Object.entries(countyData)) { if (normName(cn) === pn) return {name:cn,sessions:cs}; }
      }
    }
    return {name:'',sessions:0};
  }

  // UK county + country boundaries from ONS/martinjc
  const boundaryUrls = [
    'https://raw.githubusercontent.com/martinjc/UK-GeoJSON/master/json/administrative/eng/topo_lad.json',
    'https://raw.githubusercontent.com/martinjc/UK-GeoJSON/master/json/administrative/sco/topo_lad.json',
    'https://raw.githubusercontent.com/martinjc/UK-GeoJSON/master/json/administrative/wal/topo_lad.json',
    'https://raw.githubusercontent.com/martinjc/UK-GeoJSON/master/json/administrative/ni/topo_lgd.json'
  ];

  boundaryUrls.forEach(url => {
    fetch(url)
      .then(r => r.json())
      .then(topo => {
        const objKey = Object.keys(topo.objects)[0];
        const features = [];
        topo.objects[objKey].geometries.forEach(geom => { features.push(convertTopo(topo, geom)); });
        const gj = {type:'FeatureCollection', features: features.filter(Boolean)};
        L.geoJSON(gj, {
          style: f => {
            const {name,sessions} = findCountySessions(f.properties||{});
            return {color:'#6366f1', weight:0.8, fillColor:countyColor(name), fillOpacity:countyOpacity(name), opacity:0.7};
          },
          onEachFeature: (f, layer) => {
            const {name,sessions} = findCountySessions(f.properties||{});
            const displayName = name || ladDisplayName(f.properties||{}) || 'Unknown';
            layer.bindTooltip(
              '<strong>' + displayName + '</strong>' + (sessions ? '<br>Sessions: ' + sessions.toLocaleString() : '<br>No data'),
              {sticky:true, className:'county-tip'}
            );
            layer.on('mouseover', e => e.target.setStyle({weight:2,fillOpacity:0.9}));
            layer.on('mouseout', e => e.target.setStyle({weight:0.8,fillColor:countyColor(name),fillOpacity:countyOpacity(name)}));
          }
        }).addTo(map);
      }).catch(()=>{});
  });

  // Simple TopoJSON geometry converter (arcs → coordinates)
  function convertTopo(topo, geom) {
    try {
      const scale = topo.transform ? topo.transform.scale : [1,1];
      const translate = topo.transform ? topo.transform.translate : [0,0];
      function decodeArc(arc) {
        let x=0, y=0;
        return arc.map(([dx,dy]) => { x+=dx; y+=dy; return [x*scale[0]+translate[0], y*scale[1]+translate[1]]; });
      }
      function arcToCoords(arcIdx) {
        const reversed = arcIdx < 0;
        const pts = decodeArc(topo.arcs[reversed ? ~arcIdx : arcIdx]);
        return reversed ? pts.slice().reverse() : pts;
      }
      function ringCoords(ring) { return ring.flatMap(arcToCoords); }

      let coords;
      if (geom.type === 'Polygon') {
        coords = geom.arcs.map(ring => ringCoords(ring).map(([lng,lat]) => [lat,lng]));
        return {type:'Feature', properties: geom.properties||{}, geometry:{type:'Polygon', coordinates: geom.arcs.map(ring => ringCoords(ring))}};
      } else if (geom.type === 'MultiPolygon') {
        return {type:'Feature', properties: geom.properties||{}, geometry:{type:'MultiPolygon', coordinates: geom.arcs.map(poly => poly.map(ring => ringCoords(ring)))}};
      }
    } catch(e) {}
    return null;
  }

  // Bubble markers sized by sessions
  const maxSessions = Math.max(...cityData.map(c => c.sessions));
  const breaks = [
    {min:0, label:'< 500', color:'#c7d2fe', r:5},
    {min:500, label:'500–1k', color:'#818cf8', r:8},
    {min:1000, label:'1k–5k', color:'#6366f1', r:12},
    {min:5000, label:'5k–10k', color:'#4338ca', r:18},
    {min:10000, label:'10k+', color:'#312e81', r:24},
  ];

  function getStyle(sessions) {
    for (let i = breaks.length-1; i >= 0; i--) {
      if (sessions >= breaks[i].min) return breaks[i];
    }
    return breaks[0];
  }

  cityData.forEach(city => {
    const style = getStyle(city.sessions);
    L.circleMarker([city.lat, city.lng], {
      radius: style.r,
      fillColor: style.color,
      color: '#fff',
      weight: 1.5,
      fillOpacity: 0.85
    }).bindPopup(
      '<div class="map-popup-title">' + city.name + '</div>' +
      '<div class="map-popup-grid">' +
      '<div class="map-popup-label">Sessions</div><div class="map-popup-val">' + city.sessions.toLocaleString() + '</div>' +
      '<div class="map-popup-label">Users</div><div class="map-popup-val">' + city.users.toLocaleString() + '</div>' +
      '<div class="map-popup-label">Avg Duration</div><div class="map-popup-val">' + city.duration + '</div>' +
      '<div class="map-popup-label">Bounce Rate</div><div class="map-popup-val">' + city.bounce + '</div>' +
      '</div>',
      {maxWidth:220}
    ).addTo(map);
  });

  // Legend
  const leg = document.getElementById('legend_' + pid);
  if (leg) {
    const choroplethBreaks = [{color:'#e0e7ff',label:'Low'},{color:'#a5b4fc',label:''},{color:'#6366f1',label:''},{color:'#4338ca',label:''},{color:'#312e81',label:'High'}];
    leg.innerHTML =
      '<span style="color:#374151;font-weight:600;margin-right:4px">City bubbles:</span>' +
      breaks.map(b =>
        '<span class="map-legend-item"><span class="map-legend-dot" style="width:' + (b.r*2) + 'px;height:' + (b.r*2) + 'px;background:' + b.color + '"></span>' + b.label + '</span>'
      ).join('') +
      '<span style="margin-left:16px;color:#374151;font-weight:600;margin-right:4px">County fill:</span>' +
      choroplethBreaks.map(b =>
        '<span class="map-legend-item"><span style="width:18px;height:12px;background:' + b.color + ';border:1px solid #c7d2fe;border-radius:2px;display:inline-block"></span>' + (b.label ? b.label : '') + '</span>'
      ).join('');
  }

  setTimeout(() => map.invalidateSize(), 100);
}

const _countyMaps = {};
function initCountyMap(pid, countyData) {
  if (_countyMaps[pid]) return;
  const el = document.getElementById('gbCountyMap_' + pid);
  if (!el) return;

  const map = L.map('gbCountyMap_' + pid, {zoomControl:true, scrollWheelZoom:false}).setView([54.4, -3.2], 6);
  _countyMaps[pid] = map;

  L.tileLayer('https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png', {
    attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/">CARTO</a>',
    maxZoom:13
  }).addTo(map);

  const maxVal = Math.max(1, ...Object.values(countyData));
  const breaks = [
    {thresh:0.5, fill:'#1e1b4b', label:'Very high'},
    {thresh:0.25, fill:'#312e81', label:'High'},
    {thresh:0.1,  fill:'#4338ca', label:'Medium-high'},
    {thresh:0.04, fill:'#6366f1', label:'Medium'},
    {thresh:0.01, fill:'#a5b4fc', label:'Low'},
    {thresh:0,    fill:'#e0e7ff', label:'Very low'},
  ];

  function getColor(name) {
    const s = countyData[name] || 0;
    if (!s) return '#f1f5f9';
    const t = s / maxVal;
    for (const b of breaks) { if (t >= b.thresh) return b.fill; }
    return '#e0e7ff';
  }

  function normName(s) { return s ? s.toLowerCase().replace(/[^a-z0-9]/g,'') : ''; }
  function ladName(props) { return props['LAD13NM'] || props['LGDNAME'] || Object.values(props||{})[0] || 'Unknown'; }
  function findMatch(props) {
    // London boroughs: LAD13CD starts E09 — attribute all to "London" entry
    if (props['LAD13CD'] && props['LAD13CD'].startsWith('E09') && countyData['London']) {
      return {name:'London', sessions:countyData['London']};
    }
    const keys = ['LAD13NM','LGDNAME','CTY17NM','ctyua19nm','ctyua22nm','LAD17NM','lad17nm','lgdname','lad_name','name','NAME'];
    for (const k of keys) { if (props[k]) { const v = countyData[props[k]]; if (v !== undefined) return {name:props[k], sessions:v}; } }
    for (const k of keys) {
      if (props[k]) {
        const pn = normName(props[k]);
        for (const [cn, cs] of Object.entries(countyData)) { if (normName(cn) === pn) return {name:cn, sessions:cs}; }
      }
    }
    return {name: ladName(props), sessions: 0};
  }

  function topoConvert(topo, geom) {
    try {
      const scale = topo.transform ? topo.transform.scale : [1,1];
      const translate = topo.transform ? topo.transform.translate : [0,0];
      function decodeArc(arc) { let x=0,y=0; return arc.map(([dx,dy])=>{x+=dx;y+=dy;return[x*scale[0]+translate[0],y*scale[1]+translate[1]];}); }
      function arcCoords(i) { const r=i<0; const pts=decodeArc(topo.arcs[r?~i:i]); return r?pts.slice().reverse():pts; }
      function ring(r) { return r.flatMap(arcCoords); }
      if (geom.type==='Polygon') return {type:'Feature',properties:geom.properties||{},geometry:{type:'Polygon',coordinates:geom.arcs.map(ring)}};
      if (geom.type==='MultiPolygon') return {type:'Feature',properties:geom.properties||{},geometry:{type:'MultiPolygon',coordinates:geom.arcs.map(p=>p.map(ring))}};
    } catch(e) {}
    return null;
  }

  const urls = [
    'https://raw.githubusercontent.com/martinjc/UK-GeoJSON/master/json/administrative/eng/topo_lad.json',
    'https://raw.githubusercontent.com/martinjc/UK-GeoJSON/master/json/administrative/sco/topo_lad.json',
    'https://raw.githubusercontent.com/martinjc/UK-GeoJSON/master/json/administrative/wal/topo_lad.json',
    'https://raw.githubusercontent.com/martinjc/UK-GeoJSON/master/json/administrative/ni/topo_lgd.json'
  ];

  urls.forEach(url => {
    fetch(url).then(r=>r.json()).then(topo => {
      const key = Object.keys(topo.objects)[0];
      const features = topo.objects[key].geometries.map(g=>topoConvert(topo,g)).filter(Boolean);
      L.geoJSON({type:'FeatureCollection',features}, {
        style: f => {
          const {name} = findMatch(f.properties||{});
          return {color:'#6366f1', weight:1, fillColor:getColor(name), fillOpacity:0.8, opacity:0.6};
        },
        onEachFeature: (f, layer) => {
          const {name, sessions} = findMatch(f.properties||{});
          layer.bindTooltip(
            '<strong>' + name + '</strong><br>' + (sessions ? sessions.toLocaleString() + ' sessions' : 'No data'),
            {sticky:true, className:'county-tip'}
          );
          layer.on('mouseover', e => e.target.setStyle({weight:2, fillOpacity:0.95}));
          layer.on('mouseout', e => { const {name:n}=findMatch(f.properties||{}); e.target.setStyle({weight:1,fillColor:getColor(n),fillOpacity:0.8}); });
        }
      }).addTo(map);
    }).catch(()=>{});
  });

  // City labels overlay (no bubbles, just place name dots)
  L.tileLayer('https://{s}.basemaps.cartocdn.com/light_only_labels/{z}/{x}/{y}{r}.png', {
    pane:'shadowPane', opacity:1, maxZoom:13
  }).addTo(map);

  // Choropleth legend
  const leg = document.getElementById('countyLegend_' + pid);
  if (leg) {
    leg.innerHTML = '<span style="color:#374151;font-weight:600;margin-right:8px">Sessions per county:</span>' +
      breaks.map(b =>
        '<span class="map-legend-item"><span style="width:18px;height:12px;background:' + b.fill + ';border:1px solid rgba(99,102,241,0.3);border-radius:2px;display:inline-block"></span> ' + b.label + '</span>'
      ).join('') +
      '<span class="map-legend-item"><span style="width:18px;height:12px;background:#f1f5f9;border:1px solid #e5e7eb;border-radius:2px;display:inline-block"></span> No data</span>';
  }

  setTimeout(() => map.invalidateSize(), 100);
}
</script>
</body>
</html>"""

out = os.path.join(os.path.dirname(__file__), "index.html")
with open(out, "w") as f:
    f.write(html)

print("Dashboard written.")
