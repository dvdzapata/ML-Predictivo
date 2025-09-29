import os
import sys
import logging
from tqdm import tqdm
import pandas as pd
import numpy as np
from datetime import timedelta
from pathlib import Path
import pickle

# Prophet
from prophet import Prophet

# Random Forest
from sklearn.ensemble import RandomForestRegressor

# LSTM
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

# Configuración de logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    filename='logs/entrenamiento.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

# Configuración de carpetas
os.makedirs('modelos_guardados', exist_ok=True)
os.makedirs('resultados', exist_ok=True)

CSV_FILENAME = "10 años.. csv"
TICKERS = ["AMD", "NVDA", "AVGO"]
HORIZONTES = [1, 3, 7]  # días

# ===========================
# Utilidades generales
# ===========================
def cargar_datos_csv(nombre_archivo):
    try:
        df = pd.read_csv(nombre_archivo)
        logging.info(f"CSV cargado correctamente: {nombre_archivo}")
    except Exception as e:
        logging.error(f"Error cargando CSV: {e}")
        sys.exit(1)
    # Estandariza columnas de fecha y orden
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(['Ticker', 'Date']).reset_index(drop=True)
    return df

def preparar_dataset(df, ticker, horizonte):
    """Devuelve X, y para un ticker y un horizonte de días futuros"""
    datos = df[df['Ticker'] == ticker].copy()
    datos = datos.sort_values('Date')
    datos['Target'] = datos['Close'].shift(-horizonte)
    # Puedes añadir aquí más features técnicas si lo deseas
    datos = datos.dropna()
    X = datos[['Open', 'High', 'Low', 'Close', 'Volume']].values
    y = datos['Target'].values
    fechas = datos['Date'].values
    return X, y, fechas

def split_train_test(X, y, fechas, test_size=0.2):
    n = int(len(X) * (1 - test_size))
    return X[:n], X[n:], y[:n], y[n:], fechas[:n], fechas[n:]

def guardar_objeto(obj, ruta):
    with open(ruta, "wb") as f:
        pickle.dump(obj, f)
    logging.info(f"Guardado: {ruta}")

def guardar_resultados(df, nombre):
    ruta = f"resultados/{nombre}.csv"
    df.to_csv(ruta, index=False)
    logging.info(f"Resultados guardados en: {ruta}")

# ===========================
# Modelos
# ===========================

def entrenar_prophet(df, ticker, horizonte):
    datos = df[df['Ticker'] == ticker][['Date', 'Close']].copy()
    datos = datos.rename(columns={'Date': 'ds', 'Close': 'y'})
    # Shift target para horizonte
    datos['y'] = datos['y'].shift(-horizonte)
    datos = datos.dropna()
    train = datos[:-int(len(datos)*0.2)]
    test = datos[-int(len(datos)*0.2):]
    modelo = Prophet(daily_seasonality=True, yearly_seasonality=True)
    modelo.fit(train)
    # Predicción test
    forecast = modelo.predict(test[['ds']])
    pred = forecast['yhat'].values
    real = test['y'].values
    fechas = test['ds'].values
    return modelo, pred, real, fechas

def entrenar_rf(X_train, y_train):
    modelo = RandomForestRegressor(n_estimators=100, n_jobs=-1, random_state=42)
    modelo.fit(X_train, y_train)
    return modelo

def entrenar_lstm(X_train, y_train, epochs=20, batch_size=32):
    # Escala datos
    from sklearn.preprocessing import MinMaxScaler
    scaler_X = MinMaxScaler()
    scaler_y = MinMaxScaler()
    X_train_scaled = scaler_X.fit_transform(X_train)
    y_train_scaled = scaler_y.fit_transform(y_train.reshape(-1,1))
    # LSTM espera 3D: (samples, timesteps, features)
    X_train_lstm = np.expand_dims(X_train_scaled, axis=1)
    model = Sequential([
        LSTM(32, input_shape=(X_train_lstm.shape[1], X_train_lstm.shape[2])),
        Dropout(0.1),
        Dense(1)
    ])
    model.compile(loss='mse', optimizer='adam')
    model.fit(X_train_lstm, y_train_scaled, epochs=epochs, batch_size=batch_size, verbose=0)
    return model, scaler_X, scaler_y

