# Sitio web del Estudio Graciosi

- `estudio.json`: fuente única de los datos del estudio (nombre, domicilio, teléfonos, áreas).
- `v1-retoque/`: sitio publicado. Conserva la estética del sitio anterior en Wix.
  - `python3 build.py` genera la vista previa en `preview/`.
  - `python3 build.py --final` genera `dist/`, que es lo que publica Netlify.
- `v2-nueva-posible/`: rediseño alternativo inspirado en Clifford Chance, guardado sin publicar.
- `CHANGELOG-contenido.md`: registro de cambios de contenido.
- `REFERENCIAS-CONTENIDO.md`: análisis de sitios de referencia.

Netlify publica la carpeta `v1-retoque/dist`. Después de cada cambio hay que correr `python3 build.py --final` y guardar los cambios en el repositorio.
