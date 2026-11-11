"""Da de alta (o actualiza) el viaje de un cliente para el asistente de WhatsApp.

Ejemplo:
    python cargar_viaje.py --telefono 34600111222 --nombre "Laura Pérez" \
        --paquete "Viaje Completo" --destino "Roma" --ida 2027-03-12 --vuelta 2027-03-15 \
        --itinerario propuesta.md

El itinerario puede ser la propuesta que genera el agente (propuesta.md) o tu dossier final
con los códigos de reserva, horarios y direcciones.
"""
import argparse
from pathlib import Path

from whatsapp import db


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--telefono", required=True, help="Con prefijo y sin +: 34600111222")
    p.add_argument("--nombre", required=True)
    p.add_argument("--paquete", required=True)
    p.add_argument("--destino", required=True)
    p.add_argument("--ida", required=True, help="AAAA-MM-DD")
    p.add_argument("--vuelta", default="", help="AAAA-MM-DD")
    p.add_argument("--itinerario", required=True, help="Archivo de texto o Markdown")
    a = p.parse_args()

    telefono = "".join(c for c in a.telefono if c.isdigit())
    db.iniciar()
    db.guardar_viaje(telefono, a.nombre, a.paquete, a.destino, a.ida, a.vuelta,
                     Path(a.itinerario).read_text(encoding="utf-8"))
    print(f"Viaje de {a.nombre} guardado. El asistente ya puede atender a +{telefono}.")


if __name__ == "__main__":
    main()
