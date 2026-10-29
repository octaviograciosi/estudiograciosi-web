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
    ld["founder"] = {"@type": "Person", "name": DATOS["titular"], "jobTitle": "Abogado", "url": DOMINIO,
                     "worksFor": {"@type": "LegalService", "name": NOMBRE}}
    if not es_pendiente(dom["codigoPostal"]):
        ld["address"]["postalCode"] = dom["codigoPostal"]
    return json.dumps(ld, ensure_ascii=False).replace("</", "<\\/")


LOGO_ALTO = 324

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
  <a class="marca" href="{enlace('/')}"><img src="{asset('img/logo.webp')}" width="900" height="{LOGO_ALTO}" alt="{esc(NOMBRE)} Abogados, inicio"></a>
  <button type="button" class="abrir-menu" aria-expanded="false" aria-controls="navegacion">Menú</button>
  <nav id="navegacion" aria-label="Menú principal"><ul class="menu">{items}</ul></nav>
</div></header>"""


WHATSAPP = '<svg class="ico-wa" width="20" height="20" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>'


def whatsapp_href(numero):
    return "https://wa.me/" + telefono_href(numero).lstrip("+")


def lineas_contacto():
    dom = DATOS["domicilio"]
    cp = dom["codigoPostal"]
    lineas = [f"{esc(dom['calle'])}, {dato(cp)} {esc(dom['ciudad'])}, {esc(dom['provincia'])}."]
    lineas += [f'Email: <a href="mailto:{esc(c)}">{esc(c)}</a>' for c in DATOS["correos"]]
    for t in DATOS["telefonos"]:
        num = f'<a href="tel:{telefono_href(t["numero"])}">{esc(t["numero"])}</a>'
        if t["whatsapp"] is True:
            linea = f'<a class="wa" href="{whatsapp_href(t["numero"])}" aria-label="Escribir por WhatsApp al {esc(t["numero"])}">{WHATSAPP}</a>{num}'
        else:
            linea = f"Tel: {num}"
        lineas.append(linea)
    if DATOS.get("horarios"):
        lineas.append(f"Horarios: {dato(DATOS['horarios'])}")
    return lineas


def pie():
    cuit = DATOS["cuit"]
    nav = "".join(f'<li><a href="{href(d)}">{esc(t)}</a></li>' for d, t in MENU)
    contacto = "".join(
        f'<li><a class="wa" href="{whatsapp_href(t["numero"])}">{WHATSAPP}<span>{esc(t["numero"])}</span></a></li>'
        if t["whatsapp"] is True else f'<li><a href="tel:{telefono_href(t["numero"])}">{esc(t["numero"])}</a></li>'
        for t in DATOS["telefonos"]
    ) + "".join(f'<li><a href="mailto:{esc(c)}">{esc(c)}</a></li>' for c in DATOS["correos"])
    dom = DATOS["domicilio"]
    legal = f"Titular: {esc(DATOS['titular'])}<br>{esc(dom['calle'])}, {dato(dom['codigoPostal'])} {esc(dom['ciudad'])}, {esc(dom['provincia'])}."
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
    if (cont.hasAttribute('data-auto')) {
      // cambio automático cada 4 s; las flechas dan la vuelta; se pausa con el mouse, el foco, el toque y la pestaña oculta
      var quieto = window.matchMedia('(prefers-reduced-motion: reduce)'), pausado = false, reloj = null;
      var avanzar = function (d) {
        var n = pista.children.length, i = Math.round(pista.scrollLeft / pista.clientWidth) + d;
        i = (i + n) % n;
        pista.scrollTo({ left: i * pista.clientWidth, behavior: i === 0 && d > 0 ? 'auto' : suave() });
      };
      prev.disabled = false; sig.disabled = false;
      pista.removeEventListener('scroll', actualizar); window.removeEventListener('resize', actualizar);
      prev.addEventListener('click', function (e) { e.stopImmediatePropagation(); avanzar(-1); reiniciar(); }, true);
      sig.addEventListener('click', function (e) { e.stopImmediatePropagation(); avanzar(1); reiniciar(); }, true);
      var iniciar = function () { detener(); if (!quieto.matches && !pausado) reloj = setInterval(function () { avanzar(1); }, 4000); };
      var detener = function () { clearInterval(reloj); reloj = null; };
      var reiniciar = iniciar;
      var pausar = function (v) { pausado = v; v ? detener() : iniciar(); };
      cont.addEventListener('mouseenter', function () { pausar(true); });
      cont.addEventListener('mouseleave', function () { pausar(false); });
      cont.addEventListener('focusin', function () { pausar(true); });
      cont.addEventListener('focusout', function () { pausar(false); });
      cont.addEventListener('touchstart', function () { pausar(true); }, { passive: true });
      cont.addEventListener('touchend', function () { setTimeout(function () { pausar(false); }, 4000); }, { passive: true });
      document.addEventListener('visibilitychange', function () { pausar(document.hidden); });
      quieto.addEventListener('change', iniciar);
      iniciar();
    }
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
        "Nos mantenemos a la vanguardia de las tendencias en gestión de cobranzas y recupero crediticio, con un "
        "enfoque sostenible centrado en el respeto en el trato, disciplina en la gestión, pensamiento estratégico y "
        "compromiso con nuestros valores fundamentales. Recuperamos activos priorizando la ética, el trato cordial, "
        "la honestidad y la búsqueda de soluciones viables, teniendo la certeza de que es la manera de obtener el éxito.",
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
    "derecho-laboral": ("area-laboral.webp", "Grabado de una audiencia en una sala de tribunal"),
    "factoring": ("area-factoring.webp", "Pluma estilográfica sobre documentos en un escritorio"),
}

BANNERS = [
    # (imagen, alt, título, texto, enlace, destino); textos de los banners fijados por Octavio el 27/10/2026
    ("banner-estela", "Estela de piedra con una figura sentada y otra de pie, en relieve",
     "Calidad, servicio y compromiso",
     "Nuestra fortaleza es la atención personalizada, ágil, con un sólido conocimiento del panorama local.",
     "Quiénes somos", "/#estudio"),
    ("banner-mapa-nea", "Mapa de papel con la región del NEA en azul",
     "Cobertura en la región NEA",
     "Poseemos competencia en las provincias de Chaco, Corrientes, Formosa y Misiones, a lo que se adicionan Santa Fe y Córdoba para la rama de recupero de activos.",
     "Cobertura", "/#cobertura"),
    ("banner-columnas", "Estatua sentada frente a las columnas de un edificio de justicia",
     "Derecho comercial y recupero crediticio",
     "Históricamente uno de los rubros principales del estudio, lo que nos llevó a transitar una vasta experiencia en gestión de carteras de cobranzas y recupero de activos, logrando alcanzar la actual excelencia en la materia.",
     "Áreas de práctica", "/#areas"),
    ("banner-justicia", "Figura de la Justicia con balanza y espada",
     "Asesoramiento Estratégico",
     "Brindamos nuestra expertise en los temas que se nos presentan, manteniendo el foco en ofrecer el más alto estándar de calidad y excelencia.",
     "Contacto", "/contacto"),
]

def mapa_provincias():
    """Mapa de Argentina con las provincias de estudio.json resaltadas (contornos de Natural Earth, dominio público)."""
    mapa = json.loads((RAIZ / "src" / "mapa-provincias.json").read_text(encoding="utf-8"))
    nombres = [p["nombre"] for p in DATOS["provincias"]]
    ancho, alto = mapa["caja"][2], mapa["caja"][3]
    capas = "".join(
        f'<path class="{"prov activa" if n in nombres else "prov"}" d="{g["d"]}"/>' for n, g in mapa["provincias"].items()
    )
    # rótulos en una columna a la derecha, unidos al centro de cada provincia por una línea fina
    activas = sorted(((mapa["provincias"][n]["centro"], n) for n in nombres if n in mapa["provincias"]), key=lambda t: t[0][1])
    ys, rotulos = [], ""
    for (cx, cy), nombre in activas:
        y = max(cy, ys[-1] + 80) if ys else cy
        ys.append(y)
        rotulos += (f'<line class="guia" x1="{cx:.0f}" y1="{cy:.0f}" x2="{ancho + 40:.0f}" y2="{y:.0f}"/>'
                    f'<circle class="punto" cx="{cx:.0f}" cy="{cy:.0f}" r="9"/>'
                    f'<text class="rotulo" x="{ancho + 56:.0f}" y="{y + 15:.0f}">{esc(nombre)}</text>')
    lista = ", ".join(nombres)
    return (f'<figure class="mapa-prov"><svg viewBox="0 0 {ancho + 380:.0f} {alto:.0f}" role="img" aria-label="Mapa de Argentina con las provincias de actuación resaltadas: {esc(lista)}">'
            f'{capas}{rotulos}</svg></figure>')


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
    return f"""<div class="banners" data-pista data-auto aria-roledescription="carrusel" aria-label="Mensajes principales">
  <div class="banners-pista" data-desliza>{banners}</div>
  {FLECHAS}
