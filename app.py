import streamlit as st
import requests
import os
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

st.set_page_config(
    page_title="Brain Hunter · Asistente de Capacitación",
    page_icon="🧠",
    layout="centered"
)

# ── CREDENCIALES ─────────────────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

if not GROQ_API_KEY:
    st.error("No se encontró GROQ_API_KEY")
    st.stop()

if not QDRANT_URL:
    st.error("No se encontró QDRANT_URL")
    st.stop()

if not QDRANT_API_KEY:
    st.error("No se encontró QDRANT_API_KEY")
    st.stop()
# ─────────────────────────────────────────────────────────

if "modo_oscuro" not in st.session_state:
    st.session_state.modo_oscuro = True

modo = st.session_state.modo_oscuro

if modo:
    bg_base           = "#0d1117"
    bg_gradient       = """
        radial-gradient(ellipse at 0% 0%, rgba(30,100,210,0.25) 0%, transparent 50%),
        radial-gradient(ellipse at 100% 0%, rgba(30,180,100,0.15) 0%, transparent 50%),
        radial-gradient(ellipse at 100% 100%, rgba(220,60,30,0.20) 0%, transparent 50%),
        radial-gradient(ellipse at 0% 100%, rgba(230,160,20,0.12) 0%, transparent 50%)"""
    text_primary      = "#e6edf3"
    text_secondary    = "#8b949e"
    msg_user_bg       = "rgba(26,95,204,0.20)"
    msg_user_border   = "rgba(26,95,204,0.35)"
    msg_bot_bg        = "rgba(22,27,34,0.85)"
    msg_bot_border    = "rgba(255,255,255,0.08)"
    input_bg          = "#161b22"
    input_border      = "rgba(255,255,255,0.14)"
    input_focus       = "rgba(88,166,255,0.5)"
    input_glow        = "rgba(88,166,255,0.08)"
    input_text        = "#e6edf3"
    input_placeholder = "#484f58"
    chip_bg           = "rgba(255,255,255,0.05)"
    chip_border       = "rgba(255,255,255,0.10)"
    chip_text         = "#8b949e"
    ref_bg            = "rgba(26,95,204,0.08)"
    ref_border        = "rgba(26,95,204,0.20)"
    ref_name          = "#cdd9e5"
    ref_time          = "#6ea8fe"
    ref_btn_bg        = "rgba(26,95,204,0.20)"
    ref_btn_border    = "rgba(26,95,204,0.30)"
    ref_btn_text      = "#58a6ff"
    accent_color      = "#58a6ff"
    badge_bg          = "rgba(26,95,204,0.15)"
    badge_border      = "rgba(26,95,204,0.30)"
    badge_text        = "#6ea8fe"
    title_color       = "#e6edf3"
    accent_grad       = "linear-gradient(135deg, #58a6ff, #3fb950, #f78166)"
    switch_icon       = "☀️"
    switch_label      = "Modo claro"
    divider_color     = "rgba(255,255,255,0.08)"
    refs_title_color  = "#6e7681"
else:
    bg_base           = "#ffffff"
    bg_gradient       = """
        radial-gradient(ellipse at 0% 0%, rgba(30,100,210,0.15) 0%, transparent 45%),
        radial-gradient(ellipse at 100% 0%, rgba(30,180,100,0.10) 0%, transparent 40%),
        radial-gradient(ellipse at 100% 100%, rgba(220,60,30,0.15) 0%, transparent 45%),
        radial-gradient(ellipse at 0% 100%, rgba(230,160,20,0.10) 0%, transparent 40%)"""
    text_primary      = "#0f1923"
    text_secondary    = "#5a6a7a"
    msg_user_bg       = "rgba(26,95,204,0.10)"
    msg_user_border   = "rgba(26,95,204,0.25)"
    msg_bot_bg        = "rgba(255,255,255,0.92)"
    msg_bot_border    = "rgba(0,0,0,0.07)"
    input_bg          = "#ffffff"
    input_border      = "rgba(0,0,0,0.14)"
    input_focus       = "rgba(26,95,204,0.40)"
    input_glow        = "rgba(26,95,204,0.06)"
    input_text        = "#0f1923"
    input_placeholder = "#a0aab4"
    chip_bg           = "rgba(255,255,255,0.80)"
    chip_border       = "rgba(26,95,204,0.15)"
    chip_text         = "#3a5a8a"
    ref_bg            = "rgba(26,95,204,0.05)"
    ref_border        = "rgba(26,95,204,0.15)"
    ref_name          = "#1a2530"
    ref_time          = "#1a5fcc"
    ref_btn_bg        = "rgba(26,95,204,0.10)"
    ref_btn_border    = "rgba(26,95,204,0.25)"
    ref_btn_text      = "#1a5fcc"
    accent_color      = "#1a5fcc"
    badge_bg          = "rgba(26,95,204,0.10)"
    badge_border      = "rgba(26,95,204,0.20)"
    badge_text        = "#1a5fcc"
    title_color       = "#0f1923"
    accent_grad       = "linear-gradient(135deg, #1a5fcc, #1ab470, #dc3c1e)"
    switch_icon       = "🌙"
    switch_label      = "Modo oscuro"
    divider_color     = "rgba(0,0,0,0.07)"
    refs_title_color  = "#8a9aaa"

