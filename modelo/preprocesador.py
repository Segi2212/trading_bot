# preprocesador.py
import numpy as np
import pandas as pd

def calcular_rsi(serie, ventana=14):
    delta = serie.diff()
    ganancia = delta.clip(lower=0).rolling(window=ventana).mean()
    perdida = -delta.clip(upper=0).rolling(window=ventana).mean()
    rs = ganancia / perdida
    rsi = 100 - (100 / (1 + rs))
    return rsi

def preprocesar_para_prediccion(ohlcv, mean, std):
    """
    Prepara datos OHLCV para predecir con modelo LSTM que espera (None, 46, 10)
    """
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

    # Indicadores técnicos
    df['ema_9'] = df['close'].ewm(span=9).mean()
    df['rsi'] = calcular_rsi(df['close'])
    df['returns'] = df['close'].pct_change().fillna(0)
    df['log_volume'] = np.log1p(df['volume'])

    # Otros features adicionales (ficticios pero comunes)
    df['high_low'] = df['high'] - df['low']
    df['open_close'] = df['open'] - df['close']
    df['volatility'] = df['returns'].rolling(window=5).std().fillna(0)
    df['momentum'] = df['close'] - df['close'].shift(5)
    df['momentum'] = df['momentum'].fillna(0)

    # Eliminar filas con NaN
    df = df.dropna().reset_index(drop=True)

    # Selección de features
    features = df[['open', 'high', 'low', 'close', 'volume',
                   'ema_9', 'rsi', 'returns', 'log_volume',
                   'volatility']].values

    # Normalización
    features_norm = (features - mean) / std

    # Tomar últimos 46 pasos
    secuencia = features_norm[-46:]

    return np.expand_dims(secuencia, axis=0)  # shape: (1, 46, 10)
