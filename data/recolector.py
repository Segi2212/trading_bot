import ccxt
from config import API_KEY, API_SECRET, BITSO_SYMBOL, TIMEFRAME, N_MINUTOS_HISTORIA

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
