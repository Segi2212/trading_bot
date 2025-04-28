import numpy as np
import matplotlib.pyplot as plt
from keras.models import load_model
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns

# Cargar modelo y datos
modelo = load_model("modelo/modelo_lstm.h5")
X = np.load("dataset/X.npy")
y = np.load("dataset/y.npy")

# Predicciones
y_pred = modelo.predict(X)
y_pred_classes = np.argmax(y_pred, axis=1)

# Reporte de clasificación
print("[Evaluación] Reporte de clasificación:")
print(classification_report(y, y_pred_classes, target_names=["Baja", "Neutro", "Sube"]))

# Matriz de confusión
cm = confusion_matrix(y, y_pred_classes)

plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["Baja", "Neutro", "Sube"], yticklabels=["Baja", "Neutro", "Sube"])
plt.xlabel("Predicción")
plt.ylabel("Realidad")
plt.title("Matriz de Confusión")
plt.show()