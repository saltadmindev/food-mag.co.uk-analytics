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
    # London
    "London":"Greater London",
    # West Midlands
    "Birmingham":"West Midlands","Wolverhampton":"West Midlands","Coventry":"West Midlands",
    "Walsall":"West Midlands","Sandwell":"West Midlands","Dudley":"West Midlands","Solihull":"West Midlands",
    # Greater Manchester
    "Manchester":"Greater Manchester","Salford":"Greater Manchester","Bolton":"Greater Manchester",
    "Oldham":"Greater Manchester","Rochdale":"Greater Manchester","Stockport":"Greater Manchester","Wigan":"Greater Manchester",
    "Bury":"Greater Manchester","Tameside":"Greater Manchester","Trafford":"Greater Manchester",
    # West Yorkshire
    "Leeds":"West Yorkshire","Bradford":"West Yorkshire","Huddersfield":"West Yorkshire","Wakefield":"West Yorkshire","Halifax":"West Yorkshire",
    # South Yorkshire
    "Sheffield":"South Yorkshire","Doncaster":"South Yorkshire","Barnsley":"South Yorkshire","Rotherham":"South Yorkshire",
    # Merseyside
    "Liverpool":"Merseyside","Birkenhead":"Merseyside","Southport":"Merseyside","St Helens":"Merseyside","Knowsley":"Merseyside",
    # Devon
    "Plymouth":"Devon","Exeter":"Devon","Torquay":"Devon","Brixham":"Devon",
    "Barnstaple":"Devon","Tavistock":"Devon","Newton Abbot":"Devon",
    "Exmouth":"Devon","Honiton":"Devon","Sidmouth":"Devon","Crediton":"Devon",
    # Bristol / South West
    "Bristol":"Somerset","Bath":"Somerset","Weston-super-Mare":"Somerset",
    "Taunton":"Somerset","Yeovil":"Somerset","Bridgwater":"Somerset","Frome":"Somerset",
    "Gloucester":"Gloucestershire","Cheltenham":"Gloucestershire","Cirencester":"Gloucestershire","Stroud":"Gloucestershire",
    "Swindon":"Wiltshire","Salisbury":"Wiltshire","Chippenham":"Wiltshire","Trowbridge":"Wiltshire",
    "Truro":"Cornwall","Newquay":"Cornwall",
    # Norfolk / Suffolk / Essex
    "Norwich":"Norfolk","Great Yarmouth":"Norfolk",
    "Ipswich":"Suffolk","Bury St Edmunds":"Suffolk","Lowestoft":"Suffolk","Newmarket":"Suffolk","Haverhill":"Suffolk",
    "Colchester":"Essex","Chelmsford":"Essex","Basildon":"Essex","Southend-on-Sea":"Essex","Harlow":"Essex",
    # Tyne & Wear
    "Newcastle upon Tyne":"Tyne and Wear","Newcastle":"Tyne and Wear","Sunderland":"Tyne and Wear","Gateshead":"Tyne and Wear",
    # East Midlands
    "Nottingham":"Nottinghamshire","Leicester":"Leicestershire","Derby":"Derbyshire",
    "Northampton":"Northamptonshire","Peterborough":"Cambridgeshire","Cambridge":"Cambridgeshire",
    "Lincoln":"Lincolnshire",
    # Yorkshire
    "York":"North Yorkshire","Middlesbrough":"Cleveland",
    "Hull":"North Yorkshire","Kingston upon Hull":"North Yorkshire",
    # Lancashire
    "Preston":"Lancashire","Blackpool":"Lancashire","Blackburn":"Lancashire","Lancaster":"Lancashire",
    # Cheshire
    "Chester":"Cheshire","Warrington":"Cheshire",
    # North East
    "Durham":"Durham","Carlisle":"Cumbria",
    # Beds / Herts / Bucks
    "Luton":"Bedfordshire","Bedford":"Bedfordshire","Dunstable":"Bedfordshire",
    "Watford":"Hertfordshire","St Albans":"Hertfordshire","Stevenage":"Hertfordshire",
    "Hemel Hempstead":"Hertfordshire","Hatfield":"Hertfordshire","Welwyn Garden City":"Hertfordshire","Letchworth":"Hertfordshire","Hitchin":"Hertfordshire",
    "Milton Keynes":"Buckinghamshire","Aylesbury":"Buckinghamshire","High Wycombe":"Buckinghamshire",
    # Berkshire / Oxfordshire
    "Reading":"West Berkshire","Slough":"West Berkshire","Windsor":"West Berkshire","Maidenhead":"West Berkshire",
    "Wokingham":"West Berkshire","Bracknell":"West Berkshire","Newbury":"West Berkshire",
    "Oxford":"Oxfordshire","Banbury":"Oxfordshire","Bicester":"Oxfordshire","Witney":"Oxfordshire","Abingdon":"Oxfordshire",
    # Hampshire / Surrey / Kent / Sussex
    "Southampton":"Hampshire","Portsmouth":"Hampshire","Basingstoke":"Hampshire",
    "Winchester":"Hampshire","Aldershot":"Hampshire","Andover":"Hampshire",
    "Guildford":"Surrey","Woking":"Surrey","Crawley":"West Sussex","Worthing":"West Sussex",
    "Brighton":"East Sussex","Brighton and Hove":"East Sussex","Eastbourne":"East Sussex","Hastings":"East Sussex",
    "Canterbury":"Kent","Maidstone":"Kent","Medway":"Kent","Folkestone":"Kent",
    # West Midlands non-metro
    "Worcester":"Worcestershire","Hereford":"Worcestershire","Shrewsbury":"Shropshire","Telford":"Shropshire",
    "Stoke-on-Trent":"Staffordshire","Burton upon Trent":"Staffordshire","Stafford":"Staffordshire",
    # Scotland
    "Edinburgh":"City of Edinburgh","Glasgow":"Glasgow City","Aberdeen":"Aberdeen City",
    "Dundee":"Dundee City","Perth":"Perth and Kinross","Stirling":"Stirling","Inverness":"Highland",
    "Kilmarnock":"East Ayrshire","Ayr":"South Ayrshire","Paisley":"Renfrewshire",
    "Motherwell":"North Lanarkshire","Hamilton":"South Lanarkshire","Livingston":"West Lothian",
    "Falkirk":"Falkirk","Dunfermline":"Fife","Kirkcaldy":"Fife","Glenrothes":"Fife",
    "Dumfries":"Dumfries and Galloway","Oban":"Argyll and Bute","Fort William":"Highland",
    # Wales
    "Cardiff":"Cardiff","Swansea":"Swansea","Newport":"Newport","Wrexham":"Wrexham",
    "Barry":"Vale of Glamorgan","Bridgend":"Bridgend","Neath":"Neath Port Talbot",
    "Llanelli":"Carmarthenshire","Carmarthen":"Carmarthenshire","Merthyr Tydfil":"Merthyr Tydfil",
    "Pontypridd":"Rhondda Cynon Taf","Caerphilly":"Caerphilly","Cwmbran":"Torfaen",
    "Aberystwyth":"Ceredigion","Llandudno":"Conwy","Rhyl":"Denbighshire","Colwyn Bay":"Conwy",
    # Northern Ireland
    "Belfast":"Belfast","Derry":"Derry City and Strabane","Londonderry":"Derry City and Strabane",
    "Lisburn":"Lisburn and Castlereagh","Newry":"Newry Mourne and Down","Armagh":"Armagh City Banbridge and Craigavon",
    "Antrim":"Antrim and Newtownabbey","Ballymena":"Mid and East Antrim","Coleraine":"Causeway Coast and Glens",
    "Omagh":"Derry City and Strabane","Enniskillen":"Fermanagh and Omagh",
}

