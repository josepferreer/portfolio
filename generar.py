"""Genera el portfolio a partir de proyectos.json.

Uso (desde esta carpeta):
    python generar.py

Crea:
  - index.html          a partir de plantillas/portada.html, con una tarjeta por proyecto
  - <id>.html           una página por proyecto, con los bloques que tenga

No edites index.html ni las páginas de proyecto a mano: se sobrescriben.
Lo que se edita es proyectos.json, plantillas/portada.html y estilos.css.
"""
import sys
# la consola de Windows no sabe escribir algunos caracteres (p. ej. japonés): que no rompa el script
sys.stdout.reconfigure(errors="replace")
sys.stderr.reconfigure(errors="replace")
import json
import re
from html import escape
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
DATOS = json.loads((RAIZ / "proyectos.json").read_text(encoding="utf-8"))
PROYECTOS = DATOS["proyectos"]
# ---------- Archivo: imágenes sueltas ----------
# Basta con soltar imágenes (PNG, JPG o WEBP, de cualquier tamaño) en img/archivo/.
# El script hace una copia ligera de cada una en img/archivo/web/ (JPG, lado largo 1600 px)
# y la saca en la portada, las más nuevas primero. El nombre que se ve sale del nombre del
# archivo: «pego-trail-21k.png» -> «Pego trail 21k». Los originales no se suben a git.
# En proyectos.json se puede poner a mano: "archivo": [{"imagen": "...", "nombre": "...", "anio": 2026}]
CARPETA_ARCHIVO = RAIZ / "img" / "archivo"
FORMATOS = {".png", ".jpg", ".jpeg", ".webp"}


def _slug(texto):
    """Nombre de archivo seguro. Si el nombre no tiene letras latinas (p. ej. «ゴジラ»), uno fijo sacado de él."""
    import hashlib
    import unicodedata
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t or "imagen-" + hashlib.md5(texto.encode("utf-8")).hexdigest()[:8]


def _nombre_bonito(stem):
    t = re.sub(r"[-_]+", " ", stem).strip()
    return t[:1].upper() + t[1:]


def archivo_automatico(ya_puestas):
    """Lee img/archivo/, prepara la copia web de cada imagen nueva o cambiada y devuelve sus fichas."""
    if not CARPETA_ARCHIVO.is_dir():
        return []
    originales = sorted((f for f in CARPETA_ARCHIVO.iterdir() if f.is_file() and f.suffix.lower() in FORMATOS),
                        key=lambda f: f.stat().st_mtime, reverse=True)
    web = CARPETA_ARCHIVO / "web"
    if not originales and not web.is_dir():
        return []
    from PIL import Image
    web.mkdir(exist_ok=True)
    fichas = []
    for f in originales:
        destino = web / (_slug(f.stem) + ".jpg")
        ruta = destino.relative_to(RAIZ).as_posix()
        if f.relative_to(RAIZ).as_posix() in ya_puestas or ruta in ya_puestas:
            continue
        if not destino.exists() or destino.stat().st_mtime < f.stat().st_mtime:
            im = Image.open(f)
            im.thumbnail((1600, 1600), Image.LANCZOS)
            if im.mode in ("RGBA", "LA", "P"):
                im = im.convert("RGBA")
                fondo = Image.new("RGB", im.size, "#ECE8E3")
                fondo.paste(im, mask=im.getchannel("A"))
                im = fondo
            im.convert("RGB").save(destino, quality=84, optimize=True, progressive=True)
            print(f"  archivo: {f.name} -> {ruta} ({destino.stat().st_size // 1024} KB)")
        fichas.append({"imagen": ruta, "nombre": _nombre_bonito(f.stem), "_fecha": f.stat().st_mtime})
    # imágenes puestas directamente en web/ (por ejemplo, subidas desde la web de GitHub), sin original
    hechas = {_slug(f.stem) + ".jpg" for f in originales}
    for c in web.iterdir():
        ruta = c.relative_to(RAIZ).as_posix()
        if c.is_file() and c.suffix.lower() in FORMATOS and c.name not in hechas and ruta not in ya_puestas:
            fichas.append({"imagen": ruta, "nombre": _nombre_bonito(c.stem), "_fecha": c.stat().st_mtime})
    fichas.sort(key=lambda x: x.pop("_fecha"), reverse=True)
    return fichas


ARCHIVO = DATOS.get("archivo", [])
ARCHIVO = ARCHIVO + archivo_automatico({a["imagen"] for a in ARCHIVO})

FUENTES_BASE = "family=Instrument+Sans:ital,wght@0,400..700;1,400..700&family=Inter+Tight:wght@400;700;800"


# ---------- utilidades ----------

def e(texto):
    return escape(str(texto), quote=True)


def num(n):
    return f"{n:02d}"


def claro(hex_):
    """True si el color es claro (para elegir el color del texto encima)."""
    h = hex_.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b > 0.6


def muy_claro(hex_):
    h = hex_.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b > 0.9


def svg_con_ids_propios(ruta, prefijo):
    """Lee un SVG y renombra sus ids para que no choquen con los de otro SVG de la misma página."""
    s = (RAIZ / ruta).read_text(encoding="utf-8")
    for i in set(re.findall(r'id="([^"]+)"', s)):
        s = s.replace(f'id="{i}"', f'id="{prefijo}-{i}"').replace(f"url(#{i})", f"url(#{prefijo}-{i})")
    return s


def logo_como_simbolo(ruta, id_simbolo):
    s = svg_con_ids_propios(ruta, id_simbolo)
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    dentro = s[s.index(">", s.index("<svg")) + 1:s.rindex("</svg>")]
    return f'<symbol id="{id_simbolo}" viewBox="{vb}">{dentro}</symbol>', vb


def enlace_fuentes(extra_google=(), locales=()):
    familias = FUENTES_BASE + "".join("&family=" + g.replace(" ", "+") for g in extra_google)
    html = (
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{familias}&display=swap">'
    )
    if locales:
        caras = "".join(f'@font-face{{font-family:"{n}";src:url({r})}}' for n, r in locales)
        html += f"\n<style>{caras}</style>"
    return html


# ---------- bloques opcionales ----------

def logo_texto(b, p):
    """Logo hecho con texto (sin SVG): una o varias piezas, cada una con su letra."""
    partes = "".join(f'<span style="{t["css"]}">{e(t["texto"])}</span>' for t in b["logo_texto"])
    return f'<span class="logo-texto" role="img" aria-label="{e(p["titulo"])}">{partes}</span>'


def bloque_identidad(b, p, simbolos):
    if b.get("logo"):
        id_logo = f"logo-{p['id']}"
        simbolo, vb = logo_como_simbolo(b["logo"], id_logo)
        simbolos.append(simbolo)
        dibujo = f'<svg viewBox="{vb}" role="img" aria-label="{e(p["titulo"])}"><use href="#{id_logo}"/></svg>'
    else:
        dibujo = logo_texto(b, p)

    figs = []
    for v in b["versiones"]:
        vars_ = "".join(f";{k}:{val}" for k, val in v.get("variables", {}).items())
        borde = " borde" if muy_claro(v["fondo"]) else ""
        figs.append(
            f'<figure><div class="fondo{borde}" style="background:{v["fondo"]};color:{v["color"]}{vars_}">'
            f'{dibujo}</div>'
            f'<figcaption class="mayus">{e(v["nombre"])}</figcaption></figure>'
        )
    if b.get("icono"):
        ic = b["icono"]
        borde = " borde" if muy_claro(ic.get("fondo", "#ffffff")) else ""
        figs.append(
            f'<figure><div class="fondo icono{borde}" style="background:{ic.get("fondo", "#fff")}">'
            f'{svg_con_ids_propios(ic["archivo"], "icono-" + p["id"]) if ic["archivo"].endswith(".svg") else f"<img src=\"{ic['archivo']}\" alt=\"\">"}</div>'
            f'<figcaption class="mayus">Icono</figcaption></figure>'
        )
    html = f'<div class="logos">{"".join(figs)}</div>'

    if b.get("colores"):
        cs = "".join(
            f'<div class="{"borde" if muy_claro(c["hex"]) else ""}" style="background:{c["hex"]};color:{"#141414" if claro(c["hex"]) else "#F6F3E2"}">'
            f'<b>{e(c["nombre"])}</b>{c["hex"].upper()}</div>'
            for c in b["colores"]
        )
        html += f'<div class="sub"><span class="mayus">Color</span><div class="colores">{cs}</div></div>'

    if b.get("tipografias"):
        ts = "".join(
            f'<div><span class="muestra{" peque" if t.get("peque") else ""}" style="{t["css"]}">{e(t["muestra"])}</span>'
            f'<span class="dato mayus"><b>{e(t["nombre"])}</b>{e(t["uso"])}</span></div>'
            for t in b["tipografias"]
        )
        html += f'<div class="sub"><span class="mayus">Tipografía</span><div class="tipos">{ts}</div></div>'
    return "Identidad", html


def bloque_piezas(b, p, simbolos):
    figs = "".join(
        f'<figure><img src="{it["imagen"]}" alt="{e(it["nombre"])}" loading="lazy">'
        f'<figcaption class="mayus">{e(it["nombre"])}</figcaption></figure>'
        for it in b["items"]
    )
    return b["titulo"], f'<div class="piezas {b.get("formato", "a3")}">{figs}</div>'


def bloque_pantallas(b, p, simbolos):
    html = ""
    if b.get("enlace"):
        palabra = "la web" if b["titulo"].lower() == "web" else b["titulo"].lower()
        html += (f'<p class="ir-web"><a class="enlace mayus" href="{b["enlace"]}" target="_blank" rel="noopener">Ver {e(palabra)}</a>'
                 f'<span class="mayus">{e(b.get("texto_enlace", ""))}</span></p>')
    movil = f'<img class="movil" src="{b["movil"]}" alt="Versión de móvil" loading="lazy">' if b.get("movil") else ""
    html += (f'<div class="p-pantallas{"" if movil else " sin-movil"}">'
             f'<img src="{b["escritorio"]}" alt="Versión de ordenador" loading="lazy">{movil}</div>')
    if b.get("secciones"):
        secs = "".join(
            f'<figure><img src="{s["imagen"]}" alt="{e(s["nombre"])}" loading="lazy"><figcaption class="mayus">{e(s["nombre"])}</figcaption></figure>'
            for s in b["secciones"]
        )
        html += f'<div class="secciones">{secs}</div>'
    return b["titulo"], html


BLOQUES = {"identidad": bloque_identidad, "piezas": bloque_piezas, "pantallas": bloque_pantallas}


# ---------- página de proyecto ----------

VISOR = """
<dialog class="visor" aria-label="Pieza ampliada">
  <button class="redondo cerrar" type="button" aria-label="Cerrar"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M5 5l14 14M19 5L5 19"/></svg></button>
  <button class="redondo ant" type="button" aria-label="Anterior"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M15 5l-7 7 7 7"/></svg></button>
  <figure><img alt=""></figure>
  <button class="redondo sig" type="button" aria-label="Siguiente"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M9 5l7 7-7 7"/></svg></button>
  <p class="pie mayus"><span class="nombre-pieza"></span><span class="cuenta"></span></p>
</dialog>
<script src="visor.js"></script>"""


def pagina_proyecto(p, i):
    simbolos = []
    secciones = []
    for n, b in enumerate(p["bloques"], 1):
        titulo, cuerpo = BLOQUES[b["tipo"]](b, p, simbolos)
        secciones.append(
            f'  <section class="p-bloque">\n    <div class="cab"><h2 class="titulo">{e(titulo)}</h2>'
            f'<span class="mayus num">{num(n)}</span></div>\n    {cuerpo}\n  </section>'
        )

    # el enlace va en la ficha solo si ningún bloque lo lleva ya
    enlace_en_bloque = any(b.get("enlace") for b in p["bloques"])
    fila_enlace = ""
    if p.get("enlace") and not enlace_en_bloque:
        fila_enlace = (f'<div style="grid-column:1 / -1"><dt class="mayus">Enlace</dt>'
                       f'<dd><a class="enlace" href="{p["enlace"]}" target="_blank" rel="noopener">Ver el proyecto</a></dd></div>')

    # siguiente: solo si hay más de un proyecto
    if len(PROYECTOS) > 1:
        sig = PROYECTOS[(i + 1) % len(PROYECTOS)]
        siguiente = (f'<a class="p-siguiente" href="{sig["id"]}.html"><span class="mayus gris">Siguiente proyecto'
                     f'<span class="nombre">{e(sig["titulo"])}</span></span><span class="mayus">Ver</span></a>')
    else:
        siguiente = '<div class="p-siguiente"><span></span><a class="mayus" href="index.html#trabajos">Todos los trabajos</a></div>'

    google, locales = [], []
    for b in p["bloques"]:
        for t in b.get("tipografias", []):
            if t.get("google"):
                google.append(t["google"])
            if t.get("local"):
                locales.append((re.search(r"font-family:'?([^';]+)", t["css"]).group(1), t["local"]))

    ficha = "".join([
        f'<div><dt class="mayus">Tipo</dt><dd>{e(p["tipo"])}</dd></div>',
        f'<div><dt class="mayus">Año</dt><dd>{p["anio"]}</dd></div>',
        f'<div><dt class="mayus">Qué hice</dt><dd>{"<br>".join(e(x) for x in p["hice"])}</dd></div>',
        f'<div><dt class="mayus">Con</dt><dd>{"<br>".join(e(x) for x in p["con"])}</dd></div>',
        fila_enlace,
        # redes del proyecto (opcional): "redes": [{"nombre": "Instagram", "url": "..."}]
        (f'<div style="grid-column:1 / -1"><dt class="mayus">Redes</dt><dd>'
         + "<br>".join(f'<a class="enlace" href="{r["url"]}" target="_blank" rel="noopener">{e(r["nombre"])}</a>' for r in p["redes"])
         + '</dd></div>') if p.get("redes") else "",
    ])
    texto = "".join(f"<p>{e(t)}</p>" for t in p["texto"])
    simbolos_html = f'<svg width="0" height="0" style="position:absolute" aria-hidden="true">{"".join(simbolos)}</svg>\n' if simbolos else ""

    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(p["titulo"])} · josepferrer</title>
<meta name="description" content="{e(p["lema"])}">
{enlace_fuentes(google, locales)}
<link rel="icon" href="img/favicon.svg" type="image/svg+xml">
<link rel="icon" href="img/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="img/favicon-180.png">
<link rel="stylesheet" href="estilos.css">
<script>if(!matchMedia("(prefers-reduced-motion: reduce)").matches)document.documentElement.classList.add("mov")</script>
<script src="movimiento.js" defer></script>
</head>
<body>
<!-- Página generada por generar.py a partir de proyectos.json: no editar a mano -->
{simbolos_html}
<header class="cab-proy">
  <a href="index.html" aria-label="Volver al inicio"><img class="marca" src="img/josepferrer.svg" alt="josepferrer"></a>
  <nav class="mayus"><a href="index.html#trabajos">Trabajos</a></nav>
</header>

<main>
  <div class="p-cab">
    <h1 style="view-transition-name:titulo-{p['id']}">{e(p["titulo"])}</h1>
    <span class="mayus meta">{num(i + 1)}<br>{p["anio"]}</span>
    <p class="lema">{e(p["lema"])}</p>
  </div>

  <div class="p-ficha">
    <dl>{ficha}</dl>
    <div class="texto">{texto}</div>
  </div>

{chr(10).join(secciones)}

  {siguiente}
</main>
{VISOR}
</body>
</html>
"""


# ---------- portada ----------

def cubierta(p):
    t = p["tarjeta"]
    fondo = t.get("fondo", "var(--linea)")
    if t["tipo"] == "carteles":
        imgs = "".join(f'<img src="{s}" alt="" loading="lazy">' for s in t["imagenes"])
        return f'<div class="cubierta" style="background:{fondo}"><div class="fila">{imgs}</div></div>'
    if t["tipo"] == "pantalla":
        return f'<div class="cubierta" style="background:{fondo}"><img class="pantalla" src="{t["imagen"]}" alt="" loading="lazy"></div>'
    if t["tipo"] == "foto":
        return f'<div class="cubierta foto"><img src="{t["imagen"]}" alt="" loading="lazy"></div>'
    if t["tipo"] == "logo":
        b = next(b for b in p["bloques"] if b["tipo"] == "identidad")
        v = b["versiones"][0]
        vars_ = "".join(f";{k}:{val}" for k, val in v.get("variables", {}).items())
        s = svg_con_ids_propios(b["logo"], "tarjeta-" + p["id"]) if b.get("logo") else logo_texto(b, p)
        return f'<div class="cubierta" style="background:{v["fondo"]};color:{v["color"]}{vars_}">{s}</div>'
    raise ValueError(f'tipo de tarjeta desconocido: {t["tipo"]}')


def portada():
    tarjetas = []
    for i, p in enumerate(PROYECTOS):
        grande = " grande" if i == 0 else ""
        tarjetas.append(
            f'<a class="tarjeta{grande}" href="{p["id"]}.html">{cubierta(p)}'
            f'<div class="pie-proy mayus"><span>{num(i + 1)}</span><span class="nombre" style="view-transition-name:titulo-{p['id']}">{e(p["titulo"])}</span><span>{p["anio"]}</span></div>'
            f'<p class="etiquetas mayus">{" · ".join(e(x) for x in p["hice"])}</p></a>'
        )
    plantilla = (RAIZ / "plantillas" / "portada.html").read_text(encoding="utf-8")
    html = plantilla.replace("{{TRABAJOS}}", '<div class="tarjetas">\n      ' + "\n      ".join(tarjetas) + "\n    </div>")
    # si alguna tarjeta enseña un logo de texto, la portada necesita sus fuentes
    google = [t["google"] for p in PROYECTOS if p["tarjeta"]["tipo"] == "logo"
              for b in p["bloques"] if b["tipo"] == "identidad" for t in b.get("tipografias", []) if t.get("google")]
    html = html.replace("{{FUENTES}}", enlace_fuentes(google) if google else "")
    html = html.replace("{{ARCHIVO}}", archivo())
    html = html.replace("{{NAV_ARCHIVO}}", '<a href="#archivo">Archivo</a>' if ARCHIVO else "")
    html = html.replace("{{VISOR}}", VISOR if ARCHIVO else "")
    return "<!-- Página generada por generar.py: edita plantillas/portada.html -->\n" + html


def archivo():
    """Sección «Archivo» de la portada: imágenes sueltas, en mosaico y sin recortar. Si no hay ninguna, no sale."""
    if not ARCHIVO:
        return ""
    figs = []
    for a in ARCHIVO:
        pie = e(a["nombre"]) + (f' · {a["anio"]}' if a.get("anio") else "")
        figs.append(f'<figure><img src="{a["imagen"]}" alt="{e(a["nombre"])}" loading="lazy">'
                    f'<figcaption class="mayus">{pie}</figcaption></figure>')
    return ('<!-- Archivo: imágenes sueltas (lista «archivo» de proyectos.json) -->\n'
            '  <section id="archivo">\n    <div class="cab"><h2 class="titulo">Archivo</h2></div>\n'
            f'    <div class="archivo">{"".join(figs)}</div>\n  </section>\n')


# ---------- comprobaciones y escritura ----------

def comprobar():
    faltan = []
    ids = set()
    for p in PROYECTOS:
        if p["id"] in ids:
            faltan.append(f'id repetido: {p["id"]}')
        ids.add(p["id"])
        rutas = re.findall(r'"((?:img|fuentes)/[^"]+)"', json.dumps(p, ensure_ascii=False))
        faltan += [f'{p["id"]}: falta {r}' for r in rutas if not (RAIZ / r).exists()]
        for b in p["bloques"]:
            if b["tipo"] not in BLOQUES:
                faltan.append(f'{p["id"]}: bloque desconocido «{b["tipo"]}»')
    for a in ARCHIVO:
        if not (RAIZ / a["imagen"]).exists():
            faltan.append(f'archivo: falta {a["imagen"]}')
    if faltan:
        raise SystemExit("No se ha generado nada:\n  " + "\n  ".join(faltan))


if __name__ == "__main__":
    comprobar()
    (RAIZ / "index.html").write_text(portada(), encoding="utf-8")
    for i, p in enumerate(PROYECTOS):
        (RAIZ / f'{p["id"]}.html').write_text(pagina_proyecto(p, i), encoding="utf-8")
    print(f"Hecho: index.html y {len(PROYECTOS)} página(s) de proyecto:", ", ".join(p["id"] + ".html" for p in PROYECTOS))
