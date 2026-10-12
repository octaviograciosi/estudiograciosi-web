"""Genera el sitio del Estudio Graciosi a partir de estudio.json (fuente única de datos).

Uso:
  python3 build.py            vista previa en preview/ (enlaces relativos .html, se abre sin servidor)
  python3 build.py --final    sitio en dist/ con direcciones limpias (/areas/factoring/)
"""
import html
import json
import shutil
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).parent
DATOS = json.loads((RAIZ / "estudio.json").read_text(encoding="utf-8"))
FINAL = "--final" in sys.argv
SALIDA = RAIZ / ("dist" if FINAL else "preview")
DOMINIO = "https://www.estudiograciosi.com"

ACTUAL_ATTR = ' aria-current="page"'

MENU = [
    ("/el-estudio", "El Estudio"),
    ("/areas", "Áreas de práctica"),
    ("/equipo", "Equipo"),
    ("/cobertura", "Cobertura"),
    ("/publicaciones", "Publicaciones"),
    ("/contacto", "Contacto"),
]


# ---------- utilidades ----------

def esc(v):
    return html.escape(str(v), quote=True)


def es_pendiente(v):
    return isinstance(v, str) and v.startswith("[PENDIENTE")


def dato(v):
    """Muestra un dato; si está pendiente, lo marca visiblemente."""
    if es_pendiente(v):
        return f'<span class="pendiente">{esc(v)}</span>'
    return esc(v)


def pend(texto):
    return f'<span class="pendiente">{esc(texto)}</span>'


def slug(texto):
    t = unicodedata.normalize("NFD", texto.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return "-".join(t.split())


def lista_natural(items):
    return ", ".join(items[:-1]) + " y " + items[-1]


PROVINCIAS = [p["nombre"] for p in DATOS["provincias"]]
PROVINCIAS_TEXTO = lista_natural(PROVINCIAS)
NOMBRE = DATOS["nombre"]


class Pagina:
    def __init__(self, ruta, titulo, descripcion, cuerpo, seccion=None):
        self.ruta, self.titulo, self.descripcion, self.cuerpo, self.seccion = ruta, titulo, descripcion, cuerpo, seccion

    def archivo(self):
        if FINAL:
            return SALIDA / self.ruta.strip("/") / "index.html" if self.ruta != "/" else SALIDA / "index.html"
        return SALIDA / (("index" if self.ruta == "/" else self.ruta.strip("/")) + ".html")

    def asset(self, ruta):
        """Ruta a un archivo estático (imagen, estilos) desde esta página."""
        if FINAL:
            return "/" + ruta
        profundidad = self.ruta.strip("/").count("/") if self.ruta != "/" else 0
        return "../" * profundidad + ruta

    def url(self, destino):
        """Convierte una ruta del sitio en un enlace válido desde esta página."""
        if destino.startswith(("http", "mailto:", "tel:", "#")):
            return destino
        ruta, _, ancla = destino.partition("#")
        ruta, _, consulta = ruta.partition("?")
        if FINAL:
            r = ruta if ruta == "/" else ruta.rstrip("/") + "/"
        else:
            profundidad = self.ruta.strip("/").count("/") if self.ruta != "/" else 0
            r = "../" * profundidad + ("index" if ruta == "/" else ruta.strip("/")) + ".html"
        return r + (f"?{consulta}" if consulta else "") + (f"#{ancla}" if ancla else "")


# ---------- piezas comunes ----------

def json_ld():
    d = DATOS
    dom = d["domicilio"]
    ld = {
        "@context": "https://schema.org",
        "@type": "LegalService",
        "name": d["nombre"],
        "url": DOMINIO,
        "email": d["correos"][0],
        "telephone": [t["numero"] for t in d["telefonos"]],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": dom["calle"],
            "addressLocality": dom["ciudad"],
            "addressRegion": dom["provincia"],
            "addressCountry": "AR",
        },
        "areaServed": [{"@type": "State", "name": p} for p in PROVINCIAS],
        "knowsAbout": [a["nombre"] for a in d["areasDePractica"]],
    }
    if not es_pendiente(dom["codigoPostal"]):
        ld["address"]["postalCode"] = dom["codigoPostal"]
    return json.dumps(ld, ensure_ascii=False, indent=1).replace("</", "<\\/")


