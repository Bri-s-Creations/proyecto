"""
Módulo de Definición de Tipos de Datos Inmutables para el Filtro de IA.

Este módulo modela el dominio del sistema de corrección de alucinaciones y escaneo ético
utilizando estructuras estrictamente inmutables (dataclass con frozen=True, tuplas y enums),
siguiendo los principios de la Programación Funcional:
- Inmutabilidad garantizada (sin mutaciones de estado in-place).
- Tipado estático fuerte para evitar errores en tiempo de ejecución.
- Transparencia referencial en las estructuras de datos.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, Tuple


class EstadoDecision(Enum):
    """Estados posibles resultantes de la evaluación del agente evaluador."""
    APROBADO = "APROBADO"      # Respuesta verídica y segura; se entrega sin cambios.
    CORREGIBLE = "CORREGIBLE"  # Presenta pequeñas alucinaciones o desajustes subsanables.
    BLOQUEADO = "BLOQUEADO"    # Alucinación crítica o infracción ética severa; se cancela.


class TipoInfraccion(Enum):
    """Categorías de anomalías o infracciones detectadas."""
    NINGUNA = auto()
    ALUCINACION_DATOS = auto()
    SESGO_DISCRIMINATORIO = auto()
    LENGUAJE_OFENSIVO = auto()
    CONTRADICCION_FACTICA = auto()


class NivelSeveridad(Enum):
    """Nivel de severidad de una infracción o alucinación."""
    BAJA = 1
    MEDIA = 2
    ALTA = 3
    CRITICA = 4


@dataclass(frozen=True)
class Asercion:
    """
    Representa una aserción o proposición atómica extraída del texto.
    
    Attributes:
        afirmacion: Texto exacto de la afirmación analizada.
        entidad: Entidad o concepto clave involucrado (ej. 'Fecha de Lanzamiento', 'Autor').
        valor_original: Valor o dato numérico/nominal detectado en el borrador original.
        valor_contrastado: Valor fidedigno contrastado contra base de conocimiento (opcional).
        es_veridica: Indica si la aserción coincide con la fuente fidedigna.
        fuente_referencia: Origen de la verdad terrenal (Ground Truth).
        confianza: Nivel de certeza de la verificación (0.0 a 1.0).
    """
    afirmacion: str
    entidad: str
    valor_original: str
    valor_contrastado: Optional[str] = None
    es_veridica: bool = True
    fuente_referencia: str = ""
    confianza: float = 1.0


@dataclass(frozen=True)
class InfraccionEtica:
    """
    Representa un incidente o sesgo ético detectado en el contenido.
    
    Attributes:
        tipo: Categoría de la infracción.
        descripcion: Detalle del motivo por el cual infringe las políticas.
        severidad: Nivel de gravedad (BAJA, MEDIA, ALTA, CRITICA).
        fragmento_afectado: Segmento de texto que contiene la infracción.
    """
    tipo: TipoInfraccion
    descripcion: str
    severidad: NivelSeveridad
    fragmento_afectado: str


@dataclass(frozen=True)
class BorradorEntrada:
    """
    Encapsula la entrada inmutable que recibe el filtro de IA.
    
    Attributes:
        consulta_usuario: La pregunta o prompt original enviado por el usuario.
        respuesta_borrador: El texto preliminar generado por el LLM antes de ser validado.
        modelo_generador: Identificador del modelo que originó el borrador.
        timestamp: Marca de tiempo de la intercepción.
    """
    consulta_usuario: str
    respuesta_borrador: str
    modelo_generador: str = "LLM-Base"
    timestamp: str = ""


@dataclass(frozen=True)
class ResultadoVerificacion:
    """
    Estructura inmutable que contiene el diagnóstico de contrastación fáctica y ética.
    
    Attributes:
        indice_certeza: Coeficiente numérico global de veracidad (0.0 <= C_score <= 1.0).
        aserciones: Tupla inmutable con todas las aserciones evaluadas.
        infracciones: Tupla inmutable con las infracciones éticas detectadas.
    """
    indice_certeza: float
    aserciones: Tuple[Asercion, ...] = field(default_factory=tuple)
    infracciones: Tuple[InfraccionEtica, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class CorreccionAplicada:
    """
    Detalle de una sustitución o corrección específica realizada sobre el texto.
    
    Attributes:
        texto_original: Segmento que presentaba error o alucinación.
        texto_reemplazo: Segmento verídico de sustitución.
        justificacion: Explicación de la corrección con base en la evidencia.
        fuente: Fuente de información utilizada para contrastar.
    """
    texto_original: str
    texto_reemplazo: str
    justificacion: str
    fuente: str


@dataclass(frozen=True)
class DictamenFinal:
    """
    Resultado definitivo e inmutable emitido por el evaluador tras aplicar pattern matching.
    
    Attributes:
        estado: Estado resultante (APROBADO, CORREGIBLE, BLOQUEADO).
        texto_salida: Texto final procesado (original, corregido o mensaje de bloqueo).
        indice_certeza: Puntuación de certeza final del contenido.
        correcciones: Tupla de correcciones aplicadas durante la reescritura.
        mensaje_aviso: Mensaje descriptivo para el usuario final sobre la auditoría.
        es_bloqueado: Booleano de conveniencia para determinar si el contenido fue cancelado.
    """
    estado: EstadoDecision
    texto_salida: str
    indice_certeza: float
    correcciones: Tuple[CorreccionAplicada, ...] = field(default_factory=tuple)
    mensaje_aviso: str = ""
    es_bloqueado: bool = False
