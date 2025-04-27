import ccxt
from config import API_KEY, API_SECRET, BITSO_SYMBOL, TIMEFRAME, N_MINUTOS_HISTORIA
import numpy as np

def conectar_bitso():
    return ccxt.bitso({
        'apiKey': API_KEY,
        'secret': API_SECRET
    })

def obtener_ohlcv(exchange):
    ohlcv = exchange.fetch_ohlcv(
        symbol=BITSO_SYMBOL,
        timeframe=TIMEFRAME,
        limit=N_MINUTOS_HISTORIA
    )
    return ohlcv  # [timestamp, open, high, low, close, volume]

# 🔵 NUEVA función para pruebas
def obtener_ohlcv_test(bitso, timeframe="1m", limit=46):
    """
    Obtiene datos OHLCV para pruebas de simulación, con el shape adecuado para el modelo.
    """
    try:
        ohlcv = bitso.fetch_ohlcv("BTC/MXN", timeframe=timeframe, limit=limit)
        datos = [list(candle[1:5]) for candle in ohlcv]  # Solo Open, High, Low, Close
        datos_np = np.array(datos)

        # 🔵 Muy importante: ajustar forma (1, 46, 4)
        datos_np = datos_np.reshape((1, datos_np.shape[0], datos_np.shape[1]))

        return datos_np

    except Exception as e:
        raise Exception(f"Error al obtener datos de prueba: {e}")