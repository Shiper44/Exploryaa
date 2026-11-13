from fastapi.testclient import TestClient

from app.main import app

cliente = TestClient(app)


def test_salud():
    r = cliente.get("/api/salud")
    assert r.status_code == 200 and r.json()["ok"] is True


def test_precios_api_coincide_con_el_archivo():
    from app import precios
    r = cliente.get("/api/precios")
    assert r.status_code == 200
    d = r.json()
    assert d["paquetes"]["completo"]["desde"] == precios.precios()["paquetes"]["completo"]["desde"]
    assert d["planificacion"]["niveles"]["estandar"]["desde"] == precios.precios()["planificacion"]["niveles"]["estandar"]["desde"]
    assert r.headers["cache-control"] == "no-store"


def test_portada():
    r = cliente.get("/")
    assert r.status_code == 200
    html = r.text
    for texto in ('id="planificacion"', 'id="paquetes"', 'href="/mis-viajes"', "¿Por qué el precio es «desde»?", "¿Cuándo pago?", "[testimonio real]"):
        assert texto in html, texto
    assert "X-Robots-Tag" not in r.headers  # la portada sí se indexa


def test_paginas_privadas_no_se_indexan():
    for ruta in ("/gracias", "/mis-viajes"):
        r = cliente.get(ruta)
        assert r.status_code == 200
        assert "noindex" in r.headers["x-robots-tag"]
        assert 'name="robots" content="noindex' in r.text


def test_archivos_estaticos_y_legales():
    for ruta in ("/logo.png", "/robots.txt", "/sitemap.xml", "/legal/privacidad.html", "/legal/legal.css"):
        assert cliente.get(ruta).status_code == 200, ruta


def test_404_bonita():
    r = cliente.get("/no-existe")
    assert r.status_code == 404
    assert "no existe" in r.text.lower()
    r = cliente.get("/api/no-existe")
    assert r.status_code == 404 and r.json()["ok"] is False


def test_cabeceras_de_seguridad():
    r = cliente.get("/")
    assert r.headers["x-content-type-options"] == "nosniff"
    assert r.headers["x-frame-options"] == "DENY"


def test_no_se_sale_de_la_carpeta_web():
    r = cliente.get("/../servidor/.env.example")
    assert r.status_code == 404
    r = cliente.get("/%2e%2e/config/precios.toml")
    assert r.status_code == 404
