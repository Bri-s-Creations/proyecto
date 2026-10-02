# 🛡️ Filtro de IA: Corrección de Alucinaciones y Escaneo Ético

Sistema funcional en Python diseñado para interceptar, auditar y corregir respuestas generadas por Modelos de Lenguaje (LLMs) antes de su entrega al usuario final, garantizando veracidad fáctica y mitigación de sesgos o contenidos no deseados.

---

## 📖 Overview

El proyecto implementa un **middleware de validación y autocorrección** aplicando los fundamentos de la **Programación Funcional**:
- **Inmutabilidad:** Modelado de dominio robusto con `dataclasses(frozen=True)` y colecciones inmutables (`tuple`).
- **Funciones Puras & Transparencia Referencial:** Procesamiento determinista sin efectos secundarios en la lógica de contrastación y evaluación.
- **Decisión Declarativa:** Flujo de clasificación mediante *Pattern Matching* (`match-case`) para determinar estados: `APROBADO`, `CORREGIBLE` o `BLOQUEADO`.
- **Base de Verificación (Ground Truth):** Módulo desacoplado con hechos fidedignos para contrastar aserciones extraídas de las respuestas.

---

## 📁 Estructura del Proyecto

```text
Programación funcional/
├── .agents/                          # Configuración de reglas y skills del asistente
│   ├── rules/
│   │   └── bitacora_estudio.md       # Regla modular para bitácora
│   └── skills/
│       └── bitacora-estudio/
│           └── SKILL.md              # Skill de tracking de aprendizaje
├── data/                             # Base de conocimiento y datos de referencia (Ground Truth)
│   └── hechos.py                     # Hechos verificados (FIME, UdeC, materia, profesor, etc.)
├── filtro_ia/                         # Paquete principal del filtro funcional
│   ├── __init__.py                   # Inicializador del paquete
│   └── logica/                       # Lógica pura del sistema
│       ├── __init__.py               # Exportación de componentes lógicos
│       ├── datos.py                  # Modelos de dominio inmutables (Asercion, DictamenFinal, etc.)
│       └── evaluador.py              # Motor funcional de evaluación y pattern matching
├── AGENTS.md                         # Reglas obligatorias de asistencia y registro
├── bitacora_de_estudio.md            # Registro cronológico del progreso y metacognición
├── Correccion_de_Alucinaciones.md    # Especificación conceptual y técnica del proyecto
├── guia_semanal_unidad1.md           # Guía de estudio y ejercicios de la Unidad I
├── planeacion-docente.md             # Planeación del curso de Programación Funcional
└── README.md                         # Descripción general y mapa de la arquitectura
```

---

## 🎓 Contexto Académico
- **Materia:** Programación Funcional
- **Institución:** Facultad de Ingeniería Mecánica y Eléctrica (FIME), Universidad de Colima
- **Profesor:** Dr. Walter Alexander Mata López
- **Semestre:** 3er Semestre (2026B)
