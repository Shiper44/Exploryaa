/**
 * EXPLORYAA — Receptor del formulario de viaje
 * ------------------------------------------------------------
 * Qué hace cada vez que alguien envía el formulario de la web:
 *   1. Guarda la solicitud en la hoja "Solicitudes" de este Google Sheet.
 *   2. Envía al cliente un correo de confirmación con la marca Exploryaa.
 *   3. Te envía a ti un aviso con todos los datos del viaje.
 *
 * Instalación: ver la guía "Conectar el formulario" (pasos 1-5).
 */

// ===== AJUSTES (puedes cambiarlos) =====
const MARCA = 'Exploryaa';
const NOMBRE_REMITENTE = 'Exploryaa · Agencia de viajes';
const EMAIL_RESPUESTA = '';   // Si lo dejas vacío, las respuestas del cliente llegan a tu Gmail.
const EMAIL_AVISOS = '';      // A quién avisar de cada solicitud nueva. Vacío = tu propio Gmail.
const HORAS_RESPUESTA = '48 horas';
const WHATSAPP = '';          // Ej.: '+34 600 000 000'. Vacío = no se muestra.
const NOMBRE_HOJA = 'Solicitudes';
const COPIA_OCULTA = true;    // true = recibes en copia oculta cada confirmación que se envía al cliente.

const COLUMNAS = [
  'Fecha recepción', 'ID', 'Estado', 'Nombre', 'Email', 'Teléfono', 'Paquete',
  'Tipo de vuelo', 'Origen', 'Destino', 'Fecha ida', 'Fecha vuelta', 'Fechas flexibles',
  'Adultos', 'Niños', 'Tipo de viaje', 'Presupuesto/pers.', 'Alojamiento',
  'Sostenible', 'Extras', 'Comentarios', 'Cómo nos conoció', 'Consentimiento RGPD',
];

// ===== RECEPCIÓN DEL FORMULARIO =====
function doPost(e) {
  const lock = LockService.getScriptLock();
  try {
    lock.waitLock(20000);
    const d = JSON.parse((e && e.postData && e.postData.contents) || '{}');

    // Anti-spam: campo oculto que solo rellenan los robots
    if (d.web) return respuesta({ ok: true });

    const error = validar(d);
    if (error) return respuesta({ ok: false, error });

    const id = 'EXP-' + Utilities.formatDate(new Date(), 'Europe/Madrid', 'yyMMdd') + '-' +
      Math.random().toString(36).slice(2, 6).toUpperCase();

    guardar(d, id);
    let notion = '';
    try { notion = guardarEnNotion(d, id); }
    catch (errNotion) { console.error(errNotion); notion = '⚠️ No se pudo añadir a Notion: ' + errNotion.message; }
    const confirmacion = enviarConfirmacionCliente(d, id);
    enviarAvisoInterno(d, id, notion, confirmacion);

    return respuesta({ ok: true, id });
  } catch (err) {
    console.error(err);
    return respuesta({ ok: false, error: 'No hemos podido enviar tu solicitud. Inténtalo de nuevo en unos minutos.' });
  } finally {
    try { lock.releaseLock(); } catch (_) {}
  }
}

// Para comprobar en el navegador que el servidor está activo
function doGet() {
  return respuesta({ ok: true, servicio: 'Formulario Exploryaa activo' });
}

function respuesta(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

// ===== VALIDACIÓN (la misma que en la web, por seguridad) =====
function validar(d) {
  const txt = (v) => String(v || '').trim();
  if (!txt(d.nombre)) return 'Falta el nombre.';
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(txt(d.email))) return 'El correo electrónico no es válido.';
  if (!d.consentimiento) return 'Falta aceptar la política de privacidad.';
  if (!txt(d.origen) || !txt(d.destino) || !txt(d.fechaIda)) return 'Faltan datos del viaje.';
  if (txt(d.comentarios).length > 3000) return 'El comentario es demasiado largo.';
  return '';
}

