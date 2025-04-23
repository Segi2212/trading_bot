import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def conectar_db():
    """
    Crea la base de datos y la tabla OHLCV si no existen.
    Devuelve una conexión activa al schema.
    """
    config = {
        'host': os.getenv("DB_HOST"),
        'port': int(os.getenv("DB_PORT")),
        'user': os.getenv("DB_USER"),
        'password': os.getenv("DB_PASSWORD"),
    }

    # Conexión inicial para crear la base de datos
    conexion = mysql.connector.connect(**config)
    cursor = conexion.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv('DB_NAME')}")
    cursor.close()
    conexion.close()

    # Conexión al schema
    config['database'] = os.getenv("DB_NAME")
    conexion = mysql.connector.connect(**config)

    # Crear tabla si no existe
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ohlcv (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            timestamp BIGINT NOT NULL,
            symbol VARCHAR(20),
            timeframe VARCHAR(10),
            open DOUBLE,
            high DOUBLE,
            low DOUBLE,
            close DOUBLE,
            volume DOUBLE,
            UNIQUE(symbol, timeframe, timestamp)
        )
    """)
    conexion.commit()
    cursor.close()
    
    return conexion
