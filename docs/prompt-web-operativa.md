# Prompt: web operativa de Exploryaa (versión 2)

Encargo vigente. Sustituye a la versión 1 (consultable en el historial de Git). Novedades: Pack de Planificación con pago al enviar, área de cliente «Mis viajes», precios «desde» configurables y panel /admin con subida de documentos.

```
Actúa como desarrollador full-stack senior y diseñador web. Construye la web
de Exploryaa COMPLETA Y OPERATIVA, lista para publicar en internet.
Trabaja por fases, enséñame el resultado de cada fase y espera mi OK antes
de pasar a la siguiente.

## 1. QUÉ ES EXPLORYAA
Agencia de viajes online 100 % impulsada por IA. Lema: "Tú sueñas el viaje,
nosotros lo hacemos realidad". Público: todo el mundo, sobre todo gente que
viaja a menudo o que no viaja porque le da pereza organizar. Idioma: solo
español.
Dos tipos de producto:
A) PACK PLANIFICACIÓN (Simple, Estándar o Premium): el cliente paga solo por
   el diseño del viaje y reserva él mismo. Paga al enviar el formulario y
   recibe su planificación en su cuenta y por correo.
B) PAQUETES CON RESERVAS (Mini Escapada, Itinerario Express, Viaje Completo,
   Premium): el agente de IA genera una propuesta con vuelos, alojamiento,
   experiencias e itinerario. La asesora (yo) la reviso. EL CLIENTE SOLO PAGA
   CUANDO ACEPTA LA PROPUESTA. Después yo hago las reservas y se suben a su
   cuenta.
Todos los precios son "DESDE": el precio exacto sale en cada propuesta.

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
   - Cabecera fija: logo, menú (Cómo funciona, Planificación, Paquetes,
     Preguntas), enlace "Mis viajes" (o "Entrar") y botón dorado
     "Diseña mi viaje".
   - Hero con foto de viaje a pantalla completa, titular, subtítulo y botones
     "Diseña mi viaje" y "Ver paquetes".
   - Cómo funciona en 3 pasos: cuéntanos tu idea, recibe tu propuesta,
     disfruta tu viaje (todo en tu área "Mis viajes").
   - Sección PLANIFICACIÓN ("Tú reservas, nosotros lo diseñamos"), 3 tarjetas
     con precio "desde" (base: viajes de hasta 4 días):
     · Simple — desde [29] € — itinerario básico día a día (mañana, tarde,
       noche), lugares imprescindibles, zona recomendada para alojarse.
       PDF en 72 h. Sin revisiones.
     · Estándar — desde [59] € — todo lo de Simple + horarios y cómo moverse,
       2-3 opciones de vuelo y alojamiento con precio orientativo y enlace
       para reservar, restaurantes según gustos, mapa con los puntos del
       itinerario. Entrega en 48 h. 1 revisión. Etiqueta "Más popular".
     · Premium — desde [99] € — todo lo de Estándar + mapa interactivo con
       restaurantes, miradores y puntos de interés, actividades gratuitas por
       la zona, eventos en las fechas del viaje, plan B para días de lluvia,
       consejos locales, dossier digital maquetado. Entrega en 24-48 h.
       2 revisiones y dudas por WhatsApp hasta la salida. Tarjeta negra con
       borde dorado.
   - Sección PAQUETES CON RESERVAS (tarjetas, "desde X € por persona ·
     precio final en tu propuesta personalizada, sin compromiso"):
     · Mini Escapada 2D1N — desde [199] €/persona — 2 días / 1 noche.
       Vuelos y alojamiento, itinerario personalizado, recomendaciones
       locales, 1 revisión, enlaces y mapas.
     · Itinerario Express — desde [449] €/persona — 2-5 días. Vuelos,
       alojamiento y actividades, itinerario diario con horarios, 1 revisión,
       soporte por chat/correo.
     · Viaje Completo — desde [1.290] €/persona — 5-10 días. Vuelos,
       alojamiento, actividades y seguro, dossier digital, hasta 2 revisiones,
       soporte. Etiqueta "Más popular".
     · Exploryaa Premium — desde [2.990] €/persona — 10-21 días a medida.
       Revisiones ilimitadas, soporte por WhatsApp o llamada, asistencia
       durante el viaje. Tarjeta negra con borde dorado.
     Extras opcionales: seguro médico de viaje y actividades adicionales.
   - Formulario de viaje (ver punto 4).
   - Opiniones (de momento, huecos marcados como "[testimonio real]").
   - Preguntas frecuentes en acordeón (incluye "¿Por qué el precio es
     'desde'?" y "¿Cuándo pago?").
   - Pie: logo, aviso legal, privacidad, cookies, condiciones de contratación,
     redes sociales y "N.º de registro: [PENDIENTE]".
2. /gracias: confirmación tras enviar el formulario o pagar, con botón a
   "Mis viajes".
3. Área de cliente "Mis viajes" (ver punto 5).
4. Páginas legales con plantillas en español adaptadas a España (RGPD,
   LSSI-CE): aviso legal, política de privacidad, política de cookies y
   condiciones de contratación y cancelación. Deja entre corchetes los datos
   que tengo que rellenar (nombre, NIF, dirección, email).
5. Banner de cookies que solo cargue analítica si el usuario acepta.

## 4. FORMULARIO (en 3 pasos, con resumen del viaje en vivo al lado)
- Paso 1 "Tu viaje": tipo de servicio (Planificación Simple / Estándar /
  Premium o un paquete con reservas, en tarjetas), ida y vuelta / solo ida,
  origen*, destino* (admite "sorpréndeme" y varios destinos), fecha de ida*,
  fecha de vuelta* (solo si es ida y vuelta), casilla "fechas flexibles
  (± 3 días)", adultos* y niños con botones + y −.
- Paso 2 "Preferencias": tipo de viaje* (varias opciones: Aventura, Urbano /
  Ciudad, Relax / Bienestar, Cultural, Ocio / Diversión, Naturaleza,
  Gastronómico, Parques temáticos, Otro), ritmo (Tranquilo / Equilibrado /
  Intenso), presupuesto máximo por persona* (Hasta 300 €, 300-600 €,
  600-1.300 €, 1.300-3.000 €, Más de 3.000 €), alojamiento* (Hotel 3-5
  estrellas, Apartamento, Hostal / B&B, Casa rural, Experiencia única,
  Me da igual), experiencias sostenibles (Sí / No / Me da igual), extras y
  comentarios.
- Paso 3 "Tus datos": nombre*, email*, teléfono (opcional), cómo nos
  conociste (opcional) y casilla obligatoria de aceptación de la política de
  privacidad, con la información básica del RGPD debajo.
- Validación en cada paso con mensajes claros. Aviso visible de que el
  formulario y el asistente usan inteligencia artificial.
- Final del formulario:
  · Planificación: calcula y muestra el precio exacto (ver punto 6) y lleva
    al pago.
  · Paquetes con reservas: botón "Solicitar mi propuesta" (sin pago). El
    pago llega después, cuando el cliente acepta la propuesta.
- NO se pide crear cuenta antes del formulario: la cuenta se crea sola con
  su email al enviarlo (ver punto 5).

## 5. ÁREA DE CLIENTE "MIS VIAJES"
- Acceso sin contraseña: enlace mágico al correo y opción "Entrar con
  Google". Sesión segura (cookie httpOnly) y caducidad de los enlaces.
- La cuenta se crea automáticamente al enviar el formulario; el correo de
  confirmación incluye el enlace para entrar.
- Panel de inicio: sus viajes (próximos, en preparación y pasados) con
  cuenta atrás hasta la salida.
- Cada viaje tiene:
  · Estado en línea de tiempo: solicitud recibida → propuesta lista →
    aceptada → pagada → reservada → en viaje → finalizado (para
    planificación: pagada → en preparación → entregada).
  · Propuesta: se ve en la web, botón "Aceptar y pagar" y botón "Pedir
    cambios" (cuenta las revisiones según su nivel y avisa si se agotan).
  · Itinerario día a día con mapa interactivo y, según el nivel contratado,
    restaurantes, actividades gratuitas, eventos y plan B.
  · Reservas: billetes, confirmaciones de hotel y entradas en PDF para
    descargar.
  · Pagos: lo pagado, lo pendiente y las facturas.
  · Mensajes con la asesora y acceso directo a WhatsApp.
- Perfil viajero: gustos, alergias o necesidades, ritmo de viaje y fechas
  especiales, para rellenar más rápido el siguiente formulario.
- Después del viaje: encuesta de satisfacción.
- Cada cliente solo puede ver SUS viajes y documentos (compruébalo con tests).

## 6. PRECIOS "DESDE" (configurables en un solo archivo)
- Planificación: precio base por nivel (viajes de hasta 4 días) + extra por
  cada día adicional ([5] € Simple, [8] € Estándar, [12] € Premium) +
  [10] € por cada destino adicional. Se calcula en el formulario y se cobra
  al enviarlo.
- Paquetes con reservas: precio final = coste real del viaje (vuelos,
  alojamiento, actividades) + mis honorarios fijos por paquete
  ([49] € Mini Escapada, [89] € Express, [149] € Completo, [299] € Premium).
  Lo calcula la propuesta y yo lo reviso/ajusto en /admin antes de enviarla.
- Todos los valores entre corchetes son provisionales: ponlos en un archivo
  de configuración para que yo pueda cambiarlos sin tocar código.

## 7. BACKEND (operativo)
- Python + FastAPI. Reutiliza el agente que ya tengo en la carpeta
  exploryaa-agente (agente.py y la carpeta herramientas) sin reescribirlo.
- Base de datos: SQLite para empezar (fácil de cambiar a Postgres). Tablas:
  usuarios, perfiles, viajes/solicitudes (todos los campos del formulario,
  tipo de servicio, nivel, estado, fechas, propuesta, precio final,
  revisiones usadas), documentos (archivos subidos por viaje), pagos y
  mensajes.
- Endpoints principales:
  · POST /api/solicitudes: valida, guarda, crea o encuentra la cuenta del
    cliente y lanza el agente en segundo plano (paquetes) o crea el pago
    (planificación).
  · POST /api/auth/enlace y GET /api/auth/verificar: acceso con enlace
    mágico; también login con Google.
  · GET /api/mis-viajes y GET /api/mis-viajes/{id}: datos del área privada.
  · POST /api/mis-viajes/{id}/aceptar: crea el pago de la propuesta.
  · POST /api/mis-viajes/{id}/cambios: pide una revisión.
  · POST /api/checkout y POST /api/pagos/webhook: pagos (con verificación de
    firma e idempotencia).
- Pagos: Stripe Checkout en MODO TEST, detrás de una interfaz
  "ProveedorPago" para poder cambiarlo luego por el TPV de mi banco (Redsys)
  sin tocar el resto. Nunca toques datos de tarjeta en mi servidor.
- Correo: Resend (o SMTP configurable). Plantillas HTML con la marca:
  1) "Hemos recibido tu solicitud" + enlace a Mis viajes.
  2) "Tu propuesta está lista" / "Tu planificación está lista" + enlace.
  3) "Tus reservas ya están en Mis viajes".
  4) Enlace mágico de acceso.
  Aviso de que los precios son orientativos hasta la confirmación.
  Copia oculta de cada correo a mi email.
- Si el agente falla: reintento automático y aviso por email para mí.
- Panel de administración protegido en /admin: lista de clientes y viajes,
  cambiar estado, revisar y ajustar la propuesta y el precio antes de
  enviarla, SUBIR DOCUMENTOS (billetes, confirmaciones, dossier) que
  aparecen al momento en la cuenta del cliente, responder mensajes,
  reenviar correos y marcar incidencias.
- Seguridad: claves en .env (con .env.example sin valores), CORS limitado a
  mi dominio, límite de peticiones en formulario y login, anti-spam
  (honeypot), HTTPS, documentos privados con enlaces firmados y caducidad.

## 8. SEO Y MEDICIÓN
- Títulos, meta descripciones, Open Graph con el logo, sitemap.xml,
  robots.txt y datos estructurados de TravelAgency. El área privada, con
  noindex.
- Analítica respetuosa con la privacidad (Plausible o GA4 solo con
  consentimiento) y eventos: inicio de formulario, paso completado,
  solicitud enviada, propuesta aceptada, pago.
- Página rápida: imágenes optimizadas, carga diferida y Lighthouse de 90 o más.

## 9. PUBLICACIÓN
- Frontend en Vercel o Netlify y backend en Render o Railway (o todo en uno
  si es más sencillo). Explícame paso a paso cómo conectar mi dominio.
- Repositorio Git con un README en español para alguien no experto:
  instalación, variables de entorno, cómo probar en local (incluido
  "stripe listen" para el webhook), cómo publicar, cómo cambiar los precios
  y cómo pasar de modo test a modo real.

## 10. PRUEBAS
- Tests del formulario, del cálculo de precios, del login con enlace mágico,
  de los endpoints, del webhook con las tarjetas de prueba de Stripe y de que
  un cliente no puede ver los viajes de otro.
- Dos pruebas de punta a punta:
  1) Planificación: formulario → pago en modo test → planificación visible
     en Mis viajes + correo.
  2) Paquete: formulario → propuesta en Mis viajes → pedir cambio → aceptar
     y pagar en modo test → subo documentos en /admin → aparecen en la
     cuenta del cliente.

## ORDEN DE TRABAJO
Fase 1: estructura del proyecto y landing estática con el diseño.
Fase 2: formulario funcional, cálculo de precios y guardado en la base de
        datos.
Fase 3: cuentas de cliente (enlace mágico y Google) y área "Mis viajes".
Fase 4: pagos en modo test y webhook (planificación y aceptar propuesta).
Fase 5: conexión con el agente, propuestas y envío de correos.
Fase 6: panel /admin con subida de documentos.
Fase 7: páginas legales, cookies y SEO.
Fase 8: publicación y README.
Antes de empezar, hazme las preguntas que necesites (dominio, email de
contacto, precios…) y no inventes datos legales ni testimonios.
```