# TODO TU CSS EXACTAMENTE IGUAL AQUÍ
# NO NECESITAS CAMBIAR NADA MÁS

# ── BASE DE DATOS ────────────────────────────────────────
@st.cache_resource
def cargar_bd():
    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY
    )

    modelo = SentenceTransformer("all-MiniLM-L6-v2")

    return client, modelo

qdrant, modelo = cargar_bd()

# ── SWITCH MODO ──────────────────────────────────────────
col1, col2, col3 = st.columns([1, 1, 0.4])

with col3:
    if st.button(f"{switch_icon} {switch_label}"):
        st.session_state.modo_oscuro = not st.session_state.modo_oscuro
        st.rerun()

# ── HERO ────────────────────────────────────────────────
st.markdown(f"""
<div class="bh-hero">
    <div class="bh-badge">🧠 Asistente IA · Brain Hunter</div>
    <div class="bh-title">
        Encuentra cualquier tema<br>
        en <span class="accent">segundos</span>
    </div>
    <p class="bh-subtitle">
        Pregúntame sobre cualquier contenido de los videos de capacitación y te digo exactamente dónde está y en qué minuto.
    </p>
</div>
""", unsafe_allow_html=True)

# ── HISTORIAL ───────────────────────────────────────────
if "historial" not in st.session_state:
    st.session_state.historial = []

if len(st.session_state.historial) == 0:
    st.markdown("""
    <div class="bh-chips">
        <div class="bh-chip">¿Cómo se crean los usuarios?</div>
        <div class="bh-chip">¿Cómo funciona el predictor?</div>
        <div class="bh-chip">¿Cómo se configuran los roles?</div>
        <div class="bh-chip">¿Cómo se generan informes?</div>
        <div class="bh-chip">¿Qué es una franquicia?</div>
    </div>
    """, unsafe_allow_html=True)

for msg in st.session_state.historial:
    with st.chat_message(msg["rol"]):
        st.markdown(msg["contenido"], unsafe_allow_html=True)

# ── INPUT ───────────────────────────────────────────────
pregunta = st.chat_input("¿Qué tema estás buscando en los videos?")

if pregunta:

    st.session_state.historial.append({
        "rol": "user",
        "contenido": pregunta
    })

    with st.chat_message("user"):
        st.markdown(pregunta)

    with st.chat_message("assistant"):

        with st.spinner("Buscando en los videos..."):

            vector = modelo.encode(pregunta).tolist()

            resultados = qdrant.query_points(
                collection_name="videos_empresa",
                query=vector,
                limit=4
            ).points

            contexto = ""
            fuentes = []

            for r in resultados:
                meta = r.payload

                contexto += f"""
- Video: '{meta['video']}'
Minuto: {meta['timestamp']}
Contenido: {meta['texto']}
"""

                fuentes.append(meta)

            prompt = f"""
Eres un asistente de capacitación empresarial de Brain Hunter.

Tu trabajo es ayudar a los colaboradores a encontrar información específica dentro de los videos de entrenamiento.

El usuario preguntó:
"{pregunta}"

Fragmentos relevantes encontrados:
{contexto}

Responde en español:
1. Indica el video y minuto exacto
2. Explica brevemente el contenido
3. Si hay varios resultados útiles, menciónalos

Importante:
Usa la palabra "video" y no "curso".
Sé claro, útil y breve.
"""

            try:

                respuesta = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {GROQ_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "llama-3.3-70b-versatile",
                        "messages": [
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        "max_tokens": 1024
                    },
                    timeout=30
                )

                texto_respuesta = respuesta.json()["choices"][0]["message"]["content"]

            except Exception as e:

                texto_respuesta = f"""
⚠️ No se pudo conectar con el modelo de IA.

Error:
{str(e)}
"""

            st.markdown(texto_respuesta)

            vistos = set()

            refs_html = """
<div class="bh-refs-title">
📍 Ir directamente al video
</div>
"""

            for f in fuentes[:3]:

                key = f"{f['video']}_{f['timestamp']}"

                if key not in vistos:

                    vistos.add(key)

                    nombre = f['video'].replace('_', ' ')

                    refs_html += f"""
<div class="bh-ref">
    <div class="bh-ref-info">
        <span class="bh-ref-name">{nombre}</span>
        <span class="bh-ref-time">⏱ Minuto {f['timestamp']}</span>
    </div>

    <a href="{f['url_directa']}"
       target="_blank"
       class="bh-ref-link">
       Abrir video →
    </a>
</div>
"""

            st.markdown(refs_html, unsafe_allow_html=True)

        st.session_state.historial.append({
            "rol": "assistant",
            "contenido": texto_respuesta + refs_html
        })