// ===== GOOGLE SHEET =====
function guardar(d, id) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let hoja = ss.getSheetByName(NOMBRE_HOJA);
  if (!hoja) {
    hoja = ss.insertSheet(NOMBRE_HOJA);
    hoja.appendRow(COLUMNAS);
    hoja.getRange(1, 1, 1, COLUMNAS.length).setFontWeight('bold').setBackground('#0B0B0B').setFontColor('#D4AF37');
    hoja.setFrozenRows(1);
  }
  hoja.appendRow([
    new Date(), id, 'Nueva', d.nombre, d.email, limpiaCelda(d.telefono), d.paquete,
    d.vuelo, d.origen, d.destino, d.fechaIda, d.fechaVuelta || '', d.flexibles ? 'Sí' : 'No',
    d.adultos, d.ninos, lista(d.tipos), d.presupuesto, d.alojamiento,
    d.sostenible || '', lista(d.extras), d.comentarios || '', d.origenCliente || '', d.consentimiento ? 'Sí' : 'No',
  ].map(limpiaCelda));
}

// Evita que un texto que empiece por = + - @ se interprete como fórmula
function limpiaCelda(v) {
  if (typeof v === 'string' && /^[=+\-@]/.test(v)) return "'" + v;
  return v;
}

// ===== CORREO AL CLIENTE =====
function enviarConfirmacionCliente(d, id) {
  const nombre = esc(String(d.nombre).trim().split(/\s+/)[0]);
  const filas = resumen(d).map(([k, v]) =>
    `<tr><td style="padding:10px 0;color:#9A9A9A;font-size:14px;width:40%;vertical-align:top">${esc(k)}</td>` +
    `<td style="padding:10px 0;color:#0B0B0B;font-size:14px;font-weight:600;vertical-align:top">${esc(v)}</td></tr>`
  ).join('');

  const whatsapp = WHATSAPP
    ? `<p style="margin:0 0 8px;font-size:15px;line-height:1.6;color:#3A3A3A">¿Prisa o alguna duda? Escríbenos por WhatsApp al <strong>${esc(WHATSAPP)}</strong>.</p>`
    : '';

  const html = `
<div style="background:#F4F4F4;padding:32px 12px;font-family:Inter,Arial,Helvetica,sans-serif">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:600px;margin:0 auto;background:#FFFFFF;border-radius:16px;overflow:hidden">
    <tr><td style="background:#0B0B0B;padding:32px;text-align:center">
      <div style="font-size:28px;color:#FFFFFF">✈</div>
      <div style="font-family:'Space Grotesk',Arial,sans-serif;font-size:24px;letter-spacing:0.25em;color:#9A9A9A;font-weight:700">EXPLORYAA</div>
      <div style="width:48px;height:2px;background:#D4AF37;margin:16px auto 0"></div>
    </td></tr>
    <tr><td style="padding:36px 32px 8px">
      <h1 style="margin:0 0 16px;font-family:'Space Grotesk',Arial,sans-serif;font-size:26px;line-height:1.25;color:#0B0B0B">¡Gracias, ${nombre}! Ya estamos diseñando tu viaje</h1>
      <p style="margin:0 0 16px;font-size:15px;line-height:1.6;color:#3A3A3A">Hemos recibido tu solicitud. En un plazo de <strong>${esc(HORAS_RESPUESTA)}</strong> te enviaremos a este correo una propuesta personalizada con vuelos, alojamiento, experiencias e itinerario día a día.</p>
      <p style="margin:0 0 24px;font-size:15px;line-height:1.6;color:#3A3A3A">Solo pagas si la propuesta te convence y la aceptas: rellenar el formulario no te compromete a nada.</p>
      <div style="background:#FAF7EC;border:1px solid #E8DDB5;border-radius:12px;padding:20px 24px">
        <div style="font-size:12px;letter-spacing:0.2em;text-transform:uppercase;color:#7A5F0E;font-weight:700;margin-bottom:6px">Resumen de tu solicitud · ${esc(id)}</div>
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0">${filas}</table>
      </div>
    </td></tr>
    <tr><td style="padding:24px 32px 8px">
      <p style="margin:0 0 8px;font-size:15px;line-height:1.6;color:#3A3A3A">¿Quieres cambiar algo? Responde a este correo y lo ajustamos.</p>
      ${whatsapp}
      <p style="margin:16px 0 0;font-size:15px;line-height:1.6;color:#0B0B0B">Tú sueñas el viaje, nosotros lo hacemos realidad.<br><strong>El equipo de Exploryaa</strong></p>
    </td></tr>
    <tr><td style="padding:24px 32px 32px">
      <p style="margin:0;font-size:12px;line-height:1.6;color:#9A9A9A;border-top:1px solid #EEEEEE;padding-top:16px">Has recibido este correo porque has solicitado un viaje en Exploryaa. Tus datos se usan solo para preparar tu propuesta, según nuestra política de privacidad. Para ejercer tus derechos de acceso, rectificación o supresión, responde a este correo. Las propuestas se preparan con ayuda de inteligencia artificial y las revisa una persona.</p>
    </td></tr>
  </table>
</div>`;

  const texto = `¡Gracias, ${String(d.nombre).trim()}!\n\nHemos recibido tu solicitud (${id}). En un plazo de ${HORAS_RESPUESTA} te enviaremos tu propuesta personalizada.\n\n` +
    resumen(d).map(([k, v]) => `${k}: ${v}`).join('\n') +
    `\n\n¿Quieres cambiar algo? Responde a este correo.\n\nEl equipo de Exploryaa`;

  const opciones = { name: NOMBRE_REMITENTE, htmlBody: html };
  if (EMAIL_RESPUESTA) opciones.replyTo = EMAIL_RESPUESTA;
  if (COPIA_OCULTA) opciones.bcc = EMAIL_AVISOS || Session.getEffectiveUser().getEmail();

  const para = String(d.email).trim();
  MailApp.sendEmail(para, `Hemos recibido tu solicitud de viaje ✈ ${MARCA}`, texto, opciones);
  console.log(`Confirmación ${id} enviada a ${para}`);
  return `Enviada a ${para}` + (COPIA_OCULTA ? ' (te llega una copia oculta)' : '') +
    ` · Correos disponibles hoy: ${MailApp.getRemainingDailyQuota()}. Si no le llega, que revise spam o Promociones; si el email estaba mal, te llegará un aviso de rebote.`;
}

