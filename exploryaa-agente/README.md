# Agente Exploryaa: consulta de precios

Agente de IA que recibe la solicitud de un cliente (origen, destino, fechas, viajeros,
presupuesto máximo y gustos), consulta precios reales y propone hasta 3 paquetes
de **vuelo + alojamiento + experiencias** sin pasar del presupuesto. Solo consulta precios: no reserva ni cobra.

| Parte | Fuente | Qué hace |
|---|---|---|
| Cerebro | Claude (Anthropic) | Decide qué buscar, ajusta si no cabe y redacta la propuesta |
| Vuelos | Duffel | Solo ida o ida y vuelta, precio total para todos los pasajeros |
| Alojamiento | LiteAPI | Hoteles de la ciudad con el precio total de la estancia |
| Experiencias | Viator | Tours y actividades con precio por persona y enlace |
| Presupuesto | `armar_paquetes` | Combina todo y devuelve: Más económico / Mejor equilibrio / Más cómodo |

Si falta una clave, esa parte funciona en **modo prueba** con datos de ejemplo. Así puedes probarlo todo desde el primer día.

## Paso 1: crear las cuentas
1. **Claude**: console.anthropic.com → API Keys. Es la única obligatoria.
2. **Duffel**: app.duffel.com/join → Developers → Access tokens (modo test).
3. **LiteAPI**: liteapi.travel → crea la cuenta y copia la clave de sandbox (`sand_...`).
4. **Viator**: partnerresources.viator.com → regístrate como afiliado y copia tu API key.

## Paso 2: instalar (una sola vez)
Necesitas Python 3.10 o superior.
```bash
cd exploryaa-agente
pip install -r requirements.txt
cp .env.example .env      # en Windows: copy .env.example .env
```
Abre `.env` y pega tus claves.

## Paso 3: probar
```bash
python main.py
```
Usa `ejemplo_solicitud.json` (Barcelona → Roma, 2 personas, 900 €) y guarda la respuesta en `propuesta.md`.
Para otra solicitud, copia ese JSON, cámbialo y ejecuta `python main.py mi_solicitud.json`.

## Estructura
```
agente.py                 instrucciones del agente, herramientas y bucle con Claude
main.py                   ejecutar desde la terminal
config.py                 lee el .env
herramientas/vuelos.py         Duffel
herramientas/alojamientos.py   LiteAPI
herramientas/experiencias.py   Viator
herramientas/presupuesto.py    combina dentro del presupuesto
```

## Ajustes útiles
- **Cómo se reparte el presupuesto**: el agente puede pasar `reparto`, por ejemplo `{"vuelos":0.5,"alojamiento":0.35,"experiencias":0.15}`. Si no lo pasa, usa el presupuesto completo.
- **Qué es un buen paquete**: cambia `_puntuacion()` en `presupuesto.py`. Ahora mismo premia las estrellas, la nota del hotel, las experiencias bien valoradas y los vuelos directos.
- **Tono y formato de la propuesta**: edita `INSTRUCCIONES` en `agente.py`.

## A tener en cuenta
- **Coste de Duffel**: buscar es gratis hasta 1.500 búsquedas por cada reserva. Si casi nunca reservas a través de Duffel, podrías pagar 0,005 $ por cada búsqueda extra. Confírmalo con ellos.
- **Viator con acceso básico**: da precios y enlaces, y el cliente reserva en viator.com.
- **Webs sin API** (Google Flights, Booking, Airbnb, Kayak…): no se consultan de forma automática porque sus condiciones lo prohíben y lo bloquean. Úsalas manualmente o mediante sus programas de afiliados.
- **Precios**: son orientativos y pueden cambiar hasta que se reserva.

## Próximos pasos
1. Conectar el formulario de la web, que llamaría a `Agente().planificar(solicitud)`.
2. Enviar `propuesta.md` por correo al cliente.
3. Añadir más fuentes, como GetYourGuide y Klook cuando te aprueben como partner.