# Maps GA4 city names directly to their LAD13NM / LGDNAME in the TopoJSON
CITY_TO_LAD = {
    # Greater London — all 33 boroughs share the "London" city total (see LONDON_LADS)
    "London": "_LONDON",
    # South West England
    "Plymouth":"Plymouth","Bristol":"Bristol, City of","Bath":"Bath and North East Somerset",
    "Exeter":"Exeter","Torquay":"Torbay","Brixham":"Torbay","Swindon":"Swindon",
    "Gloucester":"Gloucester","Cheltenham":"Cheltenham","Salisbury":"Wiltshire",
    "Taunton":"Taunton Deane","Weston-super-Mare":"North Somerset","Yeovil":"South Somerset",
    "Truro":"Cornwall","Newquay":"Cornwall","Newton Abbot":"Teignbridge",
    "Exmouth":"East Devon","Honiton":"East Devon","Sidmouth":"East Devon",
    "Barnstaple":"North Devon","Tavistock":"West Devon","Crediton":"Mid Devon",
    "Frome":"Mendip","Chippenham":"Wiltshire","Trowbridge":"Wiltshire",
    "Cirencester":"Cotswold","Stroud":"Stroud","Bridgwater":"Sedgemoor",
    # West Midlands
    "Birmingham":"Birmingham","Wolverhampton":"Wolverhampton","Coventry":"Coventry",
    "Walsall":"Walsall","Dudley":"Dudley","Sandwell":"Sandwell","Solihull":"Solihull",
    "Stoke-on-Trent":"Stoke-on-Trent","Telford":"Telford and Wrekin",
    "Worcester":"Worcester","Hereford":"Herefordshire, County of","Shrewsbury":"Shropshire",
    # East Midlands
    "Leicester":"Leicester","Nottingham":"Nottingham","Derby":"Derby",
    "Northampton":"Northampton","Lincoln":"Lincoln",
    # Yorkshire
    "Leeds":"Leeds","Sheffield":"Sheffield","Bradford":"Bradford",
    "Hull":"Kingston upon Hull, City of","Kingston upon Hull":"Kingston upon Hull, City of",
    "York":"York","Huddersfield":"Kirklees","Doncaster":"Doncaster",
    "Barnsley":"Barnsley","Wakefield":"Wakefield","Rotherham":"Rotherham",
    # North West England
    "Manchester":"Manchester","Liverpool":"Liverpool","Salford":"Salford",
    "Bolton":"Bolton","Oldham":"Oldham","Rochdale":"Rochdale","Stockport":"Stockport",
    "Wigan":"Wigan","Blackpool":"Blackpool","Preston":"Preston",
    "Blackburn":"Blackburn with Darwen","Lancaster":"Lancaster",
    "Chester":"Cheshire West and Chester","Warrington":"Warrington",
    # North East England
    "Newcastle upon Tyne":"Newcastle upon Tyne","Newcastle":"Newcastle upon Tyne",
    "Sunderland":"Sunderland","Middlesbrough":"Middlesbrough","Durham":"County Durham",
    "Carlisle":"Carlisle","Hartlepool":"Hartlepool","Darlington":"Darlington",
    # East of England
    "Norwich":"Norwich","Cambridge":"Cambridge","Peterborough":"Peterborough",
    "Ipswich":"Ipswich","Luton":"Luton","Bedford":"Bedford","Chelmsford":"Chelmsford",
    "Colchester":"Colchester","Southend-on-Sea":"Southend-on-Sea",
    "Great Yarmouth":"Great Yarmouth","Lowestoft":"Waveney",
    "Bury St Edmunds":"St Edmundsbury","Haverhill":"St Edmundsbury",
    "Watford":"Watford","Stevenage":"Stevenage","Hemel Hempstead":"Dacorum",
    "St Albans":"St Albans","Harlow":"Harlow",
    "Huntingdon":"Huntingdonshire","St Neots":"Huntingdonshire","Wisbech":"Fenland",
    "Newmarket":"Forest Heath",
    # South East England
    "Brighton":"Brighton and Hove","Brighton and Hove":"Brighton and Hove",
    "Southampton":"Southampton","Portsmouth":"Portsmouth","Reading":"Reading",
    "Slough":"Slough","Medway":"Medway","Guildford":"Guildford","Woking":"Woking",
    "Bournemouth":"Bournemouth","Eastbourne":"Eastbourne","Hastings":"Hastings",
    "Canterbury":"Canterbury","Maidstone":"Maidstone",
    "Basingstoke":"Basingstoke and Deane","Winchester":"Winchester",
    "Worthing":"Worthing","Crawley":"Crawley","Aldershot":"Rushmoor",
    "Farnham":"Waverley","Aylesbury":"Aylesbury Vale","High Wycombe":"Wycombe",
    "Milton Keynes":"Milton Keynes","Oxford":"Oxford","Banbury":"Cherwell",
    "Wokingham":"Wokingham","Bracknell":"Bracknell Forest",
    "Windsor":"Windsor and Maidenhead","Maidenhead":"Windsor and Maidenhead",
    "Newbury":"West Berkshire",
    # Wales
    "Cardiff":"Cardiff","Swansea":"Swansea","Newport":"Newport","Wrexham":"Wrexham",
    "Barry":"Vale of Glamorgan","Bridgend":"Bridgend","Merthyr Tydfil":"Merthyr Tydfil",
    "Pontypridd":"Rhondda Cynon Taf","Llanelli":"Carmarthenshire",
    "Carmarthen":"Carmarthenshire","Caerphilly":"Caerphilly","Cwmbran":"Torfaen",
    "Neath":"Neath Port Talbot","Aberystwyth":"Ceredigion",
    "Colwyn Bay":"Conwy","Llandudno":"Conwy","Rhyl":"Denbighshire",
    # Scotland
    "Edinburgh":"City of Edinburgh","Glasgow":"Glasgow City","Aberdeen":"Aberdeen City",
    "Dundee":"Dundee City","Inverness":"Highland","Perth":"Perth and Kinross",
    "Stirling":"Stirling","Falkirk":"Falkirk","Dunfermline":"Fife","Kirkcaldy":"Fife",
    "Hamilton":"South Lanarkshire","Livingston":"West Lothian",
    "Kilmarnock":"East Ayrshire","Ayr":"South Ayrshire","Paisley":"Renfrewshire",
    "Motherwell":"North Lanarkshire","Dumfries":"Dumfries and Galloway",
    # Northern Ireland (LGDNAME values from ni/topo_lgd.json — no commas in names)
    "Belfast":"Belfast","Derry":"Derry and Strabane","Londonderry":"Derry and Strabane",
    "Lisburn":"Lisburn and Castlereagh","Newry":"Newry Mourne and Down",
    "Antrim":"Antrim and Newtownabbey","Ballymena":"Mid and East Antrim",
    "Coleraine":"Causeway Coast and Glens",
    "Omagh":"Fermanagh and Omagh","Enniskillen":"Fermanagh and Omagh",
}

LONDON_LADS = [
    "City of London","Barking and Dagenham","Barnet","Bexley","Brent","Bromley",
    "Camden","Croydon","Ealing","Enfield","Greenwich","Hackney",
    "Hammersmith and Fulham","Haringey","Harrow","Havering","Hillingdon",
    "Hounslow","Islington","Kensington and Chelsea","Kingston upon Thames",
    "Lambeth","Lewisham","Merton","Newham","Redbridge","Richmond upon Thames",
    "Southwark","Sutton","Tower Hamlets","Waltham Forest","Wandsworth","Westminster",
]

