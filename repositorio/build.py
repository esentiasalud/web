import json, os, re, shutil, urllib.parse, base64
from datetime import date
import builtins
def open(f, mode="r", **kw):
    if "b" not in mode: kw.setdefault("encoding", "utf-8")
    return builtins.open(f, mode, **kw)

BASE = "https://www.esentiasalud.com.ar"
WA_ESENTIA = "5493535635719"
TEL_TXT = "353 563-5719"
MAIL = "esentiasalud@gmail.com"
ADDR = "Mendoza 374/384 (esq. Pasaje Falucho)"
CITY = "Villa María, Córdoba"
MAPS = "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote("Mendoza 374, Villa María, Córdoba, Argentina")
OUT = "site"
ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
if os.path.isdir(OUT): shutil.rmtree(OUT)
shutil.copytree("static", OUT)
if os.path.isdir("media"): shutil.copytree("media", os.path.join(OUT, "media"))
try:
    AJ = json.load(open("content/ajustes.json", encoding="utf-8"))
except Exception:
    AJ = {}
INSTAGRAM = (AJ.get("instagram") or "").strip().lstrip("@").rstrip("/").split("/")[-1]
BEHOLD_ID = (AJ.get("behold_feed_id") or "").strip()
CURVES = '<img class="wm" src="img/isotipo-blanco.png" alt="" width="800" height="674"><svg class="curves" viewBox="0 0 600 400" preserveAspectRatio="xMaxYMin slice" aria-hidden="true"><path d="M180 -20 C 200 140, 420 120, 460 260 S 560 420, 640 380" fill="none" stroke="#6cc3b0" stroke-width="2"/><path d="M640 120 C 560 130, 520 220, 600 300" fill="none" stroke="#6cc3b0" stroke-width="2" opacity=".7"/></svg>'

def wa(num, msg):
    return f"https://wa.me/{num}?text=" + urllib.parse.quote(msg)

ICON_CHAT = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 12a8 8 0 0 1-11.6 7.1L4 20l1-4.2A8 8 0 1 1 20 12z"/><path d="M9.5 9.5c.3 1.9 2.1 3.8 4 4.2l1-1 1.8.8-.4 1.6c-3.3.2-6.9-3.2-6.9-6.6l1.6-.4.8 1.8z" fill="currentColor" stroke="none"/></svg>'
ICON_ARROW = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'

# ---------- profesionales ----------
P = {
 "mayra": dict(nombre="Mayra Marzioni", foto="mayra-marzioni.jpg", wa="5493534119868",
   role="Lic. en Psicopedagogía · UNVM",
   desc="Trabaja en el ámbito clínico con niñas, niños y adolescentes: evaluación, diagnóstico y tratamiento de las dificultades específicas del aprendizaje, y acompañamiento de procesos de inclusión escolar junto a la familia y la escuela.",
   tags=["Niños y adolescentes","Particular","CUD","Obras sociales"]),
 "emilia": dict(nombre="Emilia Cena", foto="emilia-cena.jpg", wa="5493534767959", mail="emicena@hotmail.com.ar",
   role="Psicopedagoga",
   desc="Acompaña y evalúa procesos de aprendizaje de niños y adolescentes desde una mirada integral e interdisciplinaria, tanto en la clínica psicopedagógica como en procesos de inclusión escolar.",
   tags=["Niños y adolescentes","Inclusión escolar"]),
 "julia": dict(nombre="Julia Dagna", foto="julia-dagna.jpg", wa="5493467438178",
   role="Lic. en Psicopedagogía",
   desc="Apoyo escolar con orientación psicopedagógica y enfoque personalizado: técnicas de estudio, ayuda con tareas y materias, y estrategias para la atención, la memoria y la planificación.",
   tags=["Apoyo escolar","Técnicas de estudio"]),
 "malena": dict(nombre="Malena Donato", foto="malena-donato.jpg", wa="5493472621664", mail="malenadonato1@gmail.com",
   role="Psicopedagoga · Orientación vocacional",
   desc="Orientación vocacional ocupacional para quienes terminan la secundaria, jóvenes que quieren repensar su carrera o trabajo, y adultos que buscan nuevos proyectos después de jubilarse. Unas 10 sesiones individuales semanales de 1 hora.",
   tags=["Adolescentes","Adultos","Orientación vocacional"]),
 "antonella_pp": dict(nombre="Antonella Pantanetti", foto="antonella-pantanetti.jpg", wa="5493537550562",
   role="Lic. en Psicopedagogía",
   desc="Acompaña a las infancias en sus experiencias de aprendizaje formal y no formal, con un abordaje que tiene en cuenta a cada paciente y al entorno que lo rodea.",
   tags=["Infancias"]),
 "nadia": dict(nombre="Nadia Prytz Nilsson", foto="nadia-prytz-nilsson.jpg", wa="5493512059101",
   role="Lic. y Prof. en Psicología · MP 6992",
   desc="Egresada de la UNC. Desde 2009 se dedica a la clínica infanto-juvenil, con formación en psicoterapia cognitiva-integrativa y terapia sistémica. Acompaña a niños, adolescentes y sus familias.",
   tags=["Niños y adolescentes","Familias","Particular","CUD"]),
 "perla": dict(nombre="Perla Faccia", foto="perla-faccia.jpg", wa="5493534252888",
   role="Lic. en Psicología",
   desc="Atención psicológica en Esentia. Escribile por WhatsApp para consultar días y horarios.",
   tags=[]),
 "macarena": dict(nombre="Macarena Pantanetti", foto="macarena-pantanetti.jpg", wa="5493537664850",
   role="Lic. en Terapia Ocupacional",
   desc="Acompaña a niñas, niños, adolescentes y adultos para que puedan realizar sus actividades y ocupaciones diarias de la forma más autónoma posible, con trabajo en equipo y una mirada puesta en el proyecto de vida de cada persona.",
   tags=["Niños","Adolescentes","Adultos","Particular","CUD"]),
 "antonella_et": dict(nombre="Antonella Pantanetti", foto="antonella-pantanetti.jpg", wa="5493537550562",
   role="Estimulación temprana · Puericultora · Doula",
   desc="Acompaña a familias en la gestación, el nacimiento y el puerperio, con un abordaje integral y afectivo. Brinda orientación en situaciones de crianza, en encuentros individuales, de pareja o grupales, y coordina talleres para profesionales y estudiantes.",
   tags=["Gestación y puerperio","Crianza","Talleres"]),
}
GROUPS = [
 ("psicopedagogia","Psicopedagogía","Aprendizaje, inclusión escolar, apoyo escolar y orientación vocacional.",["mayra","emilia","julia","malena","antonella_pp"]),
 ("psicologia","Psicología","Acompañamiento psicológico para niños, adolescentes, adultos y familias.",["nadia","perla"]),
 ("terapia-ocupacional","Terapia Ocupacional","Autonomía e independencia en las actividades de la vida diaria.",["macarena"]),
 ("crianza","Estimulación temprana y crianza","Gestación, nacimiento, puerperio y crianza.",["antonella_et"]),
]
N_PROF = len({p["nombre"] for p in P.values()})

