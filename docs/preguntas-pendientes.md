# Preguntas pendientes antes de construir la web operativa

Preguntas sobre el encargo de `prompt-web-operativa.md`. Junto a cada una está lo que se hará si no hay respuesta.

## Bloqueante para la fase 4
- **Carpeta `exploryaa-agente`** (`agente.py` y `herramientas/`): no está en el repositorio. Hay que subirla e indicar qué función se llama, qué recibe y qué devuelve, y qué claves de API usa.

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
