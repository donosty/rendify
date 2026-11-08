# Registro de activos de datos — Rendify

**Versión:** 0.2  
**Actualización:** 2026-11-07

El registro identifica fuentes y productos, sus propósitos, responsables y estado. Se distingue una integración técnica de una validación semántica o aprobación para producto.

## Estados

- **Candidata:** considerada, aún sin revisión suficiente.
- **En auditoría:** documentación, muestra o comportamiento bajo revisión.
- **Integración técnica inicial:** existe código de acceso/ingesta, pero quedan verificaciones de fuente y producto.
- **Validada técnicamente:** acceso, estructura y controles confirmados con evidencia repetible.
- **Validada para integración:** se comprobaron también semántica, periodicidad, geografía y posibilidad de unión.
- **Aprobada para producto:** existe un derivado con reglas, cobertura y limitaciones documentadas.
- **Retirada:** fuera de uso con decisión registrada.

## Registro

| Asset ID | Activo | Uso previsto | Estado (7 nov 2026) | Pendientes principales |
|---|---|---|---|---|
| SRC-DENUE | API/directorio DENUE — INEGI | Establecimientos, actividad y ubicación | **Integración técnica inicial**: cliente, Bronze y validación implementados; DAG de muestra presente | Evidencia de ejecución real; cobertura, campos, SCIAN, filtros, límites y condiciones de uso. |
| SRC-CCPV20 | Censo de Población y Vivienda 2020 | Contexto de población/vivienda | Candidata | Variables, periodo y granularidad compatibles. |
| SRC-CE24 | Censos Económicos 2024 | Referencias económicas agregadas | Candidata | Tablas publicadas, nivel geográfico y confidencialidad. |
| SRC-GEO | Catálogo geoestadístico/cartografía | Claves y límites para integración espacial | Candidata | Versión, claves y resolución territorial. |
| SRC-ENIGH24 | ENIGH 2024 | Contexto ingreso/gasto | Posible fase posterior | Diseño muestral y pertinencia geográfica. |
| PRD-GOLD-ACTIVITY-AREA | Indicadores de actividad por zona | Comparación de zonas/actividades | No implementado | Contrato Silver, definición de métricas, cobertura y linaje. |

Los roles funcionales se asignan entre el equipo en su plan de trabajo; el registro no implica asignaciones individuales formales.

## Metadatos mínimos

Por activo: ID, propósito, tipo, proveedor, responsable, ubicación, granularidad, claves, periodo, fecha de actualización, condiciones de uso, clasificación de acceso, contrato, reglas, linaje, estado, evidencia, limitaciones y retención.

## Incidencias y cambios

Registrar problemas mediante issue o registro ligado a run ID, regla, impacto, responsable y resolución. Cambios de semántica, esquema o métrica deben entrar mediante pull request.
