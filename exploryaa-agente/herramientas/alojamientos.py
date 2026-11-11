"""Búsqueda de alojamientos con LiteAPI (v3).

Documentación: https://docs.liteapi.travel/reference
Solo consulta tarifas: no hace prebook ni book.
"""
import requests

import config

LITEAPI_URL = "https://api.liteapi.travel/v3.0"


def _cabeceras():
    return {"X-API-Key": config.LITEAPI_KEY, "Accept": "application/json",
            "Content-Type": "application/json"}


def buscar_alojamientos(ciudad: str, codigo_pais: str, entrada: str, salida: str,
                        adultos: int = 2, ninos: int = 0, precio_max_total: float | None = None,
                        estrellas_min: int = 0, max_resultados: int = 8) -> dict:
    """Tarifas más baratas por hotel para toda la estancia."""
    if config.usar_prueba(config.LITEAPI_KEY):
        return _alojamientos_prueba(ciudad, entrada, salida, precio_max_total, estrellas_min)

    # 1) Lista de hoteles de la ciudad (datos estáticos: nombre, estrellas, nota)
    r = requests.get(f"{LITEAPI_URL}/data/hotels",
                     params={"countryCode": codigo_pais.upper(), "cityName": ciudad, "limit": 60},
                     headers=_cabeceras(), timeout=config.TIMEOUT)
    r.raise_for_status()
    hoteles = {h["id"]: h for h in r.json().get("data", [])
               if (h.get("stars") or 0) >= estrellas_min}
    if not hoteles:
        return {"ciudad": ciudad, "hoteles": [], "nota": "No se encontraron hoteles"}

    # 2) Tarifas en vivo para esos hoteles
    ocupacion = {"adults": adultos}
    if ninos:
        ocupacion["children"] = [10] * ninos
    cuerpo = {"hotelIds": list(hoteles)[:60], "occupancies": [ocupacion],
              "currency": config.MONEDA, "guestNationality": config.NACIONALIDAD,
              "checkin": entrada, "checkout": salida, "maxRatesPerHotel": 1}
    r = requests.post(f"{LITEAPI_URL}/hotels/rates", json=cuerpo,
                      headers=_cabeceras(), timeout=config.TIMEOUT)
    r.raise_for_status()

    resultado = []
    for item in r.json().get("data", []):
        hotel = hoteles.get(item.get("hotelId"), {})
        precio = _precio_minimo(item)
        if precio is None or (precio_max_total and precio > precio_max_total):
            continue
        resultado.append({
            "id": item.get("hotelId"),
            "nombre": hotel.get("name"),
            "estrellas": hotel.get("stars"),
            "nota_huespedes": hotel.get("rating"),
            "direccion": hotel.get("address"),
            "precio_total_estancia": precio,
            "moneda": config.MONEDA,
            "regimen": _regimen(item),
        })
    resultado.sort(key=lambda h: h["precio_total_estancia"])
    return {"ciudad": ciudad, "entrada": entrada, "salida": salida,
            "hoteles": resultado[:max_resultados],
            "nota": "precio_total_estancia es para todas las noches y huéspedes"}


def _precio_minimo(item: dict) -> float | None:
    precios = []
    for tipo in item.get("roomTypes", []):
        oferta = tipo.get("offerRetailRate") or {}
        if oferta.get("amount") is not None:
            precios.append(float(oferta["amount"]))
    return min(precios) if precios else None


def _regimen(item: dict) -> str:
    try:
        return item["roomTypes"][0]["rates"][0].get("boardName", "")
    except (KeyError, IndexError):
        return ""


def _alojamientos_prueba(ciudad, entrada, salida, precio_max_total, estrellas_min):
    base = [("Hotel Mirador", 3, 8.4, 138), ("Casa Antigua Boutique", 4, 9.1, 214),
            ("Hostal Centro", 2, 7.9, 86), ("Grand Palace", 5, 9.3, 420)]
    hoteles = [{"id": f"prueba_hotel_{i}", "nombre": f"{n} {ciudad}", "estrellas": e,
                "nota_huespedes": nota, "direccion": f"Centro de {ciudad}",
                "precio_total_estancia": p, "moneda": config.MONEDA, "regimen": "Solo alojamiento"}
               for i, (n, e, nota, p) in enumerate(base)
               if e >= estrellas_min and (not precio_max_total or p <= precio_max_total)]
    hoteles.sort(key=lambda h: h["precio_total_estancia"])
    return {"ciudad": ciudad, "entrada": entrada, "salida": salida, "hoteles": hoteles,
            "nota": "DATOS DE PRUEBA - precio_total_estancia es para todas las noches y huéspedes"}
