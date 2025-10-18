# CONTEXTO DEL PROYECTO — Fuente de verdad (versión oficial)

Generado: 2025-10-18T15:25:12Z  
Autor (entrada original): @dvdzapata  
Estado: borrador formal generado a partir de la nota del responsable. Guardar en la raíz del repo o en `C:/ML-Predictivo/docs/CONTEXT.md`.

Resumen ejecutivo
-----------------
Proyecto: entrenar modelos predictivos de corto plazo para el sector de semiconductores (horizontes +1d, +3d, +7d) sobre un amplio universo de series temporales (acciones, ETFs, índices, macro, commodities, FX y cripto).  
Objetivo inmediato: producir features exhaustivas para los tickers objetivo y entrenar de forma profesional tres familias de modelos (XGBoost, LSTM, TimesFM), con pipeline reproducible, trazabilidad total y controles rígidos de calidad de datos. Nada se cambia en los datos sin autorización explícita (`APLICAR`) y backups.

1) Propósito general
--------------------
Construir un pipeline reproducible y auditable que permita:
- Predecir movimientos a corto plazo (+1, +3, +7 días) para acciones clave del sector semiconductores.
- Entregar señales y modelos comparables entre distintas familias (boosting, DL y transformers para series temporales).
- Mantener la máxima calidad de features (cantidad y exhaustividad) para optimizar la información disponible.

2) Alcance y objetivos concretos (corrección importante)
--------------------------------------------------------
- Objetivo de predicción (targets): exclusivamente AVGO, AMD y NVDA. Estos son los tickers sobre los que se generarán las señales y se evaluarán métricas de negocio.  
- Universo auxiliar: el resto de activos (≈70 tickers semiconductores, ETFs sectoriales, índices, commodities, FX, futuros, cripto) se usan únicamente como datos de apoyo para enriquecer features y entrenar modelos — NO se consideran targets primarios.  
- Horizontes de predicción: 1 día, 3 días, 7 días.  
- Métricas principales:
  - Predictivas: MSE, MAE, R².
  - Trading-oriented: directional accuracy (hit rate), Spearman IC, rendimiento de la decila superior en test.
- Resultado mínimo esperado en la fase urgente: generar features para los tickers objetivo (AVGO, AMD, NVDA) y entrenar las 3 familias de modelos prioritarias con métricas comparativas.

3) Datos (alto nivel)
---------------------
- Origen: CSVs por ticker con historial (hasta 10 años por ahora). Granularidades disponibles: 1min, 5min, 15min, 30min, 1h, 1d.  
- Cobertura: ~70 tickers semiconductores globales (NVDA, AMD, INTC, QCOM, ARM, AVGO, MRVL, NXPI, TXN, ADI, ON, MCHP, MPWR, QRVO, SWKS, WDC, STX, MU, ...), ETFs sectoriales (SMH, SOXX, SOXQ, etc.), índices, macro, commodities, futuros y FX.  
- Estado actual: series históricas en CSVs preparados; algunas series ya han pasado QA. Hoy se están generando ~300 features basadas en OHLC para AVGO, AMD, NVDA, SMH, SOXX y SOXQ.

4) Feature engineering (línea de trabajo)
----------------------------------------
- Filosofía: generar una amplia y rica colección de features (lags, rolling stats, momentum, volumen normalizado, microstructure proxies, indicadores sectoriales y macro, cross-asset features) — tanto específicas del sector como generales.
- Entregable por ticker: archivo features por ticker + CSV combinado `superfeatures_ml_ready.csv`.
- Regla: no sobrescribir datos originales. Outputs en `C:/ML-Predictivo/data/processed/` y `.../per_ticker/`. Cada ejecución debe producir manifest y backup si sobrescribe.

5) Modelos a entrenar (prioridad y por qué)
------------------------------------------
Prioridad inicial (entrenar y comparar):
1. XGBoost — baseline de alto rendimiento para tabular y features densas.
2. LSTM (Keras/TensorFlow) — probar capacidad secuencial y dependencias temporales.
3. TimesFM (o transformer de series temporales) — escalable para múltiples horizontes y cross-ticker context.
- Objetivo: entrenar estas tres familias profesionalmente, comparar, elegir la(s) mejor(es) para despliegue.
- Nota: también mantener rutinas para Ridge / RandomForest como sanity baselines si hacen falta.

