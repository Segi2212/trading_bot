# data/preparar_dataset_entrenamiento.py

import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator
from data.recolector import conectar_bitso, obtener_ohlcv
import os

def preparar_dataset_entrenamiento():
    print("[Dataset] Conectando a Bitso...")
    bitso = conectar_bitso()

    print("[Dataset] Descargando datos OHLCV...")
    ohlcv = obtener_ohlcv(bitso)
    columnas = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    df = pd.DataFrame(ohlcv, columns=columnas)

    print("[Dataset] Calculando indicadores técnicos...")
    df['rsi'] = RSIIndicator(close=df['close'], window=14).rsi()
    df['ema_10'] = EMAIndicator(close=df['close'], window=10).ema_indicator()
    df['ema_50'] = EMAIndicator(close=df['close'], window=50).ema_indicator()
    df['ema_100'] = EMAIndicator(close=df['close'], window=100).ema_indicator()

    # Eliminar filas NaN que surgen al calcular EMAs y RSI
    df.dropna(inplace=True)

    print("[Dataset] Calculando etiquetas (sube, baja, neutro)...")
    df['future_close'] = df['close'].shift(-5)  # Cierre en 5 minutos
    df['diff'] = df['future_close'] - df['close']

    # Clasificación múltiple: 0 = baja, 1 = neutro, 2 = sube
    def etiquetar(dif):
        if dif > 0.5:  # Umbral de subida
            return 2
        elif dif < -0.5:  # Umbral de bajada
            return 0
        else:
            return 1

    df['label'] = df['diff'].apply(etiquetar)

    # Eliminar columnas que no necesitamos
    df_final = df[['open', 'high', 'low', 'close', 'volume', 'rsi', 'ema_10', 'ema_50', 'ema_100', 'label']]

    # También eliminar las últimas filas que no tienen futuro_close
    df_final.dropna(inplace=True)

    # Crear carpeta si no existe
    os.makedirs("data", exist_ok=True)

    # Guardar dataset
    df_final.to_csv("data/dataset_entrenamiento.csv", index=False)
    print("[Dataset] ✅ Dataset de entrenamiento guardado en data/dataset_entrenamiento.csv.")
