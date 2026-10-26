"""Versión 1: el sitio actual de Wix con su misma estética, corregido y fuera de Wix.

Lee los datos de ../estudio.json (fuente única).
Uso:
  python3 build.py            vista previa en preview/ (se abre sin servidor)
  python3 build.py --final    sitio en dist/ listo para Netlify
"""
import html
import json
import shutil
import sys
from pathlib import Path

RAIZ = Path(__file__).parent
DATOS = json.loads((RAIZ.parent / "estudio.json").read_text(encoding="utf-8"))
FINAL = "--final" in sys.argv
SALIDA = RAIZ / ("dist" if FINAL else "preview")
DOMINIO = "https://www.estudiograciosi.com"
NOMBRE = DATOS["nombre"]


def esc(v):
    return html.escape(str(v), quote=True)


def es_pendiente(v):
    return isinstance(v, str) and v.startswith("[PENDIENTE")


def dato(v):
    return f'<span class="pendiente">{esc(v)}</span>' if es_pendiente(v) else esc(v)


def enlace(destino):
    """'/' y '/contacto' en el sitio final; index.html y contacto.html en la vista previa."""
    if FINAL:
        return destino if destino == "/" else destino + "/"
    return "index.html" if destino == "/" else destino.strip("/") + ".html"


def asset(ruta):
    return "/" + ruta if FINAL else ruta


def telefono_href(numero):
    return "".join(c for c in numero if c.isdigit() or c == "+")


def json_ld():
    dom = DATOS["domicilio"]
    ld = {
        "@context": "https://schema.org",
        "@type": "LegalService",
        "name": NOMBRE,
        "url": DOMINIO,
        "email": DATOS["correos"][0],
        "telephone": [t["numero"] for t in DATOS["telefonos"]],
        "address": {"@type": "PostalAddress", "streetAddress": dom["calle"], "addressLocality": dom["ciudad"],
                    "addressRegion": dom["provincia"], "addressCountry": "AR"},
        "areaServed": [{"@type": "State", "name": p["nombre"]} for p in DATOS["provincias"]],
        "knowsAbout": [a["nombre"] for a in DATOS["areasDePractica"]],
    }
    if not es_pendiente(dom["codigoPostal"]):
        ld["address"]["postalCode"] = dom["codigoPostal"]
    return json.dumps(ld, ensure_ascii=False).replace("</", "<\\/")


MENU = [
    # (destino, texto)
    ("/#estudio", "El Estudio"),
    ("/#areas", "Áreas de práctica"),
    ("/#cobertura", "Cobertura"),
    ("/contacto", "Contacto"),
]


def href(destino):
    ruta, _, ancla = destino.partition("#")
    return enlace(ruta or "/") + (f"#{ancla}" if ancla else "")


def encabezado(actual):
    items = "".join(
        f'<li><a href="{href(d)}"' + (' aria-current="page"' if d == actual else "") + f">{esc(t)}</a></li>"
        for d, t in MENU
    )
    return f"""<header class="encabezado"><div class="contenedor">
  <a class="marca" href="{enlace('/')}" aria-label="{esc(NOMBRE)} Abogados, inicio">
    <span class="eg" aria-hidden="true">EG</span><span class="linea-v" aria-hidden="true"></span>
    <span class="nombre" aria-hidden="true"><span>Estudio</span><span>Graciosi</span><span>Abogados</span></span>
  </a>
  <button type="button" class="abrir-menu" aria-expanded="false" aria-controls="navegacion">Menú</button>
  <nav id="navegacion" aria-label="Menú principal"><ul class="menu">{items}</ul></nav>
</div></header>"""


def lineas_contacto():
    dom = DATOS["domicilio"]
    cp = dom["codigoPostal"]
    lineas = [f"{esc(dom['calle'])}, {dato(cp)} {esc(dom['ciudad'])}, {esc(dom['provincia'])}."]
    lineas += [f'Email: <a href="mailto:{esc(c)}">{esc(c)}</a>' for c in DATOS["correos"]]
    for t in DATOS["telefonos"]:
        linea = f'Tel: <a href="tel:{telefono_href(t["numero"])}">{esc(t["numero"])}</a>'
        if t["whatsapp"] is True:
            linea += f' · <a href="https://wa.me/{telefono_href(t["numero"]).lstrip("+")}">WhatsApp</a>'
        lineas.append(linea)
    if DATOS.get("horarios"):
        lineas.append(f"Horarios: {dato(DATOS['horarios'])}")
    return lineas