# Maps every LAD13NM (England/Wales/Scotland) and LGDNAME (NI) to its traditional county
LAD_TO_COUNTY = {
    # === GREATER LONDON (all 33 boroughs) ===
    "City of London":"Greater London","Barking and Dagenham":"Greater London","Barnet":"Greater London",
    "Bexley":"Greater London","Brent":"Greater London","Bromley":"Greater London","Camden":"Greater London",
    "Croydon":"Greater London","Ealing":"Greater London","Enfield":"Greater London","Greenwich":"Greater London",
    "Hackney":"Greater London","Hammersmith and Fulham":"Greater London","Haringey":"Greater London",
    "Harrow":"Greater London","Havering":"Greater London","Hillingdon":"Greater London","Hounslow":"Greater London",
    "Islington":"Greater London","Kensington and Chelsea":"Greater London","Kingston upon Thames":"Greater London",
    "Lambeth":"Greater London","Lewisham":"Greater London","Merton":"Greater London","Newham":"Greater London",
    "Redbridge":"Greater London","Richmond upon Thames":"Greater London","Southwark":"Greater London",
    "Sutton":"Greater London","Tower Hamlets":"Greater London","Waltham Forest":"Greater London",
    "Wandsworth":"Greater London","Westminster":"Greater London",
    # === TYNE AND WEAR ===
    "Newcastle upon Tyne":"Tyne and Wear","Gateshead":"Tyne and Wear","Sunderland":"Tyne and Wear",
    "South Tyneside":"Tyne and Wear","North Tyneside":"Tyne and Wear",
    # === NORTHUMBERLAND ===
    "Northumberland":"Northumberland",
    # === DURHAM ===
    "County Durham":"Durham","Darlington":"Durham",
    # === CLEVELAND ===
    "Hartlepool":"Cleveland","Middlesbrough":"Cleveland","Stockton-on-Tees":"Cleveland","Redcar and Cleveland":"Cleveland",
    # === CUMBRIA ===
    "Allerdale":"Cumbria","Barrow-in-Furness":"Cumbria","Carlisle":"Cumbria",
    "Copeland":"Cumbria","Eden":"Cumbria","South Lakeland":"Cumbria",
    # === LANCASHIRE ===
    "Burnley":"Lancashire","Chorley":"Lancashire","Fylde":"Lancashire","Hyndburn":"Lancashire",
    "Lancaster":"Lancashire","Pendle":"Lancashire","Preston":"Lancashire","Ribble Valley":"Lancashire",
    "Rossendale":"Lancashire","South Ribble":"Lancashire","West Lancashire":"Lancashire","Wyre":"Lancashire",
    "Blackburn with Darwen":"Lancashire","Blackpool":"Lancashire",
    # === GREATER MANCHESTER ===
    "Bolton":"Greater Manchester","Bury":"Greater Manchester","Manchester":"Greater Manchester",
    "Oldham":"Greater Manchester","Rochdale":"Greater Manchester","Salford":"Greater Manchester",
    "Stockport":"Greater Manchester","Tameside":"Greater Manchester","Trafford":"Greater Manchester","Wigan":"Greater Manchester",
    # === MERSEYSIDE ===
    "Knowsley":"Merseyside","Liverpool":"Merseyside","Sefton":"Merseyside","St. Helens":"Merseyside","Wirral":"Merseyside",
    # === CHESHIRE ===
    "Cheshire East":"Cheshire","Cheshire West and Chester":"Cheshire","Halton":"Cheshire","Warrington":"Cheshire",
    # === WEST YORKSHIRE ===
    "Bradford":"West Yorkshire","Calderdale":"West Yorkshire","Kirklees":"West Yorkshire",
    "Leeds":"West Yorkshire","Wakefield":"West Yorkshire",
    # === SOUTH YORKSHIRE ===
    "Barnsley":"South Yorkshire","Doncaster":"South Yorkshire","Rotherham":"South Yorkshire","Sheffield":"South Yorkshire",
    # === NORTH YORKSHIRE ===
    "Craven":"North Yorkshire","Hambleton":"North Yorkshire","Harrogate":"North Yorkshire","Richmondshire":"North Yorkshire",
    "Ryedale":"North Yorkshire","Scarborough":"North Yorkshire","Selby":"North Yorkshire","York":"North Yorkshire",
    "East Riding of Yorkshire":"North Yorkshire","Kingston upon Hull, City of":"North Yorkshire",
    # === LINCOLNSHIRE ===
    "Boston":"Lincolnshire","East Lindsey":"Lincolnshire","Lincoln":"Lincolnshire","North Kesteven":"Lincolnshire",
    "South Holland":"Lincolnshire","South Kesteven":"Lincolnshire","West Lindsey":"Lincolnshire",
    "North East Lincolnshire":"Lincolnshire","North Lincolnshire":"Lincolnshire",
    # === NOTTINGHAMSHIRE ===
    "Ashfield":"Nottinghamshire","Bassetlaw":"Nottinghamshire","Broxtowe":"Nottinghamshire","Gedling":"Nottinghamshire",
    "Mansfield":"Nottinghamshire","Newark and Sherwood":"Nottinghamshire","Nottingham":"Nottinghamshire","Rushcliffe":"Nottinghamshire",
    # === DERBYSHIRE ===
    "Amber Valley":"Derbyshire","Bolsover":"Derbyshire","Chesterfield":"Derbyshire","Derby":"Derbyshire",
    "Derbyshire Dales":"Derbyshire","Erewash":"Derbyshire","High Peak":"Derbyshire",
    "North East Derbyshire":"Derbyshire","South Derbyshire":"Derbyshire",
    # === LEICESTERSHIRE ===
    "Blaby":"Leicestershire","Charnwood":"Leicestershire","Harborough":"Leicestershire","Hinckley and Bosworth":"Leicestershire",
    "Leicester":"Leicestershire","Melton":"Leicestershire","North West Leicestershire":"Leicestershire","Oadby and Wigston":"Leicestershire",
    # === NORTHAMPTONSHIRE ===
    "Corby":"Northamptonshire","Daventry":"Northamptonshire","East Northamptonshire":"Northamptonshire",
    "Kettering":"Northamptonshire","Northampton":"Northamptonshire","South Northamptonshire":"Northamptonshire","Wellingborough":"Northamptonshire",
    # === STAFFORDSHIRE ===
    "Cannock Chase":"Staffordshire","East Staffordshire":"Staffordshire","Lichfield":"Staffordshire",
    "Newcastle-under-Lyme":"Staffordshire","South Staffordshire":"Staffordshire","Stafford":"Staffordshire",
    "Staffordshire Moorlands":"Staffordshire","Stoke-on-Trent":"Staffordshire","Tamworth":"Staffordshire",
    # === WEST MIDLANDS ===
    "Birmingham":"West Midlands","Coventry":"West Midlands","Dudley":"West Midlands","Sandwell":"West Midlands",
    "Solihull":"West Midlands","Walsall":"West Midlands","Wolverhampton":"West Midlands",
    # === WARWICKSHIRE ===
    "North Warwickshire":"Warwickshire","Nuneaton and Bedworth":"Warwickshire","Rugby":"Warwickshire",
    "Stratford-on-Avon":"Warwickshire","Warwick":"Warwickshire",
    # === WORCESTERSHIRE ===
    "Bromsgrove":"Worcestershire","Malvern Hills":"Worcestershire","Redditch":"Worcestershire",
    "Worcester":"Worcestershire","Wychavon":"Worcestershire","Wyre Forest":"Worcestershire",
    "Herefordshire, County of":"Worcestershire",
    # === SHROPSHIRE ===
    "Shropshire":"Shropshire","Telford and Wrekin":"Shropshire",
    # === NORFOLK ===
    "Breckland":"Norfolk","Broadland":"Norfolk","Great Yarmouth":"Norfolk","King's Lynn and West Norfolk":"Norfolk",
    "North Norfolk":"Norfolk","Norwich":"Norfolk","South Norfolk":"Norfolk",
    # === SUFFOLK ===
    "Babergh":"Suffolk","Forest Heath":"Suffolk","Ipswich":"Suffolk","Mid Suffolk":"Suffolk",
    "St Edmundsbury":"Suffolk","Suffolk Coastal":"Suffolk","Waveney":"Suffolk",
    # === CAMBRIDGESHIRE ===
    "Cambridge":"Cambridgeshire","East Cambridgeshire":"Cambridgeshire","Fenland":"Cambridgeshire",
    "Huntingdonshire":"Cambridgeshire","Peterborough":"Cambridgeshire","South Cambridgeshire":"Cambridgeshire",
    # === ESSEX ===
    "Basildon":"Essex","Braintree":"Essex","Brentwood":"Essex","Castle Point":"Essex","Chelmsford":"Essex",
    "Colchester":"Essex","Epping Forest":"Essex","Harlow":"Essex","Maldon":"Essex","Rochford":"Essex",
    "Southend-on-Sea":"Essex","Tendring":"Essex","Thurrock":"Essex","Uttlesford":"Essex",
    # === HERTFORDSHIRE ===
    "Broxbourne":"Hertfordshire","Dacorum":"Hertfordshire","East Hertfordshire":"Hertfordshire",
    "Hertsmere":"Hertfordshire","North Hertfordshire":"Hertfordshire","St Albans":"Hertfordshire",
    "Stevenage":"Hertfordshire","Three Rivers":"Hertfordshire","Watford":"Hertfordshire","Welwyn Hatfield":"Hertfordshire",
    # === BEDFORDSHIRE ===
    "Bedford":"Bedfordshire","Central Bedfordshire":"Bedfordshire","Luton":"Bedfordshire",
    # === BUCKINGHAMSHIRE ===
    "Aylesbury Vale":"Buckinghamshire","Chiltern":"Buckinghamshire","Milton Keynes":"Buckinghamshire",
    "South Bucks":"Buckinghamshire","Wycombe":"Buckinghamshire",
    # === OXFORDSHIRE ===
    "Cherwell":"Oxfordshire","Oxford":"Oxfordshire","South Oxfordshire":"Oxfordshire",
    "Vale of White Horse":"Oxfordshire","West Oxfordshire":"Oxfordshire",
    # === WEST BERKSHIRE (all Berkshire unitaries) ===
    "Bracknell Forest":"West Berkshire","Reading":"West Berkshire","Slough":"West Berkshire",
    "West Berkshire":"West Berkshire","Windsor and Maidenhead":"West Berkshire","Wokingham":"West Berkshire",
    # === HAMPSHIRE ===
    "Basingstoke and Deane":"Hampshire","East Hampshire":"Hampshire","Eastleigh":"Hampshire",
    "Fareham":"Hampshire","Gosport":"Hampshire","Hart":"Hampshire","Havant":"Hampshire",
    "New Forest":"Hampshire","Portsmouth":"Hampshire","Rushmoor":"Hampshire",
    "Southampton":"Hampshire","Test Valley":"Hampshire","Winchester":"Hampshire",
    # === SURREY ===
    "Elmbridge":"Surrey","Epsom and Ewell":"Surrey","Guildford":"Surrey","Mole Valley":"Surrey",
    "Reigate and Banstead":"Surrey","Runnymede":"Surrey","Spelthorne":"Surrey","Surrey Heath":"Surrey",
    "Tandridge":"Surrey","Waverley":"Surrey","Woking":"Surrey",
    # === KENT ===
    "Ashford":"Kent","Canterbury":"Kent","Dartford":"Kent","Dover":"Kent","Gravesham":"Kent",
    "Maidstone":"Kent","Medway":"Kent","Sevenoaks":"Kent","Shepway":"Kent","Swale":"Kent",
    "Thanet":"Kent","Tonbridge and Malling":"Kent","Tunbridge Wells":"Kent",
    # === EAST SUSSEX ===
    "Brighton and Hove":"East Sussex","Eastbourne":"East Sussex","Hastings":"East Sussex",
    "Lewes":"East Sussex","Rother":"East Sussex","Wealden":"East Sussex",
    # === WEST SUSSEX ===
    "Adur":"West Sussex","Arun":"West Sussex","Chichester":"West Sussex","Crawley":"West Sussex",
    "Horsham":"West Sussex","Mid Sussex":"West Sussex","Worthing":"West Sussex",
    # === GLOUCESTERSHIRE ===
    "Cheltenham":"Gloucestershire","Cotswold":"Gloucestershire","Forest of Dean":"Gloucestershire",
    "Gloucester":"Gloucestershire","South Gloucestershire":"Gloucestershire","Stroud":"Gloucestershire","Tewkesbury":"Gloucestershire",
    # === SOMERSET ===
    "Bath and North East Somerset":"Somerset","Mendip":"Somerset","North Somerset":"Somerset",
    "Sedgemoor":"Somerset","South Somerset":"Somerset","Taunton Deane":"Somerset","West Somerset":"Somerset",
    "Bristol, City of":"Somerset",
    # === WILTSHIRE ===
    "Swindon":"Wiltshire","Wiltshire":"Wiltshire",
    # === CORNWALL ===
    "Cornwall":"Cornwall","Isles of Scilly":"Cornwall",
    # === DEVON ===
    "East Devon":"Devon","Exeter":"Devon","Mid Devon":"Devon","North Devon":"Devon","Plymouth":"Devon",
    "South Hams":"Devon","Teignbridge":"Devon","Torbay":"Devon","Torridge":"Devon","West Devon":"Devon",
    # === DORSET ===
    "Bournemouth":"Dorset","Christchurch":"Dorset","East Dorset":"Dorset","North Dorset":"Dorset",
    "Poole":"Dorset","Purbeck":"Dorset","West Dorset":"Dorset","Weymouth and Portland":"Dorset",
    "Bournemouth, Christchurch and Poole":"Dorset",
    # === SCOTLAND (LAD names are already the council area names used in CSV) ===
    "Aberdeen City":"Aberdeen City","Aberdeenshire":"Aberdeenshire","Angus":"Angus",
    "Argyll and Bute":"Argyll and Bute","City of Edinburgh":"City of Edinburgh","Clackmannanshire":"Clackmannanshire",
    "Dumfries and Galloway":"Dumfries and Galloway","Dundee City":"Dundee City","East Ayrshire":"East Ayrshire",
    "East Dunbartonshire":"East Dunbartonshire","East Lothian":"East Lothian","East Renfrewshire":"East Renfrewshire",
    "Eilean Siar":"Eilean Siar","Falkirk":"Falkirk","Fife":"Fife","Glasgow City":"Glasgow City",
    "Highland":"Highland","Inverclyde":"Inverclyde","Midlothian":"Midlothian","Moray":"Moray",
    "North Ayrshire":"North Ayrshire","North Lanarkshire":"North Lanarkshire","Orkney Islands":"Orkney Islands",
    "Perth and Kinross":"Perth and Kinross","Renfrewshire":"Renfrewshire","Scottish Borders":"Scottish Borders",
    "Shetland Islands":"Shetland Islands","South Ayrshire":"South Ayrshire","South Lanarkshire":"South Lanarkshire",
    "Stirling":"Stirling","West Dunbartonshire":"West Dunbartonshire","West Lothian":"West Lothian",
    # === WALES (LAD names are principal areas — pass through as-is) ===
    "Blaenau Gwent":"Blaenau Gwent","Bridgend":"Bridgend","Caerphilly":"Caerphilly","Cardiff":"Cardiff",
    "Carmarthenshire":"Carmarthenshire","Ceredigion":"Ceredigion","Conwy":"Conwy","Denbighshire":"Denbighshire",
    "Flintshire":"Flintshire","Gwynedd":"Gwynedd","Isle of Anglesey":"Isle of Anglesey","Merthyr Tydfil":"Merthyr Tydfil",
    "Monmouthshire":"Monmouthshire","Neath Port Talbot":"Neath Port Talbot","Newport":"Newport",
    "Pembrokeshire":"Pembrokeshire","Powys":"Powys","Rhondda Cynon Taf":"Rhondda Cynon Taf",
    "Swansea":"Swansea","Torfaen":"Torfaen","Vale of Glamorgan":"Vale of Glamorgan","Wrexham":"Wrexham",
    # === NORTHERN IRELAND (council areas — pass through as-is) ===
    "Antrim and Newtownabbey":"Antrim and Newtownabbey","Ards and North Down":"Ards and North Down",
    "Armagh City, Banbridge and Craigavon":"Armagh City Banbridge and Craigavon",
    "Armagh City Banbridge and Craigavon":"Armagh City Banbridge and Craigavon",
    "Belfast":"Belfast","Causeway Coast and Glens":"Causeway Coast and Glens",
    "Derry City and Strabane":"Derry City and Strabane","Fermanagh and Omagh":"Fermanagh and Omagh",
    "Lisburn and Castlereagh":"Lisburn and Castlereagh","Mid and East Antrim":"Mid and East Antrim",
    "Mid Ulster":"Mid Ulster","Newry, Mourne and Down":"Newry Mourne and Down",
    "Newry Mourne and Down":"Newry Mourne and Down",
}