def encabezado(p):
    items = "".join(
        f'<li><a href="{p.url(r)}"{ACTUAL_ATTR if p.seccion == r else ""}>{esc(t)}</a></li>'
        for r, t in MENU[:-1]
    )
    return f"""<header class="encabezado">
  <div class="contenedor">
    <a class="marca" href="{p.url('/')}">{esc(NOMBRE)}</a>
    <div class="menu-acciones">
      <nav aria-label="Menú principal"><ul class="menu" id="menu">{items}<li class="solo-movil"><a href="{p.url('/contacto')}">Contacto</a></li></ul></nav>
      <button class="icono-btn" id="abrir-buscador" aria-expanded="false" aria-controls="buscador" aria-label="Buscar en el sitio">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="10.5" cy="10.5" r="7"/><path d="M20 20l-4.5-4.5"/></svg>
      </button>
    </div>
    <div class="acciones">
      <a class="contacto-enlace" href="{p.url('/contacto')}"{ACTUAL_ATTR if p.seccion == '/contacto' else ""}>Contacto</a>
      <button class="icono-btn abrir-menu" id="abrir-menu" aria-expanded="false" aria-controls="menu" aria-label="Abrir menú">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
      </button>
    </div>
  </div>
  <div class="buscador" id="buscador" hidden>
    <div class="contenedor">
      <label class="salto" for="campo-busqueda">Buscar</label>
      <input id="campo-busqueda" type="search" placeholder="Buscar en el sitio">
      <p style="margin:8px 0 0">{pend('[PENDIENTE: definir] motor de búsqueda según el alojamiento elegido')}</p>
    </div>
  </div>
</header>"""


def datos_contacto(p, en_pie=True):
    d = DATOS
    dom = d["domicilio"]
    cp = "" if es_pendiente(dom["codigoPostal"]) else dom["codigoPostal"] + " "
    lineas = [esc(dom["calle"]), esc(f"{cp}{dom['ciudad']}, {dom['provincia']}")]
    for t in d["telefonos"]:
        num = "".join(c for c in t["numero"] if c.isdigit() or c == "+")
        linea = f'<a href="tel:{num}">{esc(t["numero"])}</a>'
        if t["whatsapp"] is True:
            linea += f' · <a href="https://wa.me/{num.lstrip("+")}">WhatsApp</a>'
        lineas.append(linea)
    for c in d["correos"]:
        lineas.append(f'<a href="mailto:{esc(c)}">{esc(c)}</a>')
    lineas.append(f"Horarios: {dato(d['horarios'])}")
    return "".join(f"<span>{l}</span>" for l in lineas)


def pie(p):
    nav = "".join(f'<li><a href="{p.url(r)}">{esc(t)}</a></li>' for r, t in MENU)
    legales = [
        ("/mapa-del-sitio", "Mapa del sitio"),
        ("/accesibilidad", "Accesibilidad"),
        ("/publicidad-profesional", "Publicidad profesional"),
    ]
    leg = "".join(f'<li><a href="{p.url(r)}">{esc(t)}</a></li>' for r, t in legales)
    return f"""<footer class="pie">
  <div class="contenedor">
    <div class="columnas">
      <div><a class="marca-pie" href="{p.url('/')}">{esc(NOMBRE)}</a><address>{datos_contacto(p)}</address></div>
      <div><ul>{nav}</ul></div>
      <div><ul>{leg}</ul></div>
      <div class="derechos">© <span id="anio">2026</span> {esc(NOMBRE)}</div>
    </div>
    <p class="legal">{dato(DATOS['avisoPublicidadProfesional'])}</p>
  </div>
</footer>"""