def head(title, desc, path, extra_ld=None, og_img="img/og.jpg"):
    url = BASE + path
    ld = {
      "@context":"https://schema.org","@type":"MedicalBusiness","@id":BASE+"/#esentia",
      "name":"Esentia","alternateName":"Esentia Comunidad Profesional de Salud",
      "description":"Comunidad de profesionales de la salud y alquiler de consultorios por hora en Villa María, Córdoba.",
      "url":BASE+"/","logo":BASE+"/img/isotipo.png","image":BASE+"/img/og.jpg",
      "telephone":"+54 9 353 766-4850","email":MAIL,
      "address":{"@type":"PostalAddress","streetAddress":"Mendoza 374","addressLocality":"Villa María","addressRegion":"Córdoba","postalCode":"5900","addressCountry":"AR"},
      "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"08:00","closes":"21:00"}],
      "areaServed":"Villa María"
    }
    lds = [ld] + (extra_ld or [])
    ldtxt = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)
    return f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow">
<meta name="theme-color" content="#21314f">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_AR">
<meta property="og:site_name" content="Esentia">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/{og_img}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="favicon.png">
<link rel="apple-touch-icon" href="img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Ubuntu:wght@300;400;500;700&display=swap">
<link rel="stylesheet" href="styles.css">
{ldtxt}'''

IG_URL = f"https://www.instagram.com/{INSTAGRAM}/" if INSTAGRAM else ""
IG_FOOT = f'<li><a href="{IG_URL}" target="_blank" rel="noopener">Instagram @{INSTAGRAM}</a></li>' if INSTAGRAM else ""

def header(cur):
    items = [("index.html","Inicio"),("profesionales.html","Profesionales"),("alquiler-consultorios.html","Alquiler de consultorios"),("noticias.html","Noticias"),("index.html#contacto","Contacto")]
    AC = ' aria-current="page"'
    lis = "".join(f'<li><a href="{h}"{AC if h==cur else ""}>{t}</a></li>' for h,t in items)
    return f'''<a class="skip" href="#contenido">Saltar al contenido</a>
<header class="top"><div class="wrap nav">
<a class="brand" href="index.html" aria-label="Esentia, inicio"><img class="logo" src="img/logo.png" alt="Esentia, Comunidad Profesional de Salud" width="1200" height="176"></a>
<nav aria-label="Principal"><ul class="menu">{lis}</ul></nav>
</div></header>'''

def footer():
    return f'''<footer><div class="wrap">
<div><a class="brand" href="index.html"><img class="logo" src="img/logo-blanco.png" alt="Esentia, Comunidad Profesional de Salud" width="1200" height="176" loading="lazy"></a>
<p style="margin-top:14px;max-width:38ch">Un espacio para profesionales interdisciplinarios de la salud en Villa María.</p></div>
<div><h3>Secciones</h3><ul><li><a href="profesionales.html">Profesionales</a></li><li><a href="alquiler-consultorios.html">Alquiler de consultorios</a></li><li><a href="noticias.html">Noticias</a></li><li><a href="index.html#contacto">Contacto</a></li></ul></div>
<div><h3>Contacto</h3><ul><li>{ADDR}</li><li>{CITY}</li><li><a href="{wa(WA_ESENTIA,'Hola Esentia, quiero hacer una consulta.')}" target="_blank" rel="noopener">WhatsApp {TEL_TXT}</a></li><li><a href="mailto:{MAIL}">{MAIL}</a></li>{IG_FOOT}</ul></div>
<p class="legal">© {date.today().year} Esentia · Comunidad Profesional de Salud · Villa María, Córdoba, Argentina</p>
</div></footer>'''

def deepen(html):
    return re.sub(r'(href|src)="(?!https?:|mailto:|#|data:|/)([^"]+)"', r'\1="../\2"', html)

def page(title, desc, path, cur, body, extra_ld=None, scripts=False, og_img="img/og.jpg"):
    js = '\n<script src="main.js" defer></script>' if scripts else ''
    return f'''<!doctype html>
<html lang="es-AR">
<head>
{head(title, desc, path, extra_ld, og_img)}
</head>
<body>
{header(cur)}
<main id="contenido">
{body}
</main>
{footer()}{js}
</body>
</html>
'''

SLUG_OVR={"antonella_pp":"antonella-pantanetti-psicopedagogia","antonella_et":"antonella-pantanetti-estimulacion-temprana"}
def slug(k): return SLUG_OVR.get(k, P[k]["foto"][:-4])
GROUP_OF = {k:(gid,name) for gid,name,_,ks in GROUPS for k in ks}

def card(k):
    p = P[k]
    return f'''<a class="card link" href="profesionales/{slug(k)}.html">
