"""Ajustes del servidor. Se leen de variables de entorno o del archivo servidor/.env."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

RAIZ = Path(__file__).resolve().parents[2]          # carpeta del repositorio
load_dotenv(RAIZ / "servidor" / ".env")


def _lista(valor: str) -> list[str]:
    return [x.strip() for x in valor.split(",") if x.strip()]


@dataclass(frozen=True)
class Ajustes:
    entorno: str = field(default_factory=lambda: os.getenv("ENTORNO", "desarrollo"))
    url_publica: str = field(default_factory=lambda: os.getenv("URL_PUBLICA", "http://localhost:8000").rstrip("/"))
    origenes_permitidos: list[str] = field(default_factory=lambda: _lista(os.getenv("ORIGENES_PERMITIDOS", "")))
    carpeta_web: Path = field(default_factory=lambda: Path(os.getenv("CARPETA_WEB", RAIZ / "web")))
    archivo_precios: Path = field(default_factory=lambda: Path(os.getenv("ARCHIVO_PRECIOS", RAIZ / "config" / "precios.toml")))

    @property
    def produccion(self) -> bool:
        return self.entorno == "produccion"


ajustes = Ajustes()
