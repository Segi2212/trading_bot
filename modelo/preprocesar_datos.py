import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import RandomOverSampler
from data.preparar_dataset import cargar_datos

def preprocesar_datos(data, secuencia=46):
    # Eliminar filas con valores nulos
    data = data.dropna()

    # Asegurar que los datos estén ordenados por fecha
    data = data.sort_values('timestamp')

    # Selección de características
    features = ['close', 'volume', 'rsi', 'macd']
    X = []
    y = []

    for i in range(secuencia, len(data)):
        X.append(data[features].iloc[i-secuencia:i].values)
        y.append(data['target'].iloc[i])

    X = np.array(X)
    y = np.array(y)

    # Mostrar distribución original
    valores, conteos = np.unique(y, return_counts=True)
    print("Distribución original de clases:")
    for v, c in zip(valores, conteos):
        print(f"Clase {v}: {c} ejemplos")

    # Redimensionar para aplicar oversampling
    shape = X.shape
    X_reshaped = X.reshape((shape[0], shape[1] * shape[2]))

    # Aplicar oversampling
    ros = RandomOverSampler(random_state=42)
    X_resampled, y_resampled = ros.fit_resample(X_reshaped, y)

    # Restaurar forma 3D
    X = X_resampled.reshape((-1, shape[1], shape[2]))
    y = y_resampled

    # Mostrar distribución nueva
    valores, conteos = np.unique(y, return_counts=True)
    print("Distribución balanceada de clases:")
    for v, c in zip(valores, conteos):
        print(f"Clase {v}: {c} ejemplos")

    # División en entrenamiento y validación
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    return X_train, y_train, X_val, y_val


def obtener_datos_balanceados():
    df = cargar_datos()
    X_train, y_train, X_val, y_val = preprocesar_datos(df)

    # Volvemos a separar un conjunto de test si lo necesitas
    # Por ahora dejamos X_val como test final
    return X_train, X_val, y_train, y_val, X_val, y_val