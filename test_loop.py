# test_loop.py

import time
from data.recolector import conectar_bitso
from bot.estrategia import tomar_decision_test

def ejecutar_test_bot(iteraciones=5, delay_segundos=5):
    print(f"🚀 Iniciando prueba de {iteraciones} iteraciones (cada {delay_segundos}s)...")

    bitso = conectar_bitso()

    for i in range(iteraciones):
        print(f"\n🔵 Iteración {i+1}/{iteraciones}")
        try:
            decision = tomar_decision_test(bitso)

            if decision == "comprar":
                print("✅ [SIMULACIÓN] Comprar (no ejecutado)")
            elif decision == "vender":
                print("✅ [SIMULACIÓN] Vender (no ejecutado)")
            else:
                print("⏳ [SIMULACIÓN] Mantener posición...")

            time.sleep(delay_segundos)

        except Exception as e:
            print(f"⚠️ Error en la simulación: {str(e)}")
            time.sleep(delay_segundos)

    print("\n✅ Prueba finalizada.")

if __name__ == "__main__":
    ejecutar_test_bot()
