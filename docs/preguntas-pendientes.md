# Preguntas pendientes antes de construir la web operativa

Preguntas sobre el encargo de `prompt-web-operativa.md`. Junto a cada una está lo que se hará si no hay respuesta.

## Bloqueante para la fase 4
- **Carpeta `exploryaa-agente`** (`agente.py` y `herramientas/`): no está en el repositorio. Hay que subirla e indicar qué función se llama, qué recibe y qué devuelve, y qué claves de API usa.

## Modelo de negocio
1. **¿Qué cobra Exploryaa?** ¿Solo la planificación (el cliente reserva con los enlaces de la propuesta) o también vuelos y hotel? Afecta a los textos, a las condiciones de contratación y al registro de agencia. *Por defecto: solo la planificación.*
2. **Precios:** ¿199 / 449 / 1.290 / 2.990 € por persona? *Por defecto: sí.*
3. **Cálculo del total:** ¿precio × adultos? ¿Cuánto pagan los niños? *Por defecto: adultos precio completo, niños la mitad.*
4. **Extras** (seguro médico, actividades): ¿precio fijo cobrado en el pago o solo se anotan? *Por defecto: solo se anotan.*

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