SCRIPT = """<script>
(function () {
  var anio = document.getElementById('anio'); if (anio) anio.textContent = new Date().getFullYear();
  var quieto = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Banner: se desplaza solo cada 7 segundos, con puntos y gesto de deslizar.
  var carrusel = document.querySelector('.carrusel');
  if (carrusel) {
    var pista = carrusel.querySelector('.pista');
    var puntos = carrusel.querySelectorAll('.puntos button');
    var total = puntos.length, actual = 0, temporizador = null;
    var ir = function (i) {
      actual = (i + total) % total;
      pista.style.transform = 'translateX(' + (-100 * actual) + '%)';
      puntos.forEach(function (b, j) { if (j === actual) b.setAttribute('aria-current', 'true'); else b.removeAttribute('aria-current'); });
    };
    var iniciar = function () { if (!quieto && !temporizador) temporizador = setInterval(function () { ir(actual + 1); }, 7000); };
    var detener = function () { clearInterval(temporizador); temporizador = null; };
    puntos.forEach(function (b, j) { b.addEventListener('click', function () { detener(); ir(j); iniciar(); }); });
    carrusel.addEventListener('mouseenter', detener);
    carrusel.addEventListener('mouseleave', iniciar);
    carrusel.addEventListener('focusin', detener);
    var x0 = null;
    carrusel.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; detener(); }, { passive: true });
    carrusel.addEventListener('touchend', function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0; x0 = null;
      if (Math.abs(dx) > 40) ir(actual + (dx < 0 ? 1 : -1));
      iniciar();
    });
    iniciar();
  }

  // Tarjetas: flechas que desplazan una tarjeta por vez.
  document.querySelectorAll('[data-carrusel]').forEach(function (b) {
    var pistaT = document.getElementById(b.getAttribute('data-carrusel'));
    var actualizar = function () {
      var botones = document.querySelectorAll('[data-carrusel="' + pistaT.id + '"]');
      botones[0].disabled = pistaT.scrollLeft <= 2;
      botones[1].disabled = pistaT.scrollLeft + pistaT.clientWidth >= pistaT.scrollWidth - 2;
    };
    b.addEventListener('click', function () {
      var tarjeta = pistaT.querySelector('.tarjeta');
      var paso = tarjeta ? tarjeta.getBoundingClientRect().width + 28 : pistaT.clientWidth;
      pistaT.scrollBy({ left: paso * Number(b.getAttribute('data-dir')), behavior: quieto ? 'auto' : 'smooth' });
    });
    pistaT.addEventListener('scroll', actualizar, { passive: true });
    window.addEventListener('resize', actualizar);
    actualizar();
  });

  var conmutar = function (boton, panel, clase) {
    boton.addEventListener('click', function () {
      var abierto = boton.getAttribute('aria-expanded') === 'true';
      boton.setAttribute('aria-expanded', String(!abierto));
      if (clase) { panel.classList.toggle(clase, !abierto); } else { panel.hidden = abierto; if (!abierto) panel.querySelector('input').focus(); }
    });
  };
  conmutar(document.getElementById('abrir-menu'), document.getElementById('menu'), 'abierto');
  conmutar(document.getElementById('abrir-buscador'), document.getElementById('buscador'));
  var tipo = new URLSearchParams(location.search).get('tipo');
  var sel = document.getElementById('tipo');
  if (sel && tipo) sel.value = tipo;
})();
</script>"""


def documento(p):
    titulo = NOMBRE if p.ruta == "/" else f"{p.titulo} | {NOMBRE}"
    canonica = DOMINIO + ("/" if p.ruta == "/" else p.ruta.rstrip("/") + "/")
    css = p.asset("estilos.css")
    revision = "" if FINAL else '<div class="revision"><div class="contenedor">Vista previa. Borrador para revisión, no publicado.</div></div>\n'
    return f"""<!doctype html>
<html lang="es-AR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(titulo)}</title>
<meta name="description" content="{esc(p.descripcion)}">
<link rel="canonical" href="{canonica}">
{'<meta name="robots" content="noindex">' if not FINAL else ''}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{css}">
<script type="application/ld+json">{json_ld()}</script>
</head>
<body>
<a class="salto" href="#contenido">Ir al contenido</a>
{revision}{encabezado(p)}
<main id="contenido">
{p.cuerpo(p)}
</main>
{pie(p)}
{SCRIPT}
</body>
</html>
"""


def banner_interno(p, titulo, migas=(), foto="banner-lapacho.jpg"):
    m = ""
    if migas:
        partes = [f'<a href="{p.url("/")}">Inicio</a>'] + [f'<a href="{p.url(r)}">{esc(t)}</a>' for r, t in migas]
        m = f'<nav class="miga" aria-label="Ubicación">{" / ".join(partes)}</nav>'
    img = f'<img src="{p.asset("img/" + foto)}" alt="">' if foto else ""
    clase = "banner-interno" if foto else "banner-interno sin-foto"
    return f'<section class="{clase}">{img}<div class="contenedor">{m}<h1>{esc(titulo)}</h1></div></section>'


# ---------- contenido de las áreas ----------
# Todo sale del texto propio del sitio actual (portada, servicios 01 a 04, y "Acerca de").
# Lo que el sitio no dice queda marcado como pendiente.