// ===== AVISO PARA TI =====
function enviarAvisoInterno(d, id, notion, confirmacion) {
  const para = EMAIL_AVISOS || Session.getEffectiveUser().getEmail();
  const filas = [['Nombre', d.nombre], ['Email', d.email], ['Teléfono', d.telefono || '—']]
    .concat(resumen(d))
    .concat([['Comentarios', d.comentarios || '—'], ['Cómo nos conoció', d.origenCliente || '—']])
    .map(([k, v]) => `<tr><td style="padding:6px 12px 6px 0;color:#777">${esc(k)}</td><td style="padding:6px 0"><strong>${esc(v)}</strong></td></tr>`)
    .join('');
  const url = SpreadsheetApp.getActiveSpreadsheet().getUrl();
  MailApp.sendEmail({
    to: para,
    replyTo: String(d.email).trim(),
    subject: `🆕 Nueva solicitud ${id} · ${d.paquete} · ${d.destino}`,
    htmlBody: `<div style="font-family:Arial,sans-serif;font-size:14px">
      <h2 style="margin:0 0 12px">Nueva solicitud de viaje · ${esc(id)}</h2>
      <table>${filas}</table>
      ${confirmacion ? `<p><strong>Correo de confirmación al cliente:</strong> ${esc(confirmacion)}</p>` : ''}
      ${notion ? `<p>${notion.startsWith('http') ? `<a href="${notion}">Ver ficha en Notion</a>` : esc(notion)}</p>` : ''}
      <p><a href="${url}">Abrir la hoja de solicitudes</a> · Responde a este correo para escribir directamente al cliente.</p></div>`,
  });
}

