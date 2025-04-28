import mysql.connector
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

def conectar_mysql():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# --- Nueva función para el simulador ---
def obtener_ultimos_datos(limite=5000):
    conexion = conectar_mysql()
    cursor = conexion.cursor(dictionary=True)

    tabla = "ohlcv"

    query = f"""
    SELECT timestamp, open, high, low, close, volume
    FROM {tabla}
    ORDER BY timestamp ASC
    LIMIT {limite}
    """
    cursor.execute(query)
    resultados = cursor.fetchall()

    df = pd.DataFrame(resultados)
    # df = df.sort_values('timestamp')  # Muy importante: de más antiguo a más reciente
    df.reset_index(drop=True, inplace=True)
    
    if not df['timestamp'].is_monotonic_increasing:
        raise ValueError("[Error] Los datos no están en orden temporal ascendente. Verifica la carga.")

    cursor.close()
    conexion.close()

    return df
