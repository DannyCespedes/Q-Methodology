# Q-Methodology Digital Platform — Guía de Instalación y Uso

## Requisitos del Sistema
- Python 3.9 o superior
- pip (gestor de paquetes)

## Instalación

### 1. Crear entorno virtual (recomendado)
```bash
python -m venv venv_qmethod
source venv_qmethod/bin/activate        # Linux/macOS
venv_qmethod\Scripts\activate           # Windows
```

### 2. Instalar dependencias
```bash
pip install streamlit pandas numpy openpyxl factor_analyzer scipy matplotlib seaborn plotly
```

**Versiones recomendadas:**
```
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
openpyxl>=3.1.0
factor_analyzer>=0.5.0
scipy>=1.11.0
matplotlib>=3.7.0
seaborn>=0.12.0
plotly>=5.17.0
```

O usa el archivo requirements.txt:
```bash
pip install -r requirements.txt
```

### 3. Ejecutar la aplicación
```bash
streamlit run q_methodology_app.py
```

La aplicación se abrirá automáticamente en `http://localhost:8501`

---

## Flujo de Uso

### Paso 1 — Cargar Q-Set
Ve a **📂 Cargar Datos** → pestaña **Q-Set**.

Formato del CSV/Excel:
```
id,statement
1,La tecnología mejora la calidad de vida
2,El cambio climático requiere acción inmediata
3,...
```
La distribución cuasi-normal se configura automáticamente según el número de ítems.

### Paso 2 — Sorteo Digital (por participante)
Ve a **🎴 Sorteo Q**.
1. Ingresa el ID del participante
2. Selecciona un ítem del panel izquierdo
3. Asígnalo a una columna (la app controla cupos en tiempo real)
4. Repite hasta clasificar todos los ítems
5. Clic en **Guardar Sorteo**

### Paso 3 — O carga matriz de resultados previos
Ve a **📂 Cargar Datos** → pestaña **Matriz de Resultados**.
Carga un Excel/CSV con participantes en filas e ítems en columnas.

### Paso 4 — Análisis Factorial
Ve a **📊 Análisis Factorial**.
1. Configura: número de factores, método (PCA/Centroides), rotación
2. Clic en **Ejecutar Análisis Factorial**
3. Revisa: correlación entre personas, cargas, varianza explicada, z-scores

### Paso 5 — Informe Final
Ve a **📋 Informes**.
- Declaraciones distintivas por factor (|z| ≥ 1.96 por defecto)
- Puntos de consenso entre perspectivas
- Exporta: Z-Scores CSV, Cargas Factoriales CSV, Informe narrativo TXT

---

## Distribuciones Cuasi-Normales Predefinidas

| N° Ítems | Columnas | Distribución |
|----------|----------|--------------|
| ~17      | 7        | 1,2,3,5,3,2,1 |
| ~25      | 9        | 1,2,3,4,5,4,3,2,1 |
| ~36      | 11       | 1,2,3,4,5,6,5,4,3,2,1 |
| ~47      | 13       | 1,2,3,4,5,6,7,6,5,4,3,2,1 |

---

## Notas Metodológicas

- **Correlación by-person**: La matriz de correlación se calcula entre participantes (no entre variables), siguiendo el principio fundamental de la Metodología Q.
- **Extracción PCA**: Aplica eigendecomposición sobre la matriz de correlación entre personas.
- **Rotación Varimax**: Implementación propia + soporte de factor_analyzer.
- **Z-scores**: Calculados ponderando participantes por carga² en cada factor.
- **Declaraciones distintivas**: |z| ≥ 1.96 Y diferencia con otros factores ≥ 1.0.
- **Consenso**: Ítems con Δz < 0.8 entre todos los factores.


**Acceso a repositorio en github**
Username: DannyCespedes
password: VSCodeDaniel