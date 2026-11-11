# Prompt para Claude Code: asistente de WhatsApp y agente de Exploryaa

Abre Claude Code dentro de la carpeta `exploryaa-agente` (descomprimida del zip) y pega esto:

```
Actúa como desarrollador backend senior. En esta carpeta está el proyecto de
Exploryaa, una agencia de viajes online con IA. Léelo entero antes de tocar
nada (README.md, README_WHATSAPP.md, agente.py, herramientas/, whatsapp/,
cargar_viaje.py) y REUTILÍZALO: no lo reescribas desde cero.

Qué hay ya:
- agente.py + herramientas/: agente de Claude que consulta precios de vuelos
  (Duffel), alojamientos (LiteAPI) y experiencias (Viator) y arma paquetes
  dentro de un presupuesto. Tiene modo de prueba sin claves.
- whatsapp/: asistente de WhatsApp (Flask + WhatsApp Cloud API de Meta) que
  atiende a los clientes con su itinerario, avisa a la asesora (yo) en casos
  de cambios, quejas o emergencias, y acepta mis comandos (#r, #bot, #inc,
  #cerrar). Base de datos SQLite.

Cómo funciona el negocio:
1. El cliente rellena el formulario de la web (paquete, origen, destino, fechas,
   viajeros, preferencias, presupuesto, nombre, email, teléfono, RGPD).
2. El agente genera una propuesta y se la envía por email en minutos.
3. Yo la reviso y hablo con el cliente. EL CLIENTE SOLO PAGA CUANDO ACEPTA.
4. Tras el pago, yo hago las reservas y el cliente recibe su dossier.
5. Durante el viaje le atiende el asistente de WhatsApp y yo intervengo
   cuando hace falta.

QUÉ QUIERO QUE HAGAS (por fases; enséñame cada una y espera mi OK):

Fase 1 – Puesta en marcha en local
- Crea el entorno virtual, instala requirements.txt y copia .env.example a .env.
- Pásame una lista de las claves que necesito y dónde conseguir cada una
  (Anthropic, Meta WhatsApp, Duffel, LiteAPI, Viator), paso a paso para alguien
  no experto.
- Ejecuta el agente en modo prueba (python main.py) y el servidor de WhatsApp
  en local, y comprueba que arrancan sin errores.
- Escribe tests con pytest para el webhook (verificación, firma, mensajes
  duplicados, aviso a la asesora, comandos y número desconocido) usando un
  cliente de Claude simulado.

Fase 2 – Un solo backend
- Une todo en una sola app (Flask o FastAPI, la que veas más simple de
  mantener) con:
  · POST /api/solicitudes: recibe el formulario de la web, lo guarda y lanza
    el agente en segundo plano.
  · Email al cliente con la propuesta (Resend o SMTP configurable) y copia a mí.
  · Estados de la solicitud: recibida, propuesta_enviada, aceptada, pagada,
    reservada, en_viaje, finalizada, incidencia.
  · Al pasar a "reservada", se da de alta el viaje en el asistente de WhatsApp
    automáticamente (sustituye a cargar_viaje.py) con el dossier final.
  · /webhook de WhatsApp tal y como está ahora.
- Pasa la base de datos a Postgres opcional (SQLite por defecto).

Fase 3 – Panel para mí en /admin (con contraseña)
- Lista de solicitudes con filtros por estado, ver y editar la propuesta,
  marcar "aceptada", "pagada" y "reservada", subir o pegar el dossier final,
  ver conversaciones de WhatsApp, incidencias abiertas y botón para pausar
  o reactivar el asistente con un cliente.

Fase 4 – Mensajes proactivos de WhatsApp
- Plantillas de Meta (te dejo redactar el texto en español) para: propuesta
  lista, recordatorio de pago, viaje confirmado, "tu viaje empieza mañana"
  y "¿qué tal el viaje?" a la vuelta. Envío automático según el estado y las
  fechas, y explícame cómo pedir su aprobación en Meta.

Fase 5 – Publicación
- Despliega en Render o Railway con HTTPS, disco persistente o Postgres,
  variables de entorno y el comando gunicorn. Explícame cómo poner la URL del
  webhook en Meta y cómo conectar el formulario de la web a /api/solicitudes.
- Logs y aviso a mi WhatsApp si algo falla.

Reglas:
- No inventes claves, precios ni datos legales: pregúntame.
- Claves siempre en .env; nunca en el código ni en Git (.gitignore).
- No pidas ni guardes datos de tarjeta; el pago va por la pasarela.
- El asistente siempre se identifica como IA en el primer mensaje.
- Todo en español, con un README actualizado para alguien no experto.
Antes de empezar, hazme las preguntas que necesites.
```
