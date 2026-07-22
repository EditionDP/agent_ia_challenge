from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Importa tus funciones
from classifier import bimbam
from rag import busqueda_de_respuestas_RAG

app = FastAPI(
    title="BimBam Buy API",
    version="1.0.0",
    description="API de atención al cliente para BimBam Buy"
)


# -----------------------------
# Modelo de entrada
# -----------------------------
class Consulta(BaseModel):
    pregunta: str


# -----------------------------
# Endpoint de prueba
# -----------------------------
@app.get("/")
def inicio():
    return {
        "estado": "OK",
        "mensaje": "API BimBam Buy funcionando"
    }


# -----------------------------
# Endpoint principal
# -----------------------------
@app.post("/consultar")
def consultar(data: Consulta):

    try:

        # Clasificar intención
        clasificacion = bimbam(data.pregunta)

        decision = clasificacion["decision"]

        # -------------------------
        # Preguntas frecuentes
        # -------------------------
        if decision == "AUTO_CONSULTA":

            respuesta = busqueda_de_respuestas_RAG(data.pregunta)

            return {
                "tipo": "AUTO_CONSULTA",
                "clasificacion": clasificacion,
                "respuesta": respuesta
            }

        # -------------------------
        # Falta información
        # -------------------------
        elif decision == "PEDIR_INFO":

            return {
                "tipo": "PEDIR_INFO",
                "clasificacion": clasificacion,
                "mensaje": "Necesitamos más información para ayudarte."
            }

        # -------------------------
        # Crear solicitud
        # -------------------------
        elif decision == "GENERAR_SOLICITUD":

            return {
                "tipo": "GENERAR_SOLICITUD",
                "clasificacion": clasificacion,
                "mensaje": "La solicitud puede enviarse al CRM o base de datos."
            }

        else:

            raise HTTPException(
                status_code=400,
                detail="Decisión desconocida."
            )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    