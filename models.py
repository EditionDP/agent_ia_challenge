from typing import Literal
from pydantic import BaseModel

class BimBamOut(BaseModel):

    decision: Literal[
        "AUTO_CONSULTA",
        "PEDIR_INFO",
        "GENERAR_SOLICITUD"
    ]

    urgencia: Literal[
        "BAJA",
        "MEDIANA",
        "ALTA"
    ]

    campos_faltantes: list[str]