"""Servidor de Exploryaa: sirve la web (carpeta web/) y la API (/api/...).

Arranque en local, desde la carpeta servidor/:
    uvicorn app.main:app --reload
"""
from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from . import precios as mod_precios
from .ajustes import ajustes

WEB = ajustes.carpeta_web

# Si precios.toml tiene un error, el servidor no arranca y dice cuál es.
mod_precios.precios()

app = FastAPI(
    title="Exploryaa",
    docs_url=None if ajustes.produccion else "/api/docs",
    redoc_url=None,
    openapi_url=None if ajustes.produccion else "/api/openapi.json",
)

if ajustes.origenes_permitidos:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ajustes.origenes_permitidos,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type"],
        allow_credentials=True,
    )

PRIVADAS = ("/mis-viajes", "/api", "/admin", "/gracias")


@app.middleware("http")
async def cabeceras_seguridad(request: Request, call_next):
    respuesta = await call_next(request)
    h = respuesta.headers
    h.setdefault("X-Content-Type-Options", "nosniff")
    h.setdefault("X-Frame-Options", "DENY")
    h.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    h.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
    if ajustes.produccion:
        h.setdefault("Strict-Transport-Security", "max-age=31536000")
    ruta = request.url.path
    if ruta.startswith(PRIVADAS):
        h["X-Robots-Tag"] = "noindex, nofollow"
    if ruta.startswith("/api"):
        h.setdefault("Cache-Control", "no-store")
    elif respuesta.headers.get("content-type", "").startswith("text/html"):
        h.setdefault("Cache-Control", "no-cache")
    return respuesta


# ------------------------------- API -------------------------------
@app.get("/api/salud")
def salud():
    return {"ok": True, "servicio": "Exploryaa"}


@app.get("/api/precios")
def ver_precios():
    """Precios «desde» para la web (sin honorarios internos)."""
    return mod_precios.publicos()


# ------------------------------ Páginas -----------------------------
def _pagina(nombre: str) -> FileResponse:
    return FileResponse(WEB / nombre, media_type="text/html")


@app.get("/", include_in_schema=False)
def inicio():
    return _pagina("index.html")


@app.get("/gracias", include_in_schema=False)
def gracias():
    return _pagina("gracias.html")


@app.get("/mis-viajes", include_in_schema=False)
def mis_viajes():
    return _pagina("mis-viajes.html")


@app.exception_handler(StarletteHTTPException)
async def no_encontrado(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404 and not request.url.path.startswith("/api"):
        return FileResponse(WEB / "404.html", status_code=404, media_type="text/html")
    return JSONResponse({"ok": False, "error": exc.detail}, status_code=exc.status_code)


# Resto de archivos de la web (imágenes, páginas legales, robots.txt…)
app.mount("/", StaticFiles(directory=WEB), name="web")