def pie():
    cuit = DATOS["cuit"]
    nav = "".join(f'<li><a href="{href(d)}">{esc(t)}</a></li>' for d, t in MENU)
    contacto = "".join(
        f'<li><a href="https://wa.me/{telefono_href(t["numero"]).lstrip("+")}">WhatsApp {esc(t["numero"])}</a></li>'
        if t["whatsapp"] is True else f'<li><a href="tel:{telefono_href(t["numero"])}">{esc(t["numero"])}</a></li>'
        for t in DATOS["telefonos"]
    ) + "".join(f'<li><a href="mailto:{esc(c)}">{esc(c)}</a></li>' for c in DATOS["correos"])
    dom = DATOS["domicilio"]
    legal = f"{esc(dom['calle'])}, {dato(dom['codigoPostal'])} {esc(dom['ciudad'])}, {esc(dom['provincia'])}."
    if cuit:
        legal += f"<br>CUIT {dato(cuit)}"
    return f"""<footer class="pie"><div class="contenedor">
  <div class="pie-columnas">
    <nav aria-label="Enlaces del sitio"><ul>{nav}</ul></nav>
    <ul>{contacto}</ul>
  </div>
  <div class="legal"><span>{legal}</span><span>© <span id="anio">2026</span> {esc(NOMBRE)}</span></div>
</div></footer>"""


SCRIPT = """<script>
(function () {
  document.getElementById('anio').textContent = new Date().getFullYear();
  var boton = document.querySelector('.abrir-menu'), nav = document.getElementById('navegacion');
  boton.addEventListener('click', function () {
    var abierto = boton.getAttribute('aria-expanded') === 'true';
    boton.setAttribute('aria-expanded', String(!abierto));
    nav.classList.toggle('abierto', !abierto);
  });
  nav.addEventListener('click', function (e) { if (e.target.tagName === 'A') { nav.classList.remove('abierto'); boton.setAttribute('aria-expanded', 'false'); } });
  document.querySelectorAll('[data-pista]').forEach(function (cont) {
    var pista = cont.querySelector('[data-desliza]'), prev = cont.querySelector('[data-prev]'), sig = cont.querySelector('[data-sig]');
    var suave = function () { return window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'; };
    var paso = function () { var h = pista.firstElementChild; return h.getBoundingClientRect().width + (parseFloat(getComputedStyle(pista).columnGap) || 0); };
    var actualizar = function () { prev.disabled = pista.scrollLeft < 4; sig.disabled = pista.scrollLeft + pista.clientWidth >= pista.scrollWidth - 4; };
    prev.addEventListener('click', function () { pista.scrollBy({ left: -paso(), behavior: suave() }); });
    sig.addEventListener('click', function () { pista.scrollBy({ left: paso(), behavior: suave() }); });
    pista.addEventListener('scroll', actualizar, { passive: true });
    window.addEventListener('resize', actualizar); actualizar();
  });
})();
</script>"""


def documento(ruta, titulo, descripcion, cuerpo):
    revision = "" if FINAL else '<div class="revision"><div class="contenedor">Versión 1 · Vista previa del estilo nuevo. Borrador, no publicado.</div></div>\n'
    canonica = DOMINIO + ("/" if ruta == "/" else ruta + "/")
    return f"""<!doctype html>
<html lang="es-AR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(titulo)}</title>
<meta name="description" content="{esc(descripcion)}">
<meta name="author" content="{esc(NOMBRE)}">
<link rel="canonical" href="{canonica}">
<link rel="icon" href="{asset('favicon.svg')}" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_AR">
<meta property="og:site_name" content="{esc(NOMBRE)}">
<meta property="og:title" content="{esc(titulo)}">
<meta property="og:description" content="{esc(descripcion)}">
<meta property="og:url" content="{canonica}">
<meta property="og:image" content="{DOMINIO}/img/oficina-recepcion.jpg">
{'' if FINAL else '<meta name="robots" content="noindex">'}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{asset('estilos.css')}">
<script type="application/ld+json">{json_ld()}</script>
</head>
<body>
<a class="salto" href="#contenido">Ir al contenido</a>
{revision}{encabezado(ruta)}
<main id="contenido">
{cuerpo}
</main>
{pie()}
{SCRIPT}
</body>
</html>
"""


