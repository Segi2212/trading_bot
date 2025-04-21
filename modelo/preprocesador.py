import numpy as np
import pandas as pd

def calcular_rsi(serie, ventana=14):
    delta = serie.diff()
    ganancia = delta.clip(lower=0).rolling(window=ventana).mean()
    perdida = -delta.clip(upper=0).rolling(window=ventana).mean()
    rs = ganancia / perdida
    rsi = 100 - (100 / (1 + rs))
    return rsi

def preparar_input_lstm(ohlcv):
    """
    Convierte los datos OHLCV en un array normalizado y formateado para el modelo LSTM.
    """
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    
    # Indicadores técnicos
    df['ema_9'] = df['close'].ewm(span=9).mean()
    df['rsi'] = calcular_rsi(df['close'])

    # Eliminar filas con NaN
    df = df.dropna().reset_index(drop=True)

    # Features a usar
    features = df[['close', 'ema_9', 'rsi', 'volume']].values

    # Normalización z-score
    mean = features.mean(axis=0)
    std = features.std(axis=0)
    features_norm = (features - mean) / std

    # Tomar últimos 60 pasos
    secuencia = features_norm[-60:]

    return np.expand_dims(secuencia, axis=0)  # shape: (1, 60, 4)