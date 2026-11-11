"""Base de datos SQLite: viajes de los clientes, conversación y avisos a la asesora."""
import sqlite3
import threading
from datetime import datetime

import config

_lock = threading.Lock()


def _con():
    con = sqlite3.connect(config.WA_DB, check_same_thread=False)
    con.row_factory = sqlite3.Row
    return con


def iniciar():
    with _lock, _con() as con:
        con.executescript("""
        CREATE TABLE IF NOT EXISTS viajes (
            telefono TEXT PRIMARY KEY,          -- solo dígitos, con prefijo: 34600111222
            nombre TEXT, paquete TEXT, destino TEXT,
            fecha_ida TEXT, fecha_vuelta TEXT,
            itinerario TEXT,                    -- propuesta / dossier en texto
            bot_activo INTEGER DEFAULT 1,       -- 0 = la asesora lleva la conversación
            creado TEXT
        );
        CREATE TABLE IF NOT EXISTS mensajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telefono TEXT, rol TEXT, texto TEXT, fecha TEXT
        );
        CREATE TABLE IF NOT EXISTS procesados (wa_id TEXT PRIMARY KEY);
        CREATE TABLE IF NOT EXISTS incidencias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telefono TEXT, motivo TEXT, urgencia TEXT, estado TEXT DEFAULT 'abierta', fecha TEXT
        );
        """)


def ahora():
    return datetime.now().isoformat(timespec="seconds")


def ya_procesado(wa_id: str) -> bool:
    """Meta a veces reenvía el mismo mensaje: así no contestamos dos veces."""
    with _lock, _con() as con:
        try:
            con.execute("INSERT INTO procesados (wa_id) VALUES (?)", (wa_id,))
            return False
        except sqlite3.IntegrityError:
            return True


def guardar_viaje(telefono, nombre, paquete, destino, fecha_ida, fecha_vuelta, itinerario):
    with _lock, _con() as con:
        con.execute("""INSERT INTO viajes VALUES (?,?,?,?,?,?,?,1,?)
            ON CONFLICT(telefono) DO UPDATE SET nombre=excluded.nombre, paquete=excluded.paquete,
            destino=excluded.destino, fecha_ida=excluded.fecha_ida, fecha_vuelta=excluded.fecha_vuelta,
            itinerario=excluded.itinerario""",
                    (telefono, nombre, paquete, destino, fecha_ida, fecha_vuelta, itinerario, ahora()))


def viaje(telefono):
    with _lock, _con() as con:
        fila = con.execute("SELECT * FROM viajes WHERE telefono=?", (telefono,)).fetchone()
        return dict(fila) if fila else None


def activar_bot(telefono, activo: bool):
    with _lock, _con() as con:
        con.execute("UPDATE viajes SET bot_activo=? WHERE telefono=?", (1 if activo else 0, telefono))


def guardar_mensaje(telefono, rol, texto):
    with _lock, _con() as con:
        con.execute("INSERT INTO mensajes (telefono, rol, texto, fecha) VALUES (?,?,?,?)",
                    (telefono, rol, texto, ahora()))


def historial(telefono, limite=20):
    """Últimos mensajes en formato de la API de Claude (user / assistant)."""
    with _lock, _con() as con:
        filas = con.execute("""SELECT rol, texto FROM mensajes WHERE telefono=?
                               ORDER BY id DESC LIMIT ?""", (telefono, limite)).fetchall()
    mensajes = []
    for f in reversed(filas):
        rol = "assistant" if f["rol"] in ("asistente", "asesora") else "user"
        texto = f["texto"] if f["rol"] != "asesora" else f"[Mensaje de la asesora] {f['texto']}"
        if mensajes and mensajes[-1]["role"] == rol:
            mensajes[-1]["content"] += "\n" + texto
        else:
            mensajes.append({"role": rol, "content": texto})
    while mensajes and mensajes[0]["role"] != "user":
        mensajes.pop(0)
    return mensajes


def abrir_incidencia(telefono, motivo, urgencia):
    with _lock, _con() as con:
        cur = con.execute("INSERT INTO incidencias (telefono, motivo, urgencia, fecha) VALUES (?,?,?,?)",
                          (telefono, motivo, urgencia, ahora()))
        return cur.lastrowid


def incidencias_abiertas():
    with _lock, _con() as con:
        return [dict(f) for f in con.execute(
            "SELECT * FROM incidencias WHERE estado='abierta' ORDER BY id").fetchall()]


def cerrar_incidencia(numero):
    with _lock, _con() as con:
        return con.execute("UPDATE incidencias SET estado='cerrada' WHERE id=?", (numero,)).rowcount