<div class="ph"><img src="img/{p["foto"]}" alt="{p["nombre"]}" width="600" height="800" loading="lazy"></div>
<div class="bd"><h3>{p["nombre"]}</h3><p class="role">{p["role"]}</p><span class="more">Ver perfil {ICON_ARROW}</span></div></a>'''

def detail(sl):
    keys=[k for k in P if slug(k)==sl][:1]; p=P[keys[0]]; first=p["nombre"].split()[0]
    groups=[GROUP_OF[k] for k in keys]
    specs=""
    for k in keys:
        q=P[k]; tags="".join(f"<li>{t}</li>" for t in q["tags"])
        tags=f'<ul class="tags" aria-label="Atiende">{tags}</ul>' if tags else ""
        h=f'<h2 class="spec-t">{GROUP_OF[k][1]}</h2>' if len(keys)>1 else ""
        specs+=f'<div class="spec">{h}<p class="role">{q["role"]}</p><p class="desc">{q["desc"]}</p>{tags}</div>'
    msg=f'Hola {first}, te escribo desde la web de Esentia. Quisiera hacer una consulta.'
    mail=f'<a class="btn ghost" href="mailto:{p["mail"]}">{p["mail"]}</a>' if p.get("mail") else ""
    others=[k for gid,_,_,ks in GROUPS if gid in [g[0] for g in groups] for k in ks if slug(k)!=sl]
    seen=set(); others=[k for k in others if not (slug(k) in seen or seen.add(slug(k)))]
    if others:
        more=f'<section class="sec"><div class="wrap"><div class="group-head"><h2>Otras profesionales de {groups[0][1] if len(groups)==1 else "estas especialidades"}</h2><p><a href="profesionales.html">Ver todo el equipo</a></p></div><div class="cards mini">{"".join(card(k) for k in others)}</div></div></section>'
    else:
        more='<section class="sec"><div class="wrap"><div class="row"><a class="btn ghost" href="profesionales.html">Conocé a todo el equipo de Esentia</a></div></div></section>'
    body=f'''<section class="sec tint prof-sec"><div class="wrap">
<nav class="crumbs" aria-label="Ruta"><a href="profesionales.html">Profesionales</a> <span aria-hidden="true">/</span> <span>{p["nombre"]}</span></nav>
<div class="prof">
<img class="prof-photo" src="img/{p["foto"]}" alt="{p["nombre"]}, {p["role"].split(" · ")[0]} en Esentia Villa María" width="600" height="800">
<div class="prof-info">
<span class="eyebrow">{" · ".join(g[1] for g in groups)}</span>
<h1>{p["nombre"]}</h1>
{specs}
<div class="prof-cta"><a class="btn wa" href="{wa(p["wa"],msg)}" target="_blank" rel="noopener">{ICON_CHAT} Escribir a {first} por WhatsApp</a>{mail}</div>
<p class="note">Atiende en Esentia · {ADDR}, {CITY}. <a href="{MAPS}" target="_blank" rel="noopener">Ver mapa</a></p>
</div></div></div></section>
{more}'''
    role0=p["role"].split(" · ")[0]
    ld=[{"@context":"https://schema.org","@type":"Person","name":p["nombre"],"jobTitle":[P[k]["role"] for k in keys],"description":p["desc"],"image":BASE+"/img/"+p["foto"],"telephone":"+"+p["wa"],**({"email":p["mail"]} if p.get("mail") else {}),"worksFor":{"@id":BASE+"/#esentia"},"workLocation":{"@id":BASE+"/#esentia"}}]
    html=page(f"{p['nombre']} · {role0} en Villa María | Esentia",
              (p["desc"][:150].rsplit(" ",1)[0]+"…").replace('"',''),
              f"/profesionales/{sl}.html","profesionales.html",body,ld)
    html=re.sub(r'(href|src)="(?!https?:|mailto:|#|data:|/)([^"]+)"', r'\1="../\2"', html)
    return html

# ---------- noticias (content/noticias/*.md) ----------
import glob, html as _html, unicodedata, datetime as _dt
MESES = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"]

def _simple_yaml(txt):
    d = {}; key = None
    for ln in txt.splitlines():
        m = re.match(r'^([A-Za-z_][\w-]*):\s*(.*)$', ln)
        if m and not ln.startswith(" "):
            key = m.group(1); v = m.group(2).strip()
            if v in ("|", ">", "|-", ">-", "|+", ">+"): v = ""
            if len(v) > 1 and v[0] == v[-1] and v[0] in "\"'": v = v[1:-1]
            d[key] = v
        elif key and ln.strip():
            d[key] = (str(d[key]) + " " + ln.strip()).strip()
    return d

def _simple_md(t):
    def inline(x):
        x = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1">', x)
        x = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', x)
        x = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', x)
        return re.sub(r'(?<![\w*])\*(.+?)\*(?!\w)', r'<em>\1</em>', x)
    out = []
    for b in re.split(r'\n\s*\n', t.strip()):
        b = b.strip()
        if not b: continue
        if b.startswith("<"): out.append(b); continue
        h = re.match(r'^(#{1,4})\s+(.*)$', b)
        ls = b.splitlines()
        if h: n = max(2, min(len(h.group(1)), 4)); out.append(f"<h{n}>{inline(h.group(2))}</h{n}>")
        elif all(re.match(r'^\s*[-*]\s+', l) for l in ls): out.append("<ul>" + "".join("<li>" + inline(re.sub(r'^\s*[-*]\s+', '', l)) + "</li>" for l in ls) + "</ul>")
        elif all(re.match(r'^\s*\d+[.)]\s+', l) for l in ls): out.append("<ol>" + "".join("<li>" + inline(re.sub(r'^\s*\d+[.)]\s+', '', l)) + "</li>" for l in ls) + "</ol>")
        elif all(l.startswith(">") for l in ls): out.append("<blockquote><p>" + inline(" ".join(l.lstrip("> ") for l in ls)) + "</p></blockquote>")
        else: out.append("<p>" + inline(b.replace("\n", "<br>")) + "</p>")
    return "\n".join(out)

def _yaml(txt):
    try:
        import yaml
        return yaml.safe_load(txt) or {}
    except Exception:
        return _simple_yaml(txt)

def _md(txt):
    try:
        import markdown
        return markdown.markdown(txt, extensions=["extra", "sane_lists"])
    except Exception:
        return _simple_md(txt)

def _slugify(x):
    x = unicodedata.normalize("NFKD", x).encode("ascii", "ignore").decode()
    return re.sub(r'[^a-z0-9]+', '-', x.lower()).strip('-')[:70] or "nota"

def _date(v, fn):
    if isinstance(v, _dt.datetime): return v.date()
    if isinstance(v, _dt.date): return v
    m = re.search(r'(\d{4})-(\d{2})-(\d{2})', str(v or "") + " " + fn)
    return _dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else _dt.date.today()

def _rel(u):
    u = (u or "").strip()
    return u.lstrip("/") if u.startswith("/") and not u.startswith("//") else u

def _plain(h): return re.sub(r'\s+', ' ', _html.unescape(re.sub(r'<[^>]+>', ' ', h))).strip()

POSTS = []
for fn in sorted(glob.glob("content/noticias/*.md")):
    raw = open(fn, encoding="utf-8").read()
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n?(.*)$', raw, re.S)
    fm, body = (_yaml(m.group(1)), m.group(2)) if m else ({}, raw)
    if not isinstance(fm, dict): fm = {}
    body = fm.get("body") or body
    if str(fm.get("borrador", "")).lower() in ("true", "1", "si", "sí"): continue
    titulo = str(fm.get("title") or fm.get("titulo") or os.path.basename(fn)[:-3]).strip()
    cuerpo = re.sub(r'(href|src)="/(?!/)', r'\1="', _md(str(body)))
    fecha = _date(fm.get("date") or fm.get("fecha"), os.path.basename(fn))
    resumen = str(fm.get("summary") or fm.get("resumen") or "").strip() or (_plain(cuerpo)[:170].rsplit(" ", 1)[0] + "…")
    POSTS.append(dict(titulo=titulo, fecha=fecha, img=_rel(str(fm.get("image") or fm.get("imagen") or "")), resumen=resumen,
                      autor=str(fm.get("author") or fm.get("autor") or "").strip(), cuerpo=cuerpo,
                      slug=_slugify(re.sub(r'^\d{4}-\d{2}-\d{2}-', '', os.path.basename(fn)[:-3]) or titulo)))
POSTS.sort(key=lambda x: x["fecha"], reverse=True)
def fecha_txt(d): return f"{d.day} de {MESES[d.month-1]} de {d.year}"
E_ = _html.escape

def post_card(x):
    im = f'<div class="ph"><img src="{E_(x["img"])}" alt="" loading="lazy"></div>' if x["img"] else '<div class="ph ph-empty"><img src="img/isotipo-blanco.png" alt="" loading="lazy"></div>'
    return f'''<a class="card link post" href="noticias/{x["slug"]}.html">{im}
