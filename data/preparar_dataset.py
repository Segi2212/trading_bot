import pandas as pd
import numpy as np
import os
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator
from sklearn.preprocessing import MinMaxScaler
from data.mysql_conexion import obtener_ultimos_datos

# Configuraciones
SECUENCIA_LONGITUD = 46
UMBRAL_CAMBIO = 0.0015  # 0.15%
PASOS_ADELANTE = 3  # velas hacia el futuro para definir clase

# Crear carpeta de salida
os.makedirs("dataset", exist_ok=True)

print("[Dataset] Cargando datos...")
df = obtener_ultimos_datos(limite=10000)  # Puedes ajustar cuántas velas cargar

# Crear indicadores
print("[Dataset] Calculando indicadores técnicos...")
df['rsi'] = RSIIndicator(close=df['close'], window=14).rsi()
df['ema8'] = EMAIndicator(close=df['close'], window=8).ema_indicator()
df['ema21'] = EMAIndicator(close=df['close'], window=21).ema_indicator()
df['ema50'] = EMAIndicator(close=df['close'], window=50).ema_indicator()
df['momentum'] = df['close'] - df['close'].shift(3)

# Borrar filas con NaN
df.dropna(inplace=True)
df.reset_index(drop=True, inplace=True)

# Generar etiquetas (0: baja, 1: neutro, 2: sube)
print("[Dataset] Generando etiquetas...")
cambios = (df['close'].shift(-PASOS_ADELANTE) - df['close']) / df['close']

def etiquetar(cambio):
    if cambio < -UMBRAL_CAMBIO:
        return 0  # baja
    elif cambio > UMBRAL_CAMBIO:
        return 2  # sube
    else:
        return 1  # neutro

df['label'] = cambios.apply(etiquetar)

# Borrar las últimas filas que no tienen futuro conocido
df = df[:-PASOS_ADELANTE]

# Escalar features
features = ['open', 'high', 'low', 'close', 'volume', 'rsi', 'ema8', 'ema21', 'ema50', 'momentum']
scaler = MinMaxScaler()
df[features] = scaler.fit_transform(df[features])

# Preparar X (secuencias) y y (etiquetas)
print("[Dataset] Creando secuencias...")
X, y = [], []

for i in range(SECUENCIA_LONGITUD, len(df)):
    X.append(df[features].iloc[i-SECUENCIA_LONGITUD:i].values)
    y.append(df['label'].iloc[i])

X = np.array(X)
y = np.array(y)

print(f"[Dataset] Dataset creado: X shape {X.shape}, y shape {y.shape}")

# Guardar
np.save('dataset/X.npy', X)
np.save('dataset/y.npy', y)

print("[Dataset] ✅ Dataset guardado en carpeta 'dataset/'")

def preparar_dataset():
    pass