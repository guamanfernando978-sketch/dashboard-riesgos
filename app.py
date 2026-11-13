import os
import re
import datetime
import pandas as pd
import streamlit as st
import plotly.express as px

# -------------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
# -------------------------------------------------------------------------
st.set_page_config(
    page_title="Dashboard Ejecutivo | Gestión de Riesgos Financieros",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------------------
# ESTILO VISUAL CORPORATIVO (PALETA AZUL PIZARRA / ACERO SUAVIZADO)
# -------------------------------------------------------------------------
st.markdown("""
    <style>
    .stApp {
        background-color: #f1f5f9;
        color: #1e293b;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }

    /* Barra lateral azul pizarra sobrio (#1e3a5f) */
    section[data-testid="stSidebar"] {
        background-color: #1e3a5f;
        color: #f8fafc;
    }
    section[data-testid="stSidebar"] > div:first-child {
        padding-top: 0rem;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span {
        color: #f8fafc !important;
    }

    /* Cabecera de perfil en la barra lateral (#2b6cb0) */
    .sidebar-profile {
        background-color: #2b6cb0;
        padding: 1.3rem 1.2rem;
        margin: -1rem -1rem 1.2rem -1rem;
        display: flex;
        align-items: center;
        gap: 12px;
        border-bottom: 1px solid rgba(255,255,255,0.18);
    }
    .sidebar-avatar {
        width: 42px;
        height: 42px;
        border-radius: 50%;
        background-color: #1e3a5f;
        border: 2px solid #e2e8f0;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
        color: #ffffff;
        flex-shrink: 0;
    }
    .sidebar-profile-text h4 {
        margin: 0;
        font-size: 0.92rem;
        font-weight: 700;
        color: #ffffff !important;
        letter-spacing: 0.03em;
    }
    .sidebar-profile-text span {
        font-size: 0.78rem;
        color: #e0f2fe !important;
    }

    /* Menú de navegación en sidebar */
    section[data-testid="stSidebar"] div[role="radiogroup"] > label {
        background-color: transparent;
        padding: 8px 12px;
        border-radius: 6px;
        margin-bottom: 3px;
        transition: background-color 0.2s;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
        background-color: rgba(43, 108, 176, 0.45);
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] > label[data-checked="true"] {
        background-color: #2b6cb0 !important;
        font-weight: 600;
        border-left: 3px solid #93c5fd;
    }

    /* Etiquetas de filtros multiselect en azul acero suave */
    span[data-baseweb="tag"] {
        background-color: #2b6cb0 !important;
        color: #ffffff !important;
        border-radius: 4px !important;
    }
    span[data-baseweb="tag"] span, span[data-baseweb="tag"] svg {
        color: #ffffff !important;
        fill: #ffffff !important;
    }

    /* Encabezado Principal + Tarjeta de Contexto Ejecutivo del Apartado */
    .exec-header-wrapper {
        background-color: #ffffff;
        border-radius: 10px;
        margin-bottom: 1.3rem;
        box-shadow: 0 2px 8px rgba(30, 58, 95, 0.07);
        border: 1px solid #cbd5e1;
        overflow: hidden;
    }
    .exec-title-bar {
        background: linear-gradient(90deg, #1e3a5f 0%, #2b6cb0 100%);
        padding: 0.85rem 1.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .exec-title-bar h2 {
        margin: 0;
        font-size: 1.18rem;
        color: #ffffff !important;
        font-weight: 700;
        letter-spacing: 0.02em;
    }
    .exec-title-badge {
        background-color: rgba(255, 255, 255, 0.16);
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: #ffffff;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
    }
    .exec-context-body {
        padding: 0.9rem 1.5rem;
        background-color: #f8fafc;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 10px;
    }
    .exec-module-info {
        display: flex;
        flex-direction: column;
        gap: 3px;
    }
    .exec-module-tag {
        font-size: 0.75rem;
        font-weight: 700;
        color: #2b6cb0;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .exec-module-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #0f172a;
        margin: 0;
    }
    .exec-module-question {
        font-size: 0.88rem;
        color: #475569;
        font-style: italic;
    }
    .exec-scope-pill {
        background-color: #e2e8f0;
        color: #1e3a5f;
        padding: 6px 14px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
        border-left: 3px solid #2b6cb0;
    }

    /* Tarjetas KPI con cabecera azul suavizado */
    .kpi-card {
        background-color: #ffffff;
        border-radius: 7px;
        box-shadow: 0 2px 6px rgba(30, 58, 95, 0.06);
        border: 1px solid #e2e8f0;
        overflow: hidden;
        margin-bottom: 1rem;
    }
    .kpi-card-header {
        background-color: #2b6cb0;
        color: #ffffff;
        padding: 7px 14px;
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .kpi-card-header.dark {
        background-color: #1e3a5f;
    }
    .kpi-card-body {
        padding: 13px 16px;
    }
    .kpi-sub {
        font-size: 0.78rem;
        color: #64748b;
        margin-bottom: 2px;
    }
    .kpi-val {
        font-size: 1.8rem;
        font-weight: 800;
        color: #1e3a5f;
        line-height: 1.15;
        margin-bottom: 10px;
    }
    .progress-bg {
        width: 100%;
        height: 8px;
        background-color: #e2e8f0;
        border-radius: 4px;
        overflow: hidden;
    }
    .progress-fill {
        height: 100%;
        background-color: #2b6cb0;
    }
    .progress-fill.navy {
        background-color: #1e3a5f;
    }

    /* Encabezado de bloque para gráficos y tablas */
    .panel-header {
        background-color: #1e3a5f;
        color: #ffffff;
        padding: 9px 15px;
        border-radius: 6px 6px 0 0;
        font-size: 0.83rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-top: 0.6rem;
    }
    .panel-header.blue {
        background-color: #2b6cb0;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------------
# DICCIONARIO DE CORRECCIÓN ORTOGRÁFICA Y ESTANDARIZACIÓN
# -------------------------------------------------------------------------
DEFAULT_FILES = [
    'Levantamiento_Requerimientos_Riesgos_Financieros_Riesgo de Credito.xlsx',
    'Levantamiento_Amanda_Heredia_Riesgo_Liquidez_Riesgo Liquidez.xlsx',
    'Levantamiento_Requerimientos_Riesgos_Financieros_Riesgo de Líquidez.xlsx',
    'Levantamiento_Requerimientos_Riesgos_Financieros_Riesgo de recaudación.xlsx',
    'Levantamiento_Requerimientos_Riesgos_Financieros_Riesgo de Mercado.xlsx',
    'Levantamiento_Requerimientos_Riesgos_Financieros_Riesgo de Mercado2.xlsx'
]

PALETA_CORPORATIVA = ['#1e3a5f', '#2b6cb0', '#4299e1', '#0d9488', '#64748b', '#90cdf4']

CORRECCIONES_ORTOGRAFICAS = {
    r'\bCirtico\b': 'Crítico', r'\bcirtico\b': 'crítico',
    r'\bCritico\b': 'Crítico', r'\bcritico\b': 'crítico',
    r'\bGráfio\b': 'Gráfico', r'\bgráfio\b': 'gráfico',
    r'\bExtraacción\b': 'Extracción', r'\bextraacción\b': 'extracción',
    r'\bPawir BI\b': 'Power BI', r'\bPhyton\b': 'Python',
    r'\bsegmnetación\b': 'segmentación', r'\btremestrales\b': 'trimestrales',
    r'\bpresentaciópn\b': 'presentación', r'\bDesacarga\b': 'Descarga',
    r'\bDescraga\b': 'Descarga', r'\bInstituo\b': 'Instituto',
    r'\bManagment\b': 'Management', r'\bPLAIFICADOS\b': 'PLANIFICADOS',
    r'\bVALOES\b': 'VALORES', r'\basisrentes\b': 'asistentes',
    r'\bCapcitación\b': 'Capacitación', r'\bcongráficos\b': 'con gráficos',
    r'\bresúmen\b': 'resumen', r'\bdinámivas\b': 'dinámicas',
    r'\bElavoración\b': 'Elaboración', r'\bElaboracoón\b': 'Elaboración',
    r'\bCVS\b': 'CSV', r'\bMetodologia\b': 'Metodología',
    r'\bCalculo\b': 'Cálculo', r'\bAgrupacion\b': 'Agrupación',
    r'\bRecopilacion\b': 'Recopilación', r'\bInformacion\b': 'Información',
    r'\bLíquidez\b': 'Liquidez', r'\blíquidez\b': 'liquidez'
}

METADATA_MODULOS = {
    "0. Carga y Calidad de Datos": {
        "codigo": "MÓDULO 00 • GOBERNANZA Y CALIDAD",
        "titulo": "Diagnóstico de Carga, Trazabilidad y Completitud",
        "pregunta": "¿Qué tan completos, consistentes y trazables son los formularios levantados por cada subárea?"
    },
    "1. Resumen Ejecutivo": {
        "codigo": "MÓDULO 01 • VISIÓN EJECUTIVA",
        "titulo": "Resumen Ejecutivo del Área de Gestión de Riesgos",
        "pregunta": "¿Cuál es la magnitud operativa, tecnológica y cuantitativa que deberá soportar la plataforma institucional?"
    },
    "2. Procesos Operativos": {
        "codigo": "MÓDULO 02 • OPERACIÓN Y CRITICIDAD",
        "titulo": "Inventario Estandarizado de Procesos Operativos",
        "pregunta": "¿Qué procesos concentran mayor frecuencia de ejecución, riesgo operativo y urgencia de atención?"
    },
    "3. Fuentes y Data Warehouse": {
        "codigo": "MÓDULO 03 • ARQUITECTURA DE DATOS",
        "titulo": "Análisis de Fuentes de Información para el Data Warehouse",
        "pregunta": "¿Qué orígenes de datos, formatos y volúmenes deben consolidarse en el repositorio central?"
    },
    "4. Integraciones y Sistemas": {
        "codigo": "MÓDULO 04 • INTEROPERABILIDAD",
        "titulo": "Estandarización de Integraciones y Sistemas",
        "pregunta": "¿Con qué sistemas internos y externos debe conectarse la solución y qué validaciones requiere TI?"
    },
    "5. Modelos y Cálculos": {
        "codigo": "MÓDULO 05 • ANALÍTICA CUANTITATIVA",
        "titulo": "Inventario de Modelos Financieros y Automatización",
        "pregunta": "¿Qué modelos operan actualmente en hojas de cálculo o scripts aislados y deben estandarizarse?"
    },
    "6. Requerimientos Web y TI": {
        "codigo": "MÓDULO 06 • ALCANCE FUNCIONAL",
        "titulo": "Especificaciones Funcionales, Roles y Seguridad Web",
        "pregunta": "¿Qué módulos, reportes, controles de acceso y trazabilidad esperan los usuarios de la plataforma?"
    },
    "7. Matriz de Priorización MVP": {
        "codigo": "MÓDULO 07 • DECISIÓN ESTRATÉGICA MVP",
        "titulo": "Matriz Multicriterio de Priorización y Alcance MVP",
        "pregunta": "¿Qué procesos deben entrar en la primera versión (MVP) según criticidad, urgencia y exposición operativa?"
    }
}

def corregir_ortografia(texto):
    if not isinstance(texto, str):
        return texto
    res = texto
    for patron, reemplazo in CORRECCIONES_ORTOGRAFICAS.items():
        res = re.sub(patron, reemplazo, res)
    return res

def limpiar_texto(val):
    if pd.isna(val):
        return "Sin respuesta"
    if isinstance(val, (pd.Timestamp, datetime.datetime, datetime.date)):
        return val.strftime('%d/%m/%Y')
    s = str(val).strip()
    if not s or s.lower() == "nan":
        return "Sin respuesta"
    m_fecha = re.match(r'^(\d{4})-(\d{2})-(\d{2})\s+00:00:00$', s)
    if m_fecha:
        return f"{m_fecha.group(3)}/{m_fecha.group(2)}/{m_fecha.group(1)}"
    s_limpio = re.sub(r'\[.*?\]', '', s).strip()
    s_limpio = re.sub(r'\s+', ' ', s_limpio).strip()
    if not s_limpio or s_limpio in ['-', 'N/A', 'n/a']:
        return "Sin respuesta"
    return corregir_ortografia(s_limpio)

def limpiar_prefijo_numerico(texto):
    limpio = re.sub(r'^(Proceso|Fuente|Sistema|Modelo|Cálculo)\s*\d+\s*[:\-]?\s*', '', texto, flags=re.IGNORECASE).strip()
    limpio = re.sub(r'^\d+\.\s*', '', limpio).strip()
    return limpio if limpio else texto

def homologar_subarea(subarea):
    low = subarea.lower()
    if 'liquidez' in low or 'líquidez' in low:
        return "Riesgo de Liquidez"
    if 'crédito' in low or 'credito' in low:
        return "Riesgo de Crédito"
    if 'mercado' in low:
        return "Riesgo de Mercado"
    if 'recaudaci' in low:
        return "Riesgo de Recaudación y Contraparte"
    return subarea

def normalizar_criticidad(val):
    low = str(val).lower()
    if 'crít' in low or 'critic' in low or 'cirtic' in low:
        return "Crítico"
    if 'alt' in low:
        return "Alto"
    if 'medi' in low or 'import' in low:
        return "Medio"
    if 'baj' in low:
        return "Bajo"
    return "Sin respuesta" if val == "Sin respuesta" else val

def normalizar_frecuencia(val):
    if val == "Sin respuesta":
        return "Sin respuesta"
    low = val.lower()
    if 'diari' in low:
        return "Diario"
    if 'seman' in low:
        return "Semanal"
    if 'quincen' in low:
        return "Quincenal"
    if 'mensual' in low:
        return "Mensual"
    if 'trimestr' in low:
        return "Trimestral"
    if 'anual' in low:
        return "Anual"
    return val.capitalize()

def normalizar_formato(val):
    if val == "Sin respuesta":
        return "Sin respuesta"
    low = val.lower()
    if 'excel' in low or '.xlsx' in low or '.xls' in low:
        return "Excel (.xlsx / .xls)"
    if 'csv' in low:
        return "CSV"
    if 'tsv' in low:
        return "TSV"
    if 'sql' in low or 'base de datos' in low:
        return "Base de Datos SQL"
    if 'script' in low or '.r' in low:
        return "Script R"
    return val

def estandarizar_origen_sistema(tipo_raw, nombre_raw):
    low = (tipo_raw + " " + nombre_raw).lower()
    if 'power bi' in low or 'paquetes' in low or 'herramienta' in low or 'r ' in low:
        return "Herramienta Analítica / BI"
    if 'extern' in low or 'bolsa' in low or 'sri' in low or 'scvs' in low or 'biess' in low:
        return "Sistema / Fuente Externa"
    if 'propio' in low or 'intern' in low or 'institucional' in low or 'dnri' in low or 'dnrgc' in low or 'tecnología' in low:
        return "Sistema / Repositorio Interno"
    return "Otro / Por Clasificar"

def estandarizar_conexion_sistema(con_raw):
    if con_raw == "Sin respuesta":
        return "Sin Especificar"
    low = con_raw.lower()
    if 'descarga' in low or 'lectura directa' in low or 'csv' in low or 'tsv' in low or 'excel' in low:
        return "Descarga / Lectura de Archivos"
    if 'sql' in low or 'base de datos' in low or 'modelo de datos' in low:
        return "Conexión Base de Datos / SQL"
    if 'script' in low or 'ejecución' in low:
        return "Ejecución de Scripts"
    if 'repositorio' in low or 'carga' in low or 'nextcloud' in low or 'drive' in low:
        return "Repositorio / Carga Compartida"
    return "Otro Mecanismo"

def clasificar_familia_modelo(nombre_raw, actividad_raw):
    low = (nombre_raw + " " + actividad_raw).lower()
    if 'var' in low or 'renta fija' in low or 'renta variable' in low or 'portafolio' in low:
        return "VaR y Riesgo de Mercado"
    if 'liquidez' in low or 'lcr' in low or 'rcr' in low or 'flujo' in low or 'buffer' in low:
        return "Liquidez y Flujos de Caja"
    if 'mora' in low or 'planilla' in low or 'crédito' in low:
        return "Mora y Riesgo de Crédito"
    if 'cartera vencida' in low or 'recaudación' in low or 'rrc' in low:
        return "Cartera Vencida y Recaudación"
    if 'estrés' in low or 'sensibilidad' in low or 'backtesting' in low or 'montecarlo' in low or 'holt' in low or 'pronóstico' in low:
        return "Proyecciones y Pruebas de Estrés"
    return "Procesamiento y Agregación"

def clasificar_prioridad_mvp(puntaje):
    if puntaje >= 40:
        return "Prioridad crítica"
    elif puntaje >= 35:
        return "Prioridad alta"
    elif puntaje >= 30:
        return "Prioridad media"
    else:
        return "Prioridad baja"

def extraer_campo_clave_valor(df, etiquetas_buscadas):
    for _, row in df.iterrows():
        c0 = str(row.iloc[0]).strip().lower() if pd.notna(row.iloc[0]) else ""
        val_raw = row.iloc[1] if len(row) > 1 else None
        if pd.isna(val_raw):
            continue
        for et in etiquetas_buscadas:
            if et.lower() in c0:
                return limpiar_texto(val_raw)
    return "Sin respuesta"

def tarjeta_kpi(titulo_superior, subtitulo, valor, porcentaje=100, oscuro=False):
    clase_head = "kpi-card-header dark" if oscuro else "kpi-card-header"
    clase_bar = "progress-fill navy" if oscuro else "progress-fill"
    pct = max(0, min(100, int(porcentaje)))
    st.markdown(f"""
        <div class="kpi-card">
            <div class="{clase_head}">{titulo_superior}</div>
            <div class="kpi-card-body">
                <div class="kpi-sub">{subtitulo}</div>
                <div class="kpi-val">{valor}</div>
                <div class="progress-bg">
                    <div class="{clase_bar}" style="width: {pct}%;"></div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

@st.cache_data
def procesar_archivos(lista_archivos):
    colaboradores_data = []
    procesos_data = []
    fuentes_data = []
    sistemas_data = []
    modelos_data = []
    requerimientos_data = []

    for path in lista_archivos:
        filename = os.path.basename(path)
        try:
            xls = pd.ExcelFile(path)
            sheets = xls.sheet_names

            # --- HOJA 1: Info General ---
            if '1. Info General y Preferencias' in sheets:
                df1 = pd.read_excel(path, sheet_name='1. Info General y Preferencias', header=None)
                colab = extraer_campo_clave_valor(df1, ['colaborador', 'responsable'])
                subarea_raw = extraer_campo_clave_valor(df1, ['subárea', 'subarea'])
                subarea = homologar_subarea(subarea_raw)
                cargo = extraer_campo_clave_valor(df1, ['cargo', 'rol'])
                fecha = extraer_campo_clave_valor(df1, ['fecha'])
                capacitacion = extraer_campo_clave_valor(df1, ['tipo de apoyo', 'capacitación requerido'])
                herramientas_sug = extraer_campo_clave_valor(df1, ['funcionalidades clave'])

                colaboradores_data.append({
                    'Archivo': filename,
                    'Colaborador': colab,
                    'Subárea': subarea,
                    'Cargo': cargo,
                    'Fecha': fecha,
                    'Herramientas_Sugeridas': herramientas_sug,
                    'Capacitacion': capacitacion
                })
            else:
                colab, subarea = filename, "Desconocida"

            # --- HOJA 2: Procesos Operativos ---
            if '2. Procesos Operativos' in sheets:
                df2 = pd.read_excel(path, sheet_name='2. Procesos Operativos', header=None)
                if df2.shape[0] > 4:
                    contador_proc = 1
                    for _, row in df2.iloc[4:].iterrows():
                        p_nom = limpiar_texto(row.iloc[0])
                        desc = limpiar_texto(row.iloc[1] if len(row) > 1 else "")
                        if p_nom == "Sin respuesta" or "nombre del proceso" in p_nom.lower():
                            continue
                        if desc == "Sin respuesta" and re.match(r'^Proceso\s*\d+$', p_nom, re.IGNORECASE):
                            continue

                        nombre_base = limpiar_prefijo_numerico(p_nom)
                        nombre_estandar = f"Proceso {contador_proc}: {nombre_base}"
                        contador_proc += 1

                        freq_raw = limpiar_texto(row.iloc[2] if len(row) > 2 else "")
                        crit_raw = limpiar_texto(row.iloc[4] if len(row) > 4 else "")
                        urg_raw = limpiar_texto(row.iloc[6] if len(row) > 6 else "")

                        procesos_data.append({
                            'Archivo': filename,
                            'Colaborador': colab,
                            'Subárea': subarea,
                            'Proceso': nombre_estandar,
                            'Descripcion': desc,
                            'Frecuencia': normalizar_frecuencia(freq_raw),
                            'Tiempo': limpiar_texto(row.iloc[3] if len(row) > 3 else ""),
                            'Criticidad': normalizar_criticidad(crit_raw),
                            'Justificacion': limpiar_texto(row.iloc[5] if len(row) > 5 else ""),
                            'Urgencia_MVP': normalizar_criticidad(urg_raw)
                        })

            # --- HOJA 3: Fuentes y Datos ---
            if '3. Fuentes y Datos' in sheets:
                df3 = pd.read_excel(path, sheet_name='3. Fuentes y Datos', header=None)
                if df3.shape[0] > 4:
                    contador_f = 1
                    for _, row in df3.iloc[4:].iterrows():
                        f_nom = limpiar_texto(row.iloc[0])
                        fmt_raw = limpiar_texto(row.iloc[1] if len(row) > 1 else "")
                        vol_raw = limpiar_texto(row.iloc[2] if len(row) > 2 else "")
                        vars_raw = limpiar_texto(row.iloc[3] if len(row) > 3 else "")
                        if f_nom == "Sin respuesta" or "nombre o sistema" in f_nom.lower():
                            continue
                        if fmt_raw == "Sin respuesta" and vol_raw == "Sin respuesta":
                            continue

                        f_estandar = f"Fuente {contador_f}: {limpiar_prefijo_numerico(f_nom)}"
                        contador_f += 1

                        fuentes_data.append({
                            'Archivo': filename,
                            'Colaborador': colab,
                            'Subárea': subarea,
                            'Fuente': f_estandar,
                            'Formato': normalizar_formato(fmt_raw),
                            'Volumen': vol_raw,
                            'Variables': vars_raw
                        })

            # --- HOJA 4: Integración y Sistemas ---
            if '4. Integración y Sistemas' in sheets:
                df4 = pd.read_excel(path, sheet_name='4. Integración y Sistemas', header=None)
                if df4.shape[0] > 4:
                    contador_s = 1
                    for _, row in df4.iloc[4:].iterrows():
                        s_nom = limpiar_texto(row.iloc[0])
                        tipo_s = limpiar_texto(row.iloc[1] if len(row) > 1 else "")
                        con_s = limpiar_texto(row.iloc[2] if len(row) > 2 else "")
                        rest_s = limpiar_texto(row.iloc[3] if len(row) > 3 else "")
                        obs_s = limpiar_texto(row.iloc[4] if len(row) > 4 else "")
                        if s_nom == "Sin respuesta" or "nombre del sistema" in s_nom.lower():
                            continue
                        if tipo_s == "Sin respuesta" and con_s == "Sin respuesta" and obs_s == "Sin respuesta":
                            continue

                        s_estandar = f"Sistema {contador_s}: {limpiar_prefijo_numerico(s_nom)}"
                        contador_s += 1

                        sistemas_data.append({
                            'Archivo': filename,
                            'Colaborador': colab,
                            'Subárea': subarea,
                            'Sistema': s_estandar,
                            'Categoria_Origen': estandarizar_origen_sistema(tipo_s, s_nom),
                            'Tipo_Sistema_Detalle': tipo_s,
                            'Mecanismo_Conexion': estandarizar_conexion_sistema(con_s),
                            'Conexion_Detalle': con_s,
                            'Restricciones': rest_s,
                            'Observaciones': obs_s
                        })

            # --- HOJA 5: Cálculos y Modelos ---
            if '5. Cálculos y Modelos' in sheets:
                df5 = pd.read_excel(path, sheet_name='5. Cálculos y Modelos', header=None)
                if df5.shape[0] > 4:
                    contador_m = 1
                    for _, row in df5.iloc[4:].iterrows():
                        m_nom = limpiar_texto(row.iloc[0])
                        act_m = limpiar_texto(row.iloc[1] if len(row) > 1 else "")
                        herr_m = limpiar_texto(row.iloc[2] if len(row) > 2 else "")
                        log_m = limpiar_texto(row.iloc[3] if len(row) > 3 else "")
                        auto_m = limpiar_texto(row.iloc[4] if len(row) > 4 else "")
                        if m_nom == "Sin respuesta" or "nombre del cálculo" in m_nom.lower():
                            continue
                        if herr_m == "Sin respuesta" and log_m == "Sin respuesta":
                            continue

                        m_estandar = f"Modelo {contador_m}: {limpiar_prefijo_numerico(m_nom)}"
                        contador_m += 1

                        h_low = herr_m.lower()
                        if 'python' in h_low:
                            herr_cat = "Python"
                        elif 'r' in re.findall(r'\br\b', h_low) or ('script' in h_low and 'r' in h_low):
                            herr_cat = "Excel + R" if 'excel' in h_low else "R"
                        elif 'sql' in h_low:
                            herr_cat = "Excel + SQL" if 'excel' in h_low else "SQL"
                        elif 'excel' in h_low or 'tabla dinamica' in h_low:
                            herr_cat = "Excel"
                        else:
                            herr_cat = herr_m

                        modelos_data.append({
                            'Archivo': filename,
                            'Colaborador': colab,
                            'Subárea': subarea,
                            'Modelo': m_estandar,
                            'Familia_Modelo': clasificar_familia_modelo(m_nom, act_m),
                            'Actividad': act_m,
                            'Herramienta_Principal': herr_cat,
                            'Herramienta_Detalle': herr_m,
                            'Logica': log_m,
                            'Automatizacion': auto_m
                        })

            # --- HOJA 6: Requerimientos Web y TI ---
            if '6. Requerimientos Web y TI' in sheets:
                df6 = pd.read_excel(path, sheet_name='6. Requerimientos Web y TI', header=None)
                for _, row in df6.iterrows():
                    val0 = limpiar_texto(row.iloc[0])
                    val1 = limpiar_texto(row.iloc[1] if df6.shape[1] > 1 else "")
                    if val0 != "Sin respuesta" and val1 != "Sin respuesta" and not val0.upper().startswith("FORMATO"):
                        requerimientos_data.append({
                            'Archivo': filename,
                            'Colaborador': colab,
                            'Subárea': subarea,
                            'Seccion': val0.rstrip(':'),
                            'Detalle': val1
                        })

        except Exception as e:
            st.error(f"Error procesando {filename}: {e}")

    return (
        pd.DataFrame(colaboradores_data),
        pd.DataFrame(procesos_data),
        pd.DataFrame(fuentes_data),
        pd.DataFrame(sistemas_data),
        pd.DataFrame(modelos_data),
        pd.DataFrame(requerimientos_data)
    )

# -------------------------------------------------------------------------
# BARRA LATERAL CON DISEÑO CORPORATIVO SUAVIZADO
# -------------------------------------------------------------------------
st.sidebar.markdown("""
    <div class="sidebar-profile">
        <div class="sidebar-avatar">🏛️</div>
        <div class="sidebar-profile-text">
            <h4>RIESGOS FINANCIEROS</h4>
            <span>Panel Ejecutivo de Diagnóstico</span>
        </div>
    </div>
""", unsafe_allow_html=True)

modo_carga = st.sidebar.radio(
    "ORIGEN DE FORMULARIOS",
    ["Carpeta Local (Por Defecto)", "Subir Archivos Excel (.xlsx)"]
)

archivos_a_procesar = []
if modo_carga == "Carpeta Local (Por Defecto)":
    archivos_a_procesar = [f for f in DEFAULT_FILES if os.path.exists(f)]
else:
    uploaded_files = st.sidebar.file_uploader(
        "Seleccione formularios Excel",
        accept_multiple_files=True,
        type=['xlsx']
    )
    if uploaded_files:
        temp_dir = "temp_uploaded_excel"
        os.makedirs(temp_dir, exist_ok=True)
        for uf in uploaded_files:
            tpath = os.path.join(temp_dir, uf.name)
            with open(tpath, "wb") as f:
                f.write(uf.getbuffer())
            archivos_a_procesar.append(tpath)

if not archivos_a_procesar:
    st.warning("No se encontraron archivos Excel en la carpeta actual. Seleccione 'Subir Archivos Excel (.xlsx)' en el panel izquierdo.")
    st.stop()

df_colab, df_proc, df_fuentes, df_sist, df_modelos, df_req = procesar_archivos(archivos_a_procesar)

st.sidebar.markdown("---")
menu = st.sidebar.radio(
    "NAVEGACIÓN EJECUTIVA",
    [
        "0. Carga y Calidad de Datos",
        "1. Resumen Ejecutivo",
        "2. Procesos Operativos",
        "3. Fuentes y Data Warehouse",
        "4. Integraciones y Sistemas",
        "5. Modelos y Cálculos",
        "6. Requerimientos Web y TI",
        "7. Matriz de Priorización MVP"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**FILTROS GLOBALES**")
subareas_disp = sorted(df_colab['Subárea'].unique().tolist()) if not df_colab.empty else []
filtro_subarea = st.sidebar.multiselect("Subárea", subareas_disp, default=subareas_disp)

colabs_disp = sorted(df_colab[df_colab['Subárea'].isin(filtro_subarea)]['Colaborador'].unique().tolist()) if not df_colab.empty else []
filtro_colab = st.sidebar.multiselect("Colaborador", colabs_disp, default=colabs_disp)

# Aplicar filtros globales
f_colab = df_colab[(df_colab['Subárea'].isin(filtro_subarea)) & (df_colab['Colaborador'].isin(filtro_colab))]
f_proc = df_proc[(df_proc['Subárea'].isin(filtro_subarea)) & (df_proc['Colaborador'].isin(filtro_colab))]
f_fuentes = df_fuentes[(df_fuentes['Subárea'].isin(filtro_subarea)) & (df_fuentes['Colaborador'].isin(filtro_colab))]
f_sist = df_sist[(df_sist['Subárea'].isin(filtro_subarea)) & (df_sist['Colaborador'].isin(filtro_colab))]
f_modelos = df_modelos[(df_modelos['Subárea'].isin(filtro_subarea)) & (df_modelos['Colaborador'].isin(filtro_colab))]
f_req = df_req[(df_req['Subárea'].isin(filtro_subarea)) & (df_req['Colaborador'].isin(filtro_colab))]

# -------------------------------------------------------------------------
# ENCABEZADO EJECUTIVO DINÁMICO (CON CONTEXTO DEL APARTADO ACTUAL)
# -------------------------------------------------------------------------
meta = METADATA_MODULOS.get(menu, {"codigo": "", "titulo": menu, "pregunta": ""})
alcance_txt = f"{len(filtro_subarea)} Subáreas • {len(filtro_colab)} Colaboradores"

st.markdown(f"""
    <div class="exec-header-wrapper">
        <div class="exec-title-bar">
            <h2>SISTEMA DE DIAGNÓSTICO DE REQUERIMIENTOS — GESTIÓN DE RIESGOS FINANCIEROS</h2>
            <div class="exec-title-badge">ARQUITECTURA ON-PREMISE & MVP</div>
        </div>
        <div class="exec-context-body">
            <div class="exec-module-info">
                <span class="exec-module-tag">{meta['codigo']}</span>
                <h3 class="exec-module-title">{meta['titulo']}</h3>
                <span class="exec-module-question">Pregunta de gestión: {meta['pregunta']}</span>
            </div>
            <div class="exec-scope-pill">
                Alcance activo: {alcance_txt}
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------------
# MÓDULO 0: CARGA Y CALIDAD
# -------------------------------------------------------------------------
if menu == "0. Carga y Calidad de Datos":
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        tarjeta_kpi("FORMULARIOS", "Archivos válidos procesados", len(f_colab), 100, oscuro=False)
    with c2:
        tarjeta_kpi("COBERTURA", "Subáreas homologadas", f_colab['Subárea'].nunique(), 100, oscuro=True)
    with c3:
        tarjeta_kpi("OPERACIÓN", "Procesos inventariados", len(f_proc), 88, oscuro=False)
    with c4:
        tarjeta_kpi("ANALÍTICA", "Modelos registrados", len(f_modelos), 85, oscuro=True)

    st.markdown('<div class="panel-header">DIRECTORIO DE COLABORADORES Y PERFIL DE ADOPCIÓN TECNOLÓGICA</div>', unsafe_allow_html=True)
    st.dataframe(
        f_colab[['Colaborador', 'Subárea', 'Cargo', 'Fecha', 'Herramientas_Sugeridas', 'Capacitacion']],
        use_container_width=True,
        hide_index=True
    )

# -------------------------------------------------------------------------
# MÓDULO 1: RESUMEN EJECUTIVO
# -------------------------------------------------------------------------
elif menu == "1. Resumen Ejecutivo":
    criticos = len(f_proc[f_proc['Criticidad'] == 'Crítico'])
    pct_crit = round((criticos / len(f_proc)) * 100) if len(f_proc) else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        tarjeta_kpi("EQUIPO TÉCNICO", "Colaboradores / Subáreas", f"{len(f_colab)} / {f_colab['Subárea'].nunique()}", 100, oscuro=False)
    with c2:
        tarjeta_kpi("PROCESOS CRÍTICOS", "Tasa de criticidad alta", f"{pct_crit}% ({criticos})", pct_crit, oscuro=True)
    with c3:
        tarjeta_kpi("DATA WAREHOUSE", "Fuentes / Sistemas", f"{len(f_fuentes)} / {len(f_sist)}", 82, oscuro=False)
    with c4:
        tarjeta_kpi("AUTOMATIZACIÓN", "Modelos / Req. Web TI", f"{len(f_modelos)} / {len(f_req)}", 90, oscuro=True)

    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown('<div class="panel-header dark">DISTRIBUCIÓN DE PROCESOS OPERATIVOS POR SUBÁREA</div>', unsafe_allow_html=True)
        if not f_proc.empty:
            df_sub = f_proc.groupby('Subárea').size().reset_index(name='Cantidad').sort_values('Cantidad', ascending=True)
            fig = px.bar(
                df_sub, x='Cantidad', y='Subárea', orientation='h', text='Cantidad',
                color='Subárea', color_discrete_sequence=PALETA_CORPORATIVA
            )
            fig.update_traces(textposition='outside')
            fig.update_layout(
                showlegend=False, plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                margin=dict(t=20, b=20, l=10, r=30), height=340, yaxis_title=""
            )
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="panel-header blue">NIVEL DE CRITICIDAD OPERATIVA</div>', unsafe_allow_html=True)
        if not f_proc.empty:
            df_crit = f_proc.groupby('Criticidad').size().reset_index(name='Cantidad')
            fig2 = px.pie(
                df_crit, names='Criticidad', values='Cantidad', hole=0.58,
                color='Criticidad',
                color_discrete_map={'Crítico': '#1e3a5f', 'Alto': '#2b6cb0', 'Medio': '#63b3ed', 'Bajo': '#cbd5e1'}
            )
            fig2.update_traces(textposition='inside', textinfo='percent+label')
            fig2.update_layout(
                plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                margin=dict(t=20, b=20, l=10, r=10), height=340,
                legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig2, use_container_width=True)

# -------------------------------------------------------------------------
# MÓDULO 2: PROCESOS OPERATIVOS
# -------------------------------------------------------------------------
elif menu == "2. Procesos Operativos":
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        freqs = ["Todas"] + sorted([x for x in f_proc['Frecuencia'].unique().tolist() if x != "Sin respuesta"])
        sel_freq = st.selectbox("Filtrar por Frecuencia:", freqs)
    with col_f2:
        crits = ["Todas"] + sorted([x for x in f_proc['Criticidad'].unique().tolist() if x != "Sin respuesta"])
        sel_crit = st.selectbox("Filtrar por Criticidad:", crits)

    df_p = f_proc.copy()
    if sel_freq != "Todas":
        df_p = df_p[df_p['Frecuencia'] == sel_freq]
    if sel_crit != "Todas":
        df_p = df_p[df_p['Criticidad'] == sel_crit]

    c1, c2 = st.columns([3, 2])
    with c1:
        st.markdown('<div class="panel-header dark">MATRIZ: CRITICIDAD VS. URGENCIA MVP</div>', unsafe_allow_html=True)
        if not df_p.empty:
            cross = pd.crosstab(df_p['Criticidad'], df_p['Urgencia_MVP'], margins=True, margins_name="Total")
            st.dataframe(cross, use_container_width=True)
    with c2:
        st.markdown('<div class="panel-header blue">CARGA DE PROCESOS POR COLABORADOR</div>', unsafe_allow_html=True)
        if not df_p.empty:
            df_c = df_p.groupby(['Colaborador', 'Subárea']).size().reset_index(name='Procesos').sort_values('Procesos', ascending=False)
            st.dataframe(df_c, use_container_width=True, hide_index=True)

    st.markdown('<div class="panel-header">INVENTARIO ESTANDARIZADO DE PROCESOS OPERATIVOS</div>', unsafe_allow_html=True)
    st.dataframe(
        df_p[['Subárea', 'Colaborador', 'Proceso', 'Descripcion', 'Frecuencia', 'Tiempo', 'Criticidad', 'Urgencia_MVP']],
        use_container_width=True,
        hide_index=True
    )

# -------------------------------------------------------------------------
# MÓDULO 3: FUENTES Y DATA WAREHOUSE
# -------------------------------------------------------------------------
elif menu == "3. Fuentes y Data Warehouse":
    c1, c2, c3 = st.columns(3)
    with c1:
        tarjeta_kpi("FUENTES TOTALES", "Orígenes registrados", len(f_fuentes), 100, oscuro=False)
    with c2:
        tarjeta_kpi("COBERTURA", "Subáreas con fuentes", f_fuentes['Subárea'].nunique(), 100, oscuro=True)
    with c3:
        tarjeta_kpi("ESTANDARIZACIÓN", "Formatos identificados", f_fuentes['Formato'].nunique(), 75, oscuro=False)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="panel-header dark">DISTRIBUCIÓN POR FORMATO DE ENTRADA</div>', unsafe_allow_html=True)
        if not f_fuentes.empty:
            df_fmt = f_fuentes.groupby('Formato').size().reset_index(name='Cantidad').sort_values('Cantidad', ascending=True)
            fig = px.bar(
                df_fmt, x='Cantidad', y='Formato', orientation='h', text='Cantidad',
                color='Formato', color_discrete_sequence=PALETA_CORPORATIVA
            )
            fig.update_traces(textposition='outside')
            fig.update_layout(showlegend=False, plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', yaxis_title="", margin=dict(t=20, b=20, r=30))
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="panel-header blue">FUENTES DE DATOS POR SUBÁREA</div>', unsafe_allow_html=True)
        if not f_fuentes.empty:
            df_fsub = f_fuentes.groupby('Subárea').size().reset_index(name='Cantidad').sort_values('Cantidad', ascending=True)
            fig2 = px.bar(
                df_fsub, x='Cantidad', y='Subárea', orientation='h', text='Cantidad',
                color='Subárea', color_discrete_sequence=PALETA_CORPORATIVA
            )
            fig2.update_traces(textposition='outside')
            fig2.update_layout(showlegend=False, plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', yaxis_title="", margin=dict(t=20, b=20, r=30))
            st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="panel-header">CATÁLOGO CONSOLIDADO DE FUENTES PARA EL DATA WAREHOUSE</div>', unsafe_allow_html=True)
    st.dataframe(
        f_fuentes[['Subárea', 'Colaborador', 'Fuente', 'Formato', 'Volumen', 'Variables']],
        use_container_width=True,
        hide_index=True
    )

# -------------------------------------------------------------------------
# MÓDULO 4: INTEGRACIONES Y SISTEMAS
# -------------------------------------------------------------------------
elif menu == "4. Integraciones y Sistemas":
    pendientes_ti = len(f_sist[f_sist['Conexion_Detalle'].str.lower().str.contains("ti|habilit|confirm", na=False)])
    externos_cnt = len(f_sist[f_sist['Categoria_Origen'] == "Sistema / Fuente Externa"])

    c1, c2, c3 = st.columns(3)
    with c1:
        tarjeta_kpi("INTEROPERABILIDAD", "Sistemas estandarizados", len(f_sist), 100, oscuro=False)
    with c2:
        tarjeta_kpi("FUENTES EXTERNAS", "Entidades / Portales externos", externos_cnt, round((externos_cnt/len(f_sist))*100) if len(f_sist) else 0, oscuro=True)
    with c3:
        tarjeta_kpi("VALIDACIÓN TÉCNICA", "Sujetos a habilitación TI", pendientes_ti, round((pendientes_ti/len(f_sist))*100) if len(f_sist) else 0, oscuro=False)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="panel-header dark">CLASIFICACIÓN POR CATEGORÍA DE ORIGEN</div>', unsafe_allow_html=True)
        if not f_sist.empty:
            df_cat_s = f_sist.groupby('Categoria_Origen').size().reset_index(name='Cantidad').sort_values('Cantidad', ascending=True)
            fig = px.bar(
                df_cat_s, x='Cantidad', y='Categoria_Origen', orientation='h', text='Cantidad',
                color='Categoria_Origen', color_discrete_sequence=PALETA_CORPORATIVA
            )
            fig.update_traces(textposition='outside')
            fig.update_layout(showlegend=False, plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', yaxis_title="", margin=dict(t=20, b=20, r=30), height=280)
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="panel-header blue">MECANISMOS DE CONEXIÓN ESTANDARIZADOS</div>', unsafe_allow_html=True)
        if not f_sist.empty:
            df_con_s = f_sist.groupby('Mecanismo_Conexion').size().reset_index(name='Cantidad').sort_values('Cantidad', ascending=True)
            fig2 = px.bar(
                df_con_s, x='Cantidad', y='Mecanismo_Conexion', orientation='h', text='Cantidad',
                color='Mecanismo_Conexion', color_discrete_sequence=PALETA_CORPORATIVA
            )
            fig2.update_traces(textposition='outside')
            fig2.update_layout(showlegend=False, plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', yaxis_title="", margin=dict(t=20, b=20, r=30), height=280)
            st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="panel-header">INVENTARIO ESTANDARIZADO DE INTEGRACIONES Y SISTEMAS</div>', unsafe_allow_html=True)
    st.dataframe(
        f_sist[['Subárea', 'Colaborador', 'Sistema', 'Categoria_Origen', 'Mecanismo_Conexion', 'Conexion_Detalle', 'Restricciones', 'Observaciones']],
        use_container_width=True,
        hide_index=True
    )

# -------------------------------------------------------------------------
# MÓDULO 5: MODELOS Y CÁLCULOS
# -------------------------------------------------------------------------
elif menu == "5. Modelos y Cálculos":
    con_auto = len(f_modelos[f_modelos['Automatizacion'] != "Sin respuesta"])
    en_r_py = len(f_modelos[f_modelos['Herramienta_Principal'].str.lower().str.contains("r|python|sql", na=False)])

    c1, c2, c3 = st.columns(3)
    with c1:
        tarjeta_kpi("INVENTARIO CUANTITATIVO", "Modelos estandarizados", len(f_modelos), 100, oscuro=False)
    with c2:
        tarjeta_kpi("AUTOMATIZACIÓN", "Con solicitud de automatización", con_auto, round((con_auto/len(f_modelos))*100) if len(f_modelos) else 0, oscuro=True)
    with c3:
        tarjeta_kpi("CÓDIGO / BD", "Uso de R, Python o SQL", en_r_py, round((en_r_py/len(f_modelos))*100) if len(f_modelos) else 0, oscuro=False)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="panel-header dark">MODELOS POR FAMILIA METODOLÓGICA</div>', unsafe_allow_html=True)
        if not f_modelos.empty:
            df_fam = f_modelos.groupby('Familia_Modelo').size().reset_index(name='Cantidad').sort_values('Cantidad', ascending=True)
            fig_f = px.bar(
                df_fam, x='Cantidad', y='Familia_Modelo', orientation='h', text='Cantidad',
                color='Familia_Modelo', color_discrete_sequence=PALETA_CORPORATIVA
            )
            fig_f.update_traces(textposition='outside')
            fig_f.update_layout(showlegend=False, plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', yaxis_title="", margin=dict(t=20, b=20, r=30), height=320)
            st.plotly_chart(fig_f, use_container_width=True)

    with col2:
        st.markdown('<div class="panel-header blue">HERRAMIENTAS DE CÁLCULO POR SUBÁREA</div>', unsafe_allow_html=True)
        if not f_modelos.empty:
            df_mod_sub = f_modelos.groupby(['Subárea', 'Herramienta_Principal']).size().reset_index(name='Cantidad')
            fig = px.bar(
                df_mod_sub, x='Subárea', y='Cantidad', color='Herramienta_Principal', barmode='group',
                text='Cantidad', color_discrete_sequence=PALETA_CORPORATIVA
            )
            fig.update_traces(textposition='outside')
            fig.update_layout(plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', legend_title="Herramienta", margin=dict(t=20, b=20), height=320)
            st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="panel-header">CATÁLOGO ESTANDARIZADO DE MODELOS Y LÓGICA DE CÁLCULO</div>', unsafe_allow_html=True)
    st.dataframe(
        f_modelos[['Subárea', 'Colaborador', 'Modelo', 'Familia_Modelo', 'Herramienta_Principal', 'Actividad', 'Logica', 'Automatizacion']],
        use_container_width=True,
        hide_index=True
    )

# -------------------------------------------------------------------------
# MÓDULO 6: REQUERIMIENTOS WEB Y TI
# -------------------------------------------------------------------------
elif menu == "6. Requerimientos Web y TI":
    secciones_disp = ["Todas"] + sorted(f_req['Seccion'].unique().tolist()) if not f_req.empty else ["Todas"]
    sel_sec = st.selectbox("Filtrar por Categoría de Requerimiento:", secciones_disp)

    df_r = f_req.copy()
    if sel_sec != "Todas":
        df_r = df_r[df_r['Seccion'] == sel_sec]

    st.markdown('<div class="panel-header">ESPECIFICACIONES FUNCIONALES, SEGURIDAD Y ROLES DE PLATAFORMA</div>', unsafe_allow_html=True)
    st.dataframe(
        df_r[['Subárea', 'Colaborador', 'Seccion', 'Detalle']],
        use_container_width=True,
        hide_index=True
    )

# -------------------------------------------------------------------------
# MÓDULO 7: MATRIZ DE PRIORIZACIÓN MVP
# -------------------------------------------------------------------------
elif menu == "7. Matriz de Priorización MVP":
    st.sidebar.markdown("---")
    st.sidebar.markdown("**PESOS DEL MODELO MVP**")
    w_crit = st.sidebar.slider("Peso Criticidad Operativa", 1, 5, 4)
    w_urg = st.sidebar.slider("Peso Urgencia MVP", 1, 5, 3)
    w_freq = st.sidebar.slider("Peso Frecuencia / Exposición", 1, 5, 2)

    if not f_proc.empty:
        df_prio = f_proc.copy()
        mapa_puntaje = {'Crítico': 5, 'Alto': 4, 'Medio': 2, 'Bajo': 1, 'Sin respuesta': 0}
        mapa_freq = {'Diario': 5, 'Semanal': 4, 'Quincenal': 3, 'Mensual': 2, 'Trimestral': 1, 'Anual': 1, 'Sin respuesta': 0}

        df_prio['Pts_Criticidad'] = df_prio['Criticidad'].map(mapa_puntaje).fillna(0)
        df_prio['Pts_Urgencia'] = df_prio['Urgencia_MVP'].map(mapa_puntaje).fillna(0)
        df_prio['Pts_Frecuencia'] = df_prio['Frecuencia'].map(mapa_freq).fillna(1)

        df_prio['Score_Criticidad'] = df_prio['Pts_Criticidad'] * w_crit
        df_prio['Score_Urgencia'] = df_prio['Pts_Urgencia'] * w_urg
        df_prio['Score_Frecuencia'] = df_prio['Pts_Frecuencia'] * w_freq
        df_prio['Puntaje_MVP'] = df_prio['Score_Criticidad'] + df_prio['Score_Urgencia'] + df_prio['Score_Frecuencia']
        df_prio['Nivel_Prioridad'] = df_prio['Puntaje_MVP'].apply(clasificar_prioridad_mvp)

        # Resumen ejecutivo por Nivel de Prioridad
        p_critica = len(df_prio[df_prio['Nivel_Prioridad'] == "Prioridad crítica"])
        p_alta = len(df_prio[df_prio['Nivel_Prioridad'] == "Prioridad alta"])
        p_media = len(df_prio[df_prio['Nivel_Prioridad'] == "Prioridad media"])
        p_baja = len(df_prio[df_prio['Nivel_Prioridad'] == "Prioridad baja"])

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            tarjeta_kpi("PRIORIDAD CRÍTICA (40–42)", "Ingreso inmediato al MVP", p_critica, round((p_critica/len(df_prio))*100), oscuro=True)
        with c2:
            tarjeta_kpi("PRIORIDAD ALTA (35–39)", "Alta relevancia operativa", p_alta, round((p_alta/len(df_prio))*100), oscuro=False)
        with c3:
            tarjeta_kpi("PRIORIDAD MEDIA (30–34)", "Segunda ola / consolidación", p_media, round((p_media/len(df_prio))*100), oscuro=True)
        with c4:
            tarjeta_kpi("PRIORIDAD BAJA (< 30)", "Mantenimiento / posterior", p_baja, round((p_baja/len(df_prio))*100), oscuro=False)

        # Documentación Metodológica Defendible ante Gerencia
        with st.expander("📘 Metodología de Puntuación, Escalas y Criterios de Clasificación (Documentación Técnica)"):
            st.markdown("""
            **1. Fórmula del Puntaje Ponderado MVP:**
            $$\\text{Puntaje MVP} = (\\text{Pts. Criticidad} \\times w_1) + (\\text{Pts. Urgencia} \\times w_2) + (\\text{Pts. Frecuencia} \\times w_3)$$
            Con los pesos institucionales sugeridos por defecto ($w_1=4, w_2=3, w_3=2$), el puntaje máximo posible es **45 puntos** (y **42 puntos** para procesos críticos de ejecución semanal/mensual).

            **2. Definición y Escala de Componentes (1 a 5):**
            * **Criticidad Operativa ($w_1$):** Mide el impacto regulatorio, financiero o normativo si el proceso falla o se retrasa (`Crítico = 5`, `Alto = 4`, `Medio = 2`, `Bajo = 1`).
            * **Urgencia para el MVP ($w_2$):** Mide la necesidad declarada por el área de contar con el proceso automatizado desde la primera versión (`Crítico = 5`, `Alto = 4`, `Medio = 2`, `Bajo = 1`).
            * **Frecuencia / Exposición Operativa ($w_3$):** Representa tanto la **periodicidad de ejecución** como la **exposición recurrente al riesgo operativo manual** (`Diario = 5`, `Semanal = 4`, `Quincenal = 3`, `Mensual = 2`, `Trimestral/Anual = 1`). A mayor frecuencia, mayor acumulación de horas-hombre y exposición a errores de digitación.

            **3. Clasificación Automática por Rangos (Propuesta Inicial):**
            * **40 – 42 puntos (`Prioridad crítica`):** Procesos esenciales con exposición diaria/semanal o urgencia máxima.
            * **35 – 39 puntos (`Prioridad alta`):** Procesos críticos mensuales con alta urgencia de automatización.
            * **30 – 34 puntos (`Prioridad media`):** Procesos relevantes de soporte o periodicidad intermedia.
            * **Menos de 30 puntos (`Prioridad baja`):** Procesos de menor criticidad relativa o baja recurrencia.

            > *Nota de Gobernanza: Estos rangos y ponderaciones constituyen una propuesta técnica inicial para la discusión ejecutiva y deberán ser validados y aprobados formalmente conforme a la metodología institucional de Gestión de Riesgos.*
            """)

        # Filtro por Nivel de Prioridad
        niveles_disp = ["Todos", "Prioridad crítica", "Prioridad alta", "Prioridad media", "Prioridad baja"]
        sel_nivel = st.selectbox("Filtrar Tabla por Clasificación de Prioridad:", niveles_disp)

        # Ordenamiento encabezado por Angela Pérez en primer lugar
        df_prio['Prioridad_Lider'] = df_prio['Colaborador'].apply(lambda x: 0 if 'angela' in x.lower() else 1)
        df_prio = df_prio.sort_values(by=['Prioridad_Lider', 'Puntaje_MVP', 'Pts_Frecuencia'], ascending=[True, False, False])

        df_tabla_prio = df_prio if sel_nivel == "Todos" else df_prio[df_prio['Nivel_Prioridad'] == sel_nivel]

        st.markdown('<div class="panel-header dark">RANKING CLASIFICADO DE PROCESOS PARA EL MVP</div>', unsafe_allow_html=True)
        st.dataframe(
            df_tabla_prio[['Nivel_Prioridad', 'Puntaje_MVP', 'Subárea', 'Colaborador', 'Proceso', 'Frecuencia', 'Criticidad', 'Urgencia_MVP']],
            use_container_width=True,
            hide_index=True,
            height=380
        )

        # Selección balanceada para Top 15 (muestra los mejores de cada colaborador/subárea)
        df_bal = df_prio.sort_values(by=['Puntaje_MVP', 'Prioridad_Lider', 'Pts_Frecuencia'], ascending=[False, True, False]).copy()
        df_bal['Rank_Colaborador'] = df_bal.groupby('Colaborador').cumcount()
        df_bal = df_bal.sort_values(by=['Rank_Colaborador', 'Puntaje_MVP', 'Prioridad_Lider'], ascending=[True, False, True])
        top15_bal = df_bal.head(15).sort_values(by=['Puntaje_MVP', 'Prioridad_Lider'], ascending=[False, True])

        # Gráfico 1 a ancho completo para evitar compresión horizontal
        st.markdown('<div class="panel-header blue">TOP 15 PROCESOS PRIORITARIOS BALANCEADOS POR SUBÁREA Y COLABORADOR</div>', unsafe_allow_html=True)
        top15_plot = top15_bal.copy()
        top15_plot['Proceso_Corto'] = top15_plot['Proceso'].apply(lambda x: x[:58] + "..." if len(x) > 61 else x)
        top15_plot['Etiqueta'] = top15_plot['Colaborador'].apply(lambda x: x.split()[0]) + " (" + top15_plot['Subárea'].str.replace("Riesgo de ", "") + ") — " + top15_plot['Proceso_Corto']
        top15_plot = top15_plot.iloc[::-1]

        df_melt = top15_plot.melt(
            id_vars=['Etiqueta', 'Subárea', 'Puntaje_MVP', 'Nivel_Prioridad'],
            value_vars=['Score_Criticidad', 'Score_Urgencia', 'Score_Frecuencia'],
            var_name='Componente',
            value_name='Puntos'
        )
        df_melt['Componente'] = df_melt['Componente'].replace({
            'Score_Criticidad': 'Criticidad Operativa',
            'Score_Urgencia': 'Urgencia MVP',
            'Score_Frecuencia': 'Frecuencia / Exposición'
        })

        fig_stack = px.bar(
            df_melt,
            x='Puntos',
            y='Etiqueta',
            color='Componente',
            orientation='h',
            text='Puntos',
            color_discrete_map={'Criticidad Operativa': '#1e3a5f', 'Urgencia MVP': '#2b6cb0', 'Frecuencia / Exposición': '#63b3ed'}
        )
        fig_stack.update_traces(textposition='inside', textangle=0, insidetextanchor='middle')
        fig_stack.update_layout(
            height=580,
            plot_bgcolor='#ffffff',
            paper_bgcolor='#ffffff',
            xaxis_title="Puntaje Ponderado Acumulado",
            yaxis_title="",
            xaxis=dict(range=[0, 48]),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=20, r=30, t=45, b=30)
        )
        st.plotly_chart(fig_stack, use_container_width=True)

        # Gráfico 2: Mapa estratégico en fila independiente a ancho completo
        st.markdown('<div class="panel-header dark">MAPA ESTRATÉGICO DE IMPACTO Y CONCENTRACIÓN POR SUBÁREA</div>', unsafe_allow_html=True)
        resumen_sub = df_prio.groupby('Subárea').agg(
            Procesos=('Proceso', 'count'),
            Puntaje_Promedio=('Puntaje_MVP', 'mean'),
            Puntaje_Maximo=('Puntaje_MVP', 'max')
        ).reset_index()
        resumen_sub['Puntaje_Promedio'] = resumen_sub['Puntaje_Promedio'].round(1)

        fig_bub = px.scatter(
            resumen_sub,
            x='Procesos',
            y='Puntaje_Promedio',
            size='Puntaje_Maximo',
            color='Subárea',
            text='Subárea',
            color_discrete_sequence=PALETA_CORPORATIVA,
            size_max=45
        )
        fig_bub.update_traces(textposition='top center')
        fig_bub.update_layout(
            height=380,
            showlegend=False,
            plot_bgcolor='#ffffff',
            paper_bgcolor='#ffffff',
            xaxis_title="Cantidad de Procesos Evaluados",
            yaxis_title="Puntaje Promedio MVP",
            margin=dict(l=30, r=30, t=40, b=30)
        )
        st.plotly_chart(fig_bub, use_container_width=True)
    else:
        st.info("No hay procesos disponibles para calcular la matriz.")