</div>
<section class="central" id="estudio" aria-label="El Estudio"><div class="contenedor"><div class="interior">
  <p class="vision">Combinamos una frondosa experiencia técnica con integridad de valores que nos caracterizan, a fin de ofrecer una prestación de excelencia que sea un valor agregado para nuestros clientes.</p>
  <a class="mas" href="{enlace('/contacto')}">Más info</a>
</div></div></section>
<section class="areas" id="areas" aria-labelledby="t-areas"><div class="contenedor" data-pista>
  <div class="sec-cabecera"><h2 id="t-areas">Áreas de práctica</h2>{FLECHAS}</div>
  <div class="carrusel" data-desliza>{tarjetas}</div>
</div></section>
<section class="cobertura" id="cobertura" aria-labelledby="t-cobertura"><div class="contenedor cobertura-grilla">
  <div><h2 id="t-cobertura">Cobertura</h2><p class="bajada">Provincias donde tenemos competencia con matrícula habilitada.</p></div>
  {mapa_provincias()}
</div></section>"""


def cuerpo_contacto():
    dom = DATOS["domicilio"]
    consulta = f"{dom['calle'].split(',')[0]}, {dom['ciudad']}, {dom['provincia']}, {dom['pais']}".replace(" ", "+")
    datos = "".join(f"<p>{l}</p>" for l in lineas_contacto())
    accion = "" if FINAL else ' onsubmit="event.preventDefault()"'
    return f"""<section class="contacto"><div class="contenedor">
  <h1>Contacto</h1>
  <p class="intro">Para recibir asesoramiento o realizar una consulta, se encuentra a disposición el siguiente formulario, así como los datos de contacto del Estudio.</p>
  <div class="contacto-grilla">
    <form id="formulario" class="formulario" name="contacto" method="post" action="{enlace('/gracias')}" data-netlify="true" netlify-honeypot="sitio-web"{accion}>
      <input type="hidden" name="form-name" value="contacto">
      <p hidden><label>No completar: <input name="sitio-web" tabindex="-1" autocomplete="off"></label></p>
      <div><label for="nombre">Nombre</label><input id="nombre" name="nombre" placeholder="Nombre" autocomplete="name" required></div>
      <div><label for="correo">Email</label><input id="correo" name="correo" type="email" placeholder="Email" autocomplete="email" required></div>
      <div class="ancho"><label for="telefono">Teléfono</label><input id="telefono" name="telefono" type="tel" placeholder="Teléfono" autocomplete="tel"></div>
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
        ("/", f"{NOMBRE} | {DATOS['titular']}, abogado en Resistencia, Chaco",
         f"Estudio del abogado {DATOS['titular']}, en Resistencia, Chaco. Gestión de carteras de cobranzas y recupero crediticio, derecho comercial, derecho laboral y factoring.",
         cuerpo_inicio()),
        ("/contacto", "Contacto | " + NOMBRE,
         f"Datos de contacto y formulario de consulta de {NOMBRE} y del abogado {DATOS['titular']}, Don Bosco 137, Resistencia, Chaco.",
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