AREAS_TEXTO = {
    "gestion-temprana": {
        "resumen": "Contacto inmediato con el deudor por WhatsApp, SMS, correo y teléfono, con un trato cordial que busca reincorporarlo al ciclo comercial.",
        "entrada": "Es la primera etapa de la gestión de una cartera: el contacto con el deudor apenas se produce la mora.",
        "que": [
            "El Estudio toma contacto inmediato con el deudor por WhatsApp, SMS, correo electrónico y teléfono.",
            "El trato es cordial. El objetivo es que el cliente del acreedor regularice su situación y vuelva al ciclo comercial.",
        ],
        "como": None,
    },
    "mora-tardia": {
        "resumen": "Intimaciones con plazos perentorios y análisis de solvencia y domicilio para evaluar la conveniencia de la vía judicial.",
        "entrada": "Es la etapa en que la deuda ya no se regularizó con la gestión temprana y hay que definir si conviene avanzar por la vía judicial.",
        "que": [
            "La gestión pone el énfasis en las consecuencias legales y los costos que la deuda puede generar al deudor, con plazos perentorios para regularizar.",
            "En paralelo se analizan la solvencia y el domicilio del deudor para evaluar la conveniencia de iniciar la vía judicial.",
        ],
        "como": None,
    },
    "ejecuciones-judiciales": {
        "resumen": "Recupero de créditos en mora por vía judicial.",
        "entrada": "Es la etapa judicial del recupero, cuando la gestión extrajudicial no alcanzó para cobrar el crédito.",
        "que": [
            "El Estudio inicia y tramita las acciones judiciales para el recupero de créditos en mora.",
            f"Actúa en {PROVINCIAS_TEXTO}.",
        ],
        "como": None,
    },
    "factoring": {
        "resumen": "Compra de carteras en mora para dar liquidez inmediata al acreedor.",
        "entrada": "Una alternativa para el acreedor que necesita liquidez antes de que termine la gestión de cobro.",
        "que": [
            "El Estudio compra carteras de créditos en mora.",
            "El acreedor obtiene liquidez inmediata por esa cartera.",
        ],
        "como": None,
    },
}


# ---------- páginas ----------

def tarjetas_areas(p):
    return "".join(
        f"""<article class="tarjeta">
  <div class="imagen"><img src="{p.asset('img/area-' + a['id'] + '.jpg')}" alt="" loading="lazy"></div>
  <h3>{esc(a['nombre'])}</h3>
  <p>{esc(AREAS_TEXTO[a['id']]['resumen'])}</p>
  <a class="boton" href="{p.url(a['url'])}" aria-label="Conocer más sobre {esc(a['nombre'])}">Conocer más</a>
</article>"""
        for a in DATOS["areasDePractica"]
    )


def carrusel_areas(p, titulo="Áreas de práctica"):
    return f"""<section class="bloque" aria-labelledby="t-areas"><div class="contenedor">
  <div class="cabecera-carrusel">
    <h2 class="titulo-seccion" id="t-areas">{esc(titulo)}</h2>
    <div class="flechas">
      <button type="button" data-carrusel="areas" data-dir="-1" aria-label="Anterior"><svg width="9" height="16" viewBox="0 0 9 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M8 1L1 8l7 7"/></svg></button>
      <span class="separador" aria-hidden="true"></span>
      <button type="button" data-carrusel="areas" data-dir="1" aria-label="Siguiente"><svg width="9" height="16" viewBox="0 0 9 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M1 1l7 7-7 7"/></svg></button>
    </div>
  </div>
  <div class="tarjetas" id="areas">{tarjetas_areas(p)}</div>
</div></section>"""


