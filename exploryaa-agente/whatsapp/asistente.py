"""Cerebro del asistente de WhatsApp: Claude con el viaje del cliente y herramientas."""
import json
from datetime import date

import config
from herramientas.experiencias import buscar_experiencias
from whatsapp import db, meta

PAQUETES = """Paquetes de Exploryaa (precio único por persona):
- Mini Escapada 2D1N (2 días / 1 noche, vuelos y alojamiento) – 199 €
- Itinerario Express (2-5 días, vuelos, alojamiento y actividades) – 449 €
- Viaje Completo (5-10 días, vuelos, alojamiento, actividades y seguro) – 1.290 €
- Exploryaa Premium (10-21 días a medida, asesora personal y asistencia 24 h) – 2.990 €
El cliente rellena el formulario de la web, recibe una propuesta en minutos, la revisa con
una persona del equipo y solo paga cuando la acepta. Después el equipo hace todas las reservas."""

REGLAS = """Eres el asistente de viaje de Exploryaa por WhatsApp. Eres una inteligencia artificial
y trabajas junto a {asesora}, la persona del equipo que gestiona las reservas.

Estilo WhatsApp: mensajes cortos y cercanos, en el idioma del cliente (por defecto español),
sin títulos ni tablas. Puedes usar *negrita* y listas cortas con guiones. Como mucho 1 emoji.

Reglas:
1. Si es el primer mensaje de la conversación, preséntate y di claramente que eres un asistente
   de inteligencia artificial de Exploryaa.
2. Usa SOLO los datos del viaje que tienes abajo. Nunca inventes horarios, códigos de reserva,
   direcciones ni precios. Si no lo sabes, dilo y, si ayuda, búscalo.
3. Llama a avisar_asesora (y di al cliente que {asesora} le escribirá en breve) cuando pida:
   cambiar o cancelar una reserva, reembolsos o pagos, quejas, un problema con un vuelo, hotel
   o actividad, o cualquier cosa que requiera comprar o gestionar algo, o cuando pida hablar
   con una persona.
4. EMERGENCIA (salud, accidente, robo, peligro): lo primero, dile que llame al 112 (en la UE)
   o al número de emergencias local; después llama a avisar_asesora con urgencia "urgente".
5. Para recomendaciones en destino (qué hacer, dónde comer, cómo moverse) puedes buscar en
   internet o usar buscar_experiencias. Prioriza lo que encaje con su itinerario y su zona.
6. No pidas ni aceptes datos de tarjetas, contraseñas ni documentos de identidad por aquí.
7. Si los mensajes muestran "[Mensaje de la asesora]", ella ya habló con el cliente: sé coherente."""


def sistema(v: dict | None) -> str:
    hoy = date.today()
    base = REGLAS.format(asesora=config.ASESORA_NOMBRE) + f"\n\nHoy es {hoy.isoformat()}.\n\n"
    if not v:
        return base + ("Este número NO tiene un viaje registrado con Exploryaa. Responde dudas generales "
                       "sobre Exploryaa, invita a pedir su viaje en la web y, si dice que ya es cliente, "
                       "pídele su nombre y el email de la reserva y avisa a la asesora. No des datos de "
                       "ningún viaje.\n\n" + PAQUETES)
    dia = ""
    try:
        ida = date.fromisoformat(v["fecha_ida"])
        vuelta = date.fromisoformat(v["fecha_vuelta"]) if v.get("fecha_vuelta") else ida
        if ida <= hoy <= vuelta:
            dia = f" Hoy es el día {(hoy - ida).days + 1} del viaje."
        elif hoy < ida:
            dia = f" Faltan {(ida - hoy).days} días para la salida."
        else:
            dia = " El viaje ya terminó."
    except (TypeError, ValueError):
        pass
    return base + (f"CLIENTE: {v['nombre']} · Paquete: {v['paquete']} · Destino: {v['destino']} · "
                   f"Fechas: {v['fecha_ida']} a {v['fecha_vuelta'] or '—'}.{dia}\n\n"
                   f"ITINERARIO Y RESERVAS DEL CLIENTE:\n{v['itinerario']}\n\n{PAQUETES}")


