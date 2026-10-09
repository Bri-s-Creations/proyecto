from fastapi import FastAPI
from filtro_ia.logica.evaluador import evaluar_y_dictaminar

app = FastAPI(title="Filtro IA - Programación Funcional")

@app.get("/")
def home():
    return {"mensaje": "API de Filtro IA activa y lista."}

@app.post("/evaluar")
def evaluar_endpoint(datos: dict):
    # Pasamos los datos a la función pura que probaste en evaluador.py
    resultado = evaluar_y_dictaminar(datos)
    return {"status": "exito", "resultado": resultado}