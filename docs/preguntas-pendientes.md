# Preguntas pendientes antes de construir la web operativa

Preguntas sobre el encargo de `prompt-web-operativa.md`. Junto a cada una está lo que se hará si no hay respuesta.

## Agente (resuelto)
- La carpeta `exploryaa-agente/` ya está en el repositorio. Se llama con `Agente().planificar(solicitud)`, que recibe un diccionario como `ejemplo_solicitud.json` y devuelve la propuesta en Markdown. Usa las claves de Anthropic (obligatoria), Duffel, LiteAPI y Viator; sin ellas funciona con datos de prueba.

## Modelo de negocio (respondido)
- **Dos tipos de producto:**
  1. **Pack de Planificación:** solo planificación y asesoramiento. El cliente recibe la propuesta y reserva por su cuenta; Exploryaa no compra vuelos ni alojamiento.
  2. **Packs Exploryaa** (Mini Escapada 2D1N, Itinerario Express, Viaje Completo, Exploryaa Premium): incluyen vuelos, alojamiento y actividades, cada uno con sus ventajas.
- **Precios:** se decidirán más adelante. Mientras tanto, la web muestra `[PRECIO] €` y los precios se configuran en un solo sitio.

### Pendiente
- Qué incluye exactamente el Pack de Planificación (duración del viaje, revisiones, soporte, formato de entrega) y si se cobra por persona o por viaje.
- Cómo se cobran los Packs Exploryaa, dado que el coste de vuelos y hotel varía según destino y fechas: ¿precio cerrado, o tarifa más un presupuesto aparte?
- Quién hace las reservas de los Packs Exploryaa: a mano o el agente mediante APIs de proveedores.
- Extras (seguro médico, actividades): ¿precio fijo o solo se anotan?
- **Aviso legal:** vender vuelos + alojamiento juntos es un «viaje combinado» (Real Decreto Legislativo 1/2007, libro IV). Exige estar inscrito como agencia de viajes en tu comunidad autónoma, tener garantía de insolvencia y entregar la información precontractual obligatoria. Conviene confirmarlo con un asesor antes de vender.

## Datos que no se pueden inventar
5. Dominio. *Marcador: `exploryaa.com`.*
6. Correos: contacto público, remitente y email del propietario (copia oculta y avisos de error).
7. `logo.png`. *Mientras tanto: logo provisional en texto.*
8. Redes sociales y número de WhatsApp. *Marcador: `[PENDIENTE]`.*
9. Opciones de «¿Cómo nos conociste?». *Por defecto: Instagram, TikTok, Google, Recomendación, Otro.*

## Decisiones técnicas
10. Publicación. *Recomendado: un único servicio en Render (FastAPI sirve la web y la API).*
11. Correo. *Recomendado: Resend, con SMTP como alternativa.*
12. Analítica. *Recomendado: Plausible (sin cookies); GA4 solo con consentimiento.*
13. Stripe: ¿hay cuenta? Las claves van en `.env`, nunca en el chat ni en el repositorio.

## Nota de diseño
La fase 1 reutiliza `index.html` como base, cambiando los títulos a Space Grotesk, el formulario a 3 pasos con resumen en vivo y los testimonios a huecos `[testimonio real]`.

## Encargo del asistente de WhatsApp (`prompt-whatsapp-agente.md`)

### Revisión del código del agente
- **Firma de Meta:** `whatsapp/meta.py` acepta cualquier mensaje cuando `WA_APP_SECRET` está vacío. En producción debe rechazarlos.
- **Precios fijos en el asistente:** `whatsapp/asistente.py` (`PAQUETES`) tiene escritos 199 / 449 / 1.290 / 2.990 € y no menciona el Pack de Planificación. Debe leer los precios del mismo sitio que la web.
- **Mensajes en segundo plano:** `whatsapp/servidor.py` procesa cada mensaje en un hilo. Si el servidor se reinicia, los mensajes en curso se pierden; conviene una cola o un reintento al migrar.
- **Datos de la solicitud:** el agente espera `presupuesto_max` como un número en euros para todos los viajeros. El formulario de la web lo pide por rangos y por persona, así que hay que convertirlo.

### Diferencias entre los dos encargos (hay que elegir una versión)
| Tema | `prompt-web-operativa.md` | `prompt-whatsapp-agente.md` |
|---|---|---|
| Momento del pago | Antes de generar la propuesta (Stripe Checkout al enviar el formulario) | Solo cuando el cliente acepta la propuesta |
| Estados | pendiente_pago, pagada, generando, enviada, error | recibida, propuesta_enviada, aceptada, pagada, reservada, en_viaje, finalizada, incidencia |
| Framework | FastAPI | Flask o FastAPI, el más simple (el asistente actual usa Flask) |
| Panel /admin | Solicitudes, propuesta, reenviar correo, incidencias | Además: editar propuesta, dossier, conversaciones de WhatsApp, pausar el asistente |

**Propuesta:** tomar el flujo del encargo de WhatsApp como el definitivo, porque es el más reciente y encaja con la revisión humana:
1. La solicitud se envía gratis.
2. El agente genera la propuesta.
3. La asesora la revisa y habla con el cliente.
4. El cliente paga al aceptar, mediante un enlace de Stripe.
5. La asesora reserva y, al marcar la solicitud como «reservada», el viaje se da de alta en WhatsApp.

Así las fases de la web y las del backend quedan en un solo proyecto.

### Pendiente de confirmar
- ¿El **Pack de Planificación** también se paga al aceptar, o por adelantado?
- Teléfono de la asesora para los avisos de WhatsApp (va en `.env`, no en el repositorio).
- ¿Hay ya una cuenta de Meta Business con número verificado para la WhatsApp Cloud API?

## Formulario conectado a Google Apps Script
- `web/index.html` envía el formulario (3 pasos) a la aplicación web de Apps Script de `integraciones/google-apps-script/` mediante la función `enviarSolicitud` de `web/index.html`. Esta guarda la solicitud en Google Sheets y Notion, envía la confirmación al cliente y avisa a la asesora.
- La web sigue ya el flujo «propuesta en menos de 48 horas, solo pagas si la aceptas»: el formulario no cobra nada.
- Falta: el Pack de Planificación no está en el formulario ni en las opciones de Notion (`Paquete`); se añadirá cuando se sepa qué incluye.
