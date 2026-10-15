# app.py

import streamlit as st
import requests

st.set_page_config(page_title="TrueShield", page_icon="🛡️", layout="centered")

# Estilos visuales de TrueShield (Paleta Rosa / Morado / Blanco)
st.markdown("""
<style>
    .stApp { background-color: #ff1493 !important; }
    h1, h2, h3, label, p, span, div { color: #4b0082 !important; font-family: 'Segoe UI', sans-serif; }
    .stButton>button { 
        background-color: #ffffff !important; 
        color: #4b0082 !important; 
        border-radius: 25px !important; 
        border: 2px solid #4b0082 !important; 
        font-weight: bold !important; 
    }
    .stTextArea textarea { 
        background-color: #ffffff !important; 
        color: #1a1a1a !important; 
        border-radius: 12px !important; 
        border: 2px solid #4b0082 !important; 
    }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ TrueShield")
st.subheader("Detector de Sesgos y Veracidad Fáctica")

st.info("""
### 👋 ¡Bienvenido a TrueShield!
Esta plataforma evalúa tus textos en tiempo real utilizando una doble capa de protección:
* **Verificación Fáctica Local:** Contrasta datos institucionales frente a nuestra base de hechos verificados (FIME, Universidad de Colima, autoridades y carreras).
* **Análisis de Sesgos Sociales:** Identifica patrones de discriminación de género, edad y nivel socioeconómico.

*Ingresa cualquier enunciado abajo para comenzar con el análisis.*
""")

if "texto_input" not in st.session_state:
    st.session_state["texto_input"] = ""

texto_analizar = st.text_area(
    "Ingresa la información o afirmación a analizar:",
    value=st.session_state["texto_input"],
    height=130,
    placeholder="Escribe aquí el texto que deseas verificar..."
)

col_btn1, col_btn2 = st.columns([2, 1])

with col_btn1:
    ejecutar_analisis = st.button("🔍 Detectar Sesgo y Veracidad", use_container_width=True)

with col_btn2:
    if st.button("🧹 Limpiar texto", use_container_width=True):
        st.session_state["texto_input"] = ""
        st.rerun()

if ejecutar_analisis:
    if not texto_analizar.strip():
        st.warning("Por favor ingresa un texto antes de realizar la evaluación.")
    else:
        with st.spinner("Analizando información..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/evaluar",
                    json={"texto": texto_analizar},
                    timeout=5
                )
                if response.status_code == 200:
                    data = response.json()
                    semaforo = str(data.get("semaforo", "")).lower()
                    categoria = data.get("categoria", "")
                    nivel_sesgo = data.get("nivel_sesgo", "")
                    texto_corregido = data.get("texto_corregido", "")
                    
                    st.divider()
                    
                    if semaforo == "verde" or "ninguno" in categoria.lower():
                        st.success("✅ **No se detectó información falsa o sesgo.**")
                    else:
                        st.error("⚠️ **Se ha detectado un problema en la información.**")
                        
                        m_col1, m_col2 = st.columns(2)
                        with m_col1:
                            st.metric(label="Tipo Detectado", value=categoria)
                        with m_col2:
                            st.metric(label="Porcentaje de Confianza", value=nivel_sesgo)
                        
                        st.write("---")
                        st.subheader("💡 Propuesta de corrección / Información verídica:")
                        st.info(texto_corregido)
                        
            except Exception:
                st.error("No se pudo conectar con el servidor backend. Verifica que main.py esté ejecutándose en http://127.0.0.1:8000")

st.divider()
if st.button("⬅️ Volver a Inicio"):
    st.session_state["texto_input"] = ""
    st.rerun()