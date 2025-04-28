# main.py

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Importaciones del proyecto
from data import preparar_dataset
from modelo import entrenar_modelo, evaluar_modelo

# Paso 1: Preparar los datos
print("[Main] Preparando dataset...")
X_train, X_val, X_test, y_train, y_val, y_test = preparar_dataset.preparar_dataset()

# Paso 2: Entrenar el modelo
print("[Main] Entrenando modelo...")
modelo = entrenar_modelo.entrenar_modelo(X_train, y_train, X_val, y_val)

# Paso 3: Evaluar el modelo
print("[Main] Evaluando modelo...")
evaluar_modelo.evaluar_modelo(modelo, X_test, y_test)

print("[Main] Proceso finalizado exitosamente.")
