# ML Predictivo para Acciones y ETFs

## Contexto del Proyecto

Este repositorio contiene un flujo completo para entrenar y comparar modelos de Machine Learning para predecir precios de cierre a +1, +3 y +7 días de acciones (AMD, AVGO, NVDA) y, si se desea en el futuro, de ETFs relacionados al sector semiconductores.

### **Datasets disponibles**

- **Acciones (diario):**  
  - Archivo: `10-años-amd-nvda-avgo.csv`
  - Columnas: Ticker, Date, Open, High, Low, Close, Adjusted_close, Adjusted_low, Adjusted_high, Adjusted_open, Volume

- **ETFs (diario):**  
  - Archivo: `etf-daily.csv`
  - Columnas: Ticker, Date, Open, High, Low, Close, Adjusted_close, Adjusted_low, Adjusted_high, Adjusted_open, Volume

- **ETFs (1 hora):**  
  - Archivo: `etf-1h.csv`
  - Columnas: Ticker, Timestamp, Gmtoffset, DateTime, Open, High, Low, Close, Volume

---

## Estructura Recomendada

- `10-años-amd-nvda-avgo.csv`  — Datos diarios de AMD, AVGO, NVDA
- `etf-daily.csv`               — ETFs diarios (opcional para features futuras)
- `etf-1h.csv`                  — ETFs en 1h (opcional para features futuras)
- `entrenar_modelos.py`         — Script principal de entrenamiento y evaluación
- `modelos_guardados/`          — Modelos y normalizadores guardados automáticamente
- `resultados/`                 — Predicciones y métricas generadas
- `logs/`                       — Logs detallados de cada ejecución

---

## ¿Cómo entrenar los modelos?

1. **Instala las dependencias:**
   ```bash
   pip install pandas prophet scikit-learn tensorflow tqdm
   ```

2. **Ejecuta el script:**
   ```bash
   python entrenar_modelos.py
   ```

3. **Resultados:**
   - Modelos entrenados en `modelos_guardados/`
   - Predicciones y métricas en `resultados/`
   - Log detallado en `logs/`

---

## ¿Cómo continuar si se cierra el chat?

- **No pierdes nada importante:**  
  El script, los modelos y resultados quedan guardados en el repo.  
  Si necesitas retomar el proyecto o pedir scripts nuevos, solo copia este contexto y tus dudas en Copilot Chat.
- **Siempre ejecuta desde el repo:**  
  Así tienes todo respaldado y es fácil continuar/automatizar.

---

## ¿Quieres agregar nuevas señales (por ejemplo, ETFs como variables externas)?

- Solo pídelo aquí y se adaptará el pipeline para combinar varios archivos y mejorar los modelos.

---

**¡Listo para usar! Si tienes nuevas ideas o quieres optimizar, sólo escribe aquí.**
