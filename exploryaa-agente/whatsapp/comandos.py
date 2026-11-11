"""Comandos que la asesora envía desde su propio WhatsApp al número de Exploryaa."""
from whatsapp import db, meta

AYUDA = """Comandos de Exploryaa:
#r 34600111222 texto → responder al cliente como asesora (pausa el asistente con ese cliente)
#bot 34600111222 on → el asistente vuelve a contestar a ese cliente
#bot 34600111222 off → solo contestas tú
#inc → ver incidencias abiertas
#cerrar 12 → cerrar la incidencia 12
#ayuda → ver esta lista"""


def ejecutar(texto: str) -> str:
    partes = texto.strip().split(maxsplit=2)
    orden = partes[0].lower() if partes else ""

    if orden == "#r" and len(partes) == 3:
        telefono, mensaje = partes[1].lstrip("+"), partes[2]
        meta.enviar_texto(telefono, mensaje)
        db.guardar_mensaje(telefono, "asesora", mensaje)
        db.activar_bot(telefono, False)
        return f"Enviado a +{telefono}. El asistente queda en pausa con este cliente (#bot {telefono} on para reactivarlo)."

    if orden == "#bot" and len(partes) == 3 and partes[2].lower() in ("on", "off"):
        telefono = partes[1].lstrip("+")
        if not db.viaje(telefono):
            return f"No hay ningún viaje registrado con +{telefono}."
        db.activar_bot(telefono, partes[2].lower() == "on")
        return f"Asistente {'activado' if partes[2].lower() == 'on' else 'pausado'} para +{telefono}."

    if orden == "#inc":
        abiertas = db.incidencias_abiertas()
        if not abiertas:
            return "No hay incidencias abiertas."
        return "Incidencias abiertas:\n" + "\n".join(
            f"#{i['id']} · +{i['telefono']} · {i['urgencia']} · {i['motivo'][:80]}" for i in abiertas)

    if orden == "#cerrar" and len(partes) >= 2 and partes[1].lstrip("#").isdigit():
        n = int(partes[1].lstrip("#"))
        return f"Incidencia #{n} cerrada." if db.cerrar_incidencia(n) else f"No existe la incidencia #{n}."

    return AYUDA
