# Servidor de Exploryaa

Servidor en Python (FastAPI). Sirve la web de la carpeta `web/` y la API en `/api/...`. La guía completa de instalación y publicación llegará en la fase 8; esto es lo básico para probarlo en tu ordenador.

## Probar en local

```bash
cd servidor
python3 -m venv .venv
source .venv/bin/activate          # en Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Abre <http://localhost:8000>.

## Cambiar los precios

Todos los precios están en **`config/precios.toml`**: los «desde» de la planificación y de los paquetes, el extra por día y por destino, y tus honorarios.

1. Cambia los números y guarda el archivo.
2. Reinicia el servidor.

Si hay un error en el archivo (por ejemplo, `29 €` en lugar de `29`), el servidor no arranca y te dice qué línea corregir. Los honorarios nunca se muestran en la web.

## Tests

```bash
cd servidor
pytest
```

## Estructura

```
config/precios.toml      ← precios (el único sitio donde se cambian)
servidor/app/main.py     ← rutas: páginas y API
servidor/app/precios.py  ← lectura y validación de precios
servidor/app/ajustes.py  ← ajustes desde .env
servidor/tests/          ← pruebas automáticas
web/                     ← la web (portada, /gracias, /mis-viajes, legales)
```
