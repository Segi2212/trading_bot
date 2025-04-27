import numpy as np
import pickle
import mysql.connector
from sklearn.preprocessing import MinMaxScaler
from dotenv import load_dotenv
import os

load_dotenv()

# Conexión MySQL
conexion = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = conexion.cursor()
cursor.execute("""
    SELECT open, high, low, close FROM ohlcv
    WHERE symbol = %s AND timeframe = %s
    ORDER BY timestamp ASC
""", (os.getenv("BITSO_SYMBOL"), os.getenv("TIMEFRAME")))

datos = cursor.fetchall()
cursor.close()
conexion.close()

datos_np = np.array(datos)

if datos_np.size == 0:
    raise ValueError("❌ No se encontraron datos en la tabla OHLCV para el símbolo y timeframe especificados.")

scaler = MinMaxScaler()
datos_normalizados = scaler.fit_transform(datos_np)

# Guardar el scaler
with open("modelo/scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

# Generar X e y
ventana = 46
X, y = [], []

for i in range(len(datos_normalizados) - ventana - 1):
    secuencia = datos_normalizados[i:i+ventana]
    siguiente_cierre = datos_normalizados[i+ventana][3]
    cierre_actual = datos_normalizados[i+ventana-1][3]
    etiqueta = 1 if siguiente_cierre > cierre_actual else 0

    X.append(secuencia)
    y.append(etiqueta)

X = np.array(X)
y = np.array(y)

# Guardar
np.save("modelo/X.npy", X)
np.save("modelo/y.npy", y)

print("✅ Datos preparados y guardados.")
