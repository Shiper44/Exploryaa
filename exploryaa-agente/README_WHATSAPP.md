# Asistente de WhatsApp de Exploryaa

Un asistente de IA que atiende a tus clientes por WhatsApp. Conoce el itinerario y las reservas de cada cliente, da recomendaciones en el destino y **te avisa a ti** cuando hace falta una persona.

## Qué hace
- **Clientes con viaje registrado:** responde preguntas del tipo "¿a qué hora es la visita de mañana?" o "¿dónde ceno cerca del hotel?", siempre con los datos de su viaje. Puede buscar en internet y en Viator.
- **Números sin viaje:** resuelve dudas generales sobre Exploryaa e invita a pedir el viaje en la web. Nunca da datos de ningún viaje.
- **Te avisa por WhatsApp** cuando el cliente pide cambios, cancelaciones o reembolsos, tiene una queja o un problema con una reserva, o quiere hablar con una persona.
- **Emergencias:** primero le dice que llame al 112 o al número local, y a ti te llega un aviso 🚨 URGENTE.
- **Se presenta como IA** en el primer mensaje, como exige la ley europea.
- **No contesta dos veces** al mismo mensaje y guarda toda la conversación.

## Tus comandos
Los escribes desde tu WhatsApp personal al número de Exploryaa:

| Comando | Qué hace |
|---|---|
| `#r 34600111222 Hola Laura…` | Responde al cliente en tu nombre y pausa el asistente con él |
| `#bot 34600111222 on` / `off` | Reactiva o pausa el asistente con ese cliente |
| `#inc` | Lista las incidencias abiertas |
| `#cerrar 12` | Cierra la incidencia 12 |
| `#ayuda` | Muestra la lista de comandos |

Mientras el asistente está en pausa con un cliente, cada mensaje de ese cliente te llega a ti.

## Puesta en marcha

### 1. Crear el número en Meta (gratis para empezar)
1. Entra en developers.facebook.com, crea una app de tipo **Empresa** y añade el producto **WhatsApp**.
2. En **WhatsApp → Configuración de la API** copia el **token de acceso** y el **Phone number ID**. Para producción, crea un token permanente con un "usuario del sistema" en el Business Manager.
3. Añade tu número de empresa. Mientras pruebas puedes usar el número de prueba que da Meta.
4. En **Configuración de la app → Básica** copia la **clave secreta de la app**.

### 2. Configurar el `.env`
Rellena el bloque de WhatsApp de `.env.example`: `WA_TOKEN`, `WA_PHONE_NUMBER_ID`, `WA_APP_SECRET`, una palabra secreta inventada en `WA_VERIFY_TOKEN`, tu número en `ASESORA_WHATSAPP` (por ejemplo `34600111222`) y tu nombre en `ASESORA_NOMBRE`. También hace falta `ANTHROPIC_API_KEY`.

### 3. Arrancar el servidor
```bash
pip install -r requirements.txt
python -m whatsapp.servidor          # para probar en tu ordenador (puerto 8000)
```
Meta necesita una dirección pública con HTTPS:
- **Para probar:** ejecuta `ngrok http 8000` y usa la URL que te da.
- **Para producción:** publícalo en Render o Railway con el comando de inicio `gunicorn -w 2 -b 0.0.0.0:$PORT whatsapp.servidor:app`. En ese caso usa un disco persistente para `whatsapp.db`.

### 4. Conectar el webhook en Meta
En **WhatsApp → Configuración → Webhook**:
- **URL de devolución de llamada:** `https://TU-DIRECCION/webhook`
- **Token de verificación:** el mismo que pusiste en `WA_VERIFY_TOKEN`
- Suscríbete al campo **messages**.

### 5. Dar de alta el viaje de cada cliente
Cuando el cliente acepte su propuesta y tengas las reservas hechas:
```bash
python cargar_viaje.py --telefono 34600111222 --nombre "Laura Pérez" \
  --paquete "Viaje Completo" --destino "Roma" --ida 2027-03-12 --vuelta 2027-03-15 \
  --itinerario dossier_laura.md
```
Cuanto más completo sea el dossier (códigos de reserva, horarios, direcciones, teléfonos del hotel), mejor responderá. Más adelante lo haremos automático desde la web.

## A tener en cuenta
- **Ventana de 24 horas de WhatsApp:** solo puedes escribir texto libre a un cliente durante las 24 horas siguientes a su último mensaje. Para escribirle tú primero, por ejemplo con "tu viaje empieza mañana", hacen falta plantillas aprobadas por Meta. Eso sería el siguiente paso.
- **Coste:** Meta cobra por conversación según el país y el tipo de mensaje, y responder dentro de una conversación que inicia el cliente suele ser lo más barato. Consulta la tarifa actual en Meta. Claude cobra por uso.
- **Versión de la API:** `WA_GRAPH_VERSION` va con `v23.0` por defecto. Si Meta la retira, cámbiala por la versión actual.
- **Formato:** por ahora solo lee texto, botones y ubicaciones. A los audios y fotos responde pidiendo que lo escriban.
- **Privacidad:** el asistente nunca pide datos de tarjeta ni documentos. Añade WhatsApp a tu política de privacidad como canal de atención.