def build_gb_location(d):
    if "gb_region" not in d:
        return None
    reg_rows    = [r for r in d["gb_region"]["rows"] if r[0] not in ("(not set)","")]
    city_rows   = [r for r in d["gb_city"]["rows"] if r[0] not in ("(not set)","")]
    cr_rows     = [r for r in d["gb_city_region"]["rows"] if r[0] not in ("(not set)","")]

    # Aggregate sessions by county (for county chart / table)
    county_sessions = {}
    for r in city_rows:
        county = CITY_TO_COUNTY.get(r[0])
        if county:
            county_sessions[county] = county_sessions.get(county, 0) + int(r[1])
    county_sorted = sorted(county_sessions.items(), key=lambda x: x[1], reverse=True)

    # Build LAD-level map: GA4 city → exact LAD13NM / LGDNAME (unique value per district)
    lad_map = {}
    for r in city_rows:
        name = r[0]
        sessions = int(r[1])
        lad = CITY_TO_LAD.get(name)
        if lad == "_LONDON":
            for borough in LONDON_LADS:
                lad_map[borough] = lad_map.get(borough, 0) + sessions
        elif lad:
            lad_map[lad] = lad_map.get(lad, 0) + sessions

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
        "lad_map":           lad_map,
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
        "<div class=\"card mb-4\">"
        "<div class=\"card-body\">"
        "<h4 class=\"card-title\">Interactive Map &mdash; Sessions by City</h4>"
        "<div id=\"gbMap_" + pid + "\" class=\"gb-map\"></div>"
        "<div class=\"map-legend mt-3\" id=\"legend_" + pid + "\"></div>"
        "</div></div>"

        "<div class=\"card mb-4\">"
        "<div class=\"card-body\">"
        "<h4 class=\"card-title\">Interactive Map &mdash; Sessions by District</h4>"
        "<div id=\"gbCountyMap_" + pid + "\" class=\"gb-map\"></div>"
        "<div class=\"map-legend mt-3\" id=\"countyLegend_" + pid + "\"></div>"
        "</div></div>"

        "<div class=\"row mb-4\">"
        "<div class=\"col-lg-6\">"
        "<div class=\"card h-100\"><div class=\"card-body\">"
        "<h4 class=\"card-title\">Sessions by Region</h4>"
        "<canvas id=\"regChart_" + pid + "\" height=\"160\"></canvas>"
        "</div></div></div>"
        "<div class=\"col-lg-6\">"
        "<div class=\"card h-100\"><div class=\"card-body\">"
        "<h4 class=\"card-title\">Top 20 Cities</h4>"
        "<canvas id=\"cityChart_" + pid + "\" height=\"160\"></canvas>"
        "</div></div></div>"
        "</div>"

        "<div class=\"card mb-4\"><div class=\"card-body\">"
        "<h4 class=\"card-title\">Sessions by County (Top 30)</h4>"
        "<canvas id=\"countyChart_" + pid + "\" height=\"200\"></canvas>"
        "</div></div>"

        "<div class=\"card mb-4\"><div class=\"card-body\">"
        "<h4 class=\"card-title\">UK Regions</h4>"
        "<div class=\"table-responsive\">"
        "<table class=\"table table-hover mb-0\"><thead><tr><th>Region</th><th>Sessions</th><th>Users</th><th>Avg Duration</th><th>Bounce Rate</th></tr></thead>"
        "<tbody>" + loc["region_table"] + "</tbody></table></div>"
        "</div></div>"

        "<div class=\"card mb-4\"><div class=\"card-body\">"
        "<h4 class=\"card-title\">Cities (Top 50)</h4>"
        "<div class=\"table-responsive\">"
        "<table class=\"table table-hover mb-0\"><thead><tr><th>City</th><th>Sessions</th><th>Users</th><th>Avg Duration</th><th>Bounce Rate</th></tr></thead>"
        "<tbody>" + loc["city_table"] + "</tbody></table></div>"
        "</div></div>"

        "<div class=\"card mb-4\"><div class=\"card-body\">"
        "<h4 class=\"card-title\">City + Region (Top 100)</h4>"
        "<div class=\"table-responsive\">"
        "<table class=\"table table-hover mb-0\"><thead><tr><th>City</th><th>Region</th><th>Sessions</th><th>Users</th><th>Avg Duration</th></tr></thead>"
        "<tbody>" + loc["city_region_table"] + "</tbody></table></div>"
        "</div></div>"

        "<div class=\"card mb-4\"><div class=\"card-body\">"
        "<h4 class=\"card-title\">Sessions by County</h4>"
        "<div class=\"table-responsive\">"
        "<table class=\"table table-hover mb-0\"><thead><tr><th>County / Area</th><th>Sessions</th></tr></thead>"
        "<tbody>" + loc["county_table"] + "</tbody></table></div>"
        "</div></div>"
    )


