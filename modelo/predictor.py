# modelo/predictor.py

import numpy as np
from tensorflow.keras.models import load_model  # type: ignore
import os

# Configuración
DEBUG = os.getenv("DEBUG", "False").lower() == "true"  # Lee desde .env si quieres activar/desactivar logs

# Cargar el modelo una sola vez
modelo = load_model("modelo/modelo_lstm.h5")

def predecir_direccion(input_lstm: np.ndarray) -> tuple[int, float]:
    """
    Usa el modelo LSTM para predecir si el precio subirá (1) o bajará (0).

    Args:
        input_lstm (np.ndarray): Entrada de forma (1, ventanas, features).

    Returns:
        tuple: (clase_predicha (0 o 1), probabilidad)
    """
    prob = modelo.predict(input_lstm, verbose=0)[0][0]  # Resultado entre 0 y 1
    clase = int(prob > 0.5)  # 1: sube, 0: baja

    if DEBUG:
        print(f"[Predictor] Clase predicha: {clase} | Probabilidad: {prob:.4f}")

    return clase, prob