// ===== NOTION: tabla "Clientes- Exploryaa" =====
// La clave (ntn_...) NO va aquí: se guarda en Configuración del proyecto ›
// Propiedades de secuencia de comandos, con el nombre NOTION_TOKEN.
// ID de la tabla: si ejecutas crearTablaNotion() se guarda solo y sustituye a este.
const NOTION_DB_ID_INICIAL = '2965e5d6f08c80a3b751f9b043c8fb92';
const NOTION_DB_ID = PropertiesService.getScriptProperties().getProperty('NOTION_DB_ID') || NOTION_DB_ID_INICIAL;

// Para crear la tabla nueva: pega aquí el enlace de la página de Notion donde
// quieres que aparezca (esa página debe tener añadida la conexión de la integración).
const NOTION_PAGINA_PADRE = 'PEGA_AQUI_EL_ENLACE_DE_LA_PAGINA';
const NOTION_VERSION = '2022-06-28';

// Qué columna de Notion recibe cada dato. Basta con el principio del nombre
// (sin importar mayúsculas, tildes ni comillas).
const NOTION_COLUMNAS = {
  email: 'correo electr',
  telefono: 'telefono',
  origen: 'ciudad o pais',
  destino: 'destino de interes',
  fechas: 'fechas aprox',
  personas: 'numero de pers',
  adultos: 'adultos',
  ninos: 'ninos',
  tipos: 'tipo de viaje',
  presupuesto: 'presupuesto',
  alojamiento: 'tipo de aloj',
  sostenible: 'experiencias so',
  origenCliente: ['como nos conociste', 'como conociste'],
  comentarios: 'comentarios',
  estado: 'estado',
  consentimiento: 'acepto',
  paquete: 'paquete',
  vuelo: 'tipo de vuelo',
  flexibles: 'fechas flexibles',
  extras: 'extras',
  idSolicitud: 'id solicitud',
};

// Si una respuesta del formulario no existe tal cual en Notion, se prueban
// estas equivalencias (la primera que exista en tu tabla gana).
const NOTION_EQUIVALENCIAS = {
  'Me da igual': ['No tengo preferencia', 'Tal vez', 'Indiferente'],
  'Experiencia única (glamping, riad, casa flotante…)': ['Experiencia única'],
  'Sí': ['Si'],
};

function guardarEnNotion(d, id) {
  const token = (PropertiesService.getScriptProperties().getProperty('NOTION_TOKEN') || '').trim();
  if (!token) throw new Error('guardarEnNotion no encuentra NOTION_TOKEN');
  const esquema = notionApi('get', '/databases/' + NOTION_DB_ID, token).properties;
  const cols = Object.keys(esquema).map((nombre) => ({ nombre, ...esquema[nombre] }));
  const buscar = (prefijos) => [].concat(prefijos).map((p) => cols.find((c) => norm(c.nombre).startsWith(norm(p)))).find(Boolean);

  const viajeros = Number(d.adultos) + Number(d.ninos || 0);
  // Lo que no tenga columna propia en tu tabla se apunta en "Comentarios adicionales"
  const notas = [];

  const valores = {
    email: String(d.email).trim(), telefono: d.telefono || '', origen: d.origen, destino: d.destino,
    fechas: { start: d.fechaIda, end: d.vuelo === 'Ida y vuelta' && d.fechaVuelta ? d.fechaVuelta : null },
    personas: viajeros, adultos: Number(d.adultos), ninos: Number(d.ninos || 0), tipos: d.tipos || [], presupuesto: d.presupuesto, alojamiento: d.alojamiento,
    sostenible: d.sostenible, origenCliente: d.origenCliente, estado: 'Nuevo',
    consentimiento: d.consentimiento ? 'Sí' : 'No',
    paquete: d.paquete, vuelo: d.vuelo, flexibles: d.flexibles ? 'Sí' : 'No',
    extras: d.extras || [], idSolicitud: id,
  };

  const props = {};
  const titulo = cols.find((c) => c.type === 'title');
  props[titulo.nombre] = { title: [{ text: { content: String(d.nombre).trim() } }] };

  Object.keys(valores).forEach((clave) => {
    const col = buscar(NOTION_COLUMNAS[clave]);
    const v = valores[clave];
    if (v === '' || v == null || (Array.isArray(v) && !v.length)) return;
    if (!col && clave === 'ninos' && !v) return;
    if (!col) {
      if (clave !== 'comentarios' && clave !== 'estado') notas.push(`${clave === 'idSolicitud' ? 'Solicitud' : clave[0].toUpperCase() + clave.slice(1)}: ${textoPlano(v)}`);
      return;
    }
    const p = propiedadNotion(col, v, clave);
    if (p) props[col.nombre] = p;
    else notas.push(`${col.nombre}: ${textoPlano(v)}`);  // tipo de columna no editable por API
  });

  const colComentarios = buscar(NOTION_COLUMNAS.comentarios);
  if (colComentarios && (d.comentarios || notas.length)) {
    const texto = [d.comentarios ? d.comentarios.trim() : '', notas.join('\n')].filter(Boolean).join('\n\n');
    props[colComentarios.nombre] = { rich_text: [{ text: { content: texto.slice(0, 1900) } }] };
  }

  const pagina = notionApi('post', '/pages', token, { parent: { database_id: NOTION_DB_ID }, properties: props });
  return pagina.url || ('Respuesta de Notion: ' + JSON.stringify(pagina).slice(0, 800));
}

