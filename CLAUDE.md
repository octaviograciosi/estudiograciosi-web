# Sitio web del Estudio Graciosi: instrucciones para Claude

## Estado del proyecto (actualizado el 25/10/2026)

Esta sección resume las decisiones que Octavio tomó durante el trabajo. Cuando contradice al instructivo original (más abajo), **manda esta sección**.

- **Responder siempre en español de Argentina, con voseo.** Octavio es abogado, no programador: explicar sin jerga y pedir solo lo que tiene que hacer él.
- **Sitio publicado: `v1-retoque/`.** Conserva la estética del sitio anterior en Wix, con dos páginas: Inicio y Contacto.
  - Datos: salen de `estudio.json`, la fuente única.
  - Generación: `python3 build.py --final` genera `v1-retoque/dist/`.
  - Publicación: cada `git push` a `main` publica solo en Netlify (sitio `unrivaled-sorbet-f4d667`). La carpeta publicada está definida en `netlify.toml`.
- **Rediseño alternativo: `v2-nueva-posible/`.** Inspirado en Clifford Chance. Está guardado y no se trabaja en él salvo pedido expreso.
- **Áreas de práctica:** Recupero crediticio, Derecho comercial, Derecho laboral y Factoring. Los textos de cada área los fijó Octavio.
- **Trato en los textos:** impersonal (sin tuteo, voseo ni usted).
- **Estilo nuevo (26/10/2026, en vista previa, falta aprobación de Octavio antes de publicar):** solo cambia el diseño de `v1-retoque/`. Mismo contenido, `estudio.json`, redirecciones, formulario y despliegue.
  - Encabezado con logo EG, línea vertical y "ESTUDIO GRACIOSI ABOGADOS". Menú a la derecha en texto simple: El Estudio, Áreas de práctica, Cobertura y Contacto. **No se menciona Equipo** (decisión de Octavio). Publicaciones queda fuera hasta que haya artículos reales. En el celular el menú es desplegable.
  - Portada: cuatro banners, en este orden: estela, mapa NEA, columnas y figura de la Justicia (texto a la izquierda, imagen a la derecha), con cambio manual por flechas, sin cambio automático. Octavio eligió cuatro, aunque el instructivo original decía máximo tres. Después, bloque central (sin el párrafo de "Titular", que Octavio mandó eliminar), carrusel de Áreas de práctica con fotos, Cobertura con un mapa de Argentina que resalta las provincias de `estudio.json` (sin listado de provincias en texto) y pie gris oscuro en español. El mapa se dibuja desde `v1-retoque/src/mapa-provincias.json`, generado con `herramientas/generar_mapa.py` a partir de Natural Earth (dominio público).
  - El texto del banner de cobertura queda exactamente: "Brindamos cobertura en toda la zona NEA: Chaco, Corrientes, Formosa y Misiones." Octavio pidió no corregirlo (los datos tienen seis provincias).
  - Tipografía: Plus Jakarta Sans en todo el sitio. Color: azul marino #10284D para títulos y detalles. **Para cualquier color de acento hay que preguntarle a Octavio antes.**
  - Las fotos de `src/img/` (carpeta de Drive de Octavio) son definitivas y reemplazan la regla anterior de "solo fotos de la oficina". Se usan optimizadas (WebP, con texto alternativo).
- **No se publican:** política de privacidad, horarios ni aviso de publicidad profesional (decisión de Octavio, por ahora).
- **Se publican:** CUIT 20371576380, código postal H3500AHB y los dos teléfonos con WhatsApp.
- **Fotos:** ver "Estilo nuevo". Antes del estilo nuevo solo se usaban fotos de la oficina; Octavio decidió que las nuevas fotos son definitivas. Queda anotado confirmar el derecho de uso.
- **Skills de diseño (Emil Kowalski, licencia MIT):** instalados en `.claude/skills/`. Se usan para decisiones de diseño y animación del sitio (por ejemplo `emil-design-eng`, `animate`, `mobile-native`, `break-ui`). Se omitieron `animate-expo`, `write-swift` y `ask-sonner`, que no aplican a un sitio estático. Cuando un criterio de esos skills choque con lo que Octavio decidió o con el instructivo, manda Octavio.
- **Después de cada cambio:**
  1. Regenerar `dist/`.
  2. Revisar en computadora y en celular.
  3. Anotar el cambio en `CHANGELOG-contenido.md`.
  4. Hacer commit y push a `main`.
