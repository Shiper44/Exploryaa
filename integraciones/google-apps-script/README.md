# Conectar el formulario de Exploryaa y enviar el correo al cliente

Servidor gratuito con Google Apps Script: guarda cada solicitud en una Google Sheet, envía al cliente un correo de confirmación con la marca (desde tu Gmail) y te avisa a ti.

**URL publicada actualmente** (ya configurada en `conexion-formulario.js`, en la raíz del repositorio):
`https://script.google.com/macros/s/AKfycby2FxoEHU1cB3uJJUetMH6QeUrc8mPSMBT0qlVO7p_EiF_mGWZfQYlAuLcjwbUXP2MM/exec`

Para comprobar que está activa, ábrela en el navegador: debe responder `{"ok":true,"servicio":"Formulario Exploryaa activo"}`.

## Instalación (10 minutos)
1. Crea una Google Sheet nueva llamada "Exploryaa – Solicitudes".
2. Menú Extensiones › Apps Script. Borra lo que haya y pega `Code.gs`. Guarda.
3. Arriba elige la función `probarEnvio` y pulsa Ejecutar. Acepta los permisos de Google (Gmail y Hojas). Te llegarán dos correos de prueba y aparecerá la hoja "Solicitudes".
4. Implementar › Nueva implementación › tipo "Aplicación web". Ejecutar como: Yo. Quién tiene acceso: Cualquier usuario. Copia la URL que termina en /exec.
5. Pega esa URL en `conexion-formulario.js` (EXPLORYAA_ENDPOINT). `index.html` ya llama a `enviarSolicitud(f)` en el botón final del formulario.

Notas: Gmail gratuito permite unos 100 correos al día desde Apps Script. Si cambias Code.gs, vuelve a Implementar › Gestionar implementaciones › Editar › Nueva versión (la URL no cambia).

## Notion (tabla "Clientes- Exploryaa")
Cada solicitud crea además una fila en la tabla (ID 2965e5d6f08c80a3b751f9b043c8fb92) con estado "Nuevo". El script lee las columnas y opciones reales de la tabla y las empareja solo; paquete, extras, niños y fechas flexibles van en "Comentarios adicionales".
1. notion.so/my-integrations › Nueva integración "Formulario Exploryaa" (interna), en el espacio donde está la tabla. Copia el secreto (ntn_...).
2. En la tabla: ••• › Conexiones › añade "Formulario Exploryaa".
3. Apps Script › Configuración del proyecto (engranaje) › Propiedades de secuencia de comandos › Añadir: nombre NOTION_TOKEN, valor el secreto.
4. Ejecuta `probarNotion` (pide permiso para conectarse a servicios externos) y comprueba que aparece la fila "Cliente de Prueba".
5. Implementar › Gestionar implementaciones › Editar › Nueva versión.
Si Notion falla, el cliente recibe igualmente su correo y el aviso interno te dice qué ha pasado.

### Crear la tabla automáticamente
1. En el Notion de Exploryaa, abre la página donde quieres la tabla (p. ej. "Home de la empresa") › ••• › Conexiones › añade "Formulario Exploryaa". Copia su enlace.
2. En Code.gs pega ese enlace en NOTION_PAGINA_PADRE y guarda.
3. Elige la función `crearTablaNotion` y pulsa Ejecutar. La tabla "Clientes - Exploryaa" aparece en esa página y el script guarda su ID solo (propiedad NOTION_DB_ID).
4. Ejecuta `probarNotion` y vuelve a publicar (Gestionar implementaciones › Editar › Nueva versión).

### Columnas de la tabla en Notion (iguales que el formulario)
| Columna | Tipo | Opciones |
|---|---|---|
| Nombre | Título | — |
| Correo electrónico | Correo electrónico | — |
| Teléfono | Teléfono | — |
| Ciudad o país de origen | Texto | — |
| Destino de interés | Texto | — |
| Fechas aproximadas | Fecha (con fecha de finalización) | — |
| Número de personas | Número | — |
| Tipo de viaje | Selección múltiple | Aventura · Urbano / Ciudad · Relax / Bienestar · Cultural · Ocio / Diversión · Naturaleza · Gastronómico · Parques temáticos · Otro |
| Presupuesto por persona | Selección | Hasta 300 € · 300 – 600 € · 600 – 1.300 € · 1.300 – 3.000 € · Más de 3.000 € |
| Tipo de alojamiento | Selección | Hotel 3-5 estrellas · Apartamento · Hostal / B&B · Casa rural · Experiencia única · Me da igual |
| Experiencias sostenibles | Selección | Sí · No · Me da igual |
| Cómo conociste | Selección | Redes sociales · Google · Amigos o familia · Escuela · Otro |
| Comentarios adicionales | Texto | — |
| Estado | Estado | Nuevo · En preparación · Propuesta enviada · Aceptado y pagado · Viaje completado · Cancelado |
| Acepto la política de privacidad | Casilla de verificación | — |
| Paquete (nueva) | Selección | Mini Escapada 2D1N · Itinerario Express · Viaje Completo · Exploryaa Premium · Aún no lo sé |
| Tipo de vuelo (nueva) | Selección | Ida y vuelta · Solo ida |
| Fechas flexibles (nueva) | Casilla de verificación | — |
| Extras (nueva) | Selección múltiple | Seguro médico de viaje · Actividades adicionales |
| ID solicitud (nueva) | Texto | — |
