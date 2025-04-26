import ccxt
import time
from datetime import datetime, timedelta
from db.conexion import conectar_db
from tqdm import tqdm


import os
from dotenv import load_dotenv
load_dotenv()

EXCHANGE = ccxt.bitso()
SYMBOL = os.getenv("BITSO_SYMBOL")
TIMEFRAME = '1m'
LIMIT = 1000  # Bitso permite hasta 1000 por llamada

def guardar_en_db(conexion, ohlcv):
    cursor = conexion.cursor()
    query = """
        INSERT IGNORE INTO ohlcv (timestamp, symbol, timeframe, open, high, low, close, volume)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    datos = [(ts, SYMBOL, TIMEFRAME, o, h, l, c, v) for ts, o, h, l, c, v in ohlcv]
    cursor.executemany(query, datos)
    conexion.commit()
    cursor.close()

def descargar_datos(conexion, desde_ts, hasta_ts):
    total_minutos = (hasta_ts - desde_ts) // 60_000
    total_lotes = total_minutos // LIMIT + 1

    ts_actual = desde_ts

    with tqdm(total=total_lotes, desc="Descargando datos") as barra:
        while ts_actual < hasta_ts:
            try:
                ohlcv = EXCHANGE.fetch_ohlcv(SYMBOL, TIMEFRAME, since=ts_actual, limit=LIMIT)
                if not ohlcv:
                    break

                guardar_en_db(conexion, ohlcv)
                ts_actual = ohlcv[-1][0] + 60_000
                barra.update(1)
                time.sleep(EXCHANGE.rateLimit / 1000)
            except Exception as e:
                print("Error:", e)
                time.sleep(5)

def iniciar_descarga():
    conexion = conectar_db()

    # Rango de fechas
    hasta = int(EXCHANGE.milliseconds())
    dos_anios = 2 * 365 * 24 * 60 * 60 * 1000
    desde = hasta - dos_anios

    descargar_datos(conexion, desde, hasta)
    conexion.close()

def obtener_ultimo_timestamp(conexion):
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT MAX(timestamp) FROM ohlcv
        WHERE symbol = %s AND timeframe = %s
    """, (SYMBOL, TIMEFRAME))
    resultado = cursor.fetchone()[0]
    cursor.close()
    return resultado if resultado else None

def actualizar_datos():
    conexion = conectar_db()

    # Obtenemos el último timestamp y actual
    desde_ts = obtener_ultimo_timestamp(conexion)
    if not desde_ts:
        print("No hay datos en la base. Ejecuta una descarga completa primero.")
        return

    desde_ts += 60_000  # siguiente minuto
    hasta_ts = int(EXCHANGE.milliseconds())

    print(f"Actualizando desde {datetime.utcfromtimestamp(desde_ts / 1000)} hasta ahora...")

    descargar_datos(conexion, desde_ts, hasta_ts)
    conexion.close()
