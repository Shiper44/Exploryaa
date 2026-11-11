"""Servidor del webhook de WhatsApp.

Ejecutar:  python -m whatsapp.servidor      (desde la carpeta exploryaa-agente)
Meta envía cada mensaje a POST /webhook y verifica la URL con GET /webhook.
"""
import threading

from flask import Flask, abort, request

import config
from whatsapp import comandos, db, meta
from whatsapp.asistente import Asistente

app = Flask(__name__)
db.iniciar()
_asistente = None


def asistente():
    global _asistente
    if _asistente is None:
        _asistente = Asistente()
    return _asistente


@app.get("/")
def salud():
    return "Exploryaa WhatsApp OK"


@app.get("/webhook")
def verificar():
    if (request.args.get("hub.mode") == "subscribe"
            and config.WA_VERIFY_TOKEN
            and request.args.get("hub.verify_token") == config.WA_VERIFY_TOKEN):
        return request.args.get("hub.challenge", ""), 200
    abort(403)


@app.post("/webhook")
def recibir():
    cuerpo = request.get_data()
    if not meta.firma_valida(cuerpo, request.headers.get("X-Hub-Signature-256", "")):
        abort(401)
    datos = request.get_json(silent=True) or {}
    for mensaje in meta.extraer_mensajes(datos):
        # Respondemos a Meta al instante y procesamos en segundo plano
        threading.Thread(target=procesar, args=mensaje, daemon=True).start()
    return "ok", 200


def procesar(wa_id, telefono, nombre, tipo, texto):
    try:
        if not wa_id or db.ya_procesado(wa_id):
            return

        # Mensajes de la asesora = comandos
        if config.ASESORA_WHATSAPP and telefono == config.ASESORA_WHATSAPP:
            meta.enviar_texto(telefono, comandos.ejecutar(texto))
            return

        if not texto:
            meta.enviar_texto(telefono, "Por ahora solo puedo leer mensajes de texto 🙏 "
                                        "¿Me lo escribes, por favor?")
            return

        db.guardar_mensaje(telefono, "cliente", texto)
        v = db.viaje(telefono)
        if v and not v["bot_activo"]:
            # La asesora lleva esta conversación: solo se lo reenviamos
            if config.ASESORA_WHATSAPP:
                meta.enviar_texto(config.ASESORA_WHATSAPP,
                                  f"💬 {v['nombre']} (+{telefono}):\n{texto}\n\nResponde con: #r {telefono} tu mensaje")
            return

        respuesta = asistente().responder(telefono)
        if respuesta:
            meta.enviar_texto(telefono, respuesta)
            db.guardar_mensaje(telefono, "asistente", respuesta)
    except Exception as error:
        print(f"Error procesando mensaje de {telefono}: {error}")
        if config.ASESORA_WHATSAPP and telefono != config.ASESORA_WHATSAPP:
            meta.enviar_texto(config.ASESORA_WHATSAPP,
                              f"⚠️ El asistente falló con +{telefono}: {error}\nMensaje: {texto}")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