- **Dominio (pendiente, en curso al 25/10/2026):**
  - Decisión de Octavio: el dominio **se queda registrado en Wix** (cuesta unos US$ 20 por año, no justifica transferirlo; vence el 14/05/2027). Cloudflare quedó descartado: Wix no permite transferir directo y obliga a esperar 60 días.
  - Netlify ya reconoció estudiograciosi.com como dominio del sitio `unrivaled-sorbet-f4d667`.
  - **Falta que Octavio cambie los registros DNS en Wix** (Dominios, estudiograciosi.com, Administrar registros DNS):
    1. Borrar los tres registros A `185.230.63.171`, `185.230.63.186` y `185.230.63.107`.
    2. Agregar un registro A: host `estudiograciosi.com`, valor `75.2.60.5`.
    3. Cambiar el CNAME de `www` de `cdn3.wixdns.net` a `unrivaled-sorbet-f4d667.netlify.app`.
    4. No tocar el TXT de Facebook ni los nameservers `ns2/ns3.wixdns.net`.
  - Al 25/10/2026 esos registros todavía apuntaban a Wix. Cómo verificar: `curl "https://dns.google/resolve?name=estudiograciosi.com&type=A"` debe devolver `75.2.60.5`. Después confirmar que https://estudiograciosi.com muestre el sitio nuevo y que el candado (https) esté activo.
  - Recién con la web nueva funcionando en el dominio, Octavio da de baja el **plan del sitio** de Wix (no el dominio).
- **Formulario:** activado en Netlify (Forms). La consulta de prueba llegó. Falta confirmar con Octavio que cargó el aviso por correo a `estudiograciosi@gmail.com`.
- **Pendientes menores:** confirmar el derecho de uso de las fotos antes de usarlas, decidir si va aviso de privacidad bajo el formulario, y definir si se agregan "Cómo trabajamos" y la cobertura por provincias (ver `REFERENCIAS-CONTENIDO.md`).

---

## Instructivo original (redactado por Octavio)

# Instructivo para Claude Code: sitio web del Estudio Graciosi (estudiograciosi.com)

## 1. Contexto del proyecto

El Estudio Graciosi es un estudio jurídico de Resistencia, Chaco, Argentina, dirigido por el Dr. Octavio Graciosi. Se especializa en litigios ejecutivos y cobro judicial de deudas, con actuación en varias provincias: Chaco, Corrientes, Formosa, Misiones, Santa Fe y Córdoba.

El sitio tiene dos públicos:

1. Empresas y entidades financieras que necesitan un estudio para cobro judicial y ejecuciones.
2. Estudios jurídicos y áreas legales de empresas de otras ciudades que buscan un corresponsal en la región.

Objetivo del sitio: transmitir seriedad, criterio técnico y presencia regional, y facilitar un primer contacto claro para cualquiera de los dos públicos.

Octavio es quien aprueba todo lo que se publica. Ante cualquier duda sobre contenido jurídico, datos del estudio o texto de publicidad profesional, preguntarle antes de avanzar.

## 2. Referente de diseño: Clifford Chance

El referente principal es https://www.cliffordchance.com/home.html. Es una firma global de gran escala, así que se toma el criterio de diseño y no el tamaño. Debe adaptarse a un estudio regional, sobrio y cercano.

Antes de diseñar, abrir ese sitio en el navegador, recorrer la portada y dos o tres páginas internas, y escribir en un archivo `DISENO.md` lo que se observe: tipografía, jerarquía de títulos, paleta, espaciado, tamaño y proporción de imágenes, comportamiento del menú, diseño de las tarjetas y del pie de página. Ese archivo será la guía visual del proyecto. Referencias secundarias para consultar: sullcrom.com y foresight-law.gr.jp (por su portada limpia y su declaración de misión en pocas líneas).

Prohibido copiar textos, imágenes, logotipos, íconos ni código de cualquier sitio de referencia. Se toman principios de organización y de estilo, no material.

## 3. Qué se toma de Clifford Chance

1. Banner principal a todo el ancho con un titular corto, una frase de apoyo y un único botón. Como máximo tres mensajes, con cambio manual y no automático, para que sea accesible y no distraiga.
2. Una sola frase institucional en el centro de la portada, que diga qué hace el estudio por el cliente. Sin párrafos de historia.
3. Bloque de publicaciones en tarjetas: imagen, título, resumen de dos o tres líneas y enlace. Aquí van artículos y análisis del estudio sobre ejecución, cobro judicial y novedades normativas.
4. Lista de novedades con fecha, debajo de las publicaciones.
5. Menú principal ordenado, con submenús que se despliegan, y un buscador visible.
6. Pie de página completo: mapa del sitio, accesibilidad, aviso de publicidad profesional, privacidad, contacto.
7. Aire y orden: mucho espacio en blanco, textos cortos, imágenes grandes y de calidad.