function propiedadNotion(col, v, clave) {
  const texto = textoPlano(v);
  switch (col.type) {
    case 'email': return { email: texto };
    case 'phone_number': return { phone_number: texto };
    case 'rich_text': return { rich_text: [{ text: { content: texto.slice(0, 1900) } }] };
    case 'number': { const n = Number(v); return isNaN(n) ? null : { number: n }; }
    case 'date': return typeof v === 'object' && v.start ? { date: v } : null;
    case 'checkbox': return { checkbox: v === true || norm(texto) === 'si' };
    case 'select': return { select: { name: opcion(col.select.options, texto, clave) } };
    case 'status': {
      const o = col.status.options.find((x) => norm(x.name) === norm(texto)) || col.status.options[0];
      return o ? { status: { name: o.name } } : null;
    }
    case 'multi_select': {
      const lista = Array.isArray(v) ? v : [v];
      return { multi_select: lista.map((x) => ({ name: opcion(col.multi_select.options, String(x), clave) })) };
    }
    default: return null;
  }
}

// Elige la opción de Notion que corresponde a la respuesta del formulario.
// Si no existe ninguna parecida, Notion la crea con el texto del formulario.
function opcion(opciones, texto, clave) {
  const nombres = opciones.map((o) => o.name);
  const exacta = nombres.find((n) => norm(n) === norm(texto));
  if (exacta) return exacta;
  for (const alt of NOTION_EQUIVALENCIAS[texto] || []) {
    const m = nombres.find((n) => norm(n) === norm(alt) || norm(n).startsWith(norm(alt)));
    if (m) return m;
  }
  if (clave === 'presupuesto') {  // compara las cifras: "Más de 3.000 €" ↔ "3000+"
    const cifras = (s) => (String(s).replace(/\./g, '').match(/\d+/g) || []).join('-');
    const m = nombres.find((n) => cifras(n) && cifras(n) === cifras(texto));
    if (m) return m;
  }
  return texto.replace(/,/g, ' ').slice(0, 100);
}

function notionApi(metodo, ruta, token, cuerpo) {
  const res = UrlFetchApp.fetch('https://api.notion.com/v1' + ruta, {
    method: metodo, muteHttpExceptions: true, contentType: 'application/json',
    headers: { Authorization: 'Bearer ' + token, 'Notion-Version': NOTION_VERSION },
    payload: cuerpo ? JSON.stringify(cuerpo) : undefined,
  });
  const json = JSON.parse(res.getContentText() || '{}');
  if (res.getResponseCode() >= 300) throw new Error(json.message || ('Error ' + res.getResponseCode()));
  return json;
}

