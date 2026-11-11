"""Configuración: lee las claves del archivo .env."""
import os

from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "").strip()
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-5-5").strip()
DUFFEL_TOKEN = os.getenv("DUFFEL_TOKEN", "").strip()
LITEAPI_KEY = os.getenv("LITEAPI_KEY", "").strip()
VIATOR_API_KEY = os.getenv("VIATOR_API_KEY", "").strip()
MONEDA = os.getenv("MONEDA", "EUR").strip()
NACIONALIDAD = os.getenv("NACIONALIDAD", "ES").strip()
MODO_PRUEBA = os.getenv("MODO_PRUEBA", "0").strip() == "1"

TIMEOUT = 60  # segundos por llamada a cada API

# --- WhatsApp (Meta WhatsApp Cloud API) ---
WA_TOKEN = os.getenv("WA_TOKEN", "").strip()                 # token de acceso de Meta
WA_PHONE_NUMBER_ID = os.getenv("WA_PHONE_NUMBER_ID", "").strip()
WA_VERIFY_TOKEN = os.getenv("WA_VERIFY_TOKEN", "").strip()   # palabra secreta que tú eliges
WA_APP_SECRET = os.getenv("WA_APP_SECRET", "").strip()       # para comprobar que el aviso viene de Meta
WA_GRAPH_VERSION = os.getenv("WA_GRAPH_VERSION", "v23.0").strip()
ASESORA_WHATSAPP = os.getenv("ASESORA_WHATSAPP", "").strip()  # tu número, solo dígitos: 34600111222
ASESORA_NOMBRE = os.getenv("ASESORA_NOMBRE", "tu asesora de Exploryaa").strip()
WA_DB = os.getenv("WA_DB", "whatsapp.db").strip()
WA_BUSQUEDA_WEB = os.getenv("WA_BUSQUEDA_WEB", "1").strip() == "1"


def usar_prueba(clave: str) -> bool:
    """True si esa herramienta debe devolver datos de ejemplo."""
    return MODO_PRUEBA or not clave
