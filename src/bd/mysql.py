# mysql.py

import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def conectar_db(bd=None):
    '''
    Establece una conexión con el servidor MySQL usando las variables de entorno.

    Args:
        bd (str, opcional): Nombre de la base de datos a la que conectar. Si es None, no se selecciona ninguna.

    Returns:
        mysql.connector.connection_cext.CMySQLConnection: Objeto de conexión activo.
    '''
    config = {
        'host': os.getenv("DB_HOST"),
        'port': int(os.getenv("DB_PORT")),
        'user': os.getenv("DB_USER"),
        'password': os.getenv("DB_PASSWORD")
    }

    if bd is not None:
        config['database'] = bd

    conexion = mysql.connector.connect(**config)
    return conexion


def crear_bd(bd=os.getenv('DB_NAME')):
    '''
    Crea una base de datos en el servidor MySQL si no existe.

    Args:
        bd (str, opcional): Nombre de la base de datos a crear. Por defecto se toma de la variable de entorno DB_NAME.

    Returns:
        None
    '''
    if not bd:
        raise ValueError(
            "No se proporcionó un nombre de base de datos válido.")

    # Conexión sin especificar base de datos
    conexion = conectar_db()  # Conecta solo al servidor
    cursor = conexion.cursor()

    try:
        # Uso de backticks por seguridad
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{bd}`")
    finally:
        cursor.close()
        conexion.close()


def crear_tabla_ohlcv():
    '''
    Crea la tabla 'ohlcv' en la base de datos especificada si no existe.

    La conexión se establece usando las variables de entorno, incluida la base de datos (DB_NAME).
    La tabla incluye columnas estándar para datos de velas OHLCV y una restricción de unicidad.

    Returns:
        None
    '''
    # Conexión a la base de datos (debe existir previamente)
    conexion = conectar_db(os.getenv("DB_NAME"))
    cursor = conexion.cursor()

    try:
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
    finally:
        cursor.close()
        conexion.close()


def guardar_datos_ohlcv(datos):
    '''
    Inserta o actualiza uno o varios registros en la tabla 'ohlcv'.

    Args:
        datos (tuple o list of tuples): Un solo registro OHLCV o una lista de registros.
            Cada registro debe ser una tupla con el formato:
            (timestamp, symbol, timeframe, open, high, low, close, volume)

    Returns:
        None
    '''
    if isinstance(datos, tuple):
        datos = [datos]  # Convertir a lista para tratamiento unificado

    if not datos:
        return  # No hay datos para insertar

    conexion = conectar_db(os.getenv('DB_NAME'))
    sql = """
        INSERT INTO ohlcv (timestamp, symbol, timeframe, open, high, low, close, volume)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            open = VALUES(open),
            high = VALUES(high),
            low = VALUES(low),
            close = VALUES(close),
            volume = VALUES(volume)
    """

    cursor = conexion.cursor()
    try:
        cursor.executemany(sql, datos)
        conexion.commit()
    finally:
        cursor.close()
        conexion.close()