HERRAMIENTAS = [
    {
        "name": "avisar_asesora",
        "description": "Avisa a la asesora humana de Exploryaa por WhatsApp. Úsala para cambios, "
                       "cancelaciones, pagos, quejas, problemas con reservas, emergencias o si el "
                       "cliente pide hablar con una persona.",
        "input_schema": {"type": "object", "properties": {
            "motivo": {"type": "string", "description": "Resumen claro de lo que necesita el cliente"},
            "urgencia": {"type": "string", "enum": ["normal", "urgente"]},
            "pausar_asistente": {"type": "boolean", "description":
                                 "true si a partir de ahora debe contestar solo la asesora"}},
            "required": ["motivo", "urgencia"]},
    },
    {
        "name": "buscar_experiencias",
        "description": "Busca tours, actividades y entradas en un destino con precio y enlace (Viator).",
        "input_schema": {"type": "object", "properties": {
            "destino": {"type": "string"},
            "intereses": {"type": "string"},
            "precio_max_persona": {"type": "number"}},
            "required": ["destino"]},
    },
]
BUSQUEDA_WEB = {"type": "web_search_20250305", "name": "web_search", "max_uses": 3}


class Asistente:
    def __init__(self, cliente=None, max_pasos: int = 6):
        if cliente is None:
            import anthropic
            cliente = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
        self.cliente = cliente
        self.max_pasos = max_pasos
        self.web = config.WA_BUSQUEDA_WEB

    def _herramienta(self, telefono, v, nombre, datos):
        if nombre == "buscar_experiencias":
            return buscar_experiencias(**datos)
        if nombre == "avisar_asesora":
            numero = db.abrir_incidencia(telefono, datos["motivo"], datos.get("urgencia", "normal"))
            if datos.get("pausar_asistente"):
                db.activar_bot(telefono, False)
            if config.ASESORA_WHATSAPP:
                quien = f"{v['nombre']} ({v['destino']})" if v else "Número sin viaje registrado"
                alerta = "🚨 URGENTE" if datos.get("urgencia") == "urgente" else "Aviso"
                meta.enviar_texto(config.ASESORA_WHATSAPP,
                                  f"{alerta} #{numero} · {quien}\n+{telefono}\n\n{datos['motivo']}\n\n"
                                  f"Responde con: #r {telefono} tu mensaje")
            return {"ok": True, "incidencia": numero,
                    "asistente_pausado": bool(datos.get("pausar_asistente"))}
        raise ValueError(f"Herramienta desconocida: {nombre}")

    def _llamar(self, sist, mensajes):
        herramientas = HERRAMIENTAS + ([BUSQUEDA_WEB] if self.web else [])
        try:
            return self.cliente.messages.create(model=config.CLAUDE_MODEL, max_tokens=1500,
                                                system=sist, tools=herramientas, messages=mensajes)
        except Exception as error:
            if self.web and "web_search" in str(error):
                self.web = False  # la búsqueda web no está disponible: seguimos sin ella
                return self._llamar(sist, mensajes)
            raise

    def responder(self, telefono: str) -> str:
        v = db.viaje(telefono)
        sist = sistema(v)
        mensajes = db.historial(telefono)
        for _ in range(self.max_pasos):
            r = self._llamar(sist, mensajes)
            mensajes.append({"role": "assistant", "content": r.content})
            if r.stop_reason != "tool_use":
                return "".join(b.text for b in r.content if b.type == "text").strip()
            resultados = []
            for b in r.content:
                if b.type != "tool_use":
                    continue
                try:
                    salida = self._herramienta(telefono, v, b.name, dict(b.input))
                    resultados.append({"type": "tool_result", "tool_use_id": b.id,
                                       "content": json.dumps(salida, ensure_ascii=False)})
                except Exception as error:
                    resultados.append({"type": "tool_result", "tool_use_id": b.id,
                                       "content": f"Error: {error}", "is_error": True})
            mensajes.append({"role": "user", "content": resultados})
        return (f"Déjame consultarlo con {config.ASESORA_NOMBRE} y te escribimos en breve.")
