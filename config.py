from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("BITSO_API_KEY")
API_SECRET = os.getenv("BITSO_API_SECRET")
BITSO_SYMBOL = os.getenv("BITSO_SYMBOL")
TIMEFRAME = os.getenv("TIMEFRAME", "1m")
N_MINUTOS_HISTORIA = int(os.getenv("N_MINUTOS_HISTORIA", 60))
UMBRAL_CONFIDENCIA = float(os.getenv("UMBRAL_CONFIDENCIA", 0.6))
MONTO_POR_OPERACION = float(os.getenv("MONTO_POR_OPERACION", 500))

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
