import streamlit as st
import requests

st.title("Filtro IA - Evaluación Candidatos")

experiencia = st.number_input("Años de experiencia", min_value=0, max_value=50, value=3)
nivel_ingles = st.selectbox("Nivel de inglés", ["B1", "B2", "C1", "C2"])
proyecto_ia = st.checkbox("¿Tiene proyecto de IA realizado?")

if st.button("Evaluar Candidato"):
    datos = {
        "experiencia": experiencia,
        "ingles": nivel_ingles,
        "proyecto_ia": proyecto_ia
    }
    
    respuesta = requests.post("http://127.0.0.1:8000/evaluar", json=datos)
    
    if respuesta.status_code == 200:
        st.success(f"Resultado: {respuesta.json()}")
    else:
        st.error("Error al conectar con la API")
        