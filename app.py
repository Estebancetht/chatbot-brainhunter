import streamlit as st
import requests
from qdrant_client import QdrantClient
from qdrant_client.models import NamedVector

st.set_page_config(
    page_title="Brain Hunter · Asistente de Capacitación",
    page_icon="🧠",
    layout="centered"
)

# ── CREDENCIALES ─────────────────────────────────────────
GROQ_API_KEY   = st.secrets["GROQ_API_KEY"]
QDRANT_URL     = st.secrets["QDRANT_URL"]
QDRANT_API_KEY = st.secrets["QDRANT_API_KEY"]
# ─────────────────────────────────────────────────────────

def get_embedding(texto):
    """Obtiene embedding usando la API de Groq"""
    respuesta = requests.post(
        "https://api.groq.com/openai/v1/embeddings",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.3-70b-versatile",
            "input": texto
        },
        timeout=30
    )
    # Si Groq no soporta embeddings, usar vector de zeros como fallback
    try:
        return respuesta.json()["data"][0]["embedding"]
    except:
        # Fallback: usar búsqueda por texto simple en Qdrant
        return None

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

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

* {{ font-family: 'Inter', sans-serif; box-sizing: border-box; }}

html, body,
[data-testid="stApp"],
[data-testid="stAppViewContainer"] {{
    background-color: {bg_base} !important;
    background-image: {bg_gradient} !important;
    min-height: 100vh !important;
}}

[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] {{
    background: transparent !important;
    display: none !important;
}}

#MainMenu, footer, header {{ display: none !important; visibility: hidden !important; }}
.stDeployButton {{ display: none !important; }}

section[data-testid="stMain"] > div:first-child {{ padding-top: 0 !important; }}
.block-container {{ background: transparent !important; padding-bottom: 0 !important; }}

.bh-hero {{
    text-align: center;
    padding: 32px 24px 28px;
    max-width: 620px;
    margin: 0 auto;
}}

.bh-badge {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: {badge_bg};
    border: 1px solid {badge_border};
    border-radius: 100px;
    padding: 5px 14px;
    font-size: 11px;
    font-weight: 500;
    color: {badge_text};
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 18px;
}}

.bh-title {{
    font-size: 2.2rem;
    font-weight: 600;
    color: {title_color};
    line-height: 1.2;
    margin: 0 0 12px;
    letter-spacing: -0.02em;
}}

.bh-title .accent {{
    background: {accent_grad};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}

.bh-subtitle {{
    font-size: 0.93rem;
    color: {text_secondary};
    line-height: 1.7;
    margin: 0;
}}

.bh-chips {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    max-width: 620px;
    margin: 0 auto 28px;
    padding: 0 20px;
}}

.bh-chip {{
    background: {chip_bg};
    border: 1px solid {chip_border};
    border-radius: 100px;
    padding: 6px 14px;
    font-size: 12px;
    color: {chip_text};
    font-weight: 400;
    white-space: nowrap;
}}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {{
    background: {msg_user_bg} !important;
    border: 1px solid {msg_user_border} !important;
    border-radius: 16px 16px 4px 16px !important;
    padding: 13px 17px !important;
    margin: 6px 0 6px 80px !important;
    box-shadow: none !important;
}}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) p,
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) * {{
    color: {text_primary} !important;
    font-size: 0.93rem !important;
    background: transparent !important;
}}

[data-testid="stChatMessageAvatarUser"] {{ display: none !important; }}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {{
    background: {msg_bot_bg} !important;
    border: 1px solid {msg_bot_border} !important;
    border-radius: 4px 16px 16px 16px !important;
    padding: 15px 19px !important;
    margin: 6px 80px 6px 0 !important;
    box-shadow: none !important;
}}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) p,
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) li,
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) strong,
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) span {{
    color: {text_primary} !important;
    font-size: 0.93rem !important;
    line-height: 1.7 !important;
    background: transparent !important;
}}

[data-testid="stChatMessageAvatarAssistant"] {{ display: none !important; }}

a {{ color: {accent_color} !important; text-decoration: none !important; }}
a:hover {{ text-decoration: underline !important; }}

hr {{
    border: none !important;
    border-top: 1px solid {divider_color} !important;
    margin: 10px 0 !important;
}}

.bh-refs-title {{
    font-size: 11px;
    font-weight: 500;
    color: {refs_title_color};
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin: 14px 0 8px;
}}

.bh-ref {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: {ref_bg};
    border: 1px solid {ref_border};
    border-radius: 10px;
    padding: 9px 13px;
    margin: 5px 0;
    gap: 12px;
}}

.bh-ref-info {{
    display: flex;
    flex-direction: column;
    gap: 2px;
    flex: 1;
    min-width: 0;
}}

.bh-ref-name {{
    font-size: 13px;
    font-weight: 500;
    color: {ref_name};
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}}

.bh-ref-time {{
    font-size: 12px;
    color: {ref_time};
}}

.bh-ref-link {{
    background: {ref_btn_bg};
    border: 1px solid {ref_btn_border};
    border-radius: 8px;
    padding: 5px 12px;
    font-size: 12px;
    font-weight: 500;
    color: {ref_btn_text} !important;
    white-space: nowrap;
    flex-shrink: 0;
    text-decoration: none !important;
}}

[data-testid="stBottom"] {{
    background: transparent !important;
}}

[data-testid="stBottom"] > div,
[data-testid="stBottom"] > div > div {{
    background: transparent !important;
}}

[data-testid="stChatInput"] {{
    padding-bottom: 12px !important;
}}

[data-testid="stChatInput"] > div {{
    background: {input_bg} !important;
    border: 1.5px solid {input_border} !important;
    border-radius: 14px !important;
    box-shadow: none !important;
}}

[data-testid="stChatInput"] > div:focus-within {{
    border-color: {input_focus} !important;
    box-shadow: 0 0 0 3px {input_glow} !important;
}}

[data-testid="stChatInput"] div,
[data-testid="stChatInput"] div > div,
[data-testid="stChatInput"] div > div > div {{
    background: transparent !important;
    background-color: transparent !important;
}}

[data-testid="stChatInput"] textarea {{
    color: {input_text} !important;
    font-size: 0.93rem !important;
    background: transparent !important;
    background-color: transparent !important;
    caret-color: {accent_color} !important;
    -webkit-text-fill-color: {input_text} !important;
}}

[data-testid="stChatInput"] textarea::placeholder {{
    color: {input_placeholder} !important;
    -webkit-text-fill-color: {input_placeholder} !important;
    opacity: 1 !important;
}}

[data-testid="stChatInput"] button {{
    background: {ref_btn_bg} !important;
    border-color: {ref_btn_border} !important;
    color: {ref_btn_text} !important;
}}

[data-testid="stSpinner"] p {{
    color: {accent_color} !important;
    font-size: 0.85rem !important;
}}

.stButton > button {{
    background: {chip_bg} !important;
    border: 1px solid {chip_border} !important;
    border-radius: 100px !important;
    color: {chip_text} !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    padding: 5px 14px !important;
    box-shadow: none !important;
}}

.stButton > button:hover {{
    border-color: {input_focus} !important;
    color: {accent_color} !important;
}}

::-webkit-scrollbar {{ width: 5px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: {divider_color}; border-radius: 3px; }}
</style>
""", unsafe_allow_html=True)

# ── BASE DE DATOS ────────────────────────────────────────
@st.cache_resource
def cargar_cliente():
    return QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

qdrant = cargar_cliente()

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
    <div class="bh-title">Encuentra cualquier tema<br>en <span class="accent">segundos</span></div>
    <p class="bh-subtitle">Pregúntame sobre cualquier contenido de los videos de capacitación y te digo exactamente dónde está y en qué minuto.</p>
</div>
""", unsafe_allow_html=True)

# ── HISTORIAL ───────────────────────────────────────────
if "historial" not in st.session_state:
    st.session_state.historial = []

if len(st.session_state.historial) == 0:
    st.markdown(f"""
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
    st.session_state.historial.append({"rol": "user", "contenido": pregunta})
    with st.chat_message("user"):
        st.markdown(pregunta)

    with st.chat_message("assistant"):
        with st.spinner("Buscando en los videos..."):

            # Buscar usando scroll + filtro por texto en Qdrant
            resultados_scroll, _ = qdrant.scroll(
                collection_name="videos_empresa",
                limit=200,
                with_payload=True,
                with_vectors=False
            )

            # Filtrar por palabras clave de la pregunta
            palabras = pregunta.lower().split()
            scored = []
            for punto in resultados_scroll:
                texto = punto.payload.get("texto", "").lower()
                score = sum(1 for p in palabras if p in texto)
                if score > 0:
                    scored.append((score, punto))

            scored.sort(key=lambda x: x[0], reverse=True)
            top_resultados = [p for _, p in scored[:4]]

            # Si no hay resultados con keywords, tomar los primeros
            if not top_resultados:
                top_resultados = resultados_scroll[:4]

            contexto = ""
            fuentes = []
            for r in top_resultados:
                meta = r.payload
                contexto += f"- Video: '{meta.get('video','')}', Minuto: {meta.get('timestamp','')}, Contenido: {meta.get('texto','')}\n"
                fuentes.append(meta)

            prompt = f"""Eres un asistente de capacitación empresarial de Brain Hunter.
Tu trabajo es ayudar a los colaboradores a encontrar información específica dentro de los videos de entrenamiento.

El usuario preguntó: "{pregunta}"

Fragmentos relevantes encontrados en los videos:
{contexto}

Responde en español de forma clara, directa y amigable:
1. Indica en qué video está la información y en qué minuto exacto
2. Explica brevemente qué se trata en ese momento del video
3. Si hay varios resultados útiles, menciónalos todos

Importante: usa la palabra "video" en lugar de "curso". Sé conciso y útil."""

            try:
                respuesta = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {GROQ_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "llama-3.3-70b-versatile",
                        "messages": [{"role": "user", "content": prompt}],
                        "max_tokens": 1024
                    },
                    timeout=30
                )
                texto_respuesta = respuesta.json()["choices"][0]["message"]["content"]
            except Exception:
                texto_respuesta = "⚠️ No se pudo conectar con el modelo de IA."

            st.markdown(texto_respuesta)

            vistos = set()
            refs_html = '<div class="bh-refs-title">📍 Ir directamente al video</div>'
            for f in fuentes[:3]:
                key = f"{f.get('video','')}_{f.get('timestamp','')}"
                if key not in vistos:
                    vistos.add(key)
                    nombre = f.get('video','').replace('_', ' ')
                    refs_html += f"""<div class="bh-ref">
  <div class="bh-ref-info">
    <span class="bh-ref-name">{nombre}</span>
    <span class="bh-ref-time">⏱ Minuto {f.get('timestamp','')}</span>
  </div>
  <a href="{f.get('url_directa','')}" target="_blank" class="bh-ref-link">Abrir video →</a>
</div>"""

            st.markdown(refs_html, unsafe_allow_html=True)

        st.session_state.historial.append({
            "rol": "assistant",
            "contenido": texto_respuesta + refs_html
        })
