import numpy as np
from predictor import predecir_direccion

# Crear datos simulados (46 minutos, 4 columnas)
# Valores aleatorios pequeños para simular precios
ultimos_datos_fake = np.random.rand(46, 4)
ultimos_datos_fake = np.expand_dims(ultimos_datos_fake, axis=0)

# Probar la predicción
resultado = predecir_direccion(ultimos_datos_fake)

print(f"Predicción: el precio probablemente {resultado}")