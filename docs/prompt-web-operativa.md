# Prompt: web operativa de Exploryaa

Pégalo en Claude Code, dentro de una carpeta vacía o junto a la carpeta `exploryaa-agente`.

```
Actúa como desarrollador full-stack senior y diseñador web. Construye la web
de Exploryaa COMPLETA Y OPERATIVA, lista para publicar en internet.
Trabaja por fases, enséñame el resultado de cada fase y espera mi OK antes
de pasar a la siguiente.

## 1. QUÉ ES EXPLORYAA
Agencia de viajes online 100 % impulsada por IA. El cliente rellena un
formulario, elige un paquete, paga y recibe en su correo una propuesta de
viaje personalizada (vuelos, alojamiento, experiencias e itinerario día a día)
generada por un agente de IA. Lema: "Tú sueñas el viaje, nosotros lo hacemos
realidad". Público: todo el mundo, sobre todo gente que viaja a menudo o que
no viaja porque le da pereza organizar. Idioma: solo español.

## 2. MARCA Y DISEÑO
- Logo: logo.png (avión blanco con estela curva sobre la palabra EXPLORYAA,
  fondo negro). Úsalo en la cabecera y en el pie.
- Colores: negro #0B0B0B, blanco #FFFFFF, grises #9A9A9A y #1A1A1A,
  acento dorado #D4AF37 (botones, precios, detalles).
- Tipografías: Space Grotesk (títulos) e Inter (texto), de Google Fonts.
- Estilo premium y elegante: secciones alternas en negro y blanco, mucho aire,
  esquinas redondeadas, sombras suaves, animaciones sutiles al hacer scroll y
  la estela del avión como línea decorativa curva entre secciones.
- Responsive impecable en móvil. Accesible: contraste AA, etiquetas en todos
  los campos, navegación con teclado, botones de al menos 44 px.

## 3. PÁGINAS
1. Inicio (landing):
   - Cabecera fija: logo, menú (Cómo funciona, Paquetes, Preguntas) y botón
     dorado "Diseña mi viaje".
   - Hero con foto de viaje a pantalla completa, titular, subtítulo y botones
     "Diseña mi viaje" y "Ver paquetes".
   - Cómo funciona en 3 pasos: cuéntanos tu idea, elige tu paquete y paga,
     recibe tu viaje en tu correo.
   - Paquetes (tarjetas, precio único por persona):
     · Mini Escapada 2D1N — [PRECIO] € — 2 días / 1 noche. Itinerario
       personalizado, recomendaciones locales, 1 revisión, enlaces y mapas.
     · Itinerario Express — [PRECIO] € — 2-5 días. Itinerario diario con
       horarios, transporte y experiencias, 1 revisión, soporte por chat/correo.
     · Viaje Completo — [PRECIO] € — 5-10 días. Planificación completa,
       dossier digital, hasta 2 revisiones, soporte. Etiqueta "Más popular".
     · Exploryaa Premium — [PRECIO] € — 10-21 días a medida. Revisiones
       ilimitadas, soporte por WhatsApp o llamada, asistencia durante el viaje.
       Tarjeta negra con borde dorado.
     Extras opcionales: seguro médico de viaje y actividades adicionales.
   - Formulario de viaje (ver punto 4).
   - Opiniones (de momento, huecos marcados como "[testimonio real]").
   - Preguntas frecuentes en acordeón.
   - Pie: logo, aviso legal, privacidad, cookies, condiciones de contratación,
     redes sociales y "N.º de registro: [PENDIENTE]".
2. /gracias: confirmación tras el pago.
3. Páginas legales con plantillas en español adaptadas a España (RGPD,
   LSSI-CE): aviso legal, política de privacidad, política de cookies y
   condiciones de contratación y cancelación. Deja entre corchetes los datos
   que tengo que rellenar (nombre, NIF, dirección, email).
4. Banner de cookies que solo cargue analítica si el usuario acepta.

## 4. FORMULARIO (en 3 pasos, con resumen del viaje en vivo al lado)
- Paso 1 "Tu viaje": paquete (tarjetas), ida y vuelta / solo ida, origen*,
  destino* (admite "sorpréndeme"), fecha de ida*, fecha de vuelta* (solo si es
  ida y vuelta), casilla "fechas flexibles (± 3 días)", adultos* y niños con
  botones + y −.
- Paso 2 "Preferencias": tipo de viaje* (varias opciones: Aventura, Urbano /
  Ciudad, Relax / Bienestar, Cultural, Ocio / Diversión, Naturaleza,
  Gastronómico, Parques temáticos, Otro), presupuesto máximo por persona*
  (Hasta 300 €, 300-600 €, 600-1.300 €, 1.300-3.000 €, Más de 3.000 €),
  alojamiento* (Hotel 3-5 estrellas, Apartamento, Hostal / B&B, Casa rural,
  Experiencia única, Me da igual), experiencias sostenibles (Sí / No / Me da
  igual), extras y comentarios.
- Paso 3 "Tus datos": nombre*, email*, teléfono (opcional), cómo nos
  conociste (opcional) y casilla obligatoria de aceptación de la política de
  privacidad, con la información básica del RGPD debajo.
- Validación en cada paso con mensajes claros. Aviso visible de que el
  formulario y el asistente usan inteligencia artificial.
- El botón final muestra el precio y lleva al pago.

## 5. BACKEND (operativo)
- Python + FastAPI. Reutiliza el agente que ya tengo en la carpeta
  exploryaa-agente (agente.py y la carpeta herramientas) sin reescribirlo.
- Base de datos: SQLite para empezar (fácil de cambiar a Postgres). Tabla
  "solicitudes" con todos los campos del formulario, estado (pendiente_pago,
  pagada, generando, enviada, error), fechas y la propuesta generada.
- Endpoints:
  · POST /api/solicitudes: valida y guarda la solicitud (pendiente_pago).
  · POST /api/checkout: crea la sesión de pago del paquete elegido.
  · POST /api/pagos/webhook: confirma el pago (con verificación de firma e
    idempotencia), marca la solicitud como pagada y lanza el agente en
    segundo plano.
  · GET /api/solicitudes/{id}/estado: para la página /gracias.
- Pagos: Stripe Checkout en MODO TEST, detrás de una interfaz
  "ProveedorPago" para poder cambiarlo luego por el TPV de mi banco (Redsys)
  sin tocar el resto. Stripe se usa solo para cobrar el servicio de
  planificación de Exploryaa. Nunca toques datos de tarjeta en mi servidor.
- Correo: Resend (o SMTP configurable). Dos plantillas HTML con la marca:
  1) "Hemos recibido tu solicitud" (al pagar).
  2) "Tu viaje está listo": la propuesta del agente bien maquetada (paquetes,
     desglose de precios, itinerario día a día, enlaces de reserva) y un aviso
     de que los precios son orientativos.
  Copia oculta de cada correo a mi email.
- Si el agente falla: reintento automático y aviso por email para mí.
- Panel de administración sencillo y protegido con contraseña en /admin:
  lista de solicitudes, estado, ver propuesta, reenviar correo y marcar
  incidencias.
- Seguridad: claves en .env (con .env.example sin valores), CORS limitado a
  mi dominio, límite de peticiones en el formulario, protección anti-spam
  (honeypot) y HTTPS.

## 6. SEO Y MEDICIÓN
- Títulos, meta descripciones, Open Graph con el logo, sitemap.xml,
  robots.txt y datos estructurados de TravelAgency.
- Analítica respetuosa con la privacidad (Plausible o GA4 solo con
  consentimiento) y eventos: inicio de formulario, paso completado, pago.
- Página rápida: imágenes optimizadas, carga diferida y Lighthouse de 90 o más.

## 7. PUBLICACIÓN
- Frontend en Vercel o Netlify y backend en Render o Railway (o todo en uno
  si es más sencillo). Explícame paso a paso cómo conectar mi dominio.
- Repositorio Git con un README en español para alguien no experto:
  instalación, variables de entorno, cómo probar en local (incluido
  "stripe listen" para el webhook), cómo publicar y cómo pasar de modo test a
  modo real.

## 8. PRUEBAS
- Tests del formulario, de los endpoints y del webhook con las tarjetas de
  prueba de Stripe.
- Una prueba de punta a punta: rellenar el formulario → pagar en modo test →
  recibir los dos correos con la propuesta.

## ORDEN DE TRABAJO
Fase 1: estructura del proyecto y landing estática con el diseño.
Fase 2: formulario funcional y guardado en la base de datos.
Fase 3: pagos en modo test y webhook.
Fase 4: conexión con el agente y envío de correos.
Fase 5: panel /admin, páginas legales, cookies y SEO.
Fase 6: publicación y README.
Antes de empezar, hazme las preguntas que necesites (dominio, email de
contacto, precios…) y no inventes datos legales ni testimonios.
```
