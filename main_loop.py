import time
from bot.estrategia import tomar_decision

def ejecutar_bot():
    """
    Ejecuta el bot de trading en un bucle infinito cada minuto.
    """
    print("🤖 Bot iniciado. Monitoreando el mercado cada minuto...")

    while True:
        try:
            # Tomar decisión
            decision = tomar_decision()

            # Aquí podrías integrar la ejecución de órdenes reales con Bitso
            if decision == "comprar":
                print("✅ Comprar (aquí iría la orden real)")
            elif decision == "vender":
                print("✅ Vender (aquí iría la orden real)")
            else:
                print("⏳ Mantener posición...")

            # Esperar 60 segundos
            time.sleep(60)

        except Exception as e:
            print(f"⚠️ Error durante la ejecución: {str(e)}")
            time.sleep(60)  # Esperar antes de reintentar

if __name__ == "__main__":
    ejecutar_bot()
