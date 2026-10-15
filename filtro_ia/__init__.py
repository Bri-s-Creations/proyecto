"""
Paquete filtro_ia: Módulo de filtrado, verificación y corrección funcional de respuestas de IA.
"""

from .logica.datos import EstadoDecision, DictamenFinal
from .logica.evaluador import clasificar_dictamen, evaluar_y_dictaminar

__all__ = [
    "EstadoDecision",
    "DictamenFinal",
    "clasificar_dictamen",
    "evaluar_y_dictaminar",
]
