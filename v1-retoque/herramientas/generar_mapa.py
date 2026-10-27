"""Genera src/mapa-provincias.json (contornos simplificados de las provincias de Argentina).

Fuente: Natural Earth, ne_10m_admin_1_states_provinces (dominio público).
Uso: python3 generar_mapa.py ruta/al/ne_10m_admin_1_states_provinces.geojson
Se corre una sola vez; el sitio solo lee el JSON resultante.
"""
import json
import math
import sys
from pathlib import Path

TOL = 0.04          # grados; tolerancia de simplificación
AREA_MIN = 0.05     # grados cuadrados; descarta islas diminutas
ESCALA = 60         # unidades SVG por grado


def rdp(pts, tol):
    if len(pts) < 3:
        return pts
    (x1, y1), (x2, y2) = pts[0], pts[-1]
    dx, dy = x2 - x1, y2 - y1
    norma = math.hypot(dx, dy) or 1e-12
    mx, mi = 0, 0
    for i in range(1, len(pts) - 1):
        d = abs(dy * pts[i][0] - dx * pts[i][1] + x2 * y1 - y2 * x1) / norma
        if d > mx:
            mx, mi = d, i
    if mx > tol:
        return rdp(pts[: mi + 1], tol)[:-1] + rdp(pts[mi:], tol)
    return [pts[0], pts[-1]]


def simplificar_anillo(pts):
    # el anillo cierra sobre sí mismo: se parte en dos tramos por el punto más lejano al inicio
    mitad = max(range(len(pts)), key=lambda i: math.hypot(pts[i][0] - pts[0][0], pts[i][1] - pts[0][1]))
    return rdp(pts[: mitad + 1], TOL)[:-1] + rdp(pts[mitad:], TOL)[:-1]


def area(anillo):
    return abs(sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(anillo, anillo[1:] + anillo[:1]))) / 2


def main(origen):
    datos = json.loads(Path(origen).read_text(encoding="utf-8"))
    provincias = [f for f in datos["features"] if f["properties"].get("iso_a2") == "AR"]
    lon0, lat0 = -73.7, -22.0   # esquina noroeste del mapa continental
    anillos = {}
    for f in provincias:
        geom = f["geometry"]
        poligonos = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
        salida = []
        for pol in poligonos:
            ext = pol[0]
            if area(ext) < AREA_MIN:
                continue
            salida.append(simplificar_anillo([tuple(p) for p in ext]))
        anillos[f["properties"]["name"]] = salida
    coef = math.cos(math.radians(38))
    def proy(p):
        return ((p[0] - lon0) * coef * ESCALA, (lat0 - p[1]) * ESCALA)
    resultado, xs, ys = {}, [], []
    for nombre, pols in anillos.items():
        d = ""
        cx = cy = n = 0
        for a in pols:
            q = [proy(p) for p in a]
            xs += [p[0] for p in q]; ys += [p[1] for p in q]
            d += "M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in q) + "Z"
            mayor = max(pols, key=area)
            if a is mayor:
                cx = sum(p[0] for p in q) / len(q); cy = sum(p[1] for p in q) / len(q)
        resultado[nombre] = {"d": d, "centro": [round(cx, 1), round(cy, 1)]}
    # solo el continente: se recorta la vista (sin Tierra del Fuego ni Antártida)
    caja = [0, 0, round(max(xs), 1), round(max(ys), 1)]
    out = {"fuente": "Natural Earth (dominio público)", "provincias": resultado, "caja": caja}
    destino = Path(__file__).parent.parent / "src" / "mapa-provincias.json"
    destino.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(destino, destino.stat().st_size, "bytes", caja)


if __name__ == "__main__":
    main(sys.argv[1])
