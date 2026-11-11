/**
 * EXPLORYAA — Conexión del formulario de la web con el envío de correos
 * ------------------------------------------------------------------
 * 1. Pega aquí la URL de tu Apps Script (termina en /exec).
 * 2. En el formulario, en el último paso ("Diseñar mi viaje"), llama a
 *    enviarSolicitud(f) en lugar de marcar directamente como enviado.
 *
 * index.html ya carga este archivo y llama a enviarSolicitud(f, honeypot)
 * al pulsar "Enviar mi solicitud".
 */
const EXPLORYAA_ENDPOINT = 'https://script.google.com/macros/s/AKfycby2FxoEHU1cB3uJJUetMH6QeUrc8mPSMBT0qlVO7p_EiF_mGWZfQYlAuLcjwbUXP2MM/exec';

async function enviarSolicitud(f, honeypot = '') {
  const datos = {
    paquete: f.paquete, vuelo: f.vuelo,
    origen: f.origen.trim(), destino: f.destino.trim(),
    fechaIda: f.fechaIda, fechaVuelta: f.vuelo === 'Ida y vuelta' ? f.fechaVuelta : '',
    flexibles: f.flexibles, adultos: f.adultos, ninos: f.ninos,
    tipos: f.tipos, presupuesto: f.presupuesto, alojamiento: f.alojamiento,
    sostenible: f.sostenible, extras: f.extras, comentarios: f.comentarios.trim(),
    nombre: f.nombre.trim(), email: f.email.trim(), telefono: f.telefono.trim(),
    origenCliente: f.origenCliente, consentimiento: f.consentimiento,
    web: honeypot, // campo anti-spam oculto: debe llegar vacío
  };
  // "text/plain" evita el bloqueo CORS de Google Apps Script
  const res = await fetch(EXPLORYAA_ENDPOINT, {
    method: 'POST',
    headers: { 'Content-Type': 'text/plain;charset=utf-8' },
    body: JSON.stringify(datos),
  });
  const json = await res.json();
  if (!json.ok) throw new Error(json.error || 'No se pudo enviar la solicitud.');
  return json; // { ok: true, id: 'EXP-261111-AB12' }
}
