# ADR-0001: Gobierno de datos y arquitectura medallón

- **Estado:** adoptada como guía técnica; implementación parcial
- **Fecha de decisión:** 2026-10-21
- **Revisión de estado:** 2026-11-07
- **Decisores:** equipo de Rendify
- **Ámbito:** ciclo de vida de datos y estructura del repositorio

## Contexto

Rendify integra fuentes con diferentes estructuras, periodos, clasificaciones y unidades geográficas. El equipo necesita trazabilidad, calidad verificable, definiciones compartidas y una forma segura de promover datos desde la ingesta hasta los indicadores de producto. DENUE es la primera fuente en implementación.

## Decisión

1. Aplicar prácticas proporcionales inspiradas en DAMA-DMBOK: responsabilidades explícitas, catálogo de activos, diccionario, linaje, calidad, seguridad, integración y gestión de referencias.
2. Usar el patrón medallón como arquitectura lógica:
   - **Bronze:** respuesta original y manifiesto de ingesta.
   - **Silver:** datos normalizados y validados bajo contrato versionado.
   - **Gold:** agregados e indicadores definidos y aprobados.
   - **Quarantine:** flujo lateral para excepciones con referencia a Bronze; no es una cuarta capa medallón.
3. Mantener el desarrollo local primero. Las carpetas locales de ejecución no se versionan; el código, esquemas, catálogos pequeños y documentación sí se versionan cuando no contienen secretos ni datos restringidos.
4. Mantener DAGs de Airflow delgados y concentrar la lógica de fuente, calidad y transformación dentro del paquete Rendify.
5. No fijar el contrato definitivo de DENUE hasta verificar respuestas reales y su semántica.

## Estado de implementación al 7 de noviembre de 2026

| Elemento de la decisión | Estado | Evidencia |
|---|---|---|
| Cliente DENUE y extracción | Implementado inicialmente | `src/rendify/denue/client.py` y `extract.py`. |
| Persistencia Bronze + manifiesto | Implementada | Payload original, metadatos saneados, tamaño y SHA-256. |
| Validación de integridad Bronze | Implementada | `src/rendify/denue/validate.py`; pruebas unitarias. |
| Orquestación inicial | Implementada como DAG manual | `dags/denue_initial_extraction.py`; muestra de 15 registros, no carga completa. |
| Gobierno documental | En desarrollo | Inventario, diccionario, reglas y plan documentados. |
| Silver, Gold y cuarentena | Pendientes | Existen criterios y diseño, no transformaciones operativas. |
| Perfilado de datos | Pendiente | Script y módulo todavía son placeholders. |

## Alternativas consideradas

- **Solo carpetas raw/processed:** simple, pero no distingue original, registros normalizados y productos analíticos ni hace visibles los controles de promoción.
- **Adoptar una plataforma lakehouse completa desde el inicio:** más esfuerzo y complejidad de lo necesario para la primera extracción local.
- **Arquitectura medallón con prácticas de gobierno ligeras:** elegida por combinar claridad del ciclo de vida con esfuerzo razonable y permitir evolucionar el almacenamiento.

## Consecuencias

- Hay que mantener diccionario, reglas de calidad, activos y definiciones actualizados.
- Una validación técnica no implica que los datos sean completos o representativos de la realidad.
- La promoción entre capas requiere controles explícitos y trazabilidad.
- Algunas rutas y carpetas son objetivos documentales; se implementarán conforme existan los datasets y tareas.
- La prueba actual no demuestra cobertura completa de CDMX ni valida por sí sola el uso de DENUE para indicadores de producto.

## Criterio para completar la decisión

La implementación se considerará madura para el primer ciclo de datos cuando, además de la extracción Bronze, se haya ejecutado y documentado una muestra adecuada, perfilado su esquema y calidad, aprobado un contrato versionado, implementado la transformación Silver y su cuarentena, y pueda repetirse el procesamiento sin modificar el original. Gold requerirá definición y pruebas propias antes de publicarse.
