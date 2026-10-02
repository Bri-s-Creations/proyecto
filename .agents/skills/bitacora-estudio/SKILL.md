---
name: bitacora-estudio
description: >-
  Use this skill whenever the user gives an instruction, asks questions, requests study materials, or completes learning activities in Programación Funcional. Ensures all interactions, timestamps, user prompts, responses, and metacognitive study tracking notes are consistently recorded in bitacora_de_estudio.md.
---

# Skill: Bitácora de Estudio y Monitoreo de Aprendizaje

Este skill automatiza y estructura el registro sistemático del proceso de estudio del estudiante en la materia **Programación Funcional** (Ingeniería en Computación Inteligente).

## Objetivos del Skill
1. **Registro Cronológico**: Guardar cada indicación dada por el estudiante junto con su timestamp y la respuesta o material generado.
2. **Monitoreo Pedagógico y Metacognición**: Identificar el patrón de aprendizaje del estudiante (p. ej., resolución guiada, experimentación con código, solicitud de analogías, análisis de errores, autoevaluación).
3. **Generación y Organización de Material**: Crear materiales de estudio accionables (resúmenes, retos de código, explicaciones conceptuales, tablas comparativas) vinculados directamente en la bitácora.

---

## Procedimiento de Actualización

Cada vez que el estudiante envíe una indicación o solicitud:

1. **Obtener el Timestamp Actual**:
   - Formato recomendado: `YYYY-MM-DD HH:MM:SS (Zona Horaria Local)`

2. **Procesar la Solicitud y Generar la Respuesta**:
   - Responder al estudiante con claridad, rigor conceptual, ejemplos funcionales en Python y recursos didácticos de alta calidad.

3. **Registrar la Entrada en [`bitacora_de_estudio.md`](file:///c:/Users/bh324/OneDrive/Datos%20adjuntos/Programaci%C3%B2n%20funcional/bitacora_de_estudio.md)**:
   - Añadir una nueva sección de entrada siguiendo la plantilla estándar.

---

## Plantilla Estándar de Registro

```markdown
### 📝 Entrada #[N]: [Título breve descriptivo]
- **⏰ Timestamp:** YYYY-MM-DD HH:MM:SS [Zona Horaria]
- **👤 Indicación del Estudiante:**
  > [Texto exacto o síntesis de la indicación]

- **🎯 Eje Temático:** [Ej. Unidad 1 - Inmutabilidad / Funciones Puras / Recursión / etc.]
- **🤖 Respuesta y Material Generado:**
  [Resumen detallado del material, explicaciones, snippets de código o enlaces a guías generadas]

- **📊 Análisis del Proceso de Estudio:**
  - **Tipo de Interacción:** [Ej. Consulta teórica / Práctica de código / Planificación / Creación de recursos]
  - **Patrón de Aprendizaje Observado:** [Breve diagnóstico de cómo aborda el estudiante el concepto]
  - **Sugerencia de Seguimiento:** [Próximo paso pedagógico recomendado]

---
```

---

## Directrices de Calidad del Material
- **Ejemplos funcionales**: Usar Python declarativo, funciones puras, tipos de datos inmutables (`tuple`, `frozenset`), funciones de orden superior (`map`, `filter`, `reduce`), `functools` e `itertools`.
- **Conexión Curricular**: Conectar siempre los conceptos con la [guia_semanal_unidad1.md](file:///c:/Users/bh324/OneDrive/Datos%20adjuntos/Programaci%C3%B2n%20funcional/guia_semanal_unidad1.md) y la [planeacion-docente.md](file:///c:/Users/bh324/OneDrive/Datos%20adjuntos/Programaci%C3%B2n%20funcional/planeacion-docente.md).