def cuerpo_portada(p):
    diapositivas = [
        ("banner-panoramica.jpg", "h1", "Gestión de carteras y recupero de créditos",
         "Mora temprana, mora tardía y ejecución judicial.", "/areas", "Conocer más"),
        ("banner-inmigrantes.jpg", "h2", "Corresponsalía en seis provincias",
         PROVINCIAS_TEXTO + ".", "/cobertura", "Ver cobertura"),
        ("banner-lapacho.jpg", "h2", "Factoring de carteras en mora",
         "Liquidez inmediata para el acreedor.", "/areas/factoring", "Conocer más"),
    ]
    diap = "".join(
        f"""<div class="diapositiva" role="group" aria-roledescription="diapositiva" aria-label="{i} de {len(diapositivas)}">
  <img src="{p.asset('img/' + img)}" alt=""{' loading="lazy"' if i > 1 else ''}>
  <div class="contenedor">
    <{tag} class="titular">{esc(tit)}</{tag}>
    <p>{esc(sub)}</p>
    <a class="boton" href="{p.url(dest)}">{esc(boton)}</a>
  </div>
</div>"""
        for i, (img, tag, tit, sub, dest, boton) in enumerate(diapositivas, 1)
    )
    puntos = "".join(
        f'<button type="button" aria-label="Ver diapositiva {i}"{" aria-current=\"true\"" if i == 1 else ""}></button>'
        for i in range(1, len(diapositivas) + 1)
    )
    provs = "".join(
        f"""<li><h3><a href="{p.url('/cobertura/' + slug(x['nombre']))}">{esc(x['nombre'])}</a></h3>
<p>Actuación judicial y extrajudicial. Matrícula: {dato(x['matricula'])}</p></li>"""
        for x in DATOS["provincias"]
    )
    return f"""<section class="carrusel" aria-roledescription="carrusel" aria-label="Mensajes principales">
  <div class="pista">{diap}</div>
  <div class="puntos">{puntos}</div>
</section>
<section class="bloque institucional" aria-labelledby="t-estudio"><div class="contenedor">
  <h2 id="t-estudio">Acompañamos al acreedor en todo el ciclo del crédito impago</h2>
  <p>Del primer contacto con el deudor a la ejecución judicial, cada estrategia se evalúa por su costo y su conveniencia real para el negocio del cliente.</p>
  <a class="enlace-flecha" href="{p.url('/el-estudio')}">Conocer el Estudio</a>
</div></section>
{carrusel_areas(p)}
<section class="bloque" aria-labelledby="t-cobertura" style="padding-top:0"><div class="contenedor columnas-filete">
  <div>
    <h2 class="titulo-seccion" id="t-cobertura">Cobertura</h2>
    <p class="intro">Seis provincias, desde la oficina de {esc(DATOS['domicilio']['ciudad'])}.</p>
  </div>
  <ul>{provs}</ul>
</div></section>
{bloque_contacto(p)}"""


def bloque_contacto(p):
    return f"""<section class="bloque contacto-bloque" id="contacto" aria-labelledby="t-contacto"><div class="contenedor">
  <h2 class="titulo-seccion" id="t-contacto">Contacto</h2>
  <div class="vias">
    <div class="via"><h3>Soy una empresa o entidad financiera</h3>
      <p>Para consultas sobre gestión de carteras, recupero judicial o factoring.</p>
      <a class="boton" href="{p.url('/contacto?tipo=empresa')}">Escribir al Estudio</a></div>
    <div class="via"><h3>Soy un estudio o área legal que busca corresponsal</h3>
      <p>Para encargar actuaciones en {esc(PROVINCIAS_TEXTO)}.</p>
      <a class="boton" href="{p.url('/contacto?tipo=corresponsalia')}">Consultar corresponsalía</a></div>
  </div>
</div></section>"""


def persona_contacto(p):
    o = DATOS["equipo"][0]
    return f"""<aside class="persona" aria-label="Persona de contacto">
  <span class="etiqueta">Contacto</span>
  <div class="foto">{dato(o['foto'])}</div>
  <h3>{esc(o['nombre'])}</h3>
  <p>{esc(o['cargo'])}</p>
  <a class="boton" href="{p.url('/contacto?tipo=empresa')}">Escribir al Estudio</a>
</aside>"""


def cuerpo_el_estudio(p):
    return f"""{banner_interno(p, 'El Estudio', foto='banner-inmigrantes.jpg')}
<section class="bloque"><div class="contenedor"><div class="lectura">
  <p class="entrada">{esc(NOMBRE)} se dedica a la gestión de carteras de cobranzas y al recupero de créditos, con oficina en {esc(DATOS['domicilio']['ciudad'])}, {esc(DATOS['domicilio']['provincia'])}.</p>
  <p>El titular es {esc(DATOS['titular'])}. El Estudio gestiona carteras en tres etapas: mora temprana, mora tardía y ejecución judicial. Ofrece además la compra de carteras en mora (factoring).</p>
  <p>Antigüedad del Estudio: {pend('[PENDIENTE: confirmar] año de inicio')}</p>

  <h2>Método de trabajo</h2>
  <p>El asesoramiento parte del negocio del cliente. Antes de definir una estrategia se analizan su rentabilidad, sus costos y su conveniencia real, con una mirada de largo plazo.</p>
  <p>La gestión empieza por la vía extrajudicial y avanza a la judicial cuando el análisis de solvencia y domicilio del deudor indica que conviene.</p>

  <h2>Dónde actúa</h2>
  <p>El Estudio actúa en {esc(PROVINCIAS_TEXTO)}, y cuenta con una red de contactos y socios regionales y nacionales.</p>
  <p><a class="enlace-flecha" href="{p.url('/cobertura')}">Ver cobertura</a></p>

  <h2>Valores</h2>
  <p>{pend('[PENDIENTE: confirmar] valores que el Estudio quiere comunicar')}</p>
</div></div></section>
{bloque_contacto(p)}"""


