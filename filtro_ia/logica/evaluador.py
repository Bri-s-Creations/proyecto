"""
Módulo de Evaluación y Toma de Decisiones con Pattern Matching.

Implementa la lógica central del agente de filtrado de IA mediante programación
declarativa y coincidencia de patrones estructurales (`match...case`), garantizando:
- Funciones puras y deterministas (mismos datos de entrada -> misma salida).
- Evaluación exhaustiva de casos mediante Structural Pattern Matching.
- Manejo inmutable de estados y transformaciones declarativas.
"""

from functools import reduce
from typing import Tuple

from .datos import (
    Asercion,
    BorradorEntrada,
    CorreccionAplicada,
    DictamenFinal,
    EstadoDecision,
    InfraccionEtica,
    NivelSeveridad,
    ResultadoVerificacion,
)


def hay_infraccion_grave(infracciones: Tuple[InfraccionEtica, ...]) -> bool:
    """
    Determina de manera pura si existe al menos una infracción de severidad ALTA o CRITICA.
    
    Args:
        infracciones: Tupla inmutable de infracciones éticas detectadas.
        
    Returns:
        bool: True si existe alguna infracción severa, False en caso contrario.
    """
    return any(inf.severidad in (NivelSeveridad.ALTA, NivelSeveridad.CRITICA) for inf in infracciones)


def extraer_correcciones_necesarias(aserciones: Tuple[Asercion, ...]) -> Tuple[CorreccionAplicada, ...]:
    """
    Transforma declarativamente las aserciones no verídicas en correcciones aplicables.
    
    Args:
        aserciones: Tupla de aserciones evaluadas.
        
    Returns:
        Tuple[CorreccionAplicada, ...]: Tupla inmutable con las correcciones requeridas.
    """
    return tuple(
        CorreccionAplicada(
            texto_original=a.valor_original,
            texto_reemplazo=a.valor_contrastado if a.valor_contrastado is not None else "[Dato Corregido]",
            justificacion=f"Corrección fáctica para '{a.entidad}': se sustituye '{a.valor_original}' por fuente verídica.",
            fuente=a.fuente_referencia or "Base de Conocimiento Verificada",
        )
        for a in aserciones
        if not a.es_veridica and a.valor_contrastado is not None
    )


def aplicar_correcciones(texto_original: str, correcciones: Tuple[CorreccionAplicada, ...]) -> str:
    """
    Aplica una secuencia de correcciones sobre el texto original de forma funcional pura.
    
    Utiliza `functools.reduce` para plegar la tupla de correcciones sobre la cadena
    sin mutar variables externas ni generar efectos secundarios.
    
    Args:
        texto_original: Cadena de texto base.
        correcciones: Tupla inmutable de correcciones a aplicar.
        
    Returns:
        str: Nueva cadena de texto con las sustituciones realizadas.
    """
    def _reemplazar(acumulado: str, corr: CorreccionAplicada) -> str:
        return acumulado.replace(corr.texto_original, corr.texto_reemplazo)

    return reduce(_reemplazar, correcciones, texto_original)


