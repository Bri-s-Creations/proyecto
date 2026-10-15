# hechos.py

"""
Base de hechos verificados (Ground Truth) para TrueShield.
"""

HECHOS_VERIFICADOS = {
    "fime_carreras": [
        "ici", "computación inteligente", "computacion inteligente",
        "ime", "mecánico electricista", "mecanico electricista",
        "mecatrónica", "mecatronica",
        "iset", "sistemas eléctricos", "sistemas electricos", "telecomunicaciones"
    ],
    "director_actual": "Dr. Walter Alexander Mata López",
    "ex_director": "Víctor Castillo",
    "rector": "Dr. Christian Jorge Torres Ortiz Zermeño",
    "universidad": "Universidad de Colima",
    "campus": "Campus Coquimatlán (Coqui)"
}

OTRAS_CARRERAS_UDEC = [
    "arquitectura", "medicina", "derecho", "psicología", "psicologia", 
    "enfermería", "enfermeria", "contabilidad", "administración", "administracion",
    "pedagogía", "pedagogia", "veterinaria", "biología", "biologia"
]

def verificar_hecho(texto: str):
    texto_lower = texto.lower()

    # 1. Validación de Carreras de la FIME
    if "fime" in texto_lower or "facultad de ingeniería mecánica" in texto_lower or "facultad" in texto_lower:
        carrera_detectada = None
        for c in OTRAS_CARRERAS_UDEC:
            if c in texto_lower:
                carrera_detectada = c.capitalize()
                break
        
        if carrera_detectada:
            return {
                "es_falso": True,
                "categoria": "Veracidad / Información Falsa",
                "porcentaje": "98%",
                "texto_correcto": f"{carrera_detectada} no pertenece a la FIME. Las carreras oficiales de la FIME son: ICI (Ingeniería en Computación Inteligente), IME (Ingeniero Mecánico Electricista), Mecatrónica e ISET (Ingeniería en Sistemas Eléctricos y Telecomunicaciones)."
            }
        elif "carrera" in texto_lower and not any(c in texto_lower for c in HECHOS_VERIFICADOS["fime_carreras"]):
            return {
                "es_falso": True,
                "categoria": "Veracidad / Información Falsa",
                "porcentaje": "95%",
                "texto_correcto": "Las carreras oficiales de la FIME son únicamente: ICI, IME, Mecatrónica e ISET."
            }

    # 2. Validación de Director Actual vs Exdirector
    if "director" in texto_lower and ("fime" in texto_lower or "facultad" in texto_lower):
        if "victor" in texto_lower or "castillo" in texto_lower:
            return {
                "es_falso": True,
                "categoria": "Veracidad / Información Falsa",
                "porcentaje": "99%",
                "texto_correcto": f"Víctor Castillo es el exdirector. El director actual de la FIME es el {HECHOS_VERIFICADOS['director_actual']}."
            }

    # 3. Validación de Ubicación del Campus
    if "campus" in texto_lower or "ubicación" in texto_lower or "ubicacion" in texto_lower:
        if "coqui" not in texto_lower and "coquimatlán" not in texto_lower and "coquimatlan" not in texto_lower:
            return {
                "es_falso": True,
                "categoria": "Veracidad / Información Falsa",
                "porcentaje": "96%",
                "texto_correcto": f"La FIME se encuentra ubicada en el {HECHOS_VERIFICADOS['campus']}."
            }

    return {"es_falso": False}
