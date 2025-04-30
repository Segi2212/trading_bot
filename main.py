# main.py

from data.recolector import obtener_datos_en_vivo
from db.mysql import guardar_datos
from modelo.preprocesador import preparar_datos
from modelo.predictor import cargar_modelo, predecir
from trading.decision import tomar_decision
from trading.ejecutor import ejecutar_orden
from utils.logger import configurar_logger

logger = configurar_logger()

def main():
    try:
        # 1. Obtener datos en vivo
        datos = obtener_datos_en_vivo()
        guardar_datos(datos)  # opcional: guardar en base de datos

        # 2. Preprocesar
        X = preparar_datos(datos)

        # 3. Cargar modelo entrenado y predecir
        modelo = cargar_modelo('modelo_entrenado.h5')
        prediccion = predecir(modelo, X)

        # 4. Tomar decisión
        accion = tomar_decision(prediccion)
        logger.info(f"Predicción: {prediccion} → Acción: {accion}")

        # 5. Ejecutar orden (real o simulada)
        ejecutar_orden(accion)

    except Exception as e:
        logger.error(f"Error en el flujo principal: {e}")

if __name__ == "__main__":
    main()
