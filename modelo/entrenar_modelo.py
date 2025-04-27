import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from keras.callbacks import EarlyStopping
import json

# Cargar los datos
X = np.load("modelo/X.npy")
y = np.load("modelo/y.npy")

# Definir modelo
modelo = Sequential()
modelo.add(LSTM(units=64, return_sequences=True, input_shape=(X.shape[1], X.shape[2])))
modelo.add(Dropout(0.2))
modelo.add(LSTM(units=32))
modelo.add(Dropout(0.2))
modelo.add(Dense(units=1, activation="sigmoid"))

# Compilar
modelo.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

# Entrenar
early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

historial = modelo.fit(
    X, y,
    epochs=20,
    batch_size=64,
    validation_split=0.2,
    callbacks=[early_stop],
    verbose=1
)

# Guardar modelo
modelo.save("modelo/modelo_lstm.h5")

# Guardar historial
with open("modelo/historial_entrenamiento.json", "w") as f:
    json.dump(historial.history, f)

print("✅ Modelo entrenado y guardado con éxito.")