def clasificar_dictamen(
    verificacion: ResultadoVerificacion,
    umbral_aprobado: float = 0.85,
    umbral_minimo: float = 0.50,
) -> EstadoDecision:
    """
    Clasifica el estado de la respuesta empleando Structural Pattern Matching (`match...case`).
    
    Reglas de Decisión:
    1. Si existen infracciones éticas severas (ALTA / CRITICA) -> BLOQUEADO
    2. Si el índice de certeza es menor al umbral mínimo (< 0.50) -> BLOQUEADO
    3. Si el índice de certeza es alto (>= 0.85), no hay infracciones y todas las aserciones son verídicas -> APROBADO
    4. Si el índice está en rango aceptable (>= 0.50) pero existen aserciones corregibles -> CORREGIBLE
    5. Caso por defecto -> BLOQUEADO
    
    Args:
        verificacion: Diagnóstico inmutable de contrastación fáctica.
        umbral_aprobado: Puntuación mínima requerida para aprobación directa (defecto: 0.85).
        umbral_minimo: Puntuación mínima para admitir corrección antes de bloquear (defecto: 0.50).
        
    Returns:
        EstadoDecision: Clasificación resultante (APROBADO, CORREGIBLE, BLOQUEADO).
    """
    match verificacion:
        # Caso 1: Detección de infracciones éticas graves o críticas
        case ResultadoVerificacion(infracciones=infs) if hay_infraccion_grave(infs):
            return EstadoDecision.BLOQUEADO

        # Caso 2: Alucinación crítica o certeza inferior al umbral mínimo de seguridad
        case ResultadoVerificacion(indice_certeza=score) if score < umbral_minimo:
            return EstadoDecision.BLOQUEADO

        # Caso 3: Aprobación directa -> Certeza alta, sin infracciones y todas las aserciones verídicas
        case ResultadoVerificacion(
            indice_certeza=score,
            infracciones=(),
            aserciones=aserciones,
        ) if score >= umbral_aprobado and all(a.es_veridica for a in aserciones):
            return EstadoDecision.APROBADO

        # Caso 4: Corrección -> Certeza recuperable con aserciones contrastadas
        case ResultadoVerificacion(indice_certeza=score) if score >= umbral_minimo:
            return EstadoDecision.CORREGIBLE

        # Caso por defecto de contención
        case _:
            return EstadoDecision.BLOQUEADO


def evaluar_y_dictaminar(
    borrador: BorradorEntrada,
    verificacion: ResultadoVerificacion,
    umbral_aprobado: float = 0.85,
    umbral_minimo: float = 0.50,
) -> DictamenFinal:
    """
    Evalúa el borrador de entrada contra la verificación y genera el DictamenFinal inmutable
    utilizando Pattern Matching sobre el estado resultante.
    
    Args:
        borrador: Estructura inmutable con la consulta y el texto borrador.
        verificacion: Diagnóstico fáctico y ético de la respuesta.
        umbral_aprobado: Umbral para aprobación directa.
        umbral_minimo: Umbral mínimo admisible antes del bloqueo.
        
    Returns:
        DictamenFinal: Objeto inmutable con el dictamen, texto final y trazabilidad.
    """
    estado = clasificar_dictamen(verificacion, umbral_aprobado, umbral_minimo)

    match estado:
        case EstadoDecision.APROBADO:
            return DictamenFinal(
                estado=EstadoDecision.APROBADO,
                texto_salida=borrador.respuesta_borrador,
                indice_certeza=verificacion.indice_certeza,
                correcciones=(),
                mensaje_aviso="[APROBADO] Respuesta verificada y validada sin modificaciones requeridas.",
                es_bloqueado=False,
            )

        case EstadoDecision.CORREGIBLE:
            correcciones = extraer_correcciones_necesarias(verificacion.aserciones)
            texto_corregido = aplicar_correcciones(borrador.respuesta_borrador, correcciones)
            return DictamenFinal(
                estado=EstadoDecision.CORREGIBLE,
                texto_salida=texto_corregido,
                indice_certeza=verificacion.indice_certeza,
                correcciones=correcciones,
                mensaje_aviso=(
                    f"[CORREGIDO] Se aplicaron {len(correcciones)} correccion(es) factica(s) "
                    "basadas en fuentes de conocimiento fidedignas."
                ),
                es_bloqueado=False,
            )

        case EstadoDecision.BLOQUEADO:
            return DictamenFinal(
                estado=EstadoDecision.BLOQUEADO,
                texto_salida=(
                    "[RESPUESTA BLOQUEADA POR TRUESHIELD]\n"
                    "El contenido generado contiene alucinaciones criticas o no cumple con las "
                    "directrices de veracidad y seguridad requeridas."
                ),
                indice_certeza=verificacion.indice_certeza,
                correcciones=(),
                mensaje_aviso="[BLOQUEADO] Contenido cancelado por superar los limites tolerables de error o sesgo.",
                es_bloqueado=True,
            )