<div class="bd"><span class="date">{fecha_txt(x["fecha"])}</span><h3>{E_(x["titulo"])}</h3><p class="desc">{E_(x["resumen"])}</p><span class="more">Leer nota {ICON_ARROW}</span></div></a>'''

def post_page(x):
    url = f"{BASE}/noticias/{x['slug']}.html"
    im = f'<img class="art-img" src="{E_(x["img"])}" alt="">' if x["img"] else ""
    autor = f' · Por {E_(x["autor"])}' if x["autor"] else ""
    otros = [y for y in POSTS if y is not x][:3]
    mas = f'<section class="sec tint"><div class="wrap"><div class="group-head"><h2>Más noticias</h2><p><a href="noticias.html">Ver todas</a></p></div><div class="cards news">{"".join(post_card(y) for y in otros)}</div></div></section>' if otros else ""
    body = f'''<article class="sec art"><div class="wrap narrow">
<nav class="crumbs" aria-label="Ruta"><a href="noticias.html">Noticias</a> <span aria-hidden="true">/</span> <span>{E_(x["titulo"])}</span></nav>
<span class="eyebrow">{fecha_txt(x["fecha"])}{autor}</span>
<h1>{E_(x["titulo"])}</h1>
{im}
<div class="prose">{x["cuerpo"]}</div>
<div class="row art-share"><a class="btn wa" href="https://wa.me/?text={urllib.parse.quote(x["titulo"] + " " + url)}" target="_blank" rel="noopener">{ICON_CHAT} Compartir por WhatsApp</a><a class="btn ghost" href="noticias.html">Volver a Noticias</a></div>
</div></article>
{mas}'''
    ld = [{"@context": "https://schema.org", "@type": "Article", "headline": x["titulo"], "datePublished": x["fecha"].isoformat(),
           "description": x["resumen"], "mainEntityOfPage": url, "publisher": {"@id": BASE + "/#esentia"},
           **({"image": BASE + "/" + x["img"]} if x["img"] and not x["img"].startswith("http") else {}),
           **({"author": {"@type": "Person", "name": x["autor"]}} if x["autor"] else {"author": {"@id": BASE + "/#esentia"}})}]
    h = page(f"{x['titulo']} | Esentia", E_(x["resumen"][:155]), f"/noticias/{x['slug']}.html", "noticias.html", body, ld,
             og_img=(x["img"] if x["img"] and not x["img"].startswith("http") else "img/og.jpg"))
    return deepen(h)

if POSTS:
    news_list = f'<div class="cards news">{"".join(post_card(x) for x in POSTS)}</div>'
    news_home = f'''<section class="sec"><div class="wrap">
