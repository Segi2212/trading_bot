
import json
import os
import pandas as pd
from datetime import datetime
from modelo.predictor import predecir_direccion
from data.mysql_conexion import obtener_ultimos_datos

# Cargar configuración
with open('simulador/config_simulador.json', 'r') as f:
    config = json.load(f)

# Parámetros del simulador
SALDO_INICIAL = config["saldo_inicial"]
PORCENTAJE_OPERACION = config["porcentaje_operacion"]
COMISION = config["comision"]
LIMITE_DATOS = config["limite_datos"]

# Estado
saldo_mxn = SALDO_INICIAL
saldo_btc = 0
moneda_actual = "MXN"  # "MXN" o "BTC"
historial = []

def simular_operaciones():
    global saldo_mxn, saldo_btc, moneda_actual

    print("[Simulador] Iniciando simulación...")


    datos = obtener_ultimos_datos(limite=LIMITE_DATOS)
    
    print(f"[Simulador] Datos cargados: {len(datos)} velas")

    for i in range(46, len(datos)):
        secuencia = datos[i-46:i]
        secuencia = secuencia[['open', 'high', 'low', 'close']].values
        secuencia = secuencia.reshape((1, 46, 4))

        prediccion = predecir_direccion(secuencia)
        precio_actual = datos.iloc[i]['close']
        fecha_actual = datos.iloc[i]['timestamp']

        if prediccion[0] == 1 and moneda_actual == "MXN":
            # Comprar BTC
            cantidad_mxn = saldo_mxn * PORCENTAJE_OPERACION
            cantidad_btc = (cantidad_mxn * (1 - COMISION)) / precio_actual
            saldo_mxn -= cantidad_mxn
            saldo_btc += cantidad_btc
            moneda_actual = "BTC"

            historial.append({
                "fecha": fecha_actual,
                "operacion": "Compra BTC",
                "precio_operacion": precio_actual,
                "saldo_mxn": saldo_mxn,
                "saldo_btc": saldo_btc,
                "ganancia_porcentual": None,
                "saldo_total_mxn": saldo_mxn + saldo_btc * precio_actual
            })

        elif prediccion[0] == 0 and moneda_actual == "BTC":
            # Vender BTC
            cantidad_mxn = saldo_btc * precio_actual * (1 - COMISION)
            ganancia = (cantidad_mxn - (saldo_btc * precio_actual)) / (saldo_btc * precio_actual) if saldo_btc != 0 else 0
            ganancia_pct = ganancia * 100
            saldo_mxn += cantidad_mxn
            saldo_btc = 0
            moneda_actual = "MXN"

            historial.append({
                "fecha": fecha_actual,
                "operacion": "Venta BTC",
                "precio_operacion": precio_actual,
                "saldo_mxn": saldo_mxn,
                "saldo_btc": saldo_btc,
                "ganancia_porcentual": ganancia_pct,
                "saldo_total_mxn": saldo_mxn
            })


    # Guardar historial
    df_historial = pd.DataFrame(historial)
    df_historial.to_csv("simulador/historial_simulacion.csv", index=False)
    print("[Simulador] ✅ Simulación completada y resultados guardados.")
    
    if df_historial.empty:
        print("[Simulador] ⚠️ No hubo operaciones para graficar.")
    else:
        from simulador.graficar_resultados import graficar
        graficar()

if __name__ == "__main__":
    simular_operaciones()
