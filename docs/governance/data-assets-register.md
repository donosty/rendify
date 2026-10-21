# Registro de activos de datos — Rendify

**Versión:** 0.1  
**Estado:** inventario inicial; actualizar cuando se ejecute la primera extracción.

El registro identifica fuentes y productos, sus propósitos, responsables, condiciones de uso y estado de validación. Una fuente candidata no equivale a un activo validado ni a un dataset listo para consumo.

## 1. Estados controlados

- **Candidata:** considerada para un caso de uso, aún no verificada.
- **En auditoría:** documentación o una muestra están siendo revisadas.
- **Validada técnicamente:** acceso, estructura y controles técnicos verificados con evidencia.
- **Validada para integración:** también se comprobó semántica, periodicidad, geografía y posibilidad de unión con los otros datasets.
- **Aprobada para producto:** existe producto derivado con reglas, cobertura y limitaciones documentadas.
- **Retirada:** ya no se utiliza; queda documentado el motivo y el tratamiento de copias.

## 2. Registro inicial

| Asset ID | Activo | Proveedor | Uso previsto | Estado | Responsable interno inicial | Pendientes principales |
|---|---|---|---|---|---|---|
| SRC-DENUE | API/directorio DENUE | INEGI | Identificación, actividad, estrato y ubicación de establecimientos. | En auditoría documental; extracción autenticada pendiente | Data Steward + Data Engineer | Probar método y token, campos, paginación/volumen, actividades SCIAN, condiciones de reutilización y cobertura geográfica. |
| SRC-CCPV20 | Censo de Población y Vivienda 2020 | INEGI | Contexto de población/vivienda. | Candidata | Data Steward | Seleccionar variables, periodo, nivel territorial y formato de descarga. |
| SRC-CE24 | Censos Económicos 2024 | INEGI | Referencias económicas agregadas. | Candidata | Product Owner + Data Steward | Identificar variables publicadas, actividad, granularidad y reglas de confidencialidad. |
| SRC-GEO | Catálogo de claves geoestadísticas/cartografía | INEGI | Normalización y cruce geográfico. | Candidata | Data Steward + Data Engineer | Seleccionar versión oficial, claves y límites apropiados. |
| SRC-ENIGH24 | ENIGH 2024 | INEGI | Posible contexto de gasto/ingreso de hogares en etapa posterior. | Candidata; fuera de la extracción inicial | Analítica/ML | Revisar diseño muestral y determinar si existe un uso responsable al nivel territorial deseado. |
| PRD-GOLD-ACTIVITY-AREA | Indicadores de actividad por zona | Rendify (derivado) | Comparar presencia/composición de negocios. | No implementado | Product Owner + Analítica/ML | Definir granularidad, periodos, fórmula, calidad y linaje cuando Silver esté disponible. |

Los nombres y estados de las fuentes derivan del plan actual. Los responsables son roles funcionales a asignar entre los dos colaboradores; esta tabla no pretende afirmar que alguien ya haya aceptado formalmente cada rol.

## 3. Metadatos mínimos de un activo

Para cada nuevo activo añadir:
- Asset ID y nombre;
- descripción de negocio y preguntas que soporta;
- tipo: fuente, Bronze, Silver, Gold, catálogo de referencia o dataset de ML;
- propietario/publicador y responsable interno;
- ruta o tabla y ambiente donde vive;
- granularidad, claves, periodo de referencia y fecha de actualización;
- sistema fuente, método y condiciones de uso;
- clasificación de acceso y campos restringidos;
- versión del esquema, diccionario y reglas de calidad;
- upstream/downstream (linaje);
- estado, evidencia y limitaciones;
- política de retención y decisión de publicación.

## 4. Registro de incidencias y cambios

Los problemas que afecten semántica, calidad o disponibilidad se registran como issue de GitHub o en un registro ligado a la ejecución. El issue debe incluir el Asset ID, dataset, run ID, regla fallida, impacto, responsable y resolución. Cambios de definición o esquema deben mantener histórico a través de PR y commits, no sustituyendo documentación sin rastro.

## 5. Referencias

- [Inventario de fuentes técnicas](../data-sources.md)
- [Investigación de API DENUE](../denue-api-research.md)
- [Marco de gobierno de datos](data-governance-charter.md)
- [Plan de gestión de datos](data-management-plan.md)
