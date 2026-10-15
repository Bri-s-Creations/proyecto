# main.py

import sys
from pathlib import Path

# Garantizar resolución de módulos independiente dentro del directorio /backend
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Importación relativa y autónoma del módulo hechos
try:
    from . import hechos
except ImportError:
    import hechos

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Solicitud(BaseModel):
    texto: str

def evaluar_sesgo_social(texto: str):
    texto_lower = texto.lower()
    
    # Patrones de Sesgo de Género
    patrones_genero = [
        "no tienen voz", "mujeres no", "hombres son mejores", 
        "sin capacidad", "no sirven para", "no tienen la capacidad",
        "temple para dirigir", "las mujeres deben", "vos"
    ]
    if any(p in texto_lower for p in patrones_genero):
        return {
            "hay_sesgo": True,
            "categoria": "Sesgo de Género",
            "porcentaje": "95%",
            "sugerencia": "El desempeño y la voz en la comunidad académica se valoran bajo principios de equidad e igualdad de oportunidades, independientemente del género."
        }
        
    # Patrones de Sesgo de Edad
    patrones_edad = ["demasiado viejo", "muy joven para", "por su edad no"]
    if any(p in texto_lower for p in patrones_edad):
        return {
            "hay_sesgo": True,
            "categoria": "Sesgo de Edad",
            "porcentaje": "90%",
            "sugerencia": "Las competencias académicas y profesionales se evalúan por capacidad y mérito, no por edad."
        }

    return {"hay_sesgo": False}

@app.post("/evaluar")
def evaluar(solicitud: Solicitud):
    texto = solicitud.texto

    resultado_hechos = hechos.verificar_hecho(texto)
    resultado_sesgo = evaluar_sesgo_social(texto)

    # CASO 1: Ambas capas detectan un problema (Error fáctico + Sesgo)
    if resultado_hechos.get("es_falso") and resultado_sesgo.get("hay_sesgo"):
        correccion_combinada = (
            f"1. [Dato Fáctico]: {resultado_hechos['texto_correcto']}\n\n"
            f"2. [Análisis de Sesgo]: {resultado_sesgo['sugerencia']}"
        )
        return {
            "semaforo": "rojo",
            "categoria": f"Información Falsa + {resultado_sesgo['categoria']}",
            "nivel_sesgo": "98%",
            "texto_corregido": correccion_combinada
        }

    # CASO 2: Solo error fáctico
    if resultado_hechos.get("es_falso"):
        return {
            "semaforo": "rojo",
            "categoria": resultado_hechos["categoria"],
            "nivel_sesgo": resultado_hechos["porcentaje"],
            "texto_corregido": resultado_hechos["texto_correcto"]
        }

    # CASO 3: Solo sesgo social
    if resultado_sesgo.get("hay_sesgo"):
        return {
            "semaforo": "rojo",
            "categoria": resultado_sesgo["categoria"],
            "nivel_sesgo": resultado_sesgo["porcentaje"],
            "texto_corregido": resultado_sesgo["sugerencia"]
        }

    # CASO 4: Texto Verídico y Neutro
    return {
        "semaforo": "verde",
        "categoria": "Ninguno",
        "nivel_sesgo": "0%",
        "texto_corregido": texto
    }