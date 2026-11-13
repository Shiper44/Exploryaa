import copy
import tomllib

import pytest

from app import precios
from app.ajustes import ajustes


def datos_validos():
    with open(ajustes.archivo_precios, "rb") as f:
        return tomllib.load(f)


def test_el_archivo_real_es_valido():
    p = precios.cargar()
    assert set(p["planificacion"]["niveles"]) == {"simple", "estandar", "premium"}
    assert set(p["paquetes"]) == {"mini", "express", "completo", "premium"}
    assert p["planificacion"]["dias_incluidos"] >= 1


def test_publicos_no_muestra_honorarios():
    pub = precios.publicos()
    for paquete in pub["paquetes"].values():
        assert "honorarios" not in paquete
        assert "desde" in paquete


@pytest.mark.parametrize("ruta, valor, mensaje", [
    (("paquetes", "mini", "desde"), "199 €", "debe ser un número"),
    (("paquetes", "mini", "desde"), -5, "no puede ser negativo"),
    (("planificacion", "niveles", "simple", "por_dia_extra"), None, "debe ser un número"),
    (("planificacion", "por_destino_extra"), True, "debe ser un número"),
])
def test_errores_claros(ruta, valor, mensaje):
    d = copy.deepcopy(datos_validos())
    obj = d
    for k in ruta[:-1]:
        obj = obj[k]
    obj[ruta[-1]] = valor
    with pytest.raises(precios.ErrorPrecios, match=mensaje):
        precios.validar(d)


def test_falta_un_paquete():
    d = copy.deepcopy(datos_validos())
    del d["paquetes"]["express"]
    with pytest.raises(precios.ErrorPrecios, match="express"):
        precios.validar(d)


def test_revisiones_ilimitadas_se_permiten_en_paquetes():
    d = copy.deepcopy(datos_validos())
    d["paquetes"]["premium"]["revisiones"] = -1
    assert precios.validar(d)["paquetes"]["premium"]["revisiones"] == -1


def test_toml_mal_escrito(tmp_path):
    f = tmp_path / "precios.toml"
    f.write_text("[paquetes\nmini = ", encoding="utf-8")
    with pytest.raises(precios.ErrorPrecios, match="error de formato"):
        precios.cargar(f)
