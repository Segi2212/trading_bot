# from data.recolector import conectar_bitso, obtener_ohlcv
# from modelo.preprocesador import preparar_input_lstm

# exchange = conectar_bitso()
# ohlcv = obtener_ohlcv(exchange)

# input_lstm = preparar_input_lstm(ohlcv)

# print("Shape del input para el modelo:", input_lstm.shape)

# from modelo.predictor import predecir_direccion

# clase, prob = predecir_direccion(input_lstm)

# print("Predicción:", "📈 SUBE" if clase else "📉 BAJA", f"({prob:.2%} confianza)")

from db.descargador import actualizar_datos
actualizar_datos()