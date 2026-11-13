"""Lee y valida config/precios.toml, el único sitio donde se fijan los precios."""
from __future__ import annotations

import tomllib
from functools import lru_cache
from pathlib import Path

from .ajustes import ajustes

NIVELES = ("simple", "estandar", "premium")
PAQUETES = ("mini", "express", "completo", "premium")


class ErrorPrecios(ValueError):
    """El archivo de precios tiene un error; el mensaje dice cuál."""


def _numero(valor, donde: str, *, permitir_negativo_uno: bool = False) -> float:
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise ErrorPrecios(f"{donde} debe ser un número (sin el símbolo €)")
    if valor < 0 and not (permitir_negativo_uno and valor == -1):
        raise ErrorPrecios(f"{donde} no puede ser negativo")
    return valor


def validar(datos: dict) -> dict:
    """Comprueba que el archivo tiene todo lo necesario y devuelve una versión limpia."""
    try:
        plan = datos["planificacion"]
        niveles = plan["niveles"]
        paquetes = datos["paquetes"]
    except KeyError as e:
        raise ErrorPrecios(f"Falta la sección {e} en precios.toml") from None

    limpio = {
        "planificacion": {
            "dias_incluidos": int(_numero(plan.get("dias_incluidos"), "planificacion.dias_incluidos")),
            "por_destino_extra": _numero(plan.get("por_destino_extra"), "planificacion.por_destino_extra"),
            "niveles": {},
        },
        "paquetes": {},
    }
    for clave in NIVELES:
        if clave not in niveles:
            raise ErrorPrecios(f"Falta el nivel de planificación «{clave}»")
        n = niveles[clave]
        d = f"planificacion.niveles.{clave}"
        limpio["planificacion"]["niveles"][clave] = {
            "nombre": str(n.get("nombre") or clave.capitalize()),
            "desde": _numero(n.get("desde"), f"{d}.desde"),
            "por_dia_extra": _numero(n.get("por_dia_extra"), f"{d}.por_dia_extra"),
            "revisiones": int(_numero(n.get("revisiones"), f"{d}.revisiones")),
            "entrega": str(n.get("entrega", "")),
        }
    for clave in PAQUETES:
        if clave not in paquetes:
            raise ErrorPrecios(f"Falta el paquete «{clave}»")
        p = paquetes[clave]
        d = f"paquetes.{clave}"
        limpio["paquetes"][clave] = {
            "nombre": str(p.get("nombre") or clave.capitalize()),
            "desde": _numero(p.get("desde"), f"{d}.desde"),
            "honorarios": _numero(p.get("honorarios"), f"{d}.honorarios"),
            "revisiones": int(_numero(p.get("revisiones"), f"{d}.revisiones", permitir_negativo_uno=True)),
        }
    return limpio


def cargar(ruta: Path | None = None) -> dict:
    ruta = ruta or ajustes.archivo_precios
    try:
        with open(ruta, "rb") as f:
            datos = tomllib.load(f)
    except FileNotFoundError:
        raise ErrorPrecios(f"No encuentro el archivo de precios: {ruta}") from None
    except tomllib.TOMLDecodeError as e:
        raise ErrorPrecios(f"precios.toml tiene un error de formato: {e}") from None
    return validar(datos)


@lru_cache(maxsize=1)
def precios() -> dict:
    """Precios validados (se leen una vez al arrancar el servidor)."""
    return cargar()


def publicos() -> dict:
    """Lo que puede ver la web: los «desde», sin los honorarios internos."""
    p = precios()
    return {
        "planificacion": p["planificacion"],
        "paquetes": {
            k: {"nombre": v["nombre"], "desde": v["desde"], "revisiones": v["revisiones"]}
            for k, v in p["paquetes"].items()
        },
    }
