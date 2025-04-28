import pandas as pd
import matplotlib.pyplot as plt

def graficar():
    df = pd.read_csv("simulador/historial_simulacion.csv")

    # Crear columna de saldo total (mxn + btc convertido)
    df['saldo_total'] = df['saldo_mxn'] + df['saldo_btc'] * df['precio']

    plt.figure(figsize=(12, 6))
    plt.plot(df['fecha'], df['saldo_total'], label="Saldo Total")
    plt.xlabel("Fecha")
    plt.ylabel("Saldo (MXN estimado)")
    plt.title("Evolución del saldo en la simulación")
    plt.legend()
    plt.grid()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("simulador/evolucion_saldo.png")
    plt.show()
