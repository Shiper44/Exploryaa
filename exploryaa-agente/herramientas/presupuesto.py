"""Combina vuelo + alojamiento + experiencias sin pasar del presupuesto máximo."""


def _escalas(vuelo: dict) -> int:
    return sum(t.get("escalas", 0) for t in vuelo.get("tramos", []))


def _puntuacion(vuelo, hotel, experiencias) -> float:
    """Más alto = mejor viaje. Premia hotel bueno, experiencias valoradas y vuelos directos."""
    p = (hotel.get("estrellas") or 3) * 1.5 + (hotel.get("nota_huespedes") or 7)
    p += sum((e.get("valoracion") or 4) for e in experiencias) * 1.2
    p -= _escalas(vuelo) * 2
    return p


def armar_paquetes(vuelos: list[dict], hoteles: list[dict], experiencias: list[dict],
                   viajeros: int, presupuesto_max: float, num_experiencias: int = 2,
                   reparto: dict | None = None) -> dict:
    """Devuelve hasta 3 paquetes dentro del presupuesto:
    el más económico, el mejor equilibrio calidad-precio y el más cómodo.

    reparto (opcional) limita cuánto puede ir a cada parte, p. ej.
    {"vuelos": 0.5, "alojamiento": 0.35, "experiencias": 0.15}.
    """
    reparto = reparto or {}
    tope_vuelo = presupuesto_max * reparto["vuelos"] if "vuelos" in reparto else presupuesto_max
    tope_hotel = presupuesto_max * reparto["alojamiento"] if "alojamiento" in reparto else presupuesto_max

    exp_ordenadas = sorted(experiencias, key=lambda e: (-(e.get("valoracion") or 0),
                                                        e["precio_por_persona"]))
    candidatos = []
    for v in vuelos:
        if v["precio_total"] > tope_vuelo:
            continue
        for h in hoteles:
            if h["precio_total_estancia"] > tope_hotel:
                continue
            base = v["precio_total"] + h["precio_total_estancia"]
            if base > presupuesto_max:
                continue
            elegidas, coste_exp = [], 0.0
            for e in exp_ordenadas:
                if len(elegidas) >= num_experiencias:
                    break
                coste = e["precio_por_persona"] * viajeros
                if base + coste_exp + coste <= presupuesto_max:
                    elegidas.append(e)
                    coste_exp += coste
            total = round(base + coste_exp, 2)
            candidatos.append({
                "vuelo": v, "alojamiento": h, "experiencias": elegidas,
                "desglose": {"vuelos": v["precio_total"],
                             "alojamiento": h["precio_total_estancia"],
                             "experiencias": round(coste_exp, 2)},
                "total": total,
                "sobrante": round(presupuesto_max - total, 2),
                "puntuacion": round(_puntuacion(v, h, elegidas), 2),
            })

    if not candidatos:
        minimo = None
        if vuelos and hoteles:
            minimo = round(min(v["precio_total"] for v in vuelos)
                           + min(h["precio_total_estancia"] for h in hoteles), 2)
        return {"paquetes": [], "presupuesto_max": presupuesto_max,
                "aviso": "Ninguna combinación cabe en el presupuesto.",
                "minimo_vuelo_mas_hotel": minimo}

    economico = min(candidatos, key=lambda c: c["total"])
    equilibrio = max(candidatos, key=lambda c: c["puntuacion"] / max(c["total"], 1) * 1000
                     + c["puntuacion"])
    comodo = max(candidatos, key=lambda c: (c["puntuacion"], -c["total"]))

    paquetes, vistos = [], set()
    for etiqueta, c in (("Más económico", economico), ("Mejor equilibrio", equilibrio),
                        ("Más cómodo", comodo)):
        clave = (c["vuelo"]["id"], c["alojamiento"]["id"],
                 tuple(e["id"] for e in c["experiencias"]))
        if clave in vistos:
            continue
        vistos.add(clave)
        paquetes.append({"etiqueta": etiqueta, **c})
    return {"paquetes": paquetes, "presupuesto_max": presupuesto_max, "viajeros": viajeros}