def cuerpo_areas(p):
    return f"""{banner_interno(p, 'Áreas de práctica')}
<section class="bloque" style="padding-bottom:0"><div class="contenedor">
  <p class="entrada lectura">El Estudio acompaña al acreedor en todo el ciclo del crédito impago: de la mora temprana a la ejecución judicial, con el factoring como alternativa para obtener liquidez.</p>
  <p>{pend(DATOS['corresponsalia'])}</p>
</div></section>
{carrusel_areas(p, 'Las cuatro áreas')}
{bloque_contacto(p)}"""


def cuerpo_area(area):
    def cuerpo(p):
        t = AREAS_TEXTO[area["id"]]
        lateral = "".join(
            f'<li><a href="{p.url(a["url"])}"{ACTUAL_ATTR if a["id"] == area["id"] else ""}>{esc(a["nombre"])}</a></li>'
            for a in DATOS["areasDePractica"]
        )
        que = "".join(f"<p>{esc(x)}</p>" for x in t["que"])
        return f"""{banner_interno(p, area['nombre'], [('/areas', 'Áreas de práctica')], 'area-' + area['id'] + '.jpg')}
<section class="bloque"><div class="contenedor tres-columnas">
  <nav class="lista-lateral" aria-label="Áreas de práctica"><h2>Áreas de práctica</h2><ul>{lateral}</ul></nav>
  <div class="lectura">
    <p class="entrada">{esc(t['entrada'])}</p>
    <h2>Qué hace el Estudio</h2>{que}
    <h2>A quién ayuda</h2>
    <p>A empresas y entidades financieras con créditos en mora.</p>
    <h2>Cómo se trabaja</h2>
    <p>{pend('[PENDIENTE: confirmar] pasos, plazos habituales e informes que recibe el cliente')}</p>
  </div>
  {persona_contacto(p)}
</div></section>"""
    return cuerpo


def cuerpo_equipo(p):
    fichas = ""
    for m in DATOS["equipo"]:
        fichas += f"""<article class="ficha">
  <div class="foto">{dato(m['foto'])}</div>
  <div>
    <h2>{esc(m['nombre'])}</h2>
    <p>{esc(m['cargo'])}</p>
    <dl>
      <dt>Formación</dt><dd>{dato(m['formacion'])}</dd>
      <dt>Matrículas</dt><dd>{pend('[PENDIENTE: confirmar] matrícula por provincia')}</dd>
    </dl>
  </div>
</article>"""
    return f"""{banner_interno(p, 'Equipo')}
<section class="bloque"><div class="contenedor">
  {fichas}
  <p style="margin-top:48px">{pend('[PENDIENTE: confirmar] otros integrantes del equipo y su autorización para figurar')}</p>
</div></section>"""


def cuerpo_cobertura(p):
    provs = "".join(
        f"""<li><h3><a href="{p.url('/cobertura/' + slug(x['nombre']))}">{esc(x['nombre'])}</a></h3>
<p>Actuación judicial y extrajudicial. Matrícula: {dato(x['matricula'])}</p></li>"""
        for x in DATOS["provincias"]
    )
    return f"""{banner_interno(p, 'Cobertura', foto='banner-panoramica.jpg')}
<section class="bloque"><div class="contenedor columnas-filete">
  <div><p class="entrada">El Estudio actúa en seis provincias desde su oficina de {esc(DATOS['domicilio']['ciudad'])}, y cuenta con una red de contactos y socios regionales y nacionales.</p></div>
  <ul>{provs}</ul>
</div></section>
{bloque_contacto(p)}"""


