"""
Submódulo logica: Modelado de datos inmutables y reglas de evaluación funcional con pattern matching.
"""

from .datos import (
    Asercion,
    BorradorEntrada,
    CorreccionAplicada,
    DictamenFinal,
    EstadoDecision,
    InfraccionEtica,
    NivelSeveridad,
    ResultadoVerificacion,
    TipoInfraccion,
)
from .evaluador import (
    aplicar_correcciones,
    clasificar_dictamen,
    evaluar_y_dictaminar,
    extraer_correcciones_necesarias,
)

__all__ = [
    "EstadoDecision",
    "TipoInfraccion",
    "NivelSeveridad",
    "Asercion",
    "InfraccionEtica",
    "BorradorEntrada",
    "ResultadoVerificacion",
    "CorreccionAplicada",
    "DictamenFinal",
    "clasificar_dictamen",
    "evaluar_y_dictaminar",
    "extraer_correcciones_necesarias",
    "aplicar_correcciones",
]
