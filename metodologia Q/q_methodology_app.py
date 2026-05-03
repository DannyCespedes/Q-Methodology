"""
╔══════════════════════════════════════════════════════════════════╗
║          PLATAFORMA DIGITAL - METODOLOGIA Q                     ║
║          Análisis Factorial Q            ║
╚══════════════════════════════════════════════════════════════════╝

Instalación de dependencias:
    pip install streamlit pandas numpy openpyxl factor_analyzer scipy matplotlib seaborn plotly

Ejecución:
    streamlit run q_methodology_app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
import io
import warnings
warnings.filterwarnings("ignore")

# ── Dependencias opcionales ─────────────────────────────────────────
try:
    from factor_analyzer import FactorAnalyzer
    FA_AVAILABLE = True
except ImportError:
    FA_AVAILABLE = False

try:
    from scipy import stats
    from scipy.cluster.hierarchy import linkage, dendrogram
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False

try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import seaborn as sns
    MPL_AVAILABLE = True
except ImportError:
    MPL_AVAILABLE = False

# ════════════════════════════════════════════════════════════════════
#  CONFIGURACIÓN PÁGINA
# ════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Q-Methodology Platform",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS Global ───────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Fuentes ── */
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Playfair+Display:wght@700&family=Source+Sans+3:wght@300;400;600&display=swap');

/* ── Variables ── */
:root {
    --bg:        #0d1117;
    --surface:   #161b22;
    --surface2:  #21262d;
    --border:    #30363d;
    --accent:    #58a6ff;
    --accent2:   #3fb950;
    --accent3:   #d29922;
    --text:      #e6edf3;
    --muted:     #8b949e;
    --danger:    #f85149;
    --radius:    8px;
}

/* ── App background ── */
.stApp { background: var(--bg); color: var(--text); font-family: 'Source Sans 3', sans-serif; }
.main .block-container { padding: 1.5rem 2rem; max-width: 1400px; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--surface);
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: var(--accent);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

/* ── Títulos ── */
h1 { font-family: 'Playfair Display', serif !important; color: var(--text) !important; }
h2 { font-family: 'Source Sans 3', sans-serif !important; color: var(--accent) !important; font-weight: 600 !important; }
h3 { font-family: 'IBM Plex Mono', monospace !important; color: var(--accent2) !important; font-size: 0.9rem !important; letter-spacing: 0.08em !important; }

/* ── Tarjeta Q (sorteo) ── */
.q-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 0.75rem 1rem;
    margin: 0.3rem 0;
    font-size: 0.85rem;
    line-height: 1.4;
    cursor: grab;
    transition: border-color 0.2s, box-shadow 0.2s;
    position: relative;
}
.q-card:hover {
    border-color: var(--accent);
    box-shadow: 0 0 0 1px var(--accent);
}
.q-card .card-id {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    color: var(--muted);
    margin-bottom: 0.3rem;
}

/* ── Columna del tablero ── */
.board-col {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 0.6rem;
    min-height: 120px;
    text-align: center;
}
.board-col-header {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: var(--muted);
    letter-spacing: 0.1em;
    margin-bottom: 0.4rem;
}
.col-full { border-color: var(--danger) !important; }
.col-ok   { border-color: var(--accent2) !important; }

/* ── Badges ── */
.badge {
    display: inline-block;
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.05em;
}
.badge-blue  { background: rgba(88,166,255,0.15); color: var(--accent);  border: 1px solid rgba(88,166,255,0.3); }
.badge-green { background: rgba(63,185,80,0.15);  color: var(--accent2); border: 1px solid rgba(63,185,80,0.3);  }
.badge-amber { background: rgba(210,153,34,0.15); color: var(--accent3); border: 1px solid rgba(210,153,34,0.3); }
.badge-red   { background: rgba(248,81,73,0.15);  color: var(--danger);  border: 1px solid rgba(248,81,73,0.3);  }

/* ── Métricas ── */
div[data-testid="metric-container"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem;
}
div[data-testid="metric-container"] label { color: var(--muted) !important; font-size: 0.75rem !important; }
div[data-testid="metric-container"] div[data-testid="stMetricValue"] { color: var(--accent) !important; font-family: 'IBM Plex Mono', monospace !important; }

/* ── Botones ── */
.stButton > button {
    background: var(--accent);
    color: #0d1117;
    border: none;
    border-radius: var(--radius);
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 600;
    font-size: 0.8rem;
    letter-spacing: 0.05em;
    padding: 0.5rem 1.2rem;
    transition: opacity 0.2s;
}
.stButton > button:hover { opacity: 0.85; }

/* ── Tabs ── */
button[data-baseweb="tab"] {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.08em !important;
}

/* ── DataFrames ── */
.dataframe { font-size: 0.8rem; }

/* ── Info/warning boxes ── */
.stInfo, .stWarning, .stSuccess, .stError { border-radius: var(--radius); font-size: 0.85rem; }

/* ── Header hero ── */
.hero {
    background: linear-gradient(135deg, #161b22 0%, #0d1117 50%, #161b22 100%);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--accent2), var(--accent3));
}
.hero h1 { margin: 0; font-size: 2.2rem; }
.hero .subtitle { color: var(--muted); font-size: 0.9rem; margin-top: 0.5rem; font-family: 'IBM Plex Mono', monospace; }

/* ── Resultados cards ── */
.result-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    border-radius: var(--radius);
    padding: 1rem 1.2rem;
    margin-bottom: 0.6rem;
}
.result-card.positive { border-left-color: var(--accent2); }
.result-card.negative { border-left-color: var(--danger); }
.result-card.consensus { border-left-color: var(--accent3); }
.result-card .zscore { font-family: 'IBM Plex Mono', monospace; font-size: 1.1rem; font-weight: 600; }

/* ── Progress bar override ── */
.stProgress > div > div { background-color: var(--accent); }
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
#  ESTADO DE SESIÓN
# ════════════════════════════════════════════════════════════════════

def init_state():
    defaults = {
        "qset": None,               # DataFrame: id, statement
        "matrix": None,             # DataFrame: participantes × ítems
        "distribution": None,       # dict {valor: cupo}
        "n_columns": 9,
        "sort_results": {},         # {participant_id: {item_id: score}}
        "current_participant": None,
        "factor_results": None,
        "n_factors": 3,
        "rotation": "varimax",
        "step": "home",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ════════════════════════════════════════════════════════════════════
#  DISTRIBUCIONES CUASI-NORMALES ESTÁNDAR
# ════════════════════════════════════════════════════════════════════

DISTRIBUTIONS = {
    9:  {-4:1, -3:2, -2:3, -1:4, 0:5, 1:4, 2:3, 3:2, 4:1},   # 25 ítems
    11: {-5:1, -4:2, -3:3, -2:4, -1:5, 0:6, 1:5, 2:4, 3:3, 4:2, 5:1},  # 36 ítems
    7:  {-3:1, -2:2, -1:3, 0:5, 1:3, 2:2, 3:1},               # 17 ítems (peq)
    13: {-6:1, -5:2, -4:3, -3:4, -2:5, -1:6, 0:7, 1:6, 2:5, 3:4, 4:3, 5:2, 6:1},  # 47 ítems
}

def get_best_distribution(n_items):
    """Retorna la distribución cuasi-normal más adecuada para n_items."""
    for cols, dist in sorted(DISTRIBUTIONS.items()):
        total = sum(dist.values())
        if total >= n_items:
            # Ajustar distribución al n_items exacto
            adjusted = dict(dist)
            diff = total - n_items
            # Reducir desde columna central hacia afuera
            center = 0
            if diff > 0:
                adjusted[center] = max(1, adjusted[center] - diff)
            return cols, adjusted
    # Si n_items > 47, usar distribución de 13 columnas
    cols = 13
    dist = dict(DISTRIBUTIONS[13])
    return cols, dist

def auto_distribution(n_items):
    cols, dist = get_best_distribution(n_items)
    st.session_state["distribution"] = dist
    st.session_state["n_columns"] = cols
    return dist


# ════════════════════════════════════════════════════════════════════
#  SIDEBAR NAVEGACIÓN
# ════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("### 🔬 Q-Platform")
    st.markdown("---")

    nav = st.radio(
        "Navegación",
        ["🏠 Inicio", "📂 Cargar Datos", "🎴 Sorteo Q", "📊 Análisis Factorial", "📋 Informes"],
        index=["🏠 Inicio", "📂 Cargar Datos", "🎴 Sorteo Q", "📊 Análisis Factorial", "📋 Informes"].index(
            {"home":"🏠 Inicio","load":"📂 Cargar Datos","sort":"🎴 Sorteo Q",
             "analysis":"📊 Análisis Factorial","report":"📋 Informes"}.get(st.session_state["step"],"🏠 Inicio")
        ),
        label_visibility="collapsed",
    )

    step_map = {
        "🏠 Inicio": "home",
        "📂 Cargar Datos": "load",
        "🎴 Sorteo Q": "sort",
        "📊 Análisis Factorial": "analysis",
        "📋 Informes": "report",
    }
    st.session_state["step"] = step_map[nav]

    st.markdown("---")
    st.markdown("### Estado del Proyecto")

    if st.session_state["qset"] is not None:
        n = len(st.session_state["qset"])
        st.markdown(f'<span class="badge badge-green">✓ Q-set: {n} ítems</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge badge-red">✗ Sin Q-set</span>', unsafe_allow_html=True)

    if st.session_state["matrix"] is not None:
        p = st.session_state["matrix"].shape[0]
        st.markdown(f'<span class="badge badge-green">✓ Matriz: {p} participantes</span>', unsafe_allow_html=True)
    elif st.session_state["sort_results"]:
        p = len(st.session_state["sort_results"])
        st.markdown(f'<span class="badge badge-amber">⟳ Sorteos: {p}</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge badge-red">✗ Sin matriz</span>', unsafe_allow_html=True)

    if st.session_state["factor_results"] is not None:
        st.markdown('<span class="badge badge-blue">✓ Factores extraídos</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge badge-red">✗ Sin análisis</span>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Librerías")
    libs = {
        "factor_analyzer": FA_AVAILABLE,
        "scipy": SCIPY_AVAILABLE,
        "plotly": PLOTLY_AVAILABLE,
        "matplotlib": MPL_AVAILABLE,
    }
    for lib, ok in libs.items():
        icon = "✓" if ok else "✗"
        cls = "badge-green" if ok else "badge-red"
        st.markdown(f'<span class="badge {cls}">{icon} {lib}</span>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
#  PÁGINA: INICIO
# ════════════════════════════════════════════════════════════════════

if st.session_state["step"] == "home":
    st.markdown("""
    <div class="hero">
        <h1>Metodologia Q<br>Plataforma Digital</h1>
        <div class="subtitle">Análisis factorial de subjetividad · Metodología Q completa</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="result-card">
            <h3>01 — Q-Set</h3>
            <p style="color:#8b949e;font-size:0.85rem;">Carga tus declaraciones desde CSV o Excel. La plataforma configura automáticamente la distribución cuasi-normal.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="result-card positive">
            <h3>02 — Sorteo Digital</h3>
            <p style="color:#8b949e;font-size:0.85rem;">Tablero interactivo donde los participantes clasifican tarjetas respetando los cupos de cada columna en tiempo real.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="result-card consensus">
            <h3>03 — Análisis & Reporte</h3>
            <p style="color:#8b949e;font-size:0.85rem;">Correlación entre personas, extracción de factores PCA/Centroides, rotación Varimax, z-scores e informe completo.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## Flujo de Trabajo")

    flow = [
        ("📂", "Cargar Q-set", "CSV/Excel con las declaraciones a estudiar"),
        ("⚙️", "Configurar distribución", "La plataforma calcula la forma cuasi-normal automáticamente"),
        ("👤", "Participante sortea", "Tablero drag-and-drop con control de cupos"),
        ("💾", "Guardar sorteo", "Se acumula la matriz P×Q automáticamente"),
        ("🔢", "Análisis factorial", "PCA o centroides, rotación Varimax/Manual"),
        ("📋", "Informe final", "Z-scores, declaraciones distintivas, consensos"),
    ]

    cols = st.columns(len(flow))
    for col, (icon, title, desc) in zip(cols, flow):
        with col:
            st.markdown(f"""
            <div style="background:#161b22;border:1px solid #30363d;border-radius:8px;padding:1rem;text-align:center;">
                <div style="font-size:1.8rem;">{icon}</div>
                <div style="font-family:'IBM Plex Mono',monospace;font-size:0.75rem;color:#58a6ff;margin:0.4rem 0;">{title}</div>
                <div style="font-size:0.75rem;color:#8b949e;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.info("💡 **Comenzar**: Ve a **📂 Cargar Datos** en el panel lateral para subir tu Q-set o una matriz de resultados previos.")


# ════════════════════════════════════════════════════════════════════
#  PÁGINA: CARGAR DATOS
# ════════════════════════════════════════════════════════════════════

elif st.session_state["step"] == "load":
    st.markdown("## 📂 Cargar Datos")

    tab1, tab2, tab3 = st.tabs(["📝 Q-Set (Declaraciones)", "🗂️ Matriz de Resultados", "✍️ Entrada Manual"])

    # ── TAB 1: Q-Set ────────────────────────────────────────────────
    with tab1:
        st.markdown("### Cargar Q-Set")
        st.markdown("Sube un archivo **CSV o Excel** con al menos dos columnas: `id` y `statement` (o similares).")

        uploaded_qset = st.file_uploader(
            "Selecciona archivo Q-Set",
            type=["csv", "xlsx", "xls"],
            key="upload_qset",
            help="El archivo debe tener columnas: id (o número) y statement (o declaración/texto)"
        )

        col_ex, col_fmt = st.columns(2)
        with col_ex:
            st.markdown("**Formato esperado:**")
            ex_df = pd.DataFrame({
                "id": [1, 2, 3, 4],
                "statement": [
                    "La tecnología mejora la calidad de vida",
                    "El cambio climático requiere acción inmediata",
                    "La educación es un derecho universal",
                    "El mercado libre resuelve los problemas sociales",
                ]
            })
            st.dataframe(ex_df, use_container_width=True, hide_index=True)

        with col_fmt:
            # Botón para descargar plantilla
            template_csv = ex_df.to_csv(index=False).encode()
            st.download_button(
                "⬇️ Descargar plantilla CSV",
                data=template_csv,
                file_name="plantilla_qset.csv",
                mime="text/csv",
            )

        if uploaded_qset:
            try:
                if uploaded_qset.name.endswith(".csv"):
                    df = pd.read_csv(uploaded_qset)
                else:
                    df = pd.read_excel(uploaded_qset)

                # Normalizar nombres de columnas
                df.columns = [c.strip().lower() for c in df.columns]
                col_map = {}
                for c in df.columns:
                    if c in ["id", "número", "numero", "num", "#", "item"]:
                        col_map[c] = "id"
                    elif c in ["statement", "declaración", "declaracion", "texto", "frase", "enunciado"]:
                        col_map[c] = "statement"
                df = df.rename(columns=col_map)

                if "id" not in df.columns:
                    df.insert(0, "id", range(1, len(df) + 1))
                if "statement" not in df.columns:
                    # Tomar primera columna de texto
                    text_cols = [c for c in df.columns if c != "id"]
                    if text_cols:
                        df = df.rename(columns={text_cols[0]: "statement"})

                df["id"] = df["id"].astype(str)
                df = df[["id", "statement"]].dropna(subset=["statement"])

                st.success(f"✅ Q-Set cargado: **{len(df)} declaraciones**")
                st.dataframe(df, use_container_width=True, hide_index=True)

                if st.button("💾 Confirmar Q-Set", key="confirm_qset"):
                    st.session_state["qset"] = df.reset_index(drop=True)
                    dist = auto_distribution(len(df))
                    total = sum(dist.values())
                    st.success(f"Q-Set guardado. Distribución cuasi-normal configurada: {len(dist)} columnas, {total} cupos")
                    st.balloons()

            except Exception as e:
                st.error(f"Error al leer archivo: {e}")

    # ── TAB 2: Matriz de resultados ──────────────────────────────────
    with tab2:
        st.markdown("### Cargar Matriz de Resultados Previos")
        st.markdown("""
        Sube una **matriz de resultados** donde:
        - Las **filas** representan participantes (P-set)
        - Las **columnas** representan las puntuaciones asignadas a cada ítem Q
        - Los valores son las puntuaciones del sorteo (e.g., -4 a +4)
        """)

        uploaded_matrix = st.file_uploader(
            "Selecciona archivo Matriz",
            type=["csv", "xlsx", "xls"],
            key="upload_matrix"
        )

        ex_matrix = pd.DataFrame(
            np.random.choice(range(-4, 5), size=(4, 6)),
            index=["P01", "P02", "P03", "P04"],
            columns=[f"Q{i}" for i in range(1, 7)]
        )
        st.markdown("**Ejemplo de formato:**")
        st.dataframe(ex_matrix, use_container_width=True)

        if uploaded_matrix:
            try:
                if uploaded_matrix.name.endswith(".csv"):
                    mat = pd.read_csv(uploaded_matrix, index_col=0)
                else:
                    mat = pd.read_excel(uploaded_matrix, index_col=0)

                mat = mat.apply(pd.to_numeric, errors="coerce")
                st.success(f"✅ Matriz cargada: **{mat.shape[0]} participantes × {mat.shape[1]} ítems**")

                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("**Vista previa:**")
                    st.dataframe(mat.head(10), use_container_width=True)
                with col_b:
                    st.markdown("**Estadísticas básicas:**")
                    stats_df = pd.DataFrame({
                        "Métrica": ["Participantes", "Ítems Q", "Mín valor", "Máx valor", "Valores faltantes"],
                        "Valor": [mat.shape[0], mat.shape[1], int(mat.min().min()), int(mat.max().max()), int(mat.isnull().sum().sum())]
                    })
                    st.dataframe(stats_df, use_container_width=True, hide_index=True)

                if st.button("💾 Confirmar Matriz", key="confirm_matrix"):
                    st.session_state["matrix"] = mat
                    # Crear Q-set genérico si no existe
                    if st.session_state["qset"] is None:
                        qset_gen = pd.DataFrame({
                            "id": [str(c) for c in mat.columns],
                            "statement": [f"Ítem {c}" for c in mat.columns]
                        })
                        st.session_state["qset"] = qset_gen
                    st.success("Matriz guardada. Ve a **📊 Análisis Factorial** para continuar.")

            except Exception as e:
                st.error(f"Error al leer archivo: {e}")

    # ── TAB 3: Entrada manual ────────────────────────────────────────
    with tab3:
        st.markdown("### Crear Q-Set Manualmente")

        n_items = st.number_input("Número de declaraciones a ingresar", min_value=9, max_value=60, value=25, step=1)

        with st.form("manual_qset_form"):
            statements = []
            for i in range(int(n_items)):
                s = st.text_input(f"Declaración {i+1}", key=f"manual_stmt_{i}", placeholder=f"Escribe la declaración {i+1}...")
                statements.append(s)

            submitted = st.form_submit_button("💾 Guardar Q-Set Manual")
            if submitted:
                filled = [(str(i+1), s) for i, s in enumerate(statements) if s.strip()]
                if len(filled) < 9:
                    st.error("Debes ingresar al menos 9 declaraciones.")
                else:
                    df_manual = pd.DataFrame(filled, columns=["id", "statement"])
                    st.session_state["qset"] = df_manual
                    auto_distribution(len(df_manual))
                    st.success(f"✅ Q-Set de {len(df_manual)} declaraciones guardado.")


# ════════════════════════════════════════════════════════════════════
#  PÁGINA: SORTEO Q
# ════════════════════════════════════════════════════════════════════

elif st.session_state["step"] == "sort":
    st.markdown("## 🎴 Tablero de Sorteo Q")

    if st.session_state["qset"] is None:
        st.warning("⚠️ Primero debes cargar un Q-Set en la sección **📂 Cargar Datos**.")
        st.stop()

    qset = st.session_state["qset"]
    dist = st.session_state["distribution"]

    if dist is None:
        dist = auto_distribution(len(qset))

    # ── Configuración del participante ──────────────────────────────
    with st.expander("⚙️ Configuración del Sorteo", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            participant_id = st.text_input(
                "ID / Nombre del Participante",
                value=st.session_state.get("current_participant", ""),
                placeholder="P001, Ana García, etc."
            )
        with col2:
            st.markdown("**Distribución cuasi-normal:**")
            dist_str = " · ".join([f"{k}: {v}" for k, v in sorted(dist.items())])
            st.markdown(f'<span class="badge badge-blue">{dist_str}</span>', unsafe_allow_html=True)
            total_slots = sum(dist.values())
            st.markdown(f'<small style="color:#8b949e;">Total cupos: {total_slots} | Ítems: {len(qset)}</small>', unsafe_allow_html=True)
        with col3:
            st.markdown("**Ítems ya clasificados:**")
            current_sort = st.session_state["sort_results"].get(participant_id, {})
            n_sorted = len(current_sort)
            pct = n_sorted / len(qset) * 100 if len(qset) > 0 else 0
            st.metric("Clasificados", f"{n_sorted} / {len(qset)}", f"{pct:.0f}%")

    if not participant_id.strip():
        st.info("👆 Ingresa el ID del participante para comenzar el sorteo.")
        st.stop()

    st.session_state["current_participant"] = participant_id
    if participant_id not in st.session_state["sort_results"]:
        st.session_state["sort_results"][participant_id] = {}

    current_sort = st.session_state["sort_results"][participant_id]
    sorted_values = list(dist.keys())
    sorted_values_s = sorted(sorted_values)

    # ── Calcular cupos disponibles por columna ──────────────────────
    col_counts = {v: 0 for v in sorted_values}
    for item_id, val in current_sort.items():
        if val in col_counts:
            col_counts[val] += 1

    # ── Ítems sin clasificar ─────────────────────────────────────────
    unsorted_items = [row for _, row in qset.iterrows() if str(row["id"]) not in current_sort]

    # ── Instrucciones ────────────────────────────────────────────────
    st.markdown("""
    <div style="background:#161b22;border:1px solid #30363d;border-radius:8px;padding:1rem;margin-bottom:1rem;">
    <strong style="color:#58a6ff;">Instrucciones:</strong>
    <span style="color:#8b949e;font-size:0.85rem;">
    Selecciona un ítem del panel izquierdo y asígnalo a una columna del tablero.
    Cada columna tiene un número máximo de tarjetas. Las columnas con fondo <span style="color:#f85149;">rojo</span>
    están llenas. Las de fondo <span style="color:#3fb950;">verde</span> tienen espacio.
    </span>
    </div>
    """, unsafe_allow_html=True)

    # ── Layout principal ─────────────────────────────────────────────
    left_col, right_col = st.columns([1, 3])

    # Panel izquierdo: ítems sin clasificar
    with left_col:
        st.markdown("### Ítems sin clasificar")
        if unsorted_items:
            selected_item = st.selectbox(
                "Seleccionar ítem",
                options=[f"[{row['id']}] {row['statement'][:60]}{'...' if len(row['statement'])>60 else ''}"
                         for row in unsorted_items],
                key="selected_item_box",
                label_visibility="collapsed"
            )
            # Mostrar tarjeta seleccionada
            if selected_item:
                sel_id = selected_item.split("]")[0].strip("[")
                sel_row = qset[qset["id"] == sel_id].iloc[0]
                st.markdown(f"""
                <div class="q-card">
                    <div class="card-id">ÍTEM {sel_row['id']}</div>
                    {sel_row['statement']}
                </div>
                """, unsafe_allow_html=True)

                # Asignar puntuación
                st.markdown("**Asignar a columna:**")
                assign_col = st.selectbox(
                    "Columna",
                    options=sorted_values_s,
                    format_func=lambda x: f"{'+' if x>0 else ''}{x}  (quedan {max(0, dist[x]-col_counts[x])} cupos)",
                    key="assign_col_box"
                )

                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button("✅ Asignar", key="btn_assign"):
                        remaining = dist[assign_col] - col_counts[assign_col]
                        if remaining <= 0:
                            st.error(f"La columna {assign_col} está llena.")
                        else:
                            st.session_state["sort_results"][participant_id][sel_id] = assign_col
                            st.rerun()
                with col_btn2:
                    if st.button("🔄 Limpiar todo", key="btn_clear"):
                        st.session_state["sort_results"][participant_id] = {}
                        st.rerun()
        else:
            st.success("✅ ¡Todos los ítems clasificados!")

    # Panel derecho: tablero cuasi-normal
    with right_col:
        st.markdown("### Tablero de Distribución")

        n_cols = len(sorted_values_s)
        board_cols = st.columns(n_cols)

        for col_widget, val in zip(board_cols, sorted_values_s):
            cap = dist[val]
            used = col_counts[val]
            is_full = used >= cap
            cls = "col-full" if is_full else ("col-ok" if used > 0 else "")
            val_label = f"+{val}" if val > 0 else str(val)

            with col_widget:
                color = "#f85149" if is_full else ("#3fb950" if used > 0 else "#58a6ff")
                st.markdown(f"""
                <div style="text-align:center;margin-bottom:0.3rem;">
                    <div style="font-family:'IBM Plex Mono',monospace;font-size:1rem;
                                font-weight:700;color:{color};">{val_label}</div>
                    <div style="font-size:0.7rem;color:#8b949e;">{used}/{cap}</div>
                </div>
                """, unsafe_allow_html=True)

                # Mostrar tarjetas en esta columna
                items_in_col = [(iid, v) for iid, v in current_sort.items() if v == val]
                for iid, _ in items_in_col:
                    row_data = qset[qset["id"] == iid]
                    if not row_data.empty:
                        stmt = row_data.iloc[0]["statement"]
                        short = stmt[:40] + "..." if len(stmt) > 40 else stmt
                        st.markdown(f"""
                        <div style="background:#21262d;border:1px solid #30363d;border-radius:6px;
                                    padding:0.4rem 0.5rem;margin:0.2rem 0;font-size:0.7rem;
                                    color:#e6edf3;line-height:1.3;">
                            <span style="color:#8b949e;font-family:'IBM Plex Mono',monospace;
                                         font-size:0.6rem;">[{iid}]</span><br>{short}
                        </div>
                        """, unsafe_allow_html=True)

                # Botones de reasignación para ítems en columna
                for iid, _ in items_in_col:
                    if st.button(f"✖ {iid}", key=f"remove_{iid}_{val}", help="Quitar de esta columna"):
                        del st.session_state["sort_results"][participant_id][iid]
                        st.rerun()

    # ── Guardar sorteo completo ──────────────────────────────────────
    st.markdown("---")
    col_save1, col_save2, col_save3 = st.columns([2, 1, 1])
    with col_save1:
        total_items = len(qset)
        sorted_count = len(current_sort)
        if sorted_count == total_items:
            st.success(f"✅ Sorteo completo: {sorted_count}/{total_items} ítems clasificados")
        else:
            remaining_items = total_items - sorted_count
            st.warning(f"⚠️ Faltan {remaining_items} ítems por clasificar ({sorted_count}/{total_items})")

    with col_save2:
        if st.button("💾 Guardar Sorteo", disabled=(sorted_count < total_items)):
            # Convertir a fila de matriz
            if st.session_state["matrix"] is None:
                # Crear DataFrame
                row_data = {row["id"]: current_sort.get(row["id"], np.nan) for _, row in qset.iterrows()}
                new_row = pd.DataFrame([row_data], index=[participant_id])
                new_row.columns = [str(c) for c in new_row.columns]
                st.session_state["matrix"] = new_row
            else:
                row_data = {str(row["id"]): current_sort.get(row["id"], np.nan) for _, row in qset.iterrows()}
                # Añadir fila
                existing = st.session_state["matrix"]
                new_row = pd.Series(row_data, name=participant_id)
                if participant_id in existing.index:
                    existing.loc[participant_id] = new_row
                else:
                    st.session_state["matrix"] = pd.concat([existing, new_row.to_frame().T])
            st.success(f"✅ Sorteo de '{participant_id}' guardado en la matriz.")

    with col_save3:
        # Exportar sorteo individual
        if current_sort:
            sort_df = pd.DataFrame([
                {"id": k, "statement": qset[qset["id"]==k]["statement"].values[0] if k in qset["id"].values else k, "score": v}
                for k, v in current_sort.items()
            ])
            csv_sort = sort_df.to_csv(index=False).encode()
            st.download_button("⬇️ Exportar sorteo", csv_sort,
                               f"sorteo_{participant_id}.csv", "text/csv")


# ════════════════════════════════════════════════════════════════════
#  PÁGINA: ANÁLISIS FACTORIAL
# ════════════════════════════════════════════════════════════════════

elif st.session_state["step"] == "analysis":
    st.markdown("## 📊 Análisis Factorial Q")

    if st.session_state["matrix"] is None:
        st.warning("⚠️ No hay matriz de datos. Carga una matriz o completa sorteos en **🎴 Sorteo Q**.")
        st.stop()

    mat = st.session_state["matrix"].copy()
    mat = mat.apply(pd.to_numeric, errors="coerce").fillna(0)

    n_p, n_q = mat.shape
    st.markdown(f"**Matriz disponible:** {n_p} participantes × {n_q} ítems Q")

    # ── Configuración del análisis ───────────────────────────────────
    with st.expander("⚙️ Configuración del Análisis", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            n_factors = st.slider("Número de factores", 2, min(8, n_p-1), 3)
        with col2:
            method = st.selectbox("Método de extracción", ["PCA (Componentes Principales)", "Centroides"])
        with col3:
            rotation = st.selectbox("Rotación", ["Varimax", "Manual (sin rotación)", "Oblimin (si FA disponible)"])
        with col4:
            sig_threshold = st.number_input("Umbral significancia (z-score)", value=1.96, step=0.01)

    # ── Matriz de correlación entre personas ─────────────────────────
    st.markdown("### 1. Correlación entre Personas (R-by-Q)")
    corr_matrix = mat.T.corr()

    if PLOTLY_AVAILABLE:
        fig_corr = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns.tolist(),
            y=corr_matrix.index.tolist(),
            colorscale="RdBu",
            zmid=0,
            text=np.round(corr_matrix.values, 2),
            texttemplate="%{text}",
            textfont={"size": 8},
            colorbar=dict(title="r", thickness=12)
        ))
        fig_corr.update_layout(
            template="plotly_dark",
            paper_bgcolor="#161b22",
            plot_bgcolor="#161b22",
            height=max(350, n_p * 30),
            margin=dict(l=10, r=10, t=30, b=10),
            title=dict(text="Matriz de Correlación entre Participantes", font=dict(size=12, color="#8b949e")),
        )
        st.plotly_chart(fig_corr, use_container_width=True)
    else:
        st.dataframe(corr_matrix.round(3), use_container_width=True)

    # ── Extracción de factores ───────────────────────────────────────
    st.markdown("### 2. Extracción de Factores")

    def extract_factors_pca(data, n_factors):
        """PCA sobre la matriz de correlación entre personas (Q-methodology style)."""
        R = data.T.corr().values
        eigenvalues, eigenvectors = np.linalg.eigh(R)
        # Ordenar descendente
        idx = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]
        # Cargas = eigenvectors * sqrt(eigenvalues)
        loadings = eigenvectors[:, :n_factors] * np.sqrt(np.abs(eigenvalues[:n_factors]))
        return loadings, eigenvalues

    def varimax_rotation(loadings, tol=1e-6, max_iter=1000):
        """Rotación Varimax manual."""
        p, k = loadings.shape
        rotation_matrix = np.eye(k)
        for _ in range(max_iter):
            old_matrix = rotation_matrix.copy()
            for i in range(k):
                for j in range(i+1, k):
                    x = loadings @ rotation_matrix
                    u = x[:, i] ** 2 - x[:, j] ** 2
                    v = 2 * x[:, i] * x[:, j]
                    A = np.sum(u)
                    B = np.sum(v)
                    C = np.sum(u**2 - v**2)
                    D = np.sum(u*v)
                    num = D - 2*A*B/p
                    den = C - (A**2 - B**2)/p
                    theta = np.arctan2(num, den) / 4
                    rot = np.eye(k)
                    rot[i, i] = np.cos(theta)
                    rot[j, j] = np.cos(theta)
                    rot[i, j] = -np.sin(theta)
                    rot[j, i] = np.sin(theta)
                    rotation_matrix = rotation_matrix @ rot
            if np.allclose(rotation_matrix, old_matrix, atol=tol):
                break
        return loadings @ rotation_matrix

    if st.button("🚀 Ejecutar Análisis Factorial", key="run_analysis"):
        with st.spinner("Ejecutando análisis..."):
            try:
                # Extracción
                if FA_AVAILABLE and "Oblimin" not in rotation:
                    fa = FactorAnalyzer(n_factors=n_factors, rotation=None, method="principal")
                    fa.fit(mat.T)
                    raw_loadings = fa.loadings_
                    eigenvals = fa.get_eigenvalues()[0]
                else:
                    raw_loadings, eigenvals = extract_factors_pca(mat, n_factors)

                # Rotación
                if "Varimax" in rotation:
                    final_loadings = varimax_rotation(raw_loadings)
                elif "Oblimin" in rotation and FA_AVAILABLE:
                    fa2 = FactorAnalyzer(n_factors=n_factors, rotation="oblimin", method="principal")
                    fa2.fit(mat.T)
                    final_loadings = fa2.loadings_
                else:
                    final_loadings = raw_loadings

                # DataFrame de cargas
                factor_cols = [f"F{i+1}" for i in range(n_factors)]
                loadings_df = pd.DataFrame(final_loadings, index=mat.index, columns=factor_cols)

                # Asignación de participantes a factores
                # Un participante pertenece al factor donde su carga es más alta en valor absoluto
                # y supera el umbral: 1.96/sqrt(n_q) aprox 0.35 típico
                threshold_load = 1.96 / np.sqrt(n_q)
                assignments = []
                for p_id in mat.index:
                    row = loadings_df.loc[p_id]
                    max_load = row.abs().max()
                    if max_load >= threshold_load:
                        assigned = row.abs().idxmax()
                        sign = 1 if row[assigned] >= 0 else -1
                    else:
                        assigned = "Mixto"
                        sign = 1
                    assignments.append({"participant": p_id, "factor": assigned, "max_loading": round(max_load, 3)})

                assignments_df = pd.DataFrame(assignments)

                # Varianza explicada
                var_explained = (final_loadings ** 2).sum(axis=0) / n_p
                communalities = (final_loadings ** 2).sum(axis=1)

                # Z-scores por factor
                # Para cada factor, calcular el sorteo prototipo ponderando los participantes
                zscores_by_factor = {}
                for f in factor_cols:
                    # Participantes que pertenecen a este factor
                    p_in_factor = assignments_df[assignments_df["factor"] == f]["participant"].tolist()
                    if p_in_factor:
                        # Pesos = carga al cuadrado (weight)
                        weights = loadings_df.loc[p_in_factor, f] ** 2
                        weights = weights / weights.sum()
                        # Suma ponderada de sorteos
                        factor_sort = (mat.loc[p_in_factor].multiply(weights, axis=0)).sum()
                        # Z-score
                        mean_sort = factor_sort.mean()
                        std_sort = factor_sort.std()
                        if std_sort > 0:
                            z = (factor_sort - mean_sort) / std_sort
                        else:
                            z = factor_sort * 0
                        zscores_by_factor[f] = z
                    else:
                        zscores_by_factor[f] = pd.Series(np.zeros(n_q), index=mat.columns)

                zscores_df = pd.DataFrame(zscores_by_factor, index=mat.columns)

                # Guardar resultados
                st.session_state["factor_results"] = {
                    "loadings_df": loadings_df,
                    "assignments_df": assignments_df,
                    "var_explained": var_explained,
                    "eigenvalues": eigenvals,
                    "zscores_df": zscores_df,
                    "threshold_load": threshold_load,
                    "n_factors": n_factors,
                    "sig_threshold": sig_threshold,
                    "factor_cols": factor_cols,
                }
                st.success("✅ Análisis completado exitosamente.")

            except Exception as e:
                st.error(f"Error en el análisis: {e}")
                import traceback
                st.code(traceback.format_exc())

    # ── Mostrar resultados si existen ───────────────────────────────
    res = st.session_state.get("factor_results")
    if res:
        loadings_df = res["loadings_df"]
        assignments_df = res["assignments_df"]
        var_explained = res["var_explained"]
        factor_cols = res["factor_cols"]
        zscores_df = res["zscores_df"]

        # Varianza explicada
        st.markdown("### 3. Varianza Explicada")
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            var_df = pd.DataFrame({
                "Factor": factor_cols,
                "Varianza (%)": [round(v*100, 1) for v in var_explained],
                "Varianza Acumulada (%)": [round(sum(var_explained[:i+1])*100, 1) for i in range(len(factor_cols))]
            })
            st.dataframe(var_df, use_container_width=True, hide_index=True)
        with col_v2:
            if PLOTLY_AVAILABLE:
                fig_var = go.Figure()
                fig_var.add_bar(x=factor_cols, y=[v*100 for v in var_explained],
                                marker_color="#58a6ff", name="Varianza")
                fig_var.add_scatter(x=factor_cols, y=[sum(var_explained[:i+1])*100 for i in range(len(factor_cols))],
                                    mode="lines+markers", marker_color="#3fb950", name="Acumulada")
                fig_var.update_layout(template="plotly_dark", paper_bgcolor="#161b22",
                                      plot_bgcolor="#161b22", height=280,
                                      margin=dict(l=10,r=10,t=10,b=10), showlegend=True)
                st.plotly_chart(fig_var, use_container_width=True)

        # Cargas factoriales
        st.markdown("### 4. Cargas Factoriales por Participante")
        styled_load = loadings_df.round(3)
        st.dataframe(styled_load, use_container_width=True)

        # Asignaciones
        st.markdown("### 5. Asignación de Participantes a Factores")
        color_map = {"F1": "badge-blue", "F2": "badge-green", "F3": "badge-amber", "Mixto": "badge-red"}

        col_a1, col_a2 = st.columns([2, 1])
        with col_a1:
            st.dataframe(assignments_df, use_container_width=True, hide_index=True)
        with col_a2:
            for f in factor_cols:
                count = (assignments_df["factor"] == f).sum()
                cls = color_map.get(f, "badge-blue")
                st.markdown(f'<span class="badge {cls}">{f}: {count} participantes</span>', unsafe_allow_html=True)
            mixto = (assignments_df["factor"] == "Mixto").sum()
            if mixto > 0:
                st.markdown(f'<span class="badge badge-red">Sin asignar: {mixto}</span>', unsafe_allow_html=True)

        # Gráfico de cargas
        if PLOTLY_AVAILABLE and len(factor_cols) >= 2:
            st.markdown("### 6. Gráfico de Dispersión de Cargas (F1 vs F2)")
            colors_plot = {"F1":"#58a6ff","F2":"#3fb950","F3":"#d29922","F4":"#f85149","Mixto":"#8b949e"}
            fig_scatter = go.Figure()
            for f in factor_cols + ["Mixto"]:
                mask = assignments_df[assignments_df["factor"] == f]["participant"].tolist()
                if mask:
                    x_vals = loadings_df.loc[mask, factor_cols[0]] if factor_cols[0] in loadings_df.columns else []
                    y_vals = loadings_df.loc[mask, factor_cols[1]] if len(factor_cols) > 1 else []
                    fig_scatter.add_trace(go.Scatter(
                        x=x_vals, y=y_vals,
                        mode="markers+text",
                        text=mask,
                        textposition="top center",
                        marker=dict(size=10, color=colors_plot.get(f, "#8b949e")),
                        name=f
                    ))
            fig_scatter.update_layout(
                template="plotly_dark", paper_bgcolor="#161b22", plot_bgcolor="#161b22",
                height=400, xaxis_title=factor_cols[0], yaxis_title=factor_cols[1],
                margin=dict(l=10,r=10,t=10,b=10)
            )
            # Líneas de referencia
            fig_scatter.add_hline(y=0, line_color="#30363d", line_width=1)
            fig_scatter.add_vline(x=0, line_color="#30363d", line_width=1)
            st.plotly_chart(fig_scatter, use_container_width=True)

        # Z-scores por factor
        st.markdown("### 7. Z-Scores de Ítems por Factor")
        if st.session_state["qset"] is not None:
            qset_ref = st.session_state["qset"].set_index("id")
            zscores_with_stmt = zscores_df.copy()
            zscores_with_stmt.index = zscores_with_stmt.index.astype(str)
            # Añadir declaración
            stmts = []
            for idx in zscores_with_stmt.index:
                if idx in qset_ref.index:
                    stmts.append(qset_ref.loc[idx, "statement"][:60])
                else:
                    stmts.append(str(idx))
            zscores_with_stmt.insert(0, "Declaración", stmts)
            st.dataframe(zscores_with_stmt.round(3), use_container_width=True)
        else:
            st.dataframe(zscores_df.round(3), use_container_width=True)


# ════════════════════════════════════════════════════════════════════
#  PÁGINA: INFORMES
# ════════════════════════════════════════════════════════════════════

elif st.session_state["step"] == "report":
    st.markdown("## 📋 Informe Final")

    res = st.session_state.get("factor_results")
    if res is None:
        st.warning("⚠️ Ejecuta primero el **Análisis Factorial** para generar los informes.")
        st.stop()

    qset = st.session_state["qset"]
    mat = st.session_state["matrix"]
    loadings_df = res["loadings_df"]
    assignments_df = res["assignments_df"]
    zscores_df = res["zscores_df"]
    factor_cols = res["factor_cols"]
    sig_threshold = res.get("sig_threshold", 1.96)
    var_explained = res["var_explained"]

    qset_dict = {}
    if qset is not None:
        for _, row in qset.iterrows():
            qset_dict[str(row["id"])] = row["statement"]

    def get_stmt(item_id):
        return qset_dict.get(str(item_id), f"Ítem {item_id}")

    # ── Resumen ejecutivo ────────────────────────────────────────────
    st.markdown("### Resumen Ejecutivo")
    col_r1, col_r2, col_r3, col_r4 = st.columns(4)
    with col_r1:
        st.metric("Participantes", mat.shape[0] if mat is not None else "N/A")
    with col_r2:
        st.metric("Ítems Q", mat.shape[1] if mat is not None else "N/A")
    with col_r3:
        st.metric("Factores", len(factor_cols))
    with col_r4:
        total_var = round(sum(var_explained)*100, 1)
        st.metric("Varianza Total Explicada", f"{total_var}%")

    st.markdown("---")

    # ── Por cada factor ──────────────────────────────────────────────
    for fi, f in enumerate(factor_cols):
        color_hex = ["#58a6ff","#3fb950","#d29922","#f85149","#a371f7","#ffa657"][fi % 6]

        st.markdown(f"""
        <div style="border-left:3px solid {color_hex};padding:0.5rem 1rem;
                    background:#161b22;border-radius:0 8px 8px 0;margin:1rem 0 0.5rem;">
            <span style="font-family:'Playfair Display',serif;font-size:1.3rem;color:{color_hex};">
                {f} — Perspectiva {fi+1}
            </span>
            <span style="color:#8b949e;font-size:0.85rem;margin-left:1rem;">
                Varianza explicada: {round(var_explained[fi]*100,1)}%
            </span>
        </div>
        """, unsafe_allow_html=True)

        # Participantes en este factor
        p_in_f = assignments_df[assignments_df["factor"] == f]

        col_f1, col_f2 = st.columns([1, 2])
        with col_f1:
            st.markdown("**Participantes:**")
            if not p_in_f.empty:
                for _, row in p_in_f.iterrows():
                    st.markdown(f"""
                    <div style="background:#21262d;border-radius:6px;padding:0.4rem 0.8rem;
                                margin:0.2rem 0;font-size:0.8rem;font-family:'IBM Plex Mono',monospace;">
                        {row['participant']}
                        <span style="color:#8b949e;float:right;">{row['max_loading']:.3f}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown('<span class="badge badge-red">Sin participantes asignados</span>', unsafe_allow_html=True)

        with col_f2:
            # Top declaraciones positivas y negativas
            if f in zscores_df.columns:
                zf = zscores_df[f].copy()
                zf.index = zf.index.astype(str)
                zf_sorted = zf.sort_values(ascending=False)

                col_pos, col_neg = st.columns(2)
                with col_pos:
                    st.markdown(f'<span class="badge badge-green">▲ Más características (+)</span>', unsafe_allow_html=True)
                    for item_id, z in zf_sorted.head(5).items():
                        stmt = get_stmt(item_id)[:70]
                        z_color = "#3fb950" if z >= sig_threshold else "#8b949e"
                        sig_mark = " ★" if z >= sig_threshold else ""
                        st.markdown(f"""
                        <div class="result-card positive" style="padding:0.5rem 0.8rem;margin:0.2rem 0;">
                            <div class="zscore" style="color:{z_color};font-size:0.9rem;">z={z:+.2f}{sig_mark}</div>
                            <div style="font-size:0.75rem;color:#e6edf3;">{stmt}</div>
                        </div>
                        """, unsafe_allow_html=True)
                with col_neg:
                    st.markdown(f'<span class="badge badge-red">▼ Más características (−)</span>', unsafe_allow_html=True)
                    for item_id, z in zf_sorted.tail(5).items():
                        stmt = get_stmt(item_id)[:70]
                        z_color = "#f85149" if z <= -sig_threshold else "#8b949e"
                        sig_mark = " ★" if z <= -sig_threshold else ""
                        st.markdown(f"""
                        <div class="result-card negative" style="padding:0.5rem 0.8rem;margin:0.2rem 0;">
                            <div class="zscore" style="color:{z_color};font-size:0.9rem;">z={z:+.2f}{sig_mark}</div>
                            <div style="font-size:0.75rem;color:#e6edf3;">{stmt}</div>
                        </div>
                        """, unsafe_allow_html=True)

        st.markdown("---")

    # ── Declaraciones Distintivas ────────────────────────────────────
    st.markdown("### Declaraciones Distintivas por Factor")
    st.markdown(f"Umbral de significancia: **|z| ≥ {sig_threshold}**")

    for fi, f in enumerate(factor_cols):
        if f not in zscores_df.columns:
            continue
        zf = zscores_df[f].copy()
        other_factors = [x for x in factor_cols if x != f]

        distinctive_pos = []
        distinctive_neg = []

        for item_id in zf.index:
            z_this = zf[str(item_id)] if str(item_id) in zf.index else 0
            z_others = [zscores_df.loc[item_id, of] for of in other_factors if item_id in zscores_df.index and of in zscores_df.columns]

            # Distintivo positivo: z alto en este factor Y diferente de otros
            if z_this >= sig_threshold:
                if all(z_this - zo >= 1.0 for zo in z_others):
                    distinctive_pos.append((item_id, z_this))
            # Distintivo negativo
            elif z_this <= -sig_threshold:
                if all(zo - z_this >= 1.0 for zo in z_others):
                    distinctive_neg.append((item_id, z_this))

        color_hex = ["#58a6ff","#3fb950","#d29922","#f85149","#a371f7","#ffa657"][fi % 6]
        st.markdown(f'<div style="color:{color_hex};font-family:IBM Plex Mono,monospace;font-size:0.85rem;margin-top:0.8rem;">■ {f} — Declaraciones Distintivas</div>', unsafe_allow_html=True)

        if distinctive_pos or distinctive_neg:
            col_dp, col_dn = st.columns(2)
            with col_dp:
                for item_id, z in sorted(distinctive_pos, key=lambda x: -x[1])[:5]:
                    st.markdown(f"""
                    <div class="result-card positive">
                        <div style="font-family:'IBM Plex Mono',monospace;font-size:0.7rem;color:#8b949e;">
                            [{item_id}] z = {z:+.2f} ★
                        </div>
                        <div style="font-size:0.82rem;">{get_stmt(item_id)}</div>
                    </div>
                    """, unsafe_allow_html=True)
            with col_dn:
                for item_id, z in sorted(distinctive_neg, key=lambda x: x[1])[:5]:
                    st.markdown(f"""
                    <div class="result-card negative">
                        <div style="font-family:'IBM Plex Mono',monospace;font-size:0.7rem;color:#8b949e;">
                            [{item_id}] z = {z:+.2f} ★
                        </div>
                        <div style="font-size:0.82rem;">{get_stmt(item_id)}</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown('<span class="badge badge-amber">Sin declaraciones distintivas identificadas</span>', unsafe_allow_html=True)

    # ── Puntos de Consenso ───────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Puntos de Consenso")
    st.markdown("Declaraciones donde **todos los factores coinciden** en su valoración (sin diferencias significativas entre factores).")

    if len(factor_cols) >= 2:
        consensus_items = []
        for item_id in zscores_df.index:
            z_values = [zscores_df.loc[item_id, f] for f in factor_cols if f in zscores_df.columns]
            if len(z_values) >= 2:
                z_range = max(z_values) - min(z_values)
                z_mean = np.mean(z_values)
                # Consenso: poca variación entre factores y todos en misma dirección
                if z_range < 0.8:
                    consensus_items.append({
                        "item_id": item_id,
                        "z_mean": round(z_mean, 3),
                        "z_range": round(z_range, 3),
                        "statement": get_stmt(item_id)
                    })

        if consensus_items:
            # Separar positivos y negativos
            pos_cons = [c for c in consensus_items if c["z_mean"] > 0.5]
            neg_cons = [c for c in consensus_items if c["z_mean"] < -0.5]
            neutral_cons = [c for c in consensus_items if -0.5 <= c["z_mean"] <= 0.5]

            if pos_cons:
                st.markdown('<span class="badge badge-green">Acuerdo positivo generalizado</span>', unsafe_allow_html=True)
                for c in sorted(pos_cons, key=lambda x: -x["z_mean"])[:5]:
                    st.markdown(f"""
                    <div class="result-card consensus">
                        <div style="font-family:'IBM Plex Mono',monospace;font-size:0.7rem;color:#8b949e;">
                            [{c['item_id']}] z̄={c['z_mean']:+.2f} | Δ={c['z_range']:.2f}
                        </div>
                        <div style="font-size:0.82rem;">{c['statement']}</div>
                    </div>
                    """, unsafe_allow_html=True)

            if neg_cons:
                st.markdown('<span class="badge badge-red">Acuerdo negativo generalizado</span>', unsafe_allow_html=True)
                for c in sorted(neg_cons, key=lambda x: x["z_mean"])[:5]:
                    st.markdown(f"""
                    <div class="result-card" style="border-left-color:#f85149;">
                        <div style="font-family:'IBM Plex Mono',monospace;font-size:0.7rem;color:#8b949e;">
                            [{c['item_id']}] z̄={c['z_mean']:+.2f} | Δ={c['z_range']:.2f}
                        </div>
                        <div style="font-size:0.82rem;">{c['statement']}</div>
                    </div>
                    """, unsafe_allow_html=True)

            if neutral_cons:
                st.markdown('<span class="badge badge-amber">Ítems neutrales compartidos</span>', unsafe_allow_html=True)
                for c in neutral_cons[:3]:
                    st.markdown(f"""
                    <div class="result-card" style="border-left-color:#d29922;">
                        <div style="font-family:'IBM Plex Mono',monospace;font-size:0.7rem;color:#8b949e;">
                            [{c['item_id']}] z̄={c['z_mean']:+.2f} | Δ={c['z_range']:.2f}
                        </div>
                        <div style="font-size:0.82rem;">{c['statement']}</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No se identificaron puntos de consenso claros con los umbrales actuales.")

    # ── Exportar informe completo ────────────────────────────────────
    st.markdown("---")
    st.markdown("### Exportar Datos")

    col_exp1, col_exp2, col_exp3 = st.columns(3)
    with col_exp1:
        # Exportar Z-scores
        z_export = zscores_df.copy()
        z_export.index = z_export.index.astype(str)
        if qset is not None:
            z_export.insert(0, "Declaración", [get_stmt(i) for i in z_export.index])
        csv_z = z_export.round(4).to_csv().encode()
        st.download_button("⬇️ Z-Scores (CSV)", csv_z, "zscores_por_factor.csv", "text/csv")

    with col_exp2:
        # Exportar cargas factoriales
        csv_load = loadings_df.round(4).to_csv().encode()
        st.download_button("⬇️ Cargas Factoriales (CSV)", csv_load, "cargas_factoriales.csv", "text/csv")

    with col_exp3:
        # Exportar asignaciones
        csv_assign = assignments_df.to_csv(index=False).encode()
        st.download_button("⬇️ Asignaciones (CSV)", csv_assign, "asignaciones_factores.csv", "text/csv")

    # ── Informe narrativo en texto ───────────────────────────────────
    st.markdown("### Informe Narrativo Generado")

    narrative = f"""
# INFORME Q-METHODOLOGY
{'='*60}

## Datos del Estudio
- Participantes (P-set): {mat.shape[0] if mat is not None else 'N/A'}
- Declaraciones (Q-set): {mat.shape[1] if mat is not None else 'N/A'}
- Factores extraídos: {len(factor_cols)}
- Varianza total explicada: {round(sum(var_explained)*100, 1)}%
- Umbral de significancia: |z| ≥ {sig_threshold}

## Factores Identificados
"""
    for fi, f in enumerate(factor_cols):
        p_in_f = assignments_df[assignments_df["factor"] == f]["participant"].tolist()
        ve = round(var_explained[fi]*100, 1)
        narrative += f"""
### {f} — Perspectiva {fi+1}
- Varianza explicada: {ve}%
- Participantes: {', '.join(p_in_f) if p_in_f else 'Ninguno'}
"""
        if f in zscores_df.columns:
            zf = zscores_df[f]
            top3 = zf.nlargest(3)
            bot3 = zf.nsmallest(3)
            narrative += "- Top 3 ítems más acordados:\n"
            for iid, z in top3.items():
                narrative += f"  * [{iid}] z={z:+.2f} — {get_stmt(iid)[:80]}\n"
            narrative += "- Top 3 ítems más rechazados:\n"
            for iid, z in bot3.items():
                narrative += f"  * [{iid}] z={z:+.2f} — {get_stmt(iid)[:80]}\n"

    narrative += f"""
## Notas Metodológicas
- Método de extracción: PCA / Factor Analysis
- Rotación aplicada: {res.get('rotation', 'Varimax')}
- Correlaciones calculadas entre personas (by-person factor analysis)
- Los z-scores representan el sorteo prototípico de cada factor
- Declaraciones distintivas: |z| ≥ {sig_threshold} y diferencia entre factores ≥ 1.0

---
Generado por Q-Methodology Digital Platform
"""

    st.text_area("Informe completo (editable)", narrative, height=400)
    report_bytes = narrative.encode("utf-8")
    st.download_button("⬇️ Descargar Informe (.txt)", report_bytes, "informe_q_methodology.txt", "text/plain")
