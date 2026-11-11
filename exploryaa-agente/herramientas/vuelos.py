"""Búsqueda de vuelos (solo ida o ida y vuelta) con la API de Duffel.

Documentación: https://duffel.com/docs/api/offer-requests
Solo consulta precios: no crea pedidos ni reservas.
"""
import requests

import config

DUFFEL_URL = "https://api.duffel.com"


def _cabeceras():
    return {
        "Authorization": f"Bearer {config.DUFFEL_TOKEN}",
        "Duffel-Version": "v2",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


def buscar_codigo_aeropuerto(texto: str) -> list[dict]:
    """Convierte 'Barcelona' en códigos IATA (BCN...)."""
    if config.usar_prueba(config.DUFFEL_TOKEN):
        ejemplos = {"barcelona": "BCN", "madrid": "MAD", "roma": "FCO", "paris": "PAR",
                    "parís": "PAR", "londres": "LON", "lisboa": "LIS", "tokio": "TYO"}
        codigo = ejemplos.get(texto.lower().strip(), texto.upper()[:3])
        return [{"codigo": codigo, "nombre": texto, "tipo": "city", "prueba": True}]

    r = requests.get(f"{DUFFEL_URL}/places/suggestions", params={"query": texto},
                     headers=_cabeceras(), timeout=config.TIMEOUT)
    r.raise_for_status()
    return [
        {"codigo": p.get("iata_code"), "nombre": p.get("name"), "tipo": p.get("type"),
         "ciudad": p.get("city_name")}
        for p in r.json().get("data", [])[:5]
    ]


def _resumir_tramo(tramo: dict) -> dict:
    segmentos = tramo.get("segments", [])
    primero, ultimo = segmentos[0], segmentos[-1]
    return {
        "origen": tramo.get("origin", {}).get("iata_code"),
        "destino": tramo.get("destination", {}).get("iata_code"),
        "salida": primero.get("departing_at"),
        "llegada": ultimo.get("arriving_at"),
        "duracion": tramo.get("duration"),
        "escalas": len(segmentos) - 1,
        "aerolineas": sorted({s.get("marketing_carrier", {}).get("name", "") for s in segmentos}),
    }


def buscar_vuelos(origen: str, destino: str, fecha_ida: str, fecha_vuelta: str | None = None,
                  adultos: int = 1, ninos: int = 0, clase: str = "economy",
                  max_escalas: int = 1, max_resultados: int = 8) -> dict:
    """Devuelve las ofertas más baratas. Sin fecha_vuelta = solo ida."""
    if config.usar_prueba(config.DUFFEL_TOKEN):
        return _vuelos_prueba(origen, destino, fecha_ida, fecha_vuelta, adultos + ninos)

    tramos = [{"origin": origen, "destination": destino, "departure_date": fecha_ida}]
    if fecha_vuelta:
        tramos.append({"origin": destino, "destination": origen, "departure_date": fecha_vuelta})
    pasajeros = [{"type": "adult"}] * adultos + [{"age": 10}] * ninos

    cuerpo = {"data": {"slices": tramos, "passengers": pasajeros,
                       "cabin_class": clase, "max_connections": max_escalas}}
    r = requests.post(f"{DUFFEL_URL}/air/offer_requests",
                      params={"return_offers": "true", "supplier_timeout": 20000},
                      json=cuerpo, headers=_cabeceras(), timeout=config.TIMEOUT)
    r.raise_for_status()
    ofertas = r.json().get("data", {}).get("offers", [])
    ofertas.sort(key=lambda o: float(o.get("total_amount", 0)))

    resultado = []
    for o in ofertas[:max_resultados]:
        resultado.append({
            "id": o.get("id"),
            "precio_total": float(o.get("total_amount", 0)),
            "moneda": o.get("total_currency"),
            "aerolinea": o.get("owner", {}).get("name"),
            "tramos": [_resumir_tramo(t) for t in o.get("slices", [])],
            "equipaje_incluido": _equipaje(o),
        })
    return {"tipo_viaje": "ida y vuelta" if fecha_vuelta else "solo ida",
            "pasajeros": adultos + ninos, "ofertas": resultado,
            "nota": "precio_total es para todos los pasajeros"}


def _equipaje(oferta: dict) -> str:
    try:
        maletas = oferta["slices"][0]["segments"][0]["passengers"][0].get("baggages", [])
        return ", ".join(f'{b["quantity"]}x {b["type"]}' for b in maletas) or "solo equipaje de mano"
    except (KeyError, IndexError):
        return "desconocido"


def _vuelos_prueba(origen, destino, fecha_ida, fecha_vuelta, pasajeros):
    base = [("Vueling", 62, 0), ("Iberia", 95, 0), ("Ryanair", 41, 0), ("ITA Airways", 118, 1)]
    factor = 2 if fecha_vuelta else 1
    ofertas = []
    for i, (aerolinea, precio, escalas) in enumerate(base):
        tramos = [{"origen": origen, "destino": destino, "salida": f"{fecha_ida}T08:{10 + i * 5}:00",
                   "llegada": f"{fecha_ida}T10:{20 + i * 5}:00", "duracion": "PT2H10M",
                   "escalas": escalas, "aerolineas": [aerolinea]}]
        if fecha_vuelta:
            tramos.append({"origen": destino, "destino": origen, "salida": f"{fecha_vuelta}T19:00:00",
                           "llegada": f"{fecha_vuelta}T21:10:00", "duracion": "PT2H10M",
                           "escalas": escalas, "aerolineas": [aerolinea]})
        ofertas.append({"id": f"prueba_vuelo_{i}", "precio_total": precio * factor * pasajeros,
                        "moneda": config.MONEDA, "aerolinea": aerolinea, "tramos": tramos,
                        "equipaje_incluido": "solo equipaje de mano"})
    ofertas.sort(key=lambda o: o["precio_total"])
    return {"tipo_viaje": "ida y vuelta" if fecha_vuelta else "solo ida", "pasajeros": pasajeros,
            "ofertas": ofertas, "nota": "DATOS DE PRUEBA - precio_total es para todos los pasajeros"}
