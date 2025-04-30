# tests/test_predictor.py

import numpy as np
from modelo.predictor import Predictor

def dummy_data():
    # 60 filas de OHLCV para que queden al menos 47 tras el dropna
    return np.array([
        [i, 100 + i, 101 + i, 99 + i, 100 + i, 10 + i] for i in range(70)
    ])

def test_predecir_dummy():
    ohlcv = dummy_data()

    # Dummy mean y std de tamaño 10 para que coincida con los features
    mean = np.array([100, 101, 99, 100, 10, 100, 50, 0.01, 2.5, 0.02])
    std = np.array([1, 1, 1, 1, 1, 1, 10, 0.02, 1, 0.01])

    predictor = Predictor('modelo/modelo_lstm.h5', mean, std)
    clase, probas = predictor.predecir(ohlcv)

    print("Clase:", clase)
    print("Probs:", probas)

    assert isinstance(clase, int)
    assert isinstance(probas, np.ndarray)
    assert len(probas) == 3
    assert np.isclose(sum(probas), 1.0, atol=1e-5)

if __name__ == "__main__":
    test_predecir_dummy()
