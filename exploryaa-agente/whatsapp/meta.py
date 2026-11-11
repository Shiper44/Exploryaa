"""Conexión con la WhatsApp Cloud API de Meta: enviar mensajes y validar avisos."""
import hashlib
import hmac

import requests

import config

LIMITE = 4000  # WhatsApp admite hasta 4096 caracteres por mensaje de texto


def firma_valida(cuerpo: bytes, cabecera: str) -> bool:
    """Comprueba la cabecera X-Hub-Signature-256 con el App Secret."""
    if not config.WA_APP_SECRET:
        return True  # sin secreto configurado (solo para pruebas locales)
    esperado = "sha256=" + hmac.new(config.WA_APP_SECRET.encode(), cuerpo, hashlib.sha256).hexdigest()
    return hmac.compare_digest(esperado, cabecera or "")


def _trozos(texto: str):
    while len(texto) > LIMITE:
        corte = texto.rfind("\n", 0, LIMITE)
        corte = corte if corte > 0 else LIMITE
        yield texto[:corte]
        texto = texto[corte:].lstrip()
    if texto:
        yield texto


def enviar_texto(telefono: str, texto: str):
    """Envía un mensaje de texto (dentro de la ventana de 24 h desde el último mensaje del cliente)."""
    if not (config.WA_TOKEN and config.WA_PHONE_NUMBER_ID):
        print(f"[SIMULADO → {telefono}] {texto}")
        return
    url = f"https://graph.facebook.com/{config.WA_GRAPH_VERSION}/{config.WA_PHONE_NUMBER_ID}/messages"
    cabeceras = {"Authorization": f"Bearer {config.WA_TOKEN}", "Content-Type": "application/json"}
    for trozo in _trozos(texto):
        r = requests.post(url, headers=cabeceras, timeout=config.TIMEOUT, json={
            "messaging_product": "whatsapp", "to": telefono, "type": "text",
            "text": {"body": trozo, "preview_url": True}})
        if r.status_code >= 400:
            print(f"Error enviando a {telefono}: {r.status_code} {r.text}")


def extraer_mensajes(datos: dict):
    """Saca de un aviso de Meta los mensajes entrantes: (id, telefono, nombre, tipo, texto)."""
    for entrada in datos.get("entry", []):
        for cambio in entrada.get("changes", []):
            valor = cambio.get("value", {})
            nombres = {c.get("wa_id"): c.get("profile", {}).get("name", "")
                       for c in valor.get("contacts", [])}
            for m in valor.get("messages", []):
                tipo = m.get("type")
                texto = ""
                if tipo == "text":
                    texto = m.get("text", {}).get("body", "")
                elif tipo == "button":
                    texto = m.get("button", {}).get("text", "")
                elif tipo == "interactive":
                    i = m.get("interactive", {})
                    texto = (i.get("button_reply") or i.get("list_reply") or {}).get("title", "")
                elif tipo == "location":
                    loc = m.get("location", {})
                    texto = f"[Ubicación compartida] lat {loc.get('latitude')}, lon {loc.get('longitude')} {loc.get('name', '')}".strip()
                yield m.get("id"), m.get("from"), nombres.get(m.get("from"), ""), tipo, texto
