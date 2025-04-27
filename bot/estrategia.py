import numpy as np
from data.recolector import obtener_ohlcv
from modelo.predictor import predecir_direccion
from data.recolector import obtener_ohlcv_test

VENTANA = 46  # Número de datos históricos que espera el modelo
FEATURES = 4  # open, high, low, close

def preparar_input(datos_recientes: list) -> np.ndarray:
    """
    Prepara los datos recientes en el formato correcto para el modelo LSTM.

    Args:
        datos_recientes (list): Lista de OHLCV recientes.

    Returns:
        np.ndarray: Input para el modelo de forma (1, ventana, features).
    """
    array = np.array([d[1:5] for d in datos_recientes])  # extraemos [open, high, low, close]
    array = array.reshape(1, VENTANA, FEATURES)
    return array

def tomar_decision() -> str:
    """
    Obtiene los datos más recientes, predice y toma una decisión: 'comprar', 'vender', 'mantener'.

    Returns:
        str: Acción recomendada.
    """
    # 1. Obtener los datos más recientes
    datos_recientes = obtener_ohlcv(VENTANA)

    # Validación
    if len(datos_recientes) < VENTANA:
        print("[Estrategia] No hay suficientes datos para predecir.")
        return "esperar"

    # 2. Preparar input
    input_lstm = preparar_input(datos_recientes)

    # 3. Predecir
    clase, probabilidad = predecir_direccion(input_lstm)

    # 4. Tomar decisión basada en la predicción
    if clase == 1:
        decision = "comprar"
    else:
        decision = "vender"

    print(f"[Estrategia] Decisión: {decision} | Confianza: {probabilidad:.4f}")
    return decision

def tomar_decision_test(bitso):
    """
    Decide si comprar, vender o mantener usando datos simulados de prueba.
    """
    datos = obtener_ohlcv_test(bitso)

    clase, probabilidad = predecir_direccion(datos)

    if clase == 1 and probabilidad > 0.55:
        return "comprar"
    elif clase == 0 and probabilidad < 0.45:
        return "vender"
    else:
        return "mantener"