"""Agente Exploryaa: Claude decide qué buscar, usa las herramientas y redacta la propuesta."""
import json
from datetime import date

import config
from herramientas.alojamientos import buscar_alojamientos
from herramientas.experiencias import buscar_experiencias
from herramientas.presupuesto import armar_paquetes
from herramientas.vuelos import buscar_codigo_aeropuerto, buscar_vuelos

INSTRUCCIONES = """Eres el agente de viajes de Exploryaa, una agencia de viajes online con IA.
Tu trabajo es CONSULTAR PRECIOS y proponer el mejor viaje posible dentro del presupuesto máximo
del cliente. No reservas nada: la reserva la hace una persona del equipo después.

Cómo trabajar:
1. Si el origen o el destino no son códigos IATA, usa buscar_codigo_aeropuerto.
2. Busca vuelos (solo ida o ida y vuelta, según pida el cliente), alojamientos y experiencias.
   Puedes lanzar las tres búsquedas a la vez.
3. Llama a armar_paquetes con el presupuesto máximo. Usa los resultados guardados de tus búsquedas.
4. Si no cabe nada, prueba de nuevo: menos estrellas, más escalas, otro aeropuerto cercano o
   menos experiencias. Si aun así no cabe, dilo claramente e indica el mínimo necesario.
5. Nunca inventes precios: usa solo los que devuelven las herramientas.

Respuesta final (en español, cercana y clara):
- Resumen del viaje solicitado.
- Hasta 3 paquetes (Más económico / Mejor equilibrio / Más cómodo) con vuelo, alojamiento,
  experiencias, desglose de precios, total y cuánto sobra del presupuesto.
- Tu recomendación y por qué.
- Un itinerario día a día del paquete recomendado.
- Aviso: los precios son orientativos y pueden cambiar hasta que se reserve.
Si alguna herramienta devolvió DATOS DE PRUEBA, avísalo al principio."""

HERRAMIENTAS = [
    {
        "name": "buscar_codigo_aeropuerto",
        "description": "Convierte el nombre de una ciudad o aeropuerto en códigos IATA.",
        "input_schema": {"type": "object", "properties": {
            "texto": {"type": "string", "description": "Ciudad o aeropuerto, p. ej. 'Barcelona'"}},
            "required": ["texto"]},
    },
    {
        "name": "buscar_vuelos",
        "description": "Busca vuelos solo ida (sin fecha_vuelta) o ida y vuelta. Devuelve las "
                       "ofertas más baratas con precio total para todos los pasajeros.",
        "input_schema": {"type": "object", "properties": {
            "origen": {"type": "string", "description": "Código IATA de origen"},
            "destino": {"type": "string", "description": "Código IATA de destino"},
            "fecha_ida": {"type": "string", "description": "AAAA-MM-DD"},
            "fecha_vuelta": {"type": "string", "description": "AAAA-MM-DD; omitir si es solo ida"},
            "adultos": {"type": "integer", "minimum": 1},
            "ninos": {"type": "integer", "minimum": 0},
            "clase": {"type": "string", "enum": ["economy", "premium_economy", "business", "first"]},
            "max_escalas": {"type": "integer", "minimum": 0, "maximum": 2}},
            "required": ["origen", "destino", "fecha_ida"]},
    },
    {
        "name": "buscar_alojamientos",
        "description": "Busca hoteles en una ciudad con el precio total de la estancia.",
        "input_schema": {"type": "object", "properties": {
            "ciudad": {"type": "string"},
            "codigo_pais": {"type": "string", "description": "ISO de 2 letras, p. ej. IT"},
            "entrada": {"type": "string", "description": "AAAA-MM-DD"},
            "salida": {"type": "string", "description": "AAAA-MM-DD"},
            "adultos": {"type": "integer", "minimum": 1},
            "ninos": {"type": "integer", "minimum": 0},
            "precio_max_total": {"type": "number"},
            "estrellas_min": {"type": "integer", "minimum": 0, "maximum": 5}},
            "required": ["ciudad", "codigo_pais", "entrada", "salida"]},
    },
    {
        "name": "buscar_experiencias",
        "description": "Busca tours, actividades y entradas en un destino. Precio por persona.",
        "input_schema": {"type": "object", "properties": {
            "destino": {"type": "string"},
            "intereses": {"type": "string", "description": "p. ej. 'gastronomía', 'museos'"},
            "precio_max_persona": {"type": "number"}},
            "required": ["destino"]},
    },
    {
        "name": "armar_paquetes",
        "description": "Combina los últimos vuelos, alojamientos y experiencias encontrados y "
                       "devuelve hasta 3 paquetes que no superan el presupuesto máximo.",
        "input_schema": {"type": "object", "properties": {
            "viajeros": {"type": "integer", "minimum": 1},
            "presupuesto_max": {"type": "number", "description": "Total para todos los viajeros"},
            "num_experiencias": {"type": "integer", "minimum": 0, "maximum": 6},
            "reparto": {"type": "object", "description":
                        "Opcional. Fracción máxima por parte, p. ej. "
                        "{\"vuelos\":0.5,\"alojamiento\":0.35,\"experiencias\":0.15}"}},
            "required": ["viajeros", "presupuesto_max"]},
    },
]