## 4. Estructura de la portada

De arriba hacia abajo:

1. Encabezado con logotipo, menú principal, buscador y botón de contacto siempre visible.
2. Banner principal con titular, frase de apoyo y un botón.
3. Frase institucional única.
4. Áreas de práctica en tarjetas: ejecuciones y litigios ejecutivos, cobro judicial, y las demás que Octavio confirme.
5. Cobertura territorial: las seis provincias, con enlace a una página por provincia.
6. Publicaciones recientes en tarjetas.
7. Novedades con fecha.
8. Bloque de contacto con dos vías diferenciadas: "Soy una empresa o entidad financiera" y "Soy un estudio o área legal que busca corresponsal".
9. Pie de página.

## 5. Menú principal (máximo seis ítems)

1. El Estudio
2. Áreas de práctica
3. Equipo
4. Cobertura
5. Publicaciones
6. Contacto

No agregar un acceso para clientes ni ningún portal si el estudio no cuenta con uno. Si Octavio lo quiere, se diseña después.

## 6. Páginas internas

1. El Estudio: presentación breve, método de trabajo y valores. Sin cifras que Octavio no haya confirmado.
2. Áreas de práctica: una página por área, con explicación clara, a quién ayuda, cómo se trabaja y un botón de contacto.
3. Equipo: una ficha por integrante, con foto real, cargo, formación y matrículas profesionales según figuren en el archivo de datos. Solo con la autorización de cada persona.
4. Cobertura: una página por provincia, con matrículas y forma de actuación en esa jurisdicción.
5. Publicaciones: artículos con autor, fecha de publicación y fecha de última revisión visibles.
6. Contacto: formulario corto (nombre, correo, teléfono, tipo de consulta y mensaje), datos del estudio, mapa y horarios.

## 7. Estilo visual

1. Sobrio, institucional y actual. Nada que se parezca a un comercio ni a una plantilla genérica de abogados (sin balanzas, martillos, columnas ni fotos de archivo de apretones de manos).
2. Paleta de dos o tres colores como máximo, con buen contraste. Proponer la paleta en `DISENO.md` a partir de lo observado en el referente y de los colores actuales del estudio, y esperar mi aprobación.
3. Tipografía seria y muy legible. Una familia para títulos y otra para texto, como máximo.
4. Fotografías reales del estudio, de la ciudad de Resistencia o del equipo. Si no hay material, dejar espacios reservados marcados como `[PENDIENTE: foto]` y no usar imágenes de archivo que parezcan genéricas.
5. Pocas animaciones, suaves, y que respeten la preferencia de movimiento reducido del usuario.

## 8. Tono y redacción

1. Español de Argentina, formal pero cercano, sin jerga innecesaria.
2. Frases cortas. Un titular dice una sola cosa.
3. No usar guiones largos, flechas ni símbolos decorativos en los textos del sitio.
4. Escribir siempre "Estudio Graciosi" de la misma forma. Mantener coherencia en mayúsculas y en el nombre de las áreas.
5. Evitar frases vacías del tipo "compromiso inquebrantable con la justicia". Preferir descripciones concretas de lo que el estudio hace.

## 9. Reglas para mantener la información del sitio

1. Fuente única de datos. Los datos del estudio (razón social, domicilio, teléfonos, correos, horarios, matrículas por provincia, áreas de práctica, integrantes del equipo) viven en un solo archivo, por ejemplo `src/data/estudio.json` o el equivalente según la tecnología. Ninguna página debe tener esos datos escritos a mano. Si un dato cambia, se modifica en un solo lugar y se propaga a todo el sitio, incluidos el pie de página, la página de contacto y los datos estructurados.
2. No inventar información. Nunca agregar datos jurídicos, cifras, resultados de casos, antigüedad, cantidad de clientes, premios ni matrículas que no estén en el archivo de datos o que Octavio no haya confirmado. Si falta un dato, dejar un marcador visible `[PENDIENTE: confirmar]` y avisarle.
3. Cuidado con las afirmaciones profesionales. Evitar promesas de resultado, comparaciones con otros estudios y cualquier texto que pueda chocar con las normas de publicidad de los colegios de abogados de las provincias donde el estudio tiene matrícula. Ante la duda, redactar de manera informativa y sobria, y consultar.
4. Coherencia territorial y de servicios. La lista de provincias y de servicios debe ser idéntica en la portada, en las páginas de servicios, en el SEO y en los datos estructurados. Si se agrega o quita una provincia o un servicio, actualizar todas las apariciones.
5. Separar lo estable de lo temporal. Las novedades, la normativa comentada y los artículos llevan fecha de publicación y de última revisión visibles. Lo normativo (leyes, aranceles, topes) debe indicar su fecha de vigencia y no presentarse como permanente. Antes de publicar algo normativo, marcarlo para revisión de Octavio.
6. Datos personales y confidencialidad. Nunca publicar nombres de clientes, números de expediente, CUIJ ni detalles de casos reales sin autorización expresa. No incluir datos personales del equipo (celulares, domicilios particulares) más allá de lo que figure como público en el archivo de datos.