# ---------- Inicio ----------
# Textos del sitio actual. Cambios respecto de Wix, registrados en CHANGELOG-contenido.md:
# nombre "Estudio Graciosi", "primera etapa", cifras sin confirmar quitadas, frase de visión
# "frondosa experiencia" se mantiene por decisión de Octavio (9/10), enlaces "Leer más" rotos quitados.

SERVICIOS = {
    # Textos de la tarjeta por área (id de estudio.json). Recupero crediticio resume los servicios 01 a 03
    # del sitio actual; los textos de las cuatro áreas los fijó Octavio el 9/10/2026.
    "recupero-crediticio":
        "Gestión integral de carteras en mora, en tres etapas. En la mora temprana se toma contacto inmediato con "
        "el deudor por omnicanalidad, con un trato cordial que prioriza que se reincorpore al ciclo comercial de la "
        "empresa. En la mora tardía se ponen de manifiesto las consecuencias legales y los mayores costos del "
        "incumplimiento, se fijan plazos perentorios y se analiza la solvencia así como la localización del deudor. "
        "Si la gestión extrajudicial no prospera, se inicia la vía judicial y se tramita la ejecución hasta el cobro "
        "del crédito.",
    "derecho-comercial":
        "Asesoramiento y representación de empresas en asuntos comerciales, confección y revisión de contratos, "
        "defensas ante reclamos y demandas de diferente índole, análisis de incumplimientos, intervención en "
        "concursos y quiebras. Se trabaja sobre la planificación anticipada en coherencia con la perspectiva del "
        "negocio del cliente.",
    "derecho-laboral":
        "Defensa y patrocinio en juicios laborales. Representación en sede administrativa y judicial. Planificación "
        "de los equipos de trabajo y la organización de la empresa, en conjunto con el departamento de recursos "
        "humanos.",
    "factoring":
        "Adquisición de carteras de cuentas en mora en los casos en que la empresa acreedora desee obtener liquidez "
        "inmediata y no decida ingresar en el ciclo regular de cobranza que normalmente gestiona el estudio.",
}


FOTOS_AREA = {
    "recupero-crediticio": ("area-geometrica.webp", "Líneas y volúmenes geométricos en tonos claros"),
    "derecho-comercial": ("area-biblioteca.webp", "Estantería con tomos de legislación y jurisprudencia"),
    "derecho-laboral": ("area-relieve.webp", "Relieve en madera con una balanza"),
    "factoring": ("area-oficina.webp", "Área de trabajo de la oficina del Estudio"),
}

BANNERS = [
    # (imagen, alt, título, texto, enlace, destino)
    ("banner-columnas", "Estatua sentada frente a las columnas de un edificio de justicia",
     "Derecho comercial y recupero crediticio",
     "Somos un estudio especializado en derecho comercial, laboral y gestión de carteras de cobranzas.",
     "Áreas de práctica", "/#areas"),
    ("banner-mapa-nea", "Mapa de papel con la región del NEA en azul",
     "Cobertura en la región",
     "Brindamos cobertura en toda la zona NEA: Chaco, Corrientes, Formosa y Misiones.",
     "Cobertura", "/#cobertura"),
    ("banner-justicia", "Figura de la Justicia con balanza y espada",
     "Consultas",
     "Las consultas se reciben por formulario, por teléfono y por WhatsApp.",
     "Contacto", "/contacto"),
]

FLECHAS = """<div class="flechas"><button type="button" data-prev aria-label="Anterior"><svg width="9" height="14" viewBox="0 0 9 14" aria-hidden="true"><path d="M8 1L2 7l6 6" fill="none" stroke="currentColor" stroke-width="1.6"/></svg></button><button type="button" data-sig aria-label="Siguiente"><svg width="9" height="14" viewBox="0 0 9 14" aria-hidden="true"><path d="M1 1l6 6-6 6" fill="none" stroke="currentColor" stroke-width="1.6"/></svg></button></div>"""