class Agente:
    def __init__(self, cliente=None, max_pasos: int = 15, verbose: bool = True):
        if cliente is None:
            import anthropic  # se importa aquí para poder probar sin la librería instalada
            cliente = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
        self.cliente = cliente
        self.max_pasos = max_pasos
        self.verbose = verbose
        self.memoria = {"vuelos": [], "hoteles": [], "experiencias": []}

    # --- ejecución de herramientas -------------------------------------------------------
    def ejecutar(self, nombre: str, datos: dict):
        if nombre == "buscar_codigo_aeropuerto":
            return buscar_codigo_aeropuerto(**datos)
        if nombre == "buscar_vuelos":
            r = buscar_vuelos(**datos)
            self.memoria["vuelos"] = r["ofertas"]
            return r
        if nombre == "buscar_alojamientos":
            r = buscar_alojamientos(**datos)
            self.memoria["hoteles"] = r["hoteles"]
            return r
        if nombre == "buscar_experiencias":
            r = buscar_experiencias(**datos)
            self.memoria["experiencias"] = r["experiencias"]
            return r
        if nombre == "armar_paquetes":
            return armar_paquetes(self.memoria["vuelos"], self.memoria["hoteles"],
                                  self.memoria["experiencias"], **datos)
        raise ValueError(f"Herramienta desconocida: {nombre}")

    # --- bucle principal -------------------------------------------------------------------
    def planificar(self, solicitud: dict) -> str:
        mensaje = (f"Hoy es {date.today().isoformat()}. Solicitud del cliente:\n"
                   + json.dumps(solicitud, ensure_ascii=False, indent=2))
        mensajes = [{"role": "user", "content": mensaje}]

        for _ in range(self.max_pasos):
            respuesta = self.cliente.messages.create(
                model=config.CLAUDE_MODEL, max_tokens=8000, system=INSTRUCCIONES,
                tools=HERRAMIENTAS, messages=mensajes)
            mensajes.append({"role": "assistant", "content": respuesta.content})

            if respuesta.stop_reason != "tool_use":
                return "".join(b.text for b in respuesta.content if b.type == "text")

            resultados = []
            for bloque in respuesta.content:
                if bloque.type != "tool_use":
                    continue
                if self.verbose:
                    print(f"  -> {bloque.name}({json.dumps(bloque.input, ensure_ascii=False)})")
                try:
                    salida = self.ejecutar(bloque.name, dict(bloque.input))
                    resultados.append({"type": "tool_result", "tool_use_id": bloque.id,
                                       "content": json.dumps(salida, ensure_ascii=False)})
                except Exception as error:  # el agente ve el error y puede corregirse
                    resultados.append({"type": "tool_result", "tool_use_id": bloque.id,
                                       "content": f"Error: {error}", "is_error": True})
            mensajes.append({"role": "user", "content": resultados})

        return "El agente alcanzó el máximo de pasos sin terminar. Revisa la solicitud."