function textoPlano(v) {
  if (Array.isArray(v)) return v.join(', ');
  if (v && typeof v === 'object' && v.start) return v.start + (v.end ? ' → ' + v.end : '');
  return String(v == null ? '' : v);
}

function norm(s) {
  return String(s).normalize('NFD').replace(/[̀-ͯ]/g, '')
    .replace(/^[^a-z0-9]+/i, '').toLowerCase().replace(/\s+/g, ' ').trim();
}

// ===== CREA LA TABLA "Clientes - Exploryaa" CON LAS COLUMNAS DEL FORMULARIO =====
// Ejecútala UNA vez desde el editor. Después, el formulario escribe en esta tabla.
function crearTablaNotion() {
  const token = PropertiesService.getScriptProperties().getProperty('NOTION_TOKEN');
  if (!token) throw new Error('Falta NOTION_TOKEN en Propiedades de secuencia de comandos.');
  const idPadre = (String(NOTION_PAGINA_PADRE).replace(/-/g, '').match(/[0-9a-f]{32}/i) || [])[0];
  if (!idPadre) throw new Error('Pega en NOTION_PAGINA_PADRE el enlace de la página de Notion.');

  const sel = (opciones, color) => ({ options: opciones.map((name, i) => ({ name, color: Array.isArray(color) ? color[i] : color })) });
  const props = {
    'Nombre': { title: {} },
    'Correo electrónico': { email: {} },
    'Teléfono': { phone_number: {} },
    'Paquete': { select: sel(['Mini Escapada 2D1N', 'Itinerario Express', 'Viaje Completo', 'Exploryaa Premium', 'Aún no lo sé'], ['blue', 'green', 'yellow', 'orange', 'gray']) },
    'Tipo de vuelo': { select: sel(['Ida y vuelta', 'Solo ida'], ['blue', 'purple']) },
    'Ciudad o país de origen': { rich_text: {} },
    'Destino de interés': { rich_text: {} },
    'Fechas aproximadas': { date: {} },
    'Fechas flexibles': { checkbox: {} },
    'Adultos': { number: { format: 'number' } },
    'Niños': { number: { format: 'number' } },
    'Número de personas': { number: { format: 'number' } },
    'Tipo de viaje': { multi_select: sel(['Aventura', 'Urbano / Ciudad', 'Relax / Bienestar', 'Cultural', 'Ocio / Diversión', 'Naturaleza', 'Gastronómico', 'Parques temáticos', 'Otro'],
      ['brown', 'gray', 'blue', 'purple', 'pink', 'green', 'orange', 'yellow', 'default']) },
    'Presupuesto por persona': { select: sel(['Hasta 300 €', '300 – 600 €', '600 – 1.300 €', '1.300 – 3.000 €', 'Más de 3.000 €'], ['gray', 'blue', 'green', 'orange', 'red']) },
    'Tipo de alojamiento': { select: sel(['Hotel 3-5 estrellas', 'Apartamento', 'Hostal / B&B', 'Casa rural', 'Experiencia única', 'Me da igual'], ['blue', 'green', 'yellow', 'brown', 'purple', 'gray']) },
    'Experiencias sostenibles': { select: sel(['Sí', 'No', 'Me da igual'], ['green', 'red', 'gray']) },
    'Extras': { multi_select: sel(['Seguro médico de viaje', 'Actividades adicionales'], ['blue', 'orange']) },
    'Comentarios adicionales': { rich_text: {} },
    '¿Cómo nos conociste?': { select: sel(['Redes sociales', 'Google', 'Amigos o familia', 'Escuela', 'Otro'], ['pink', 'blue', 'green', 'yellow', 'gray']) },
    'Acepto la política de privacidad': { checkbox: {} },
    'Estado': { select: sel(['Nuevo', 'En preparación', 'Propuesta enviada', 'Aceptado y pagado', 'Viaje completado', 'Cancelado'], ['blue', 'yellow', 'purple', 'green', 'gray', 'red']) },
    'ID solicitud': { rich_text: {} },
    'Fecha de solicitud': { created_time: {} },
  };
  const db = notionApi('post', '/databases', token, {
    parent: { type: 'page_id', page_id: idPadre },
    title: [{ type: 'text', text: { content: 'Clientes - Exploryaa' } }],
    is_inline: true,
    properties: props,
  });
  PropertiesService.getScriptProperties().setProperty('NOTION_DB_ID', db.id.replace(/-/g, ''));
  console.log('Tabla creada: ' + db.url);
  return db.url;
}

