# ML Predictivo para AVGO, AMD, NVDA

## Contexto del proyecto

Este repositorio contiene el proyecto de predicción de precios de acciones para AVGO, AMD y NVDA usando Machine Learning.  
El objetivo es predecir el precio de cierre a +1, +3 y +7 días usando tres modelos principales:
- Prophet
- Random Forest
- LSTM

**El dataset es un CSV con 10 años de cotizaciones.**

---

## Estructura recomendada

- `10 años.. csv` — Dataset con las columnas: Ticker, Date, Open, High, Low, Close, Adjusted_close, Adjusted_low, Adjusted_high, Adjusted_open, Volume
- `entrenar_modelos.py` — Script principal para entrenamiento y evaluación.
- `modelos_guardados/` — Aquí se guardarán los modelos entrenados y normalizadores.
- `resultados/` — Aquí se encontrarán las predicciones y métricas.
- `logs/` — Logs detallados de cada ejecución.

---

## ¿Cómo continuar si se cierra el chat?

1. **Siempre deja los scripts y modelos guardados en el repo.**
2. Si quieres retomar, simplemente copia este contexto y tus dudas en el chat de Copilot o GitHub Copilot Chat.
3. Yo (Copilot) puedo continuar desde cualquier paso, solo dime qué archivos tienes y qué necesitas.

---

## ¿Cómo entrenar los modelos?

1. Instala dependencias:

   ```bash
   pip install pandas prophet scikit-learn tensorflow tqdm
   ```

2. Ejecuta el script:

   ```bash
   python entrenar_modelos.py
   ```

3. Los modelos entrenados estarán en `modelos_guardados/`, los resultados en `resultados/` y los logs detallados en `logs/`.

---

## ¿Cómo agregar nuevas predicciones o ajustar modelos?

- Puedes pedirme scripts adicionales para predicción, comparación de modelos, visualización o ajuste de hiperparámetros.
- Si necesitas modificar el flujo, solo dime qué necesitas y se adapta el código.

---

**Ante cualquier corte, vuelve a este README y sigue desde aquí.**