<div class="group-head"><h2>Últimas noticias</h2><p><a href="noticias.html">Ver todas las noticias</a></p></div>
<div class="cards news">{"".join(post_card(x) for x in POSTS[:3])}</div></div></section>'''
else:
    news_list = '<p class="lead">Todavía no hay notas publicadas. Pronto vas a encontrar acá novedades y artículos del equipo de Esentia.</p>'
    news_home = ""
news_body = f'''<section class="sec navy-head">{CURVES}<div class="wrap">
<div class="sec-head" style="margin-bottom:0"><span class="eyebrow">Noticias</span><h1 style="font-size:clamp(34px,5vw,54px)">Novedades y artículos</h1>
<p class="lead">Notas, novedades y artículos escritos por el equipo de Esentia sobre salud, aprendizaje y crianza.</p></div>
</div></section>
<div class="sec" style="padding-top:48px"><div class="wrap">{news_list}</div></div>'''

# ---------- instagram ----------
if INSTAGRAM:
    feed = f'<behold-widget feed-id="{E_(BEHOLD_ID)}"></behold-widget>' if BEHOLD_ID else ""
    ig_home = f'''<section class="sec" id="instagram"><div class="wrap">
<div class="group-head"><h2>Seguinos en Instagram</h2><p><a href="{IG_URL}" target="_blank" rel="noopener">@{INSTAGRAM}</a></p></div>
{feed}
<div class="row" style="margin-top:22px"><a class="btn primary" href="{IG_URL}" target="_blank" rel="noopener">Ver @{INSTAGRAM} en Instagram {ICON_ARROW}</a></div>
</div></section>'''
    IG_SCRIPT = '\n<script type="module" src="https://w.behold.so/widget.js"></script>' if BEHOLD_ID else ""
else:
    ig_home = ""; IG_SCRIPT = ""

# ---------- index ----------
mosaic = ["macarena-pantanetti.jpg","mayra-marzioni.jpg","nadia-prytz-nilsson.jpg","emilia-cena.jpg","malena-donato.jpg","perla-faccia.jpg"]
chips = "".join(f'<li><a href="profesionales.html#{gid}">{name} <span>{len(ks)}</span></a></li>' for gid,name,_,ks in GROUPS)
index_body = f'''
<section class="hero navy">{CURVES}
<div class="wrap hero-grid">
<div class="hero-copy">
<span class="eyebrow">Villa María, Córdoba</span>
<h1>Profesionales de la salud, <span>juntos en un mismo espacio</span></h1>
<p class="lead">Esentia reúne a profesionales de psicopedagogía, psicología, terapia ocupacional y crianza que trabajan de forma interdisciplinaria. También alquilamos consultorios por hora a colegas que quieran sumarse.</p>
<div class="row"><a class="btn mint" href="profesionales.html">Conocé a los profesionales {ICON_ARROW}</a><a class="btn outline-w" href="alquiler-consultorios.html">Alquilar un consultorio</a></div>
</div>
<div class="collage">
<img class="c1" src="img/esentia-cartel.jpg" alt="Cartel de Esentia en la entrada" width="1400" height="933">
<img class="c2" src="img/consultorio-sillones-turquesa.jpg" alt="Consultorio de Esentia con sillones" width="1400" height="933">
<img class="c3" src="img/tarjetas.jpg" alt="Tarjetas de Esentia" width="1280" height="605">
<img class="c4" src="img/sala-de-espera.jpg" alt="Sala de espera de Esentia" width="933" height="1400">
</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="doors">
<a class="door pac" href="profesionales.html"><span class="tag">Para pacientes y familias</span><h3>Busco un profesional</h3><p>Conocé quiénes atienden en Esentia, qué hace cada uno y escribiles directo por WhatsApp.</p><span class="go">Ver profesionales {ICON_ARROW}</span></a>
<a class="door pro" href="alquiler-consultorios.html"><span class="tag">Para profesionales de la salud</span><h3>Quiero alquilar un consultorio</h3><p>Consultorios por hora o por módulo de 4 horas. Pedí una entrevista para conocernos y ver disponibilidad.</p><span class="go">Ver precios y cómo sumarte {ICON_ARROW}</span></a>
</div></div></section>

<section class="sec tint"><div class="wrap">
<div class="sec-head"><span class="eyebrow">Especialidades</span><h2>¿Qué estás buscando?</h2><p class="lead">{N_PROF} profesionales atienden hoy en Esentia. Elegí una especialidad para ver quiénes son.</p></div>
<ul class="chips">{chips}</ul>
</div></section>

<section class="sec"><div class="wrap split">
<div class="sec-head" style="margin-bottom:0"><span class="eyebrow">Nuestro concepto</span><h2>Una estructura molecular de especialistas</h2>
<p class="lead">Como los átomos de una molécula, cada profesional aporta su disciplina y, en conjunto, forman una comunidad. Por eso trabajamos con una mirada integral e interdisciplinaria, en diálogo con las familias, las escuelas y otros profesionales.</p>
<div class="row" style="margin-top:8px"><a class="btn ghost" href="alquiler-consultorios.html#espacio">Ver el espacio</a></div></div>
<div class="trio"><img src="img/pin.jpg" alt="Pin con el logo de Esentia" loading="lazy"><img src="img/consultorio-sillones-violeta.jpg" alt="Consultorio de Esentia con sillones" loading="lazy"><img src="img/consultorio-infantil.jpg" alt="Consultorio para infancias en Esentia" loading="lazy"></div>
</div></section>

