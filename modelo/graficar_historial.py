import json
import matplotlib.pyplot as plt

# Cargar historial
with open("modelo/historial_entrenamiento.json", "r") as f:
    historial = json.load(f)

# Graficar Loss
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(historial['loss'], label='Entrenamiento')
plt.plot(historial['val_loss'], label='Validación')
plt.title('Pérdida (Loss)')
plt.xlabel('Épocas')
plt.ylabel('Pérdida')
plt.legend()

# Graficar Accuracy
plt.subplot(1, 2, 2)
plt.plot(historial['accuracy'], label='Entrenamiento')
plt.plot(historial['val_accuracy'], label='Validación')
plt.title('Precisión (Accuracy)')
plt.xlabel('Épocas')
plt.ylabel('Precisión')
plt.legend()

plt.tight_layout()
plt.show()
