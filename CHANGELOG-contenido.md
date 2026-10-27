# Registro de cambios de contenido

## 2026-10-07

- Octavio aprueba las decisiones del inventario (`INVENTARIO-CONTENIDO.md`). Siguen pendientes los puntos 6 a 9.
- Primera propuesta de portada (`preview/portada.html`, generada desde `src/portada.template.html` y `estudio.json` con `build.py`). Es un borrador sin publicar.
  - Titular del banner: reescrito a partir de "Somos un estudio especializado en gestión de carteras de cobranzas y recupero crediticio".
  - Frase institucional: reescrita a partir de la presentación de la portada y de "La Visión" (Acerca de). Reemplaza la frase "frondosa experiencia", que se descarta.
  - Descripciones de las áreas: tomadas de los servicios 01 a 04 de la portada actual. Se quitaron las cifras sin confirmar ("miles de expedientes", "cientos de demandas").
  - Publicaciones y novedades: solo la estructura, sin contenido, hasta que Octavio decida sobre la sección.
  - El CUIT no figura en el pie de página hasta que Octavio lo confirme.
- Octavio aprueba la estructura y el estilo de la portada.
- Tipografía: Plus Jakarta Sans. Octavio pidió la más parecida a la de Clifford Chance (CliffordChanceVariableVF, una fuente propia que no se puede usar). Elegida comparando las dos fuentes lado a lado; reemplaza a Lato. Los títulos llevan un interletrado de -0,015 em para igualar el ancho del original.
- Trato en los textos: impersonal, sin tuteo, voseo ni usted.
- Páginas internas, primera versión (21 páginas generadas por `build.py`): El Estudio, Áreas de práctica y una página por área, Equipo, Cobertura y una página por provincia, Publicaciones, Contacto, Mapa del sitio, más las páginas legales con marcadores (privacidad, publicidad profesional, accesibilidad).
  - Todos los textos salen del sitio actual (portada, servicios 01 a 04 y "Acerca de"). Donde el sitio actual no dice nada (cómo se trabaja en cada área, la forma de actuación por provincia, los valores) queda `[PENDIENTE]`.
  - La portada pasa a tener un único h1. Los otros dos mensajes del banner usan h2 con el mismo estilo.
  - `redirecciones.txt`: las 301 de la tabla aprobada. `build.py --final` genera `dist/` con direcciones limpias, `sitemap.xml` y `_redirects`.
- Octavio decide no publicar una política de privacidad por ahora. Se quitan la página y su enlace en el pie de página. La dirección vieja de Wix (`/política-de-privacidad`) redirige a la portada.
- Quedan para después: la revisión de las páginas internas y los textos pendientes ("cómo se trabaja" en cada área, la forma de actuación por provincia).

## 2026-10-07 (rediseño)

- A pedido de Octavio, la portada sigue de cerca el formato de Clifford Chance:
  - Encabezado con la marca arriba y el menú debajo.
  - Banner con fotos a todo el ancho que se desplaza solo, con puntos indicadores. Reemplaza el cambio manual 1/2/3 que pedía el instructivo; lo decidió Octavio.
  - Frase institucional más corta.
  - Áreas de práctica en un carrusel de tarjetas con foto (formato "Thought Leadership").
  - Cobertura en columnas con filete vertical (formato "News").
  - Pie de página oscuro.
- Fotos de Resistencia aportadas por Octavio (adjuntas al chat). Antes de publicar el sitio hay que confirmar que hay derecho de uso de cada una: varias parecen tomadas de internet, y una tenía marca de agua de "regionlitoral", que se recortó.
- Publicaciones y novedades salen de la portada hasta que haya contenido.
- Frase institucional nueva: "Acompañamos al acreedor en todo el ciclo del crédito impago". El texto de apoyo sale de la presentación y de "La Visión" del sitio actual.

## 2026-10-08