def panel_html(p, pid, active):
    cls = "panel active" if active else "panel"
    age_html = "<canvas id=\"ageChart_" + pid + "\" height=\"160\"></canvas>" if p["has_age"] else "<p class=\"text-muted font-italic\">Insufficient data &mdash; enable Google Signals in GA4.</p>"
    gen_html = "<canvas id=\"genderChart_" + pid + "\" height=\"160\"></canvas>" if p["has_gen"] else "<p class=\"text-muted font-italic\">Insufficient data &mdash; enable Google Signals in GA4.</p>"
    return (
        "<div class=\"" + cls + "\" id=\"panel_" + pid + "\">"

        # KPI stat cards
        "<div class=\"card-group mb-4\">"
        "<div class=\"card border-right\">"
        "<div class=\"card-body\">"
        "<div class=\"d-flex align-items-center\">"
        "<div>"
        "<h2 class=\"text-dark mb-1 font-weight-medium\">" + p["total_sessions"] + "</h2>"
        "<h6 class=\"text-muted font-weight-normal mb-0\">Total Sessions</h6>"
        "</div>"
        "<div class=\"ml-auto\"><span class=\"opacity-7 text-muted\"><i data-feather=\"bar-chart-2\" class=\"stat-icon\"></i></span></div>"
        "</div></div></div>"

        "<div class=\"card border-right\">"
        "<div class=\"card-body\">"
        "<div class=\"d-flex align-items-center\">"
        "<div>"
        "<h2 class=\"text-dark mb-1 font-weight-medium\">" + p["total_users"] + "</h2>"
        "<h6 class=\"text-muted font-weight-normal mb-0\">Active Users</h6>"
        "</div>"
        "<div class=\"ml-auto\"><span class=\"opacity-7 text-muted\"><i data-feather=\"users\" class=\"stat-icon\"></i></span></div>"
        "</div></div></div>"

        "<div class=\"card border-right\">"
        "<div class=\"card-body\">"
        "<div class=\"d-flex align-items-center\">"
        "<div>"
        "<h2 class=\"text-dark mb-1 font-weight-medium\">" + p["avg_duration"] + "</h2>"
        "<h6 class=\"text-muted font-weight-normal mb-0\">Avg Session Duration</h6>"
        "</div>"
        "<div class=\"ml-auto\"><span class=\"opacity-7 text-muted\"><i data-feather=\"clock\" class=\"stat-icon\"></i></span></div>"
        "</div></div></div>"

        "<div class=\"card border-right\">"
        "<div class=\"card-body\">"
        "<div class=\"d-flex align-items-center\">"
        "<div>"
        "<h2 class=\"text-dark mb-1 font-weight-medium kpi-sm\">" + p["top_country"] + "</h2>"
        "<h6 class=\"text-muted font-weight-normal mb-0\">Top Country</h6>"
        "<small class=\"text-muted\">" + p["top_country_s"] + " sessions</small>"
        "</div>"
        "<div class=\"ml-auto\"><span class=\"opacity-7 text-muted\"><i data-feather=\"globe\" class=\"stat-icon\"></i></span></div>"
        "</div></div></div>"

        "<div class=\"card border-right\">"
        "<div class=\"card-body\">"
        "<div class=\"d-flex align-items-center\">"
        "<div>"
        "<h2 class=\"text-dark mb-1 font-weight-medium kpi-sm\">" + p["top_channel"] + "</h2>"
        "<h6 class=\"text-muted font-weight-normal mb-0\">Top Channel</h6>"
        "<small class=\"text-muted\">" + p["top_channel_s"] + " sessions</small>"
        "</div>"
        "<div class=\"ml-auto\"><span class=\"opacity-7 text-muted\"><i data-feather=\"trending-up\" class=\"stat-icon\"></i></span></div>"
        "</div></div></div>"

        "<div class=\"card\">"
        "<div class=\"card-body\">"
        "<div class=\"d-flex align-items-center\">"
        "<div>"
        "<h2 class=\"text-dark mb-1 font-weight-medium kpi-sm\">" + p["top_device"] + "</h2>"
        "<h6 class=\"text-muted font-weight-normal mb-0\">Top Device</h6>"
        "<small class=\"text-muted\">" + p["top_device_s"] + " sessions</small>"
        "</div>"
        "<div class=\"ml-auto\"><span class=\"opacity-7 text-muted\"><i data-feather=\"monitor\" class=\"stat-icon\"></i></span></div>"
        "</div></div></div>"
        "</div>"  # end card-group

        # Sessions & Users Over Time
        "<div class=\"card mb-4\"><div class=\"card-body\">"
        "<h4 class=\"card-title\">Sessions &amp; Users Over Time</h4>"
        "<canvas id=\"trendChart_" + pid + "\" height=\"70\"></canvas>"
        "</div></div>"

        # Sessions by Country + Traffic Channels
        "<div class=\"row mb-4\">"
        "<div class=\"col-lg-8\">"
        "<div class=\"card h-100\"><div class=\"card-body\">"
        "<h4 class=\"card-title\">Sessions by Country</h4>"
        "<canvas id=\"geoChart_" + pid + "\" height=\"120\"></canvas>"
        "</div></div></div>"
        "<div class=\"col-lg-4\">"
        "<div class=\"card h-100\"><div class=\"card-body\">"
        "<h4 class=\"card-title\">Traffic Channels</h4>"
        "<canvas id=\"channelChart_" + pid + "\" height=\"120\"></canvas>"
        "</div></div></div>"
        "</div>"

        # Device / OS / Browser
        "<div class=\"row mb-4\">"
        "<div class=\"col-lg-4\">"
        "<div class=\"card h-100\"><div class=\"card-body\">"
        "<h4 class=\"card-title\">Device Type</h4>"
        "<canvas id=\"deviceChart_" + pid + "\" height=\"180\"></canvas>"
        "</div></div></div>"
        "<div class=\"col-lg-4\">"
        "<div class=\"card h-100\"><div class=\"card-body\">"
        "<h4 class=\"card-title\">Operating System</h4>"
        "<canvas id=\"osChart_" + pid + "\" height=\"180\"></canvas>"
        "</div></div></div>"
        "<div class=\"col-lg-4\">"
        "<div class=\"card h-100\"><div class=\"card-body\">"
        "<h4 class=\"card-title\">Browser</h4>"
        "<canvas id=\"browserChart_" + pid + "\" height=\"180\"></canvas>"
        "</div></div></div>"
        "</div>"

        # Age + Gender
        "<div class=\"row mb-4\">"
        "<div class=\"col-lg-6\">"
        "<div class=\"card h-100\"><div class=\"card-body\">"
        "<h4 class=\"card-title\">Age Bracket</h4>" + age_html +
        "</div></div></div>"
        "<div class=\"col-lg-6\">"
        "<div class=\"card h-100\"><div class=\"card-body\">"
        "<h4 class=\"card-title\">Gender</h4>" + gen_html +
        "</div></div></div>"
        "</div>"

        # Channel Performance table
        "<div class=\"card mb-4\"><div class=\"card-body\">"
        "<h4 class=\"card-title\">Channel Performance</h4>"
        "<div class=\"table-responsive\">"
        "<table class=\"table table-hover mb-0\"><thead><tr><th>Channel</th><th>Sessions</th><th>Users</th><th>Bounce Rate</th><th>Avg Duration</th></tr></thead>"
        "<tbody>" + p["ch_table"] + "</tbody></table></div>"
        "</div></div>"

        # Traffic Sources + Landing Pages
        "<div class=\"row mb-4\">"
        "<div class=\"col-lg-6\">"
        "<div class=\"card h-100\"><div class=\"card-body\">"
        "<h4 class=\"card-title\">Traffic Sources</h4>"
        "<div class=\"table-responsive\">"
        "<table class=\"table table-hover mb-0\"><thead><tr><th>Source</th><th>Medium</th><th>Sessions</th><th>Users</th></tr></thead>"
        "<tbody>" + p["src_table"] + "</tbody></table></div>"
        "</div></div></div>"
        "<div class=\"col-lg-6\">"
        "<div class=\"card h-100\"><div class=\"card-body\">"
        "<h4 class=\"card-title\">Top Landing Pages</h4>"
        "<div class=\"table-responsive\">"
        "<table class=\"table table-hover mb-0\"><thead><tr><th>Page</th><th>Sessions</th><th>Bounce</th><th>Duration</th></tr></thead>"
        "<tbody>" + p["lp_table"] + "</tbody></table></div>"
        "</div></div></div>"
        "</div>"

        # Site Search Terms
        "<div class=\"card mb-4\"><div class=\"card-body\">"
        "<h4 class=\"card-title\">Site Search Terms</h4>" + p["st_html"] +
        "</div></div>"

        + gb_location_html(p, pid) +
        "</div>"  # end panel
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
        lines.append("const lad_map_" + pid + " = " + json.dumps(loc["lad_map"]) + ";")
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
  if(typeof city_map_data_{p}!=='undefined') initGBMap('{p}', city_map_data_{p});
  if(typeof lad_map_{p}!=='undefined') initCountyMap('{p}', lad_map_{p});
""".replace("{p}", pid)


html = """<!DOCTYPE html>
<html dir="ltr" lang="en">
<head>
<meta charset="UTF-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>GA4 Dashboard &mdash; food-mag.co.uk</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Rubik:wght@300;400;500;700&display=swap" rel="stylesheet">
<link href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" rel="stylesheet">
<style>
  /* ===== Base ===== */
  body { font-family: 'Rubik', sans-serif; background: #f4f6f9; color: #455a64; }

  /* ===== Topbar ===== */
  .topbar { height: 64px; background: #fff; border-bottom: 1px solid #e9ecef; position: fixed; top: 0; left: 0; right: 0; z-index: 1030; display: flex; align-items: center; padding: 0 24px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
  .topbar .logo-text { font-size: 17px; font-weight: 700; color: #455a64; margin-right: 8px; }
  .topbar .logo-sub  { font-size: 13px; color: #9aabbe; }
  .topbar .gen-date  { margin-left: auto; font-size: 12px; color: #9aabbe; }

  /* ===== Sidebar ===== */
  .left-sidebar { position: fixed; top: 64px; left: 0; bottom: 0; width: 260px; background: #fff; border-right: 1px solid #e9ecef; overflow-y: auto; z-index: 1020; }
  .sidebar-nav { padding: 16px 0; }
  .sidebar-nav .nav-small-cap { padding: 10px 20px 4px; font-size: 11px; font-weight: 600; color: #9aabbe; text-transform: uppercase; letter-spacing: 0.06em; }
  .sidebar-nav .sidebar-item { list-style: none; }
  .sidebar-nav .sidebar-link { display: flex; align-items: center; gap: 10px; padding: 9px 20px; font-size: 14px; color: #455a64; cursor: pointer; transition: background 0.15s, color 0.15s; border-left: 3px solid transparent; text-decoration: none; background: none; border-top: none; border-right: none; border-bottom: none; width: 100%; text-align: left; }
  .sidebar-nav .sidebar-link:hover { background: #f4f6f9; color: #5f76e8; }
  .sidebar-nav .sidebar-link.active { background: #eef1fd; color: #5f76e8; border-left-color: #5f76e8; font-weight: 500; }
  .sidebar-nav .sidebar-link .feather-icon { width: 16px; height: 16px; flex-shrink: 0; }
  .sidebar-nav .has-arrow::after { content: '\\203A'; margin-left: auto; font-size: 16px; color: #9aabbe; transition: transform 0.2s; }
  .sidebar-nav .has-arrow[aria-expanded="true"]::after { transform: rotate(90deg); }
  .sidebar-nav .first-level { padding: 0; margin: 0; }
  .sidebar-nav .first-level .sidebar-item .sidebar-link { padding-left: 46px; font-size: 13px; }
  .sidebar-nav .list-divider { height: 1px; background: #e9ecef; margin: 8px 0; list-style: none; }

  /* ===== Page wrapper ===== */
  .page-wrapper { margin-left: 260px; margin-top: 64px; min-height: calc(100vh - 64px); }
  .page-breadcrumb { padding: 16px 24px 0; }
  .page-breadcrumb .page-title { font-size: 18px; font-weight: 500; color: #455a64; margin-bottom: 2px; }
  .container-fluid { padding: 20px 24px 40px; }

  /* ===== Panels ===== */
  .panel { display: none; }
  .panel.active { display: block; }

  /* ===== Cards ===== */
  .card { border: 1px solid #e9ecef; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
  .card-title { font-size: 11px; font-weight: 600; color: #9aabbe; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 16px; }
  .card-group .card { border-radius: 8px; }

  /* ===== KPI stat icons ===== */
  .stat-icon { width: 28px; height: 28px; color: #9aabbe; }
  .kpi-sm { font-size: 20px !important; }

  /* ===== Tables ===== */
  .table thead th { font-size: 11px; font-weight: 600; color: #9aabbe; text-transform: uppercase; letter-spacing: 0.04em; border-top: none; border-bottom: 1px solid #e9ecef; padding: 8px 12px; }
  .table tbody td { font-size: 13px; color: #455a64; padding: 9px 12px; border-top: 1px solid #f4f6f9; vertical-align: middle; }
  .table-hover tbody tr:hover td { background: #f8f9fc; }
  .truncate { max-width: 220px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

  /* ===== Channel badges ===== */
  .badge-direct       { background: #eff6ff; color: #2563eb; }
  .badge-organicsearch { background: #f0fdf4; color: #16a34a; }
  .badge-referral     { background: #faf5ff; color: #7c3aed; }
  .badge-email        { background: #fffbeb; color: #d97706; }
  .badge-paidsearch   { background: #fef2f2; color: #dc2626; }
  .badge-organicsocial { background: #f0f9ff; color: #0284c7; }
  .badge-unassigned   { background: #f9fafb; color: #9aabbe; }

  /* ===== Maps ===== */
  .gb-map { height: 500px; border-radius: 6px; overflow: hidden; }
  .map-legend { display: flex; flex-wrap: wrap; gap: 12px; font-size: 12px; color: #6b7280; align-items: center; }
  .map-legend-item { display: flex; align-items: center; gap: 6px; }
  .map-legend-dot { border-radius: 50%; display: inline-block; }
  .county-tip { background: #fff; border: 1px solid #e9ecef; border-radius: 6px; padding: 6px 10px; font-size: 12px; color: #455a64; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
  .leaflet-popup-content-wrapper { border-radius: 8px !important; box-shadow: 0 4px 16px rgba(0,0,0,0.12) !important; border: 1px solid #e9ecef !important; }
  .leaflet-popup-content { margin: 12px 16px !important; font-family: 'Rubik', sans-serif !important; font-size: 13px !important; }
  .map-popup-title { font-weight: 700; font-size: 14px; color: #455a64; margin-bottom: 8px; }
  .map-popup-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 4px 16px; }
  .map-popup-label { color: #9aabbe; font-size: 11px; text-transform: uppercase; letter-spacing: 0.04em; }
  .map-popup-val { color: #455a64; font-weight: 600; }

  /* ===== Misc ===== */
  .note { font-size: 12px; color: #9aabbe; font-style: italic; }
  @media (max-width: 992px) {
    .left-sidebar { transform: translateX(-260px); }
    .page-wrapper { margin-left: 0; }
  }
</style>
</head>
<body>

<div id="main-wrapper" data-theme="light" data-layout="vertical" data-navbarbg="skin6" data-sidebartype="full" data-sidebar-position="fixed" data-header-position="fixed" data-boxed-layout="full">

  <!-- ===== Topbar ===== -->
  <header class="topbar" data-navbarbg="skin6">
    <span class="logo-text">food-mag.co.uk</span>
    <span class="logo-sub">Analytics Dashboard</span>
    <span class="gen-date">Generated """ + raw["generated"] + """</span>
  </header>

  <!-- ===== Left Sidebar ===== -->
  <aside class="left-sidebar" data-sidebarbg="skin6">
    <nav class="sidebar-nav">
      <ul id="sidebarnav" class="p-0 m-0">
        <li class="list-divider"></li>
        <li class="nav-small-cap"><span>Worldwide</span></li>
        <li class="sidebar-item">
          <button class="sidebar-link active" id="nav_ww_6m" onclick="showPanel('ww_6m')">
            <i data-feather="bar-chart-2" class="feather-icon"></i><span>Last 6 Months</span>
          </button>
        </li>
        <li class="sidebar-item">
          <button class="sidebar-link" id="nav_ww_12m" onclick="showPanel('ww_12m')">
            <i data-feather="bar-chart-2" class="feather-icon"></i><span>Last 12 Months</span>
          </button>
        </li>
        <li class="list-divider"></li>
        <li class="nav-small-cap"><span>GB Analytics</span></li>
        <li class="sidebar-item">
          <button class="sidebar-link" id="nav_gb_6m" onclick="showPanel('gb_6m')">
            <i data-feather="map" class="feather-icon"></i><span>Last 6 Months</span>
          </button>
        </li>
        <li class="sidebar-item">
          <button class="sidebar-link" id="nav_gb_12m" onclick="showPanel('gb_12m')">
            <i data-feather="map" class="feather-icon"></i><span>Last 12 Months</span>
          </button>
        </li>
      </ul>
    </nav>
  </aside>

  <!-- ===== Page Wrapper ===== -->
  <div class="page-wrapper">

    <!-- Breadcrumb -->
    <div class="page-breadcrumb">
      <div class="row">
        <div class="col-12 align-self-center">
          <h3 class="page-title" id="breadcrumb-title">Worldwide &mdash; Last 6 Months</h3>
        </div>
      </div>
    </div>

    <!-- Main content -->
    <div class="container-fluid">
""" + panel_html(p_ww6, "ww_6m", True) + panel_html(p_ww12, "ww_12m", False) + panel_html(p_gb6, "gb_6m", False) + panel_html(p_gb12, "gb_12m", False) + """
    </div>
  </div>
</div>

<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.bundle.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/feather-icons/dist/feather.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
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

const _maps = {};
function initGBMap(pid, cityData) {
  if (_maps[pid]) return;
  const el = document.getElementById('gbMap_' + pid);
  if (!el) return;

  const map = L.map('gbMap_' + pid, {zoomControl:true, scrollWheelZoom:false, minZoom:7}).setView([54.4, -3.2], 7);
  _maps[pid] = map;

  L.tileLayer('https://api.os.uk/maps/raster/v1/zxy/Light_3857/{z}/{x}/{y}.png?key=ubDCdHVhUQGyehuSrSkgfBifOjgkuA0F', {
    attribution:'&copy; <a href="https://www.ordnancesurvey.co.uk/">Ordnance Survey</a>',
    minZoom:7, maxZoom:20
  }).addTo(map);

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

  const leg = document.getElementById('legend_' + pid);
  if (leg) {
    leg.innerHTML =
      '<span style="color:#455a64;font-weight:600;margin-right:8px">Sessions by city:</span>' +
      breaks.map(b =>
        '<span class="map-legend-item"><span class="map-legend-dot" style="width:' + (b.r*2) + 'px;height:' + (b.r*2) + 'px;background:' + b.color + '"></span>' + b.label + '</span>'
      ).join('');
  }

  setTimeout(() => map.invalidateSize(), 300);
}

const _countyMaps = {};
function initCountyMap(pid, ladData) {
  if (_countyMaps[pid]) return;
  const el = document.getElementById('gbCountyMap_' + pid);
  if (!el) return;

  const map = L.map('gbCountyMap_' + pid, {zoomControl:true, scrollWheelZoom:false, minZoom:7}).setView([54.4, -3.2], 7);
  _countyMaps[pid] = map;

  L.tileLayer('https://api.os.uk/maps/raster/v1/zxy/Light_3857/{z}/{x}/{y}.png?key=ubDCdHVhUQGyehuSrSkgfBifOjgkuA0F', {
    attribution:'&copy; <a href="https://www.ordnancesurvey.co.uk/">Ordnance Survey</a>',
    minZoom:7, maxZoom:20
  }).addTo(map);

  const maxVal = Math.max(1, ...Object.values(ladData));
  const breaks = [
    {thresh:0.5, fill:'#1e1b4b', label:'Very high'},
    {thresh:0.25, fill:'#312e81', label:'High'},
    {thresh:0.1,  fill:'#4338ca', label:'Medium-high'},
    {thresh:0.04, fill:'#6366f1', label:'Medium'},
    {thresh:0.01, fill:'#a5b4fc', label:'Low'},
    {thresh:0,    fill:'#e0e7ff', label:'Very low'},
  ];

  function getColor(sessions) {
    if (!sessions) return '#f1f5f9';
    const t = sessions / maxVal;
    for (const b of breaks) { if (t >= b.thresh) return b.fill; }
    return '#e0e7ff';
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
          const lad = f.properties['LAD13NM'] || f.properties['LGDNAME'] || '';
          return {color:'#6366f1', weight:1, fillColor:getColor(ladData[lad]||0), fillOpacity:0.8, opacity:0.6};
        },
        onEachFeature: (f, layer) => {
          const lad = f.properties['LAD13NM'] || f.properties['LGDNAME'] || '';
          const sessions = ladData[lad] || 0;
          layer.bindTooltip(
            '<strong>' + lad + '</strong><br>' + (sessions ? sessions.toLocaleString() + ' sessions' : 'No data'),
            {sticky:true, className:'county-tip'}
          );
          layer.on('mouseover', e => e.target.setStyle({weight:2, fillOpacity:0.95}));
          layer.on('mouseout', e => {
            const s = ladData[f.properties['LAD13NM'] || f.properties['LGDNAME'] || ''] || 0;
            e.target.setStyle({weight:1, fillColor:getColor(s), fillOpacity:0.8});
          });
        }
      }).addTo(map);
    }).catch(()=>{});
  });

  const leg = document.getElementById('countyLegend_' + pid);
  if (leg) {
    leg.innerHTML = '<span style="color:#455a64;font-weight:600;margin-right:8px">Sessions by district:</span>' +
      breaks.map(b =>
        '<span class="map-legend-item"><span style="width:18px;height:12px;background:' + b.fill + ';border:1px solid rgba(99,102,241,0.3);border-radius:2px;display:inline-block"></span> ' + b.label + '</span>'
      ).join('') +
      '<span class="map-legend-item"><span style="width:18px;height:12px;background:#f1f5f9;border:1px solid #e9ecef;border-radius:2px;display:inline-block"></span> No data</span>';
  }

  setTimeout(() => map.invalidateSize(), 300);
}

// Sidebar nav
function showPanel(pid) {
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  const el = document.getElementById('panel_' + pid);
  if (el) el.classList.add('active');
  // update breadcrumb
  const titles = {ww_6m:'Worldwide — Last 6 Months', ww_12m:'Worldwide — Last 12 Months', gb_6m:'GB Analytics — Last 6 Months', gb_12m:'GB Analytics — Last 12 Months'};
  document.getElementById('breadcrumb-title').textContent = titles[pid] || pid;
  // update active nav link
  document.querySelectorAll('.sidebar-link').forEach(l => l.classList.remove('active'));
  const navEl = document.getElementById('nav_' + pid);
  if (navEl) navEl.classList.add('active');
  // lazy init charts/maps
  const inits = {ww_6m:initww_6m, ww_12m:initww_12m, gb_6m:initgb_6m, gb_12m:initgb_12m};
  if (inits[pid]) inits[pid]();
  setTimeout(() => {
    if (_maps[pid]) _maps[pid].invalidateSize();
    if (_countyMaps[pid]) _countyMaps[pid].invalidateSize();
  }, 250);
}

// Init feather icons
feather.replace();

// Show first panel on load
document.addEventListener('DOMContentLoaded', function() { showPanel('ww_6m'); });
</script>
</body>
</html>"""

out = os.path.join(os.path.dirname(__file__), "index.html")
with open(out, "w") as f:
    f.write(html)

print("Dashboard written.")