{news_home}
{ig_home}
<section class="sec tint" id="contacto"><div class="wrap">
<div class="sec-head"><span class="eyebrow">Contacto</span><h2>Visitanos en Villa María</h2><p class="lead">Para consultas de pacientes, escribile directo al profesional desde su tarjeta. Para alquilar un consultorio o consultas generales, escribinos a Esentia.</p></div>
<dl class="contact">
<div><dt>Dirección</dt><dd>{ADDR}<br>{CITY}</dd><dd><a href="{MAPS}" target="_blank" rel="noopener">Ver en Google Maps</a></dd></div>
<div><dt>WhatsApp</dt><dd>{TEL_TXT}</dd><dd><a href="{wa(WA_ESENTIA,'Hola Esentia, quiero hacer una consulta.')}" target="_blank" rel="noopener">Escribinos</a></dd></div>
<div><dt>Email</dt><dd><a href="mailto:{MAIL}">{MAIL}</a></dd><dd class="note">Lunes a viernes de 8 a 21 h</dd></div>
</dl>
</div></section>
'''

# ---------- profesionales ----------
groups_html = ""
for gid,name,sub,ks in GROUPS:
    groups_html += f'''<section class="group" id="{gid}" aria-labelledby="h-{gid}">
<div class="group-head"><h2 id="h-{gid}">{name}</h2><p>{sub}</p></div>
<div class="cards mini">{"".join(card(k) for k in ks)}</div></section>'''
persons = []
for gid,name,_,ks in GROUPS:
    for k in ks:
        p=P[k]
        persons.append({"@type":"Person","name":p["nombre"],"jobTitle":p["role"],"image":BASE+"/img/"+p["foto"],"telephone":"+"+p["wa"],"worksFor":{"@id":BASE+"/#esentia"},"knowsAbout":name})
prof_ld = [{"@context":"https://schema.org","@type":"ItemList","name":"Profesionales de Esentia","itemListElement":[{"@type":"ListItem","position":i+1,"item":x} for i,x in enumerate(persons)]}]
prof_body = f'''
<section class="sec navy-head">{CURVES}<div class="wrap">
<div class="sec-head"><span class="eyebrow">Profesionales</span><h1 style="font-size:clamp(34px,5vw,54px)">Quiénes atienden en Esentia</h1>
<p class="lead">Psicopedagogas, psicólogas, terapeuta ocupacional y acompañamiento en crianza en Villa María. Tocá cada profesional para conocer a qué se dedica y escribirle directo por WhatsApp.</p></div>
<ul class="chips">{chips.replace('profesionales.html#','#')}</ul>
</div></section>
<div class="sec" style="padding-top:48px"><div class="wrap">{groups_html}</div></div>
'''

# ---------- galería ----------
GAL=[("consultorio-sillones-turquesa","Consultorio con sillones para entrevistas","wide"),
 ("consultorio-infantil","Consultorio con mesa de trabajo","tall"),
 ("sala-de-espera","Sala de espera","tall"),
 ("consultorio-sillones-violeta","Consultorio con sillones y alfombra","tall"),
 ("consultorio-luz-natural","Consultorio con luz natural","wide"),
 ("consultorio-escritorio-infantil","Consultorio con mobiliario para infancias","tall"),
 ("sala-sillones-rosa","Sillones junto a la ventana","tall"),
 ("consultorio-mesa-azul","Mesa de trabajo","tall"),
 ("consultorio-rincon","Rincón con sillón y mesa auxiliar","tall")]
gal_html='<div class="gallery">'+''.join(f'<figure class="{c}"><a href="img/{f}.jpg" target="_blank" rel="noopener"><img src="img/{f}.jpg" alt="{t} en Esentia, Villa María" loading="lazy"></a><figcaption>{t}</figcaption></figure>' for f,t,c in GAL)+'</div>'

# ---------- alquiler ----------
msg_alq = "Hola Esentia, soy profesional de la salud y quiero coordinar una entrevista para alquilar un consultorio. Mi profesión es: "
alq_ld = [{"@context":"https://schema.org","@type":"Service","name":"Alquiler de consultorios por hora","provider":{"@id":BASE+"/#esentia"},"areaServed":"Villa María, Córdoba","serviceType":"Alquiler de consultorios para profesionales de la salud",
  "offers":[{"@type":"Offer","name":n,"price":str(p),"priceCurrency":"ARS"} for n,p in [("Hora suelta Grupo 1",6500),("Módulo 4 h Grupo 1",24000),("Hora suelta Grupo 2",6000),("Módulo 4 h Grupo 2",22000),("Hora suelta Grupo 3",5500),("Módulo 4 h Grupo 3",20000)]]}]
alq_body = f'''
<section class="hero navy">{CURVES}
<div class="wrap hero-grid"><div class="hero-copy">
<span class="eyebrow">Alquiler de consultorios · Villa María</span>
<h1>Tu consultorio por hora, en una <span>comunidad de salud</span></h1>
<p class="lead">Consultorios equipados para profesionales de la salud, por hora suelta o por módulo de 4 horas, de lunes a viernes de 8 a 21 h. Sin contratos largos y con un precio que baja cuantas más horas usás.</p>
<div class="row"><a class="btn wa" href="{wa(WA_ESENTIA,msg_alq)}" target="_blank" rel="noopener">{ICON_CHAT} Pedir una entrevista</a><a class="btn outline-w" href="#precios">Ver precios</a></div>
</div><img class="hero-photo" src="img/consultorio-luz-natural.jpg" alt="Consultorio de Esentia con mesa de trabajo y luz natural" width="1400" height="933"></div></section>

<section class="sec"><div class="wrap">
<div class="sec-head"><span class="eyebrow">Cómo sumarte</span><h2>Primero nos conocemos</h2><p class="lead">Esentia es una comunidad interdisciplinaria. Antes de confirmar un alquiler hacemos una entrevista para conocer tu profesión y tu forma de trabajo, y para ver qué días y horarios tenemos disponibles para ofrecerte.</p></div>
<ol class="steps">
<li><h3>Escribinos</h3><p>Contanos por WhatsApp tu profesión y qué días y horarios buscás.</p></li>
<li class="key"><h3>Entrevista previa</h3><p>Coordinamos un encuentro para conocernos y evaluar juntos si Esentia es el espacio para tu práctica.</p></li>
<li><h3>Disponibilidad</h3><p>Te ofrecemos los consultorios y horarios libres, y confirmamos tu reserva.</p></li>
<li><h3>Empezás a atender</h3><p>Recibís tu llave y manejás tu propia agenda. Pagás a mes vencido.</p></li>
</ol>
</div></section>

