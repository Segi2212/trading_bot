import numpy as np
from tensorflow.keras.models import load_model

# Cargar el modelo (puedes adaptar la ruta según cómo lo guardes)
modelo = load_model("modelo/modelo_lstm.h5")

def predecir_direccion(input_lstm):
    """
    Usa el modelo LSTM para predecir si el precio subirá (1) o bajará (0).
    Retorna una tupla (clase, probabilidad).
    """
    prob = modelo.predict(input_lstm, verbose=0)[0][0]  # valor entre 0 y 1
    clase = int(prob > 0.5)  # 1: subir, 0: bajar
    return clase, prob