def cuerpo_provincia(prov):
    def cuerpo(p):
        lateral = "".join(
            f'<li><a href="{p.url("/cobertura/" + slug(x["nombre"]))}"{ACTUAL_ATTR if x["nombre"] == prov["nombre"] else ""}>{esc(x["nombre"])}</a></li>'
            for x in DATOS["provincias"]
        )
        areas = "".join(f'<li><a href="{p.url(a["url"])}">{esc(a["nombre"])}</a></li>' for a in DATOS["areasDePractica"])
        return f"""{banner_interno(p, prov['nombre'], [('/cobertura', 'Cobertura')])}
<section class="bloque"><div class="contenedor tres-columnas">
  <nav class="lista-lateral" aria-label="Provincias"><h2>Provincias</h2><ul>{lateral}</ul></nav>
  <div class="lectura">
    <p class="entrada">Actuación judicial y extrajudicial del Estudio en {esc(prov['nombre'])}.</p>
    <h2>Matrícula</h2>
    <p>{dato(prov['matricula'])}</p>
    <h2>Forma de actuación</h2>
    <p>{pend('[PENDIENTE: confirmar] si actúa directamente o con corresponsales, y en qué circunscripciones')}</p>
    <h2>Áreas de práctica</h2>
    <ul>{areas}</ul>
  </div>
  {persona_contacto(p)}
</div></section>"""
    return cuerpo


def cuerpo_contacto(p):
    d = DATOS
    dom = d["domicilio"]
    consulta_mapa = f"{dom['calle'].split(',')[0]}, {dom['ciudad']}, {dom['provincia']}, {dom['pais']}"
    mapa = "https://maps.google.com/maps?q=" + consulta_mapa.replace(" ", "+") + "&output=embed"
    return f"""{banner_interno(p, 'Contacto', foto=None)}
<section class="bloque"><div class="contenedor contacto-grilla">
  <div>
    <p class="entrada">Para consultas de empresas y entidades financieras, y para estudios o áreas legales que buscan corresponsal.</p>
    <form class="formulario" action="#" method="post">
      <p style="margin:0">{pend('[PENDIENTE: definir] servicio que recibe los envíos del formulario')}</p>
      <div><label for="nombre">Nombre y apellido</label><input id="nombre" name="nombre" autocomplete="name" required></div>
      <div><label for="correo">Correo electrónico</label><input id="correo" name="correo" type="email" autocomplete="email" required></div>
      <div><label for="telefono">Teléfono <span class="opcional">(opcional)</span></label><input id="telefono" name="telefono" type="tel" autocomplete="tel"></div>
      <div><label for="tipo">Tipo de consulta</label>
        <select id="tipo" name="tipo" required>
          <option value="empresa">Empresa o entidad financiera</option>
          <option value="corresponsalia">Estudio o área legal que busca corresponsal</option>
          <option value="otra">Otra consulta</option>
        </select></div>
      <div><label for="mensaje">Mensaje</label><textarea id="mensaje" name="mensaje" required></textarea></div>
      <div class="aviso">
        <p>Enviar este formulario no genera una relación profesional con el Estudio.</p>
        <p>No se debe enviar documentación confidencial por esta vía.</p>
        <p>Después del envío: {pend('[PENDIENTE: confirmar] quién responde y en qué plazo')}</p>
      </div>
      <div><button class="boton" type="submit">Enviar consulta</button></div>
    </form>
  </div>
  <div class="datos">
    <h2 class="titulo-seccion" style="font-size:24px;margin-bottom:8px">{esc(NOMBRE)}</h2>
    <address style="font-style:normal;display:grid;gap:6px">{datos_contacto(p)}</address>
    <iframe class="mapa" title="Mapa de la ubicación del Estudio" loading="lazy" src="{esc(mapa)}"></iframe>
  </div>
</div></section>"""


def cuerpo_pendiente(titulo, texto):
    def cuerpo(p):
        return f"""{banner_interno(p, titulo, foto=None)}
<section class="bloque"><div class="contenedor lectura"><p>{pend(texto)}</p></div></section>"""
    return cuerpo


def cuerpo_publicaciones(p):
    return f"""{banner_interno(p, 'Publicaciones')}
<section class="bloque"><div class="contenedor">
  <p>{pend('[PENDIENTE: confirmar] si la sección sale en el lanzamiento y quién redacta')}</p>
  <p class="lectura">Cada artículo mostrará autor, fecha de publicación y fecha de última revisión. Los textos sobre normativa indicarán su fecha de vigencia.</p>
</div></section>"""