- Octavio divide el proyecto en dos versiones:
  1. **Retoque de la web actual**, manteniendo su estética. Es la prioridad.
  2. **Nueva posible versión**: el rediseño inspirado en Clifford Chance queda guardado en `v2-nueva-posible/`, con la vista previa publicada en https://claude.ai/artifact/EMnBzictidKMB43XxrY1YK (versión 3). No se sigue trabajando en ella por ahora.
- **Versión 1** (`v1-retoque/`): Octavio elige sacar el sitio de Wix y conservar su estética actual. Hay dos páginas, Inicio y Contacto, como hoy.
  - Se mantienen el diseño, los colores (azul marino #10284D, azul #015989, celeste #0285CE, gris #F0F2F4) y las fotos de la oficina publicadas en Wix.
  - Tipografías: las de Wix (Kepler, Didot italic, Proxima Nova) tienen licencia solo dentro de Wix. Se reemplazan por Crimson Pro, Playfair Display en cursiva y Figtree.
  - Nombre: "Estudio Graciosi" en lugar de "Graciosi & Asociados" / "Estudio Graciosi & Asociados", como confirmó Octavio.
  - Servicios: textos originales, con dos correcciones: "primer etapa" pasa a "primera etapa", y se quitan las cifras sin confirmar ("miles de expedientes", "cientos de demandas"). Se quitan los enlaces "Leer más", que llevaban a la misma portada.
  - La frase "frondosa experiencia…" se reemplaza por la visión de "Acerca de", resumida.
  - Botón "Contacto" de la portada: ahora lleva a la página de contacto. Antes abría una llamada.
  - Contacto: "Contáctanos" pasa a "Contacto", con el texto en trato impersonal. Se corrige el domicilio, que decía "Don Bosco 42". Se suma el segundo teléfono, el campo "tipo de consulta" y el aviso de que el formulario no genera relación profesional. Se quitan los íconos de LinkedIn y Facebook, que enlazaban a las páginas de Wix y no a las del Estudio.
  - Pie: domicilio con Oficina 3. El CUIT, el código postal, los horarios y el aviso de publicidad profesional quedan marcados como pendientes. Se quita el enlace a la política de privacidad y "© 2025" pasa a mostrar el año actual.
  - Las demás páginas de Wix, que tienen texto de plantilla, redirigen a Inicio (301).
- Octavio redefine "Nuestros servicios" (versión 1), con efecto también en `estudio.json`:
  1. **Recupero crediticio:** resume los servicios 01 a 03 del sitio actual (gestión temprana, mora tardía, ejecuciones judiciales).
  2. **Derecho comercial:** texto nuevo redactado por Claude. Octavio tiene que revisar cada servicio enumerado.
  3. **Derecho laboral:** texto nuevo redactado por Claude. Falta confirmar si el Estudio representa a empleadores, a trabajadores o a ambos.
  4. **Factoring:** se mantiene el texto original.
- Banner principal (versión 1): "Somos un estudio especializado en derecho comercial, laboral y gestión de carteras de cobranzas.", texto indicado por Octavio.

## 2026-10-09

- Versión 1, cambios pedidos por Octavio:
  - **Marca** (encabezado y pie): "Estudio Graciosi" sin cursiva, en la tipografía de los títulos, con "Abogados" al lado. Reemplaza a "Estudio de abogados".
  - **Pie:** sobre "© Estudio Graciosi" ya no va nada; se quita el marcador del aviso de publicidad profesional.
  - **Datos confirmados:** se publica el CUIT 20371576380, el código postal H3500AHB y el número +54 9 3624 856500. Los horarios no se publican.
  - **Textos de Recupero crediticio, Derecho comercial y Derecho laboral:** redactados por Octavio. Solo se corrigieron espacios dobles y "localizacióndel".
  - **Frase de la sección de visión:** vuelve "Combinamos una frondosa experiencia técnica…", por decisión de Octavio.

## 2026-10-12

- Versión 1:
  - **WhatsApp:** Octavio confirma que +54 9 3624 856500 tiene WhatsApp; se agrega el enlace.
  - **"Abogados" junto a la marca:** más chico (15 px) y centrado con la línea del nombre.
  - **Submenús en la barra superior:**
    - Inicio.
    - El Estudio: Presentación, Nuestra visión, La oficina.
    - Servicios: las cuatro áreas.
    - Contacto: Formulario de consulta, Teléfonos y correo, Ubicación.
    
    Cada opción lleva a su sección dentro de Inicio o de Contacto. En el celular, el menú se abre con el ícono ☰ y los submenús con la flecha.
- **Encabezado al estilo Clifford Chance** (versión mínima, a pedido de Octavio):
  - Marca grande arriba ("Estudio Graciosi", con "Abogados" al lado) y menú en una fila debajo.
  - Tres opciones: El Estudio, Servicios y Contacto, con sus submenús. Se quita "Inicio" porque la marca lleva a la portada.
  - A la derecha, en lugar de "Log in", va "Consultas por WhatsApp".
  - Sin buscador: con dos páginas no hace falta.
- **Menú siempre visible:** se quita el ícono ☰. Las tres opciones quedan a la vista en cualquier ancho, también en el celular. En pantallas chicas se oculta "Consultas por WhatsApp" de la barra; el WhatsApp sigue en Contacto y en el pie.
- **Preparación para publicar** (versión 1): revisión completa de `dist/`, sin enlaces rotos, errores ni desbordes en celular. Se agregan:
  - Página "Consulta enviada" (`/gracias/`), a la que lleva el formulario.
  - Campo oculto contra spam en el formulario.
  - Página de error 404.
  - Ícono de pestaña con las iniciales "EG", como el cartel de la puerta.
  - Vista previa al compartir el enlace (Open Graph), con la foto de la recepción.
  - `robots.txt`.
- **Repositorio:** el proyecto pasa a GitHub (`octaviograciosi/estudiograciosi-web`), conectado a Netlify; cada push a `main` publica solo. El formulario queda activado en Netlify (Octavio confirmó que llegó la consulta de prueba). Se suma `CLAUDE.md`, con el instructivo original de Octavio y, arriba, el estado actual del proyecto.

## 2026-10-25

- Dominio: se decide dejar estudiograciosi.com registrado en Wix (la diferencia de costo con otro registrador es de unos US$ 10 por año). Los registros DNS todavía apuntan a Wix; falta que Octavio los cambie a Netlify. Detalle en `CLAUDE.md`.

## 2026-10-26

- Se instalan en el proyecto (`.claude/skills/`) 12 skills de diseño y animación de Emil Kowalski (https://github.com/emilkowalski/skills, licencia MIT). No cambian el contenido del sitio.

## 2026-10-26

- **Estilo visual nuevo de la versión 1** (solo diseño; vista previa pendiente de aprobación, no publicado en Netlify):
  - Encabezado con logo EG, línea vertical y "ESTUDIO GRACIOSI ABOGADOS". Menú: El Estudio, Áreas de práctica, Cobertura y Contacto. Octavio pide no mencionar Equipo. Publicaciones no se incluye porque no hay artículos.
  - Tres banners con cambio manual: derecho comercial y recupero crediticio (texto del banner indicado por Octavio), cobertura (texto exacto de la referencia, sin corregir) y consultas ("Las consultas se reciben por formulario, por teléfono y por WhatsApp.").
  - Bloque central con los textos ya aprobados (presentación y frase de visión). Las áreas de práctica conservan los textos de Octavio y suman foto.
  - Cobertura: las seis provincias de `estudio.json` en grilla de dos columnas. El banner menciona cuatro, como pidió Octavio.
  - Pie gris oscuro, en español, con enlaces centrados en dos columnas. El CUIT y el domicilio se mantienen; sobre el © no va nada más.
  - Tipografía Plus Jakarta Sans en todo el sitio. Sin color de acento.
  - Fotos aportadas por Octavio (carpeta de Drive), optimizadas en WebP. La foto de la estela de piedra no se usa por ahora. Para Factoring se usa la foto propia del área de trabajo.
  - Sin cambios en `estudio.json`, redirecciones, formulario ni Netlify.

## 2026-10-27

- Estilo nuevo, ajustes pedidos por Octavio (vista previa, sin publicar):
  - Cuatro banners con las fotos indicadas: 1 estela de piedra ("Estudio Graciosi" y la frase del banner de Octavio), 2 mapa del NEA (texto sin corregir), 3 estatua frente a las columnas (texto de la referencia de Octavio sobre carteras de cobranzas y recupero de activos) y 4 figura de la Justicia.
  - Se elimina de la portada el párrafo "Titular: Octavio Graciosi. Nuestro equipo se destaca…". Queda la frase de visión.
  - Cobertura: se quita el listado de provincias y se muestra un mapa de Argentina con las seis provincias de `estudio.json` resaltadas y rotuladas. Contornos de Natural Earth (dominio público), simplificados.
  - Nuevas fotos para las tarjetas: Derecho laboral (grabado de una audiencia) y Factoring (pluma sobre documentos). Se recortó el borde inferior de la foto de Derecho laboral, que traía una leyenda de numeración de banco de imágenes.
  - Pendiente: la foto de Derecho laboral parece una vista previa de Shutterstock (330 px, con leyenda). Hay que confirmar que Octavio tiene la licencia antes de publicar. La de Factoring viene de Unsplash.

## 2026-10-27 (textos y contacto)

- Textos de los banners, fijados por Octavio:
  1. "Estudio líder en calidad, servicio y compromiso" y "Nuestra fortaleza es la atención personalizada, ágil, con un sólido conocimiento del panorama local." (Quiénes somos).
  2. "Cobertura en la región NEA" y "Poseemos competencia en las provincias de Chaco, Corrientes, Formosa y Misiones, a lo que se adicionan Santa Fe y Córdoba para la rama de recupero de activos." (Cobertura). Reemplaza el texto anterior del banner de cobertura.
  3. "Derecho comercial y recupero crediticio" y el texto sobre la experiencia en gestión de carteras de cobranzas y recupero de activos (Áreas de práctica).
  4. "Asesoramiento Estratégico" y "Brindamos nuestra expertise en los temas que se nos presentan…" (Contacto). Reemplaza al banner "Consultas".
- Bloque central: se elimina el título "Estudio Graciosi". Queda la frase "Combinamos una frondosa experiencia técnica…".
- Cobertura: la bajada pasa a "Provincias donde tenemos competencia con matrícula habilitada." Las matrículas siguen como `[PENDIENTE: confirmar]` en `estudio.json`; hay que confirmarlas con Octavio antes de publicar.
- Recupero crediticio: texto nuevo de Octavio ("Nos mantenemos a la vanguardia de las tendencias…"). Se corrigieron "mantenernos", "menra", "basta" (vasta) y "certeza que" (certeza de que).
- Contacto: el texto introductorio queda solo con "Para recibir asesoramiento o realizar una consulta, se encuentra a disposición el siguiente formulario, así como los datos de contacto del Estudio." Se elimina el desplegable "Tipo de consulta" del formulario. El logo de WhatsApp reemplaza a "Tel:" y a "WhatsApp" en cada línea de teléfono, en Contacto y en el pie.
- Aviso: los textos con "líder", "excelencia", "más alto estándar", "éxito" son afirmaciones de publicidad profesional. Octavio decidió usarlos; conviene revisarlos con las normas de los colegios de abogados antes de publicar.

## 2026-10-27 (publicación)

- Octavio aprueba el estilo nuevo y confirma que las matrículas de las seis provincias están al día. `estudio.json` lo registra (los números de matrícula siguen pendientes y no se publican).
- Logo: se usa el archivo oficial de Octavio (`logo.webp`) en el encabezado, en lugar del logo armado con texto.
- Se genera `dist/` y se publica en Netlify.