## 10. Requisitos técnicos

1. Diseño adaptable (responsive), probado primero en celular. Buena parte de las visitas llegará desde el teléfono.
2. Rendimiento: carga rápida en celular, imágenes optimizadas y con tamaños definidos.
3. Accesibilidad: contraste suficiente, navegación completa con teclado, texto alternativo en las imágenes, títulos en orden jerárquico y tamaño de letra mínimo de 16 px en el texto de lectura.
4. SEO: título y descripción únicos por página, una sola fuente para los metadatos, direcciones URL claras en español y mapa del sitio. Incluir datos estructurados de tipo LegalService (schema.org) generados desde el archivo único de datos.
5. Formulario de contacto: pedir solo lo necesario, aclarar que enviar el formulario no genera una relación profesional con el estudio, indicar qué pasa después y no pedir documentación confidencial por esa vía.
6. Aviso de publicidad profesional y política de privacidad visibles en el pie de página. El texto exacto lo confirma Octavio.

## 11. Forma de trabajo

1. Antes de modificar nada, leer este archivo y revisar `DISENO.md` y el archivo de datos. Antes de construir cualquier página, completar el inventario del contenido actual descripto en la sección 12 y esperar su aprobación.
2. Trabajar en una rama o en una vista previa. No desplegar a producción hasta que Octavio apruebe.
3. Mostrar primero una propuesta de portada (estructura y estilo) y esperar su aprobación antes de construir las páginas internas.
4. Registrar cada cambio de contenido en `CHANGELOG-contenido.md`, con fecha, qué cambió y por qué.
5. No eliminar páginas ni cambiar direcciones URL sin avisar. Si se hace, dejar redirecciones 301 para no perder posicionamiento.
6. Cada tres meses, revisar el sitio completo y entregar un informe de posibles desactualizaciones (teléfonos o correos que no funcionan, enlaces rotos, textos con fechas viejas, integrantes que ya no estén). Solo informe, sin cambios automáticos.

## 12. Qué hacer con el contenido actual de la web

El texto que hoy está publicado en estudiograciosi.com no se copia tal cual ni se descarta. Se usa como material de partida, con este procedimiento:

1. Recorrer el sitio actual completo (todas las páginas, incluidas las de artículos, si las hay) y armar un inventario en `INVENTARIO-CONTENIDO.md`, con una tabla que tenga: página, dirección URL actual, resumen del contenido, fecha si figura, y una decisión propuesta para cada bloque.
2. Las decisiones posibles son cuatro: conservar tal cual, actualizar, reescribir o descartar. Justificar cada una en una línea.
3. Los datos fijos que se encuentren (domicilio, teléfonos, correos, horarios, matrículas, áreas de práctica, integrantes del equipo) se pasan al archivo único de datos. Si hay contradicciones entre páginas o con lo que Octavio informó, marcarlas con `[PENDIENTE: confirmar]` y no elegir una versión por cuenta propia.
4. Los textos normativos o con fecha antigua (leyes, aranceles, topes, plazos) se marcan para revisión de Octavio antes de reutilizarlos.
5. Conservar las direcciones URL actuales siempre que sea posible. Si cambian, registrar la equivalencia en el inventario y preparar redirecciones 301.
6. Los textos que se reescriban deben mantener el sentido jurídico original y no sumar afirmaciones nuevas. Todo lo que se agregue debe salir de datos confirmados.
7. No construir ni modificar ninguna página hasta que Octavio apruebe el inventario.

## 13. Datos que Octavio debe confirmar antes de publicar

1. Texto legal de publicidad profesional para el pie de página.
2. Lista definitiva de áreas de práctica.
3. Integrantes del equipo que aparecerán y sus fichas.
4. Fotografías y logotipo en alta calidad.
5. Teléfonos, correos y horarios públicos.
6. Si habrá sección de publicaciones desde el lanzamiento y quién redacta los artículos.
7. Colores y tipografías actuales del estudio, si deben conservarse.