// Prueba solo la parte de Notion (no envía correos)
function probarNotion() {
  console.log(guardarEnNotion({
    paquete: 'Viaje Completo', vuelo: 'Ida y vuelta', origen: 'Barcelona', destino: 'Japón (PRUEBA)',
    fechaIda: '2027-04-10', fechaVuelta: '2027-04-18', flexibles: true, adultos: 2, ninos: 1,
    tipos: ['Cultural', 'Gastronómico'], presupuesto: 'Más de 3.000 €', alojamiento: 'Me da igual',
    sostenible: 'Me da igual', extras: ['Seguro médico de viaje'], comentarios: 'Fila de prueba, puedes borrarla',
    nombre: 'Cliente de Prueba', email: 'prueba@ejemplo.com', telefono: '600000000',
    origenCliente: 'Otro', consentimiento: true,
  }, 'EXP-PRUEBA'));
}

// ===== AYUDANTES =====
function resumen(d) {
  const fechas = fechaBonita(d.fechaIda) +
    (d.vuelo === 'Ida y vuelta' && d.fechaVuelta ? ' → ' + fechaBonita(d.fechaVuelta) : ' (solo ida)') +
    (d.flexibles ? ' · flexibles ± 3 días' : '');
  const viajeros = d.adultos + (Number(d.adultos) === 1 ? ' adulto' : ' adultos') +
    (Number(d.ninos) ? ' · ' + d.ninos + (Number(d.ninos) === 1 ? ' niño' : ' niños') : '');
  return [
    ['Paquete', d.paquete],
    ['Ruta', `${d.origen} → ${d.destino}`],
    ['Fechas', fechas],
    ['Viajeros', viajeros],
    ['Estilo de viaje', lista(d.tipos) || '—'],
    ['Presupuesto', d.presupuesto ? d.presupuesto + ' por persona' : '—'],
    ['Alojamiento', d.alojamiento || '—'],
    ['Experiencias sostenibles', d.sostenible || '—'],
    ['Extras', lista(d.extras) || '—'],
  ];
}

function lista(v) { return Array.isArray(v) ? v.join(', ') : (v || ''); }

function fechaBonita(iso) {
  if (!iso) return '—';
  const m = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic'];
  const [y, mo, dd] = String(iso).split('-');
  return parseInt(dd, 10) + ' ' + m[parseInt(mo, 10) - 1] + ' ' + y;
}

function esc(v) {
  return String(v == null ? '' : v)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

// ===== PRUEBA: ejecútala desde el editor para recibir un correo de ejemplo =====
function probarEnvio() {
  const yo = Session.getEffectiveUser().getEmail();
  const resultado = doPost({ postData: { contents: JSON.stringify({
    paquete: 'Viaje Completo', vuelo: 'Ida y vuelta', origen: 'Barcelona', destino: 'Japón',
    fechaIda: '2027-04-10', fechaVuelta: '2027-04-18', flexibles: true, adultos: 2, ninos: 0,
    tipos: ['Cultural', 'Gastronómico'], presupuesto: '1.300 – 3.000 €', alojamiento: 'Hotel 3-5 estrellas',
    sostenible: 'Me da igual', extras: ['Seguro médico de viaje'], comentarios: 'Es nuestra luna de miel',
    nombre: 'Cliente de Prueba', email: yo, telefono: '', origenCliente: 'Instagram', consentimiento: true,
  }) } });
  console.log(resultado.getContent());
}
