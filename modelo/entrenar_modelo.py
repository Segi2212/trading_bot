import numpy as np
from sklearn.utils import class_weight
from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras.optimizers import Adam
import joblib

def entrenar_modelo(X_train, y_train, X_val, y_val):
    # Calcular pesos de clases
    pesos = class_weight.compute_class_weight(
        class_weight='balanced',
        classes=np.unique(y_train),
        y=y_train
    )
    class_weights = dict(enumerate(pesos))

    print(f"[Modelo] Pesos de clases aplicados: {class_weights}")

    model = Sequential()
    model.add(LSTM(64, input_shape=(X_train.shape[1], X_train.shape[2])))
    model.add(Dense(3, activation='softmax'))  # 3 clases: Baja, Neutro, Sube

    model.compile(optimizer=Adam(learning_rate=0.001),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    model.fit(
        X_train, y_train,
        epochs=50,
        batch_size=64,
        validation_data=(X_val, y_val),
        class_weight=class_weights,  # <<< Aquí aplicamos el balanceo
        verbose=2
    )

    model.save('modelo_entrenado.h5')
    print("[Modelo] Entrenamiento terminado y modelo guardado.")

    return model