def predecir_lstm(model, scaler_X, scaler_y, X_test):
    X_test_scaled = scaler_X.transform(X_test)
    X_test_lstm = np.expand_dims(X_test_scaled, axis=1)
    y_pred_scaled = model.predict(X_test_lstm, verbose=0)
    y_pred = scaler_y.inverse_transform(y_pred_scaled)
    return y_pred.flatten()

# ===========================
# Entrenamiento principal
# ===========================

def main():
    df = cargar_datos_csv(CSV_FILENAME)
    resultados_totales = []
    for ticker in TICKERS:
        for horizonte in HORIZONTES:
            logging.info(f"Entrenando {ticker} +{horizonte} días")
            # Prophet
            try:
                modelo_prophet, pred_p, real_p, fechas_p = entrenar_prophet(df, ticker, horizonte)
                guardar_objeto(modelo_prophet, f"modelos_guardados/prophet_{ticker}_{horizonte}.pkl")
                df_prophet = pd.DataFrame({'Date': fechas_p, 'Ticker': ticker, 'Modelo': 'Prophet', 'Horizonte': horizonte, 'Real': real_p, 'Prediccion': pred_p})
                guardar_resultados(df_prophet, f"predicciones_prophet_{ticker}_{horizonte}")
                resultados_totales.append(df_prophet)
            except Exception as e:
                logging.error(f"Prophet fallo para {ticker} +{horizonte}: {e}")
            # Random Forest
            try:
                X, y, fechas = preparar_dataset(df, ticker, horizonte)
                X_train, X_test, y_train, y_test, fechas_train, fechas_test = split_train_test(X, y, fechas)
                modelo_rf = entrenar_rf(X_train, y_train)
                guardar_objeto(modelo_rf, f"modelos_guardados/rf_{ticker}_{horizonte}.pkl")
                y_pred_rf = modelo_rf.predict(X_test)
                df_rf = pd.DataFrame({'Date': fechas_test, 'Ticker': ticker, 'Modelo': 'RandomForest', 'Horizonte': horizonte, 'Real': y_test, 'Prediccion': y_pred_rf})
                guardar_resultados(df_rf, f"predicciones_rf_{ticker}_{horizonte}")
                resultados_totales.append(df_rf)
            except Exception as e:
                logging.error(f"Random Forest fallo para {ticker} +{horizonte}: {e}")
            # LSTM
            try:
                modelo_lstm, scaler_X, scaler_y = entrenar_lstm(X_train, y_train)
                modelo_lstm.save(f"modelos_guardados/lstm_{ticker}_{horizonte}.h5")
                # Guardar los scalers
                guardar_objeto(scaler_X, f"modelos_guardados/lstm_scalerX_{ticker}_{horizonte}.pkl")
                guardar_objeto(scaler_y, f"modelos_guardados/lstm_scalerY_{ticker}_{horizonte}.pkl")
                y_pred_lstm = predecir_lstm(modelo_lstm, scaler_X, scaler_y, X_test)
                df_lstm = pd.DataFrame({'Date': fechas_test, 'Ticker': ticker, 'Modelo': 'LSTM', 'Horizonte': horizonte, 'Real': y_test, 'Prediccion': y_pred_lstm})
                guardar_resultados(df_lstm, f"predicciones_lstm_{ticker}_{horizonte}")
                resultados_totales.append(df_lstm)
            except Exception as e:
                logging.error(f"LSTM fallo para {ticker} +{horizonte}: {e}")
    # Guardar resumen
    df_total = pd.concat(resultados_totales, ignore_index=True)
    guardar_resultados(df_total, "predicciones_todos_los_modelos")
    logging.info("Entrenamiento completo. Revisa la carpeta resultados/ y modelos_guardados/")

if __name__ == "__main__":
    main()
