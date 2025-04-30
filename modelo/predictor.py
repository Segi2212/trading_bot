# predictor.py

import numpy as np
from tensorflow.keras.models import load_model # type: ignore
from .preprocesador import preprocesar_para_prediccion

class Predictor:
    def __init__(self, modelo_path, mean, std):
        self.modelo = load_model(modelo_path)
        self.mean = mean
        self.std = std

    def predecir(self, ohlcv):
        entrada = preprocesar_para_prediccion(ohlcv, self.mean, self.std)
        salida = self.modelo.predict(entrada, verbose=0)
        return int(np.argmax(salida)), salida[0]