if __name__ == "__main__":
    # Demostracion y pruebas funcionales deterministas
    print("=== DEMOSTRACION DE EVALUADOR FUNCIONAL CON MATCH-CASE ===")

    # 1. Caso Aprobado
    borrador_ok = BorradorEntrada(
        consulta_usuario="En que ano se publico Python 3.0?",
        respuesta_borrador="Python 3.0 fue lanzado oficialmente en diciembre de 2008.",
    )
    verificacion_ok = ResultadoVerificacion(
        indice_certeza=0.98,
        aserciones=(
            Asercion(
                afirmacion="Python 3.0 fue lanzado en 2008",
                entidad="Ano de Lanzamiento",
                valor_original="2008",
                valor_contrastado="2008",
                es_veridica=True,
                fuente_referencia="Python Software Foundation",
                confianza=0.99,
            ),
        ),
    )
    dictamen_ok = evaluar_y_dictaminar(borrador_ok, verificacion_ok)
    print(f"\n[Caso 1: {dictamen_ok.estado.value}]")
    print(f"Salida: {dictamen_ok.texto_salida}")
    print(f"Aviso: {dictamen_ok.mensaje_aviso}")
    assert dictamen_ok.estado == EstadoDecision.APROBADO
    assert not dictamen_ok.es_bloqueado

    # 2. Caso Corregible
    borrador_err = BorradorEntrada(
        consulta_usuario="Quien creo Python y en que ano?",
        respuesta_borrador="Python fue creado por Guido van Rossum en 1999.",
    )
    verificacion_err = ResultadoVerificacion(
        indice_certeza=0.75,
        aserciones=(
            Asercion(
                afirmacion="Python fue creado en 1999",
                entidad="Ano de Creacion",
                valor_original="1999",
                valor_contrastado="1991",
                es_veridica=False,
                fuente_referencia="Documentacion Oficial de Python",
                confianza=0.95,
            ),
        ),
    )
    dictamen_err = evaluar_y_dictaminar(borrador_err, verificacion_err)
    print(f"\n[Caso 2: {dictamen_err.estado.value}]")
    print(f"Salida corregida: {dictamen_err.texto_salida}")
    print(f"Aviso: {dictamen_err.mensaje_aviso}")
    for c in dictamen_err.correcciones:
        print(f" - {c.justificacion}")
    assert dictamen_err.estado == EstadoDecision.CORREGIBLE
    assert "1991" in dictamen_err.texto_salida

    # 3. Caso Bloqueado
    borrador_bloq = BorradorEntrada(
        consulta_usuario="Genera informacion medica",
        respuesta_borrador="Informacion erronea con alto riesgo y datos inventados.",
    )
    verificacion_bloq = ResultadoVerificacion(
        indice_certeza=0.25,
        infracciones=(
            InfraccionEtica(
                tipo=TipoInfraccion.ALUCINACION_DATOS,
                descripcion="Alucinacion severa en datos criticos de salud",
                severidad=NivelSeveridad.CRITICA,
                fragmento_afectado="Informacion erronea",
            ),
        ),
    )
    dictamen_bloq = evaluar_y_dictaminar(borrador_bloq, verificacion_bloq)
    print(f"\n[Caso 3: {dictamen_bloq.estado.value}]")
    print(f"Salida: {dictamen_bloq.texto_salida}")
    print(f"Aviso: {dictamen_bloq.mensaje_aviso}")
    assert dictamen_bloq.estado == EstadoDecision.BLOQUEADO
    assert dictamen_bloq.es_bloqueado

    print("\n>>> TODAS LAS PRUEBAS DE MATCH-CASE Y MODELOS INMUTABLES PASARON EXITOSAMENTE. <<<")