<section class="sec tint" id="espacio"><div class="wrap">
<div class="sec-head"><span class="eyebrow">El espacio</span><h2>Conocé los consultorios</h2><p class="lead">Siete consultorios con estilos distintos: algunos pensados para infancias, otros para entrevistas y terapia de adultos.</p></div>
{gal_html}
<h3 class="subh">Lo que incluye</h3>
<div class="feat">
<div><h3>Consultorios equipados</h3><p>Escritorio, sillas y aire acondicionado en cada consultorio.</p></div>
<div><h3>Espacios comunes</h3><p>Sala de espera, baño y cocina para vos y tus pacientes.</p></div>
<div><h3>Servicios incluidos</h3><p>El valor del alquiler ya incluye todos los servicios del espacio.</p></div>
<div><h3>Acceso con llave</h3><p>Entrás y salís en tus horarios confirmados, con tu propia llave.</p></div>
<div><h3>Difusión</h3><p>Promocionamos los servicios de cada disciplina en nuestra web y redes.</p></div>
<div><h3>Flexibilidad</h3><p>Podés sumar horas durante el mes o pedir un turno excepcional.</p></div>
</div>
</div></section>

<section class="sec band" id="precios"><div class="wrap">
<div class="sec-head"><span class="eyebrow">Precios desde el 1 de octubre de 2026</span><h2>Cuantas más horas reservás, menos pagás por hora</h2><p class="lead">Tu grupo se define por el total de horas que reservás en el mes, y todas las horas de ese mes se cobran al precio de tu grupo.</p></div>
<div class="plans">
<div class="plan"><div><div class="t">Grupo 1</div><h3>Flexible</h3><div class="r">Menos de 15 h por mes</div></div><div class="ln"><span class="k">Hora suelta</span><span class="v">$6.500</span></div><div class="ln"><span class="k">Módulo 4 h</span><span class="v">$24.000<small>$6.000 por hora</small></span></div></div>
<div class="plan"><div><div class="t">Grupo 2</div><h3>Frecuente</h3><div class="r">De 15 a 30 h por mes</div></div><div class="ln"><span class="k">Hora suelta</span><span class="v">$6.000</span></div><div class="ln"><span class="k">Módulo 4 h</span><span class="v">$22.000<small>$5.500 por hora</small></span></div></div>
<div class="plan best"><span class="badge">Mejor precio</span><div><div class="t">Grupo 3</div><h3>Estable</h3><div class="r">Más de 30 h por mes</div></div><div class="ln"><span class="k">Hora suelta</span><span class="v">$5.500</span></div><div class="ln"><span class="k">Módulo 4 h</span><span class="v">$20.000<small>$5.000 por hora</small></span></div></div>
</div>
<div class="fine"><span>Módulo = 4 horas seguidas en un mismo día.</span><span>Los feriados no se cobran.</span><span>Pago a mes vencido: del 1 al 10 precio base, del 11 al 20 +5%, del 21 en adelante +10%.</span></div>

<div class="calc">
<form id="calcForm" novalidate>
<div><h3>Calculá cuánto pagarías</h3><p class="note">Estimación para un mes de 4 semanas con horarios fijos.</p></div>
<div class="field"><label for="dias">Días por semana</label><div class="stepper"><button type="button" data-t="dias" data-d="-1" aria-label="Restar un día">−</button><input id="dias" type="number" inputmode="numeric" min="1" max="5" step="1" value="2"><button type="button" data-t="dias" data-d="1" aria-label="Sumar un día">+</button></div></div>
<div class="field"><label for="horas">Horas seguidas cada día</label><div class="stepper"><button type="button" data-t="horas" data-d="-0.5" aria-label="Restar media hora">−</button><input id="horas" type="number" inputmode="decimal" min="0.5" max="13" step="0.5" value="4"><button type="button" data-t="horas" data-d="0.5" aria-label="Sumar media hora">+</button></div></div>
</form>
<div class="result" aria-live="polite"><span class="grp" id="rGrp">Grupo 3 · Estable</span><div class="big" id="rTotal">$ 160.000</div>
<dl><dt>Horas en el mes</dt><dd id="rHs">32 h</dd><dt>Costo por día</dt><dd id="rDia">$ 20.000</dd><dt>Promedio por hora</dt><dd id="rHora">$ 5.000</dd></dl>
<p class="note">Si el mes tiene 5 semanas de tus días, también se cobran. Precio base pagando del 1 al 10.</p></div>
</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head"><span class="eyebrow">Dinámica de trabajo</span><h2>Lo que conviene saber</h2></div>
<ul class="rules">
<li>Los días y horarios se confirman antes de empezar. Solo se usa el espacio con disponibilidad confirmada.</li>
<li>Podés sumar horas durante el mes, consultando antes la disponibilidad.</li>
<li>Para quitar un día u horario confirmado, avisá antes del cambio de mes.</li>
<li>La reserva se abona aunque el paciente no asista.</li>
<li>No hay secretaría: cada profesional lleva su propia agenda.</li>
<li>Los consultorios son compartidos: cuidamos el espacio y los materiales de cada colega.</li>
<li>Para dejar Esentia, avisá con un mes de anticipación.</li>
<li>No derivamos pacientes, pero sí difundimos los servicios de cada disciplina.</li>
</ul>
<div class="cta" style="margin-top:56px"><div><h2 style="font-size:clamp(24px,3vw,32px)">¿Querés atender en Esentia?</h2><p style="margin-top:8px">Escribinos con tu profesión y los horarios que buscás. Coordinamos una entrevista y te contamos qué disponibilidad tenemos.</p></div>
<div class="row"><a class="btn wa" href="{wa(WA_ESENTIA,msg_alq)}" target="_blank" rel="noopener">{ICON_CHAT} Pedir entrevista</a><a class="btn ghost" href="mailto:{MAIL}?subject=Alquiler%20de%20consultorio">Escribir un email</a></div></div>
</div></section>
'''

pages = {
 "index.html": page("Esentia | Comunidad Profesional de Salud en Villa María",
   "Psicopedagogía, psicología, terapia ocupacional y crianza en Villa María, Córdoba. Conocé a los profesionales de Esentia y alquilá consultorios por hora.",
   "/", "index.html", index_body),
 "profesionales.html": page("Profesionales de la salud en Villa María | Esentia",
   "Psicopedagogas, psicólogas, terapeuta ocupacional y acompañamiento en crianza en Villa María. Conocé a cada profesional de Esentia y escribile por WhatsApp.",
   "/profesionales.html", "profesionales.html", prof_body, prof_ld),
 "alquiler-consultorios.html": page("Alquiler de consultorios por hora en Villa María | Esentia",
   "Alquilá consultorios equipados por hora o por módulo en Villa María. Precios por grupo según horas mensuales. Pedí una entrevista por WhatsApp.",
   "/alquiler-consultorios.html", "alquiler-consultorios.html", alq_body, alq_ld, scripts=True),
 "noticias.html": page("Noticias y artículos | Esentia Villa María",
   "Novedades y artículos del equipo de Esentia sobre salud, aprendizaje y crianza en Villa María.",
   "/noticias.html", "noticias.html", news_body),
}
if IG_SCRIPT: pages["index.html"] = pages["index.html"].replace("\n</body>", IG_SCRIPT + "\n</body>")
POST_PAGES = {x["slug"]: post_page(x) for x in POSTS}
os.makedirs(os.path.join(OUT, "noticias"), exist_ok=True)
for sl, h in POST_PAGES.items(): open(os.path.join(OUT, "noticias", sl + ".html"), "w", encoding="utf-8").write(h)
for fn, html in pages.items():
    open(os.path.join(OUT, fn), "w").write(html)
os.makedirs(os.path.join(OUT,"profesionales"),exist_ok=True)
SLUGS=list(dict.fromkeys(slug(k) for k in P))
DETAIL={sl:detail(sl) for sl in SLUGS}
for sl,h in DETAIL.items(): open(os.path.join(OUT,"profesionales",sl+".html"),"w").write(h)

open(os.path.join(OUT,"robots.txt"),"w").write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
today = date.today().isoformat()
urls = "".join(f"<url><loc>{BASE}{p}</loc><lastmod>{today}</lastmod></url>" for p in ["/","/profesionales.html","/alquiler-consultorios.html","/noticias.html"]+[f"/profesionales/{x}.html" for x in SLUGS]+[f"/noticias/{x}.html" for x in POST_PAGES])
open(os.path.join(OUT,"sitemap.xml"),"w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
open(os.path.join(OUT,"_headers"),"w").write("""/*
  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=()
  Content-Security-Policy: default-src 'self'; img-src 'self' data: https:; media-src 'self' https:; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; script-src 'self' https://w.behold.so; connect-src 'self' https://*.behold.so; frame-ancestors 'none'; base-uri 'self'; form-action 'none'; upgrade-insecure-requests
""")
open(os.path.join(OUT,"404.html"),"w").write(page("Página no encontrada | Esentia","Esta página no existe.","/404.html","",
  '<section class="sec"><div class="wrap"><div class="sec-head"><h1>No encontramos esta página</h1><p class="lead">Puede que el enlace haya cambiado.</p><div class="row"><a class="btn primary" href="index.html">Ir al inicio</a></div></div></div></section>').replace('content="index,follow"','content="noindex"'))

# ---------- preview (solo para la vista previa, no se usa en Netlify) ----------
PV = os.environ.get("ESENTIA_PREVIEW")
if PV:
    css = open(os.path.join(OUT,"styles.css")).read()
    js = open(os.path.join(OUT,"main.js")).read()
    os.makedirs(PV+"/img", exist_ok=True)
    for f in os.listdir(os.path.join(OUT,"img")): shutil.copy(os.path.join(OUT,"img",f), PV+"/img/"+f)
    shutil.copy(os.path.join(OUT,"favicon.png"),PV+"/favicon.png")
    for fn, html in pages.items():
        h = html.replace('<link rel="stylesheet" href="styles.css">', f"<style>{css}</style>").replace('<script src="main.js" defer></script>', f"<script>{js}</script>")
        if fn == "index.html":
            h = re.sub(r'<!doctype html>\s*<html[^>]*>\s*<head>\s*','',h)
            h = h.replace('</head>\n<body>\n','').replace('\n</body>\n</html>\n','')
            h = h.replace('<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n','')
        open(PV+"/"+fn,"w").write(h)
    os.makedirs(PV+"/profesionales",exist_ok=True)
    for sl,h in DETAIL.items():
        open(PV+"/profesionales/"+sl+".html","w").write(h.replace('<link rel="stylesheet" href="../styles.css">', f"<style>{css}</style>"))

    os.makedirs(PV+"/noticias",exist_ok=True)
    for sl,h in POST_PAGES.items():
        open(PV+"/noticias/"+sl+".html","w").write(h.replace('<link rel="stylesheet" href="../styles.css">', f"<style>{css}</style>"))
    if os.path.isdir("media"): shutil.copytree("media", PV+"/media", dirs_exist_ok=True)
print(f"ok: {len(pages)} páginas, {len(SLUGS)} perfiles, {len(POST_PAGES)} noticias")
