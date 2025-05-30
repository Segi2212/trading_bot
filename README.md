1. 🧠 Proyecto de Trading Algorítmico con Criptomonedas (BTC/MXN)
Este bot realiza predicciones cada minuto utilizando un modelo LSTM para comprar o vender BTC en tiempo real a través de la API de Bitso, con operaciones automatizadas 24/7. (Python requerido: 3.9.0)

2. 📦 Manejo de configuración con .env
En lugar de codificar datos sensibles, se definieron variables en un archivo .env y se cargan desde config.py usando python-dotenv.
Variables definidas:
- BITSO_API_KEY
- BITSO_API_SECRET
- BITSO_SYMBOL
- TIMEFRAME
- N_MINUTOS_HISTORIA
- UMBRAL_CONFIDENCIA
- MONTO_POR_OPERACION

3. 📚 requirements.txt con versiones compatibles

4. 🔌 Recolección de datos desde Bitso
Se implementó el módulo /data/recolector.py, que permite:
Conectarse a la API de Bitso con ccxt.
Obtener velas OHLCV de 1 minuto (últimos 60 datos por defecto).

5. 🧹 Preprocesamiento para el modelo LSTM
En /modelo/preprocesador.py se añadió:
Conversión de datos a DataFrame.
Cálculo de indicadores técnicos (EMA, RSI).
Normalización.
Reorganización del input para LSTM en formato [1, 60, features].

6. Generación de venv:
py -m venv venv

7. Inicio de venv:
venv\Scripts\activate

8. Actualizar pip
py -m pip install --upgrade pip

9. Instalar dependencias:
pip install -r requirements.txt