6) Infraestructura y entorno
---------------------------
- Sistema: Microsoft Windows 11 Pro for Workstations.
- Máquina: Lenovo ThinkStation (Xeon W-2133, 64 GB RAM, SSDs, GPU Quadro P2000 con 5120 MB dedicada).
- Software: Python (entorno `ml-times`), CUDA y librerías (instalar según se necesite). Se buscarán siempre las mejores librerías (LightGBM/XGBoost/CatBoost/TensorFlow/PyTorch/TimesFM implementations) y se hará fallback seguro si alguna falta.
- Repositorio: scripts en `C:/ML-Predictivo/scripts/`, outputs en `C:/ML-Predictivo/data/processed` y `C:/ML-Predictivo/modelos_guardados/`.

7) Reglas operativas y de seguridad (reglas de oro)
---------------------------------------------------
- PRINCIPAL: Ningún cambio en los datos originales (CSV) sin BACKUP atómico y autorización explícita `APLICAR` (exacto, todo mayúsculas).  
- Dry-run por defecto: todos los scripts mutativos deben soportar `--dry-run` y ejecutarse así por defecto. `--apply` u `APLICAR` habilita el modo mutativo.  
- Backups y manifests: antes de sobrescribir, crear backup `.orig.TIMESTAMP` o `.bak` y escribir manifest JSON con hashes (md5/sha256), lista de inputs y outputs y timestamp.  
- Trazabilidad: todos los scripts escriben logs detallados (rotación/compresión opcional) y manifiesto con quien aplicó los cambios.  
- Minimalismo en correcciones: al corregir código, modificar SOLO la parte concreta que falle o necesite mejora; respetar el resto del pipeline.  
- No presuposiciones: nunca asumir nombres de columnas/paths; los scripts deben detectar o pedir .env/config (prepararé .env templates).  
- Calidad del código: entrega final sin errores sintácticos, optimizado, con manejo de excepciones y compatibilidades (Windows, paths, posibles librerías faltantes).

8) Estado actual (qué hay y qué falta)
--------------------------------------
Hecho:
- Base de CSV histórica (10 años) disponible para muchos tickers.
- Scripts de QA y detección de scale changes parcheados (heurística por bloques).
- Se detectaron 5 candidates de scale_change para NVDA (QA JSON actualizado y backup creado).

Pendiente (prioridad):
1. Generar features exhaustivas para los tickers objetivo (AVGO, AMD, NVDA) y ETFs relacionados. — URGENTE.
2. Consolidar `superfeatures_ml_ready.csv` (procesado en `data/processed`).
3. Entrenar los 3 modelos prioritarios (XGBoost, LSTM, TimesFM) y producir comparativa.
4. Revisar las detecciones de scale_changes y decidir aplicar ajustes sólo si se autoriza (`APLICAR`).
5. Automatizar pipeline with guardrails and manifests.

9) Procedimiento operativo recomendado (pasos concretos)
--------------------------------------------------------
(Se ejecutan SOLO con autorización o en modo dry-run para inspección)

A. Generar features (por ticker y combinado)
   - Ejecutar `compute_features.py` → produce `per_ticker/<TICKER>__features.csv` y `superfeatures_ml_ready.csv`.
   - Guardar manifest y log en `data/processed/`.

B. Entrenamiento (batería)
   - Ejecutar `train_all_models.py` sobre `superfeatures_ml_ready.csv`.
   - Guardar modelos, `models_comparison_*.csv`, metrics JSON y logs en `modelos_guardados/models/`.

C. Revisión y aplicar ajustes (opcional)
   - Ejecutar `apply_scale_adjustments.py --dry-run` vía wrapper `enforce_dry_run_wrapper.py`.
   - Revisar manifest (backups listados).
   - Si OK, autorizar con `APLICAR` para ejecutar en modo real; luego repetir A+B y comparar.

D. Auditoría y reversión
   - Cada cambio mutativo debe generar manifest y backup; la reversión consiste en restaurar el backup y regenerar summary.

10) Next steps (inmediato — sugerencia operativa)
-------------------------------------------------
- Paso inmediato 1 (APROBACIÓN NEEDED): generar features para AVGO, AMD, NVDA y ETFs sectoriales. — Produce `superfeatures_ml_ready.csv`.  
- Paso inmediato 2 (una vez completado el anterior): entrenar la batería XGBoost / LSTM / TimesFM y entregar `models_comparison` y metrics.  
- Paso inmediato 3: revisión humana rápida de detecciones de scale_change; decidir aplicar o no.

11) Roles y responsabilidades
------------------------------
- Responsable de decisiones de aplicación de cambios en datos: @dvdzapata (tú). Tu autorización = `APLICAR`.
- Desarrollo de scripts, mantenimiento y ejecución segura: Asistente (yo) — preparo scripts finales, manifests y comandos exactos.  
- Revisión/QA humana: equipo o persona designada por ti (puedes delegar).

12) Notas técnicas y operativas (detalles útiles)
------------------------------------------------
- Scripts deben usar logging estructurado (JSON lines option) para facilitar ingestión en sistemas de monitoreo.  
- Scripts deben validar disponibilidad de librerías y elegir fallback (ej. si XGBoost no instalado usar LightGBM o RF) y reportarlo en logs.  
- Para reproducibilidad se debe guardar `requirements.txt` o `conda` env export y hash de entorno cuando se ejecuta entrenamiento.  
- Evitar suposiciones de columnas: usar detección automática + archivo `.env` con mappings si es necesario.

13) Glosario (rápido)
---------------------
- `scale_change` / split: evento corporativo que requiere reescala de precios históricos.  
- `manifest`: JSON que lista inputs, outputs, hashes, timestamp, usuario y acción (dry-run/apply).  
- `APLICAR`: autorización explícita (todo en mayúsculas) para ejecutar acciones mutativas sobre datos.

14) Documentación y seguimiento
-------------------------------
- Guardar este `CONTEXT.md` en el repo y actualizar tras cada ejecución autorizada.  
- Cada ejecución mutativa añade entrada a `modelos_guardados/qa_report/ops_log.json` con manifest path y metadatos.

15) Comandos de ejemplo (placeholders)
-------------------------------------
(Se deben adaptar con rutas reales; los scripts están preparados para detección automática de columnas)
- Generar features:
  ```
  conda activate ml-times
  python "C:/ML-Predictivo/scripts/compute_features.py" --input-dir "C:/ML-Predictivo/modelos_guardados/qa_report/tmp_per_ticker" --outdir "C:/ML-Predictivo/data/processed" --force --verbose
  ```
- Entrenar batería de modelos:
  ```
  python "C:/ML-Predictivo/scripts/train_all_models.py" --input "C:/ML-Predictivo/data/processed/superfeatures_ml_ready.csv" --outdir "C:/ML-Predictivo/modelos_guardados/models" --n-jobs 4 --verbose
  ```
- Dry-run de ajustes por splits:
  ```
  python enforce_dry_run_wrapper.py --script scripts/apply_scale_adjustments.py --args '--input "tmp_per_ticker/NVDA_US____input.csv" --qa "per_ticker/NVDA_US____qa.json"' 
  ```
- Aplicar ajustes (solo después de validar manifest y con autorización `APLICAR`):
  ```
  python enforce_dry_run_wrapper.py --script scripts/apply_scale_adjustments.py --args '...' --apply
  ```

16) Comentarios finales y compromiso
------------------------------------
He convertido tu texto y priorities in this version formal del CONTEXT.md.  
Compromiso operativo del asistente:
- No ejecutaré ningún paso mutativo sin tu autorización `APLICAR`.  
- A partir de ahora usaré este CONTEXT.md como la fuente de verdad para proponer cualquier cambio o script.  
- Cuando quieras que ejecute alguno de los pasos urgentes, responde con `APLICAR` y especifica qué paso (por ejemplo: "APLICAR: generar features y entrenar") — yo devolveré el manifest y el comando exacto listo para copiar/ejecutar.