def construir():
    paginas = [
        Pagina("/", NOMBRE, "Gestión de carteras de cobranzas y recupero de créditos en " + PROVINCIAS_TEXTO + ".", cuerpo_portada),
        Pagina("/el-estudio", "El Estudio", f"Quiénes somos y cómo trabaja {NOMBRE}, con oficina en Resistencia, Chaco.", cuerpo_el_estudio, "/el-estudio"),
        Pagina("/areas", "Áreas de práctica", "Gestión temprana, mora tardía, ejecuciones judiciales y factoring.", cuerpo_areas, "/areas"),
        Pagina("/equipo", "Equipo", f"Integrantes de {NOMBRE}.", cuerpo_equipo, "/equipo"),
        Pagina("/cobertura", "Cobertura", f"Actuación en {PROVINCIAS_TEXTO}.", cuerpo_cobertura, "/cobertura"),
        Pagina("/publicaciones", "Publicaciones", f"Artículos y análisis de {NOMBRE} sobre ejecución y cobro judicial.", cuerpo_publicaciones, "/publicaciones"),
        Pagina("/contacto", "Contacto", f"Contacto con {NOMBRE}: domicilio, teléfonos, correo y formulario de consulta.", cuerpo_contacto, "/contacto"),
        Pagina("/publicidad-profesional", "Publicidad profesional", f"Aviso de publicidad profesional de {NOMBRE}.",
               cuerpo_pendiente("Publicidad profesional", DATOS["avisoPublicidadProfesional"])),
        Pagina("/accesibilidad", "Accesibilidad", f"Declaración de accesibilidad del sitio de {NOMBRE}.",
               cuerpo_pendiente("Accesibilidad", "[PENDIENTE: redactar] declaración de accesibilidad")),
    ]
    for a in DATOS["areasDePractica"]:
        paginas.append(Pagina(a["url"], a["nombre"], f"{a['nombre']}: {AREAS_TEXTO[a['id']]['resumen']}", cuerpo_area(a), "/areas"))
    for x in DATOS["provincias"]:
        paginas.append(Pagina("/cobertura/" + slug(x["nombre"]), f"Cobertura en {x['nombre']}",
                              f"Actuación de {NOMBRE} en {x['nombre']}.", cuerpo_provincia(x), "/cobertura"))

    def cuerpo_mapa(p):
        def li(r, t, hijos=""):
            return f'<li><a href="{p.url(r)}">{esc(t)}</a>{hijos}</li>'
        areas = "<ul>" + "".join(li(a["url"], a["nombre"]) for a in DATOS["areasDePractica"]) + "</ul>"
        provs = "<ul>" + "".join(li("/cobertura/" + slug(x["nombre"]), x["nombre"]) for x in DATOS["provincias"]) + "</ul>"
        items = li("/", "Inicio") + li("/el-estudio", "El Estudio") + li("/areas", "Áreas de práctica", areas) + li("/equipo", "Equipo") \
            + li("/cobertura", "Cobertura", provs) + li("/publicaciones", "Publicaciones") + li("/contacto", "Contacto") + li("/publicidad-profesional", "Publicidad profesional") + li("/accesibilidad", "Accesibilidad")
        return f'{banner_interno(p, "Mapa del sitio", foto=None)}<section class="bloque"><div class="contenedor mapa-sitio"><ul>{items}</ul></div></section>'

    paginas.append(Pagina("/mapa-del-sitio", "Mapa del sitio", f"Todas las páginas del sitio de {NOMBRE}.", cuerpo_mapa))

    # Títulos y descripciones únicos por página (requisito de SEO del instructivo).
    for campo in ("titulo", "descripcion"):
        valores = [getattr(p, campo) for p in paginas]
        repetidos = {v for v in valores if valores.count(v) > 1}
        assert not repetidos, f"{campo} repetido: {repetidos}"

    if SALIDA.exists():
        shutil.rmtree(SALIDA)
    for p in paginas:
        destino = p.archivo()
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(documento(p), encoding="utf-8")
    shutil.copy(RAIZ / "src" / "estilos.css", SALIDA / "estilos.css")
    shutil.copytree(RAIZ / "src" / "img", SALIDA / "img")

    if FINAL:
        urls = "".join(f"<url><loc>{DOMINIO}{'/' if p.ruta == '/' else p.ruta + '/'}</loc></url>" for p in paginas)
        (SALIDA / "sitemap.xml").write_text(
            f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>', encoding="utf-8")
        shutil.copy(RAIZ / "redirecciones.txt", SALIDA / "_redirects")
    print(f"{len(paginas)} páginas generadas en {SALIDA.name}/")


if __name__ == "__main__":
    construir()
