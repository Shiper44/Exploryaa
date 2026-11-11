"""Búsqueda de experiencias y actividades con la Viator Partner API v2.

Documentación: https://docs.viator.com/partner-api/technical
Con acceso básico de afiliado: precios + enlace; el cliente reserva en viator.com.
"""
import requests

import config

VIATOR_URL = "https://api.viator.com/partner"


def _cabeceras():
    return {"exp-api-key": config.VIATOR_API_KEY,
            "Accept": "application/json;version=2.0",
            "Accept-Language": "es-ES",
            "Content-Type": "application/json"}


def buscar_experiencias(destino: str, intereses: str = "", precio_max_persona: float | None = None,
                        max_resultados: int = 8) -> dict:
    """Busca actividades por texto, p. ej. destino='Roma', intereses='gastronomía'."""
    if config.usar_prueba(config.VIATOR_API_KEY):
        return _experiencias_prueba(destino, precio_max_persona)

    termino = f"{destino} {intereses}".strip()
    cuerpo = {"searchTerm": termino, "currency": config.MONEDA,
              "searchTypes": [{"searchType": "PRODUCTS",
                               "pagination": {"start": 1, "count": 30}}]}
    r = requests.post(f"{VIATOR_URL}/search/freetext", json=cuerpo,
                      headers=_cabeceras(), timeout=config.TIMEOUT)
    r.raise_for_status()
    productos = r.json().get("products", {}).get("results", [])

    resultado = []
    for p in productos:
        precio = (p.get("pricing", {}).get("summary", {}) or {}).get("fromPrice")
        if precio is None or (precio_max_persona and precio > precio_max_persona):
            continue
        resenas = p.get("reviews", {}) or {}
        resultado.append({
            "id": p.get("productCode"),
            "titulo": p.get("title"),
            "precio_por_persona": float(precio),
            "moneda": config.MONEDA,
            "valoracion": resenas.get("combinedAverageRating"),
            "num_resenas": resenas.get("totalReviews"),
            "duracion": _duracion(p.get("duration", {})),
            "enlace": p.get("productUrl"),
            "fuente": "Viator",
        })
    resultado.sort(key=lambda e: (-(e["valoracion"] or 0), e["precio_por_persona"]))
    return {"destino": destino, "experiencias": resultado[:max_resultados],
            "nota": "precio_por_persona; multiplica por el número de viajeros"}


def _duracion(d: dict) -> str:
    minutos = d.get("fixedDurationInMinutes") or d.get("variableDurationFromMinutes")
    return f"{round(minutos / 60, 1)} h" if minutos else ""


def _experiencias_prueba(destino, precio_max_persona):
    base = [("Free tour por el casco antiguo", 15, 4.8, "2.5 h"),
            ("Ruta gastronómica con degustación", 69, 4.9, "3 h"),
            ("Entrada sin colas al monumento principal", 32, 4.6, "1.5 h"),
            ("Excursión de día completo a los alrededores", 119, 4.7, "9 h")]
    exp = [{"id": f"prueba_exp_{i}", "titulo": f"{t} de {destino}", "precio_por_persona": p,
            "moneda": config.MONEDA, "valoracion": v, "num_resenas": 1200 - i * 200,
            "duracion": d, "enlace": "https://www.viator.com/", "fuente": "Viator (prueba)"}
           for i, (t, p, v, d) in enumerate(base)
           if not precio_max_persona or p <= precio_max_persona]
    exp.sort(key=lambda e: (-e["valoracion"], e["precio_por_persona"]))
    return {"destino": destino, "experiencias": exp,
            "nota": "DATOS DE PRUEBA - precio_por_persona; multiplica por el número de viajeros"}
