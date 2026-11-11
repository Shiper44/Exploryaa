"""Ejecuta el agente con una solicitud de ejemplo o con un archivo JSON.

Uso:
    python main.py                      # usa ejemplo_solicitud.json
    python main.py mi_solicitud.json    # usa tu propio archivo
"""
import json
import sys
from pathlib import Path

import config
from agente import Agente


def main():
    ruta = Path(sys.argv[1] if len(sys.argv) > 1 else "ejemplo_solicitud.json")
    solicitud = json.loads(ruta.read_text(encoding="utf-8"))

    if not config.ANTHROPIC_API_KEY:
        sys.exit("Falta ANTHROPIC_API_KEY en el archivo .env (consíguela en console.anthropic.com).")

    for nombre, clave in (("Vuelos (Duffel)", config.DUFFEL_TOKEN),
                          ("Alojamientos (LiteAPI)", config.LITEAPI_KEY),
                          ("Experiencias (Viator)", config.VIATOR_API_KEY)):
        modo = "PRUEBA" if config.usar_prueba(clave) else "REAL"
        print(f"{nombre}: modo {modo}")

    print("\nBuscando el mejor viaje...\n")
    propuesta = Agente().planificar(solicitud)
    print("\n" + propuesta)

    Path("propuesta.md").write_text(propuesta, encoding="utf-8")
    print("\nPropuesta guardada en propuesta.md")


if __name__ == "__main__":
    main()
