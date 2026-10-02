"""
Paquete filtro_ia: Módulo de filtrado, verificación y corrección funcional de respuestas de IA.
"""

from .logica.datos import (
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
from .logica.evaluador import (
    clasificar_dictamen,
    evaluar_y_dictaminar,
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
]