def cuerpo_inicio():
    banners = ""
    for n, (img, alt, titulo, texto, enl, dest) in enumerate(BANNERS):
        h = "h1" if n == 0 else "h2"
        carga = "" if n == 0 else ' loading="lazy"'
        banners += f"""<section class="banner" aria-roledescription="diapositiva" aria-label="{n + 1} de {len(BANNERS)}">
  <picture><img src="{asset('img/' + img + '-1600.webp')}" srcset="{asset('img/' + img + '-800.webp')} 800w, {asset('img/' + img + '-1600.webp')} 1600w" sizes="100vw" width="1600" height="900" alt="{esc(alt)}"{carga}></picture>
  <div class="texto"><div><{h}>{esc(titulo)}</{h}><p>{esc(texto)}</p><a class="mas" href="{href(dest)}">{esc(enl)}</a></div></div>
</section>"""
    tarjetas = ""
    for a in DATOS["areasDePractica"]:
        foto, alt = FOTOS_AREA[a["id"]]
        tarjetas += f"""<article class="tarjeta" id="{a["id"]}"><img src="{asset('img/' + foto)}" width="900" height="600" loading="lazy" alt="{esc(alt)}"><h3>{esc(a["nombre"])}</h3><p>{esc(SERVICIOS[a["id"]])}</p><a class="mas" href="{enlace('/contacto')}">Más info<span class="sr-only"> sobre {esc(a["nombre"])}</span></a></article>"""
    provincias = "".join(
        f'<li><h3>{esc(p["nombre"])}</h3></li>' for p in DATOS["provincias"]
    )
    return f"""<div class="banners" data-pista aria-roledescription="carrusel" aria-label="Mensajes principales">
  <div class="banners-pista" data-desliza>{banners}</div>
  {FLECHAS}
</div>
<section class="central" id="estudio" aria-labelledby="t-estudio"><div class="contenedor"><div class="interior">
  <h2 id="t-estudio">{esc(NOMBRE)}</h2>
  <p>Titular: {esc(DATOS['titular'])}. Nuestro equipo se destaca por su capacidad de gestión y respuesta frente a la asignación de grandes carteras, abordando tres etapas en el proceso de recuperación de deudas: a) mora temprana; b) mora tardía; y c) ejecución judicial.</p>
  <p class="vision">Combinamos una frondosa experiencia técnica con integridad de valores que nos caracterizan, a fin de ofrecer una prestación de excelencia que sea un valor agregado para nuestros clientes.</p>
  <a class="mas" href="{enlace('/contacto')}">Más info</a>
</div></div></section>
<section class="areas" id="areas" aria-labelledby="t-areas"><div class="contenedor" data-pista>
  <div class="sec-cabecera"><h2 id="t-areas">Áreas de práctica</h2>{FLECHAS}</div>
  <div class="carrusel" data-desliza>{tarjetas}</div>
</div></section>
<section class="cobertura" id="cobertura" aria-labelledby="t-cobertura"><div class="contenedor">
  <h2 id="t-cobertura">Cobertura</h2>
  <p class="bajada">Provincias en las que actúa el Estudio.</p>
  <ul class="notas">{provincias}</ul>
</div></section>"""


def cuerpo_contacto():
    dom = DATOS["domicilio"]
    consulta = f"{dom['calle'].split(',')[0]}, {dom['ciudad']}, {dom['provincia']}, {dom['pais']}".replace(" ", "+")
    datos = "".join(f"<p>{l}</p>" for l in lineas_contacto())
    accion = "" if FINAL else ' onsubmit="event.preventDefault()"'
    return f"""<section class="contacto"><div class="contenedor">
  <h1>Contacto</h1>
  <p class="intro">{esc(NOMBRE)} brinda soluciones en el ámbito de la gestión de carteras de cobranzas y el recupero crediticio. Para recibir asesoramiento o realizar una consulta, el formulario y los datos de contacto del Estudio están a disposición.</p>
  <div class="contacto-grilla">
    <form id="formulario" class="formulario" name="contacto" method="post" action="{enlace('/gracias')}" data-netlify="true" netlify-honeypot="sitio-web"{accion}>
      <input type="hidden" name="form-name" value="contacto">
      <p hidden><label>No completar: <input name="sitio-web" tabindex="-1" autocomplete="off"></label></p>
      <div><label for="nombre">Nombre</label><input id="nombre" name="nombre" placeholder="Nombre" autocomplete="name" required></div>
      <div><label for="correo">Email</label><input id="correo" name="correo" type="email" placeholder="Email" autocomplete="email" required></div>
      <div class="ancho"><label for="telefono">Teléfono</label><input id="telefono" name="telefono" type="tel" placeholder="Teléfono" autocomplete="tel"></div>
      <div class="ancho"><label for="tipo">Tipo de consulta</label>
        <select id="tipo" name="tipo"><option value="empresa">Empresa o entidad financiera</option><option value="corresponsalia">Estudio que busca corresponsal</option><option value="otra">Otra consulta</option></select></div>
      <div class="ancho"><label for="mensaje">Mensaje</label><textarea id="mensaje" name="mensaje" placeholder="Mensaje" required></textarea></div>
      <div class="ancho"><button class="boton" type="submit">Enviar mensaje</button>
        <p class="aviso">Enviar este formulario no genera una relación profesional con el Estudio. No se debe enviar documentación confidencial por esta vía.</p></div>
    </form>
    <div class="datos" id="datos">
      <p>Oficina en Resistencia, Chaco:</p>
      {datos}
    </div>
  </div>
</div></section>
<iframe id="ubicacion" class="mapa" title="Mapa de la ubicación del Estudio" loading="lazy" src="https://maps.google.com/maps?q={esc(consulta)}&amp;output=embed"></iframe>"""


def cuerpo_simple(titulo, texto):
    return f"""<section class="contacto simple"><div class="contenedor">
  <h1>{esc(titulo)}</h1>
  <p class="intro">{esc(texto)}</p>
  <p><a class="boton" href="{enlace('/')}">Volver al inicio</a></p>
</div></section>"""


FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="#10284D"/><text x="32" y="43" font-family="Georgia, serif" font-size="30" fill="#fff" text-anchor="middle">EG</text></svg>"""


def construir():
    paginas = [
        ("/", NOMBRE + " | Estudio de abogados en Resistencia, Chaco",
         "Estudio especializado en gestión de carteras de cobranzas y recupero crediticio, derecho comercial, derecho laboral y factoring. Resistencia, Chaco.",
         cuerpo_inicio()),
        ("/contacto", "Contacto | " + NOMBRE,
         f"Datos de contacto y formulario de consulta de {NOMBRE}, Don Bosco 137, Resistencia, Chaco.",
         cuerpo_contacto()),
    ]
    if SALIDA.exists():
        shutil.rmtree(SALIDA)
    SALIDA.mkdir()
    for ruta, titulo, desc, cuerpo in paginas:
        destino = SALIDA / ("index.html" if ruta == "/" else (ruta.strip("/") + "/index.html" if FINAL else ruta.strip("/") + ".html"))
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(documento(ruta, titulo, desc, cuerpo), encoding="utf-8")
    gracias = documento("/gracias", "Consulta enviada | " + NOMBRE, "Confirmación de envío del formulario de consulta.",
                        cuerpo_simple("Consulta enviada", "La consulta se envió correctamente al Estudio."))
    error = documento("/404", "Página no encontrada | " + NOMBRE, "La página buscada no existe.",
                      cuerpo_simple("Página no encontrada", "La dirección ingresada no existe en este sitio."))
    for nombre, html_ in (("gracias", gracias), ("404", error)):
        if FINAL and nombre == "gracias":
            (SALIDA / "gracias").mkdir(exist_ok=True)
            (SALIDA / "gracias" / "index.html").write_text(html_.replace("<link rel=\"canonical\"", '<meta name="robots" content="noindex">\n<link rel="canonical"'), encoding="utf-8")
        else:
            (SALIDA / f"{nombre}.html").write_text(html_, encoding="utf-8")
    (SALIDA / "favicon.svg").write_text(FAVICON, encoding="utf-8")
    shutil.copy(RAIZ / "src" / "estilos.css", SALIDA / "estilos.css")
    shutil.copytree(RAIZ / "src" / "img", SALIDA / "img")
    if FINAL:
        shutil.copy(RAIZ / "redirecciones.txt", SALIDA / "_redirects")
        (SALIDA / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {DOMINIO}/sitemap.xml\n", encoding="utf-8")
        urls = "".join(f"<url><loc>{DOMINIO}{'/' if r == '/' else r + '/'}</loc></url>" for r, *_ in paginas)
        (SALIDA / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>', encoding="utf-8")
    print(f"{len(paginas)} páginas generadas en {SALIDA.name}/")


if __name__ == "__main__":
    construir()
