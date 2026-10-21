# ADR-0001: Gobierno de datos y arquitectura medallón

- **Estado:** propuesto para revisión
- **Fecha:** 2026-10-21
- **Decisores:** equipo de Rendify
- **Ámbito:** ciclo de vida de datos y estructura del repositorio

## Contexto

Rendify integrará fuentes con diferentes estructuras, periodos, clasificaciones y unidades geográficas. El equipo necesita trazabilidad, calidad verificable, definiciones compartidas y una forma segura de promover datos desde la ingesta hasta los indicadores de producto. La primera fuente en auditoría es DENUE.

## Decisión

1. Aplicar prácticas proporcionales inspiradas en DAMA-DMBOK: responsabilidades explícitas, catálogo de activos, diccionario, linaje, calidad, seguridad, integración y gestión de referencias.
2. Usar el patrón medallón como arquitectura lógica:
   - Bronze: respuesta original y manifiesto de ingesta.
   - Silver: datos normalizados y validados bajo contrato versionado.
   - Gold: agregados e indicadores definidos y aprobados.
   - Quarantine: flujo lateral para excepciones con referencia a Bronze; no es una cuarta capa medallón.
3. Mantener el desarrollo local primero. Las carpetas locales de ejecución no se versionan; el código, esquemas, catálogos pequeños y documentación sí se versionan si no contienen secretos ni datos restringidos.
4. Mantener DAGs de Airflow delgados y concentrar la lógica de fuente, calidad y transformación dentro del paquete de Rendify.
5. No fijar todavía un contrato definitivo de DENUE hasta inspeccionar una respuesta real con token válido.

## Alternativas consideradas

- **Solo carpetas raw/processed:** simple, pero no distingue original, datos normalizados y productos analíticos ni hace visibles los controles de promoción.
- **Adoptar una plataforma lakehouse completa desde el inicio:** mayor esfuerzo y complejidad que lo necesario para la primera extracción local.
- **Arquitectura medallón con prácticas de gobierno ligeras:** elegida por combinar claridad del ciclo de vida con esfuerzo razonable y posibilidad de migrar el almacenamiento en el futuro.

## Consecuencias

- Hay que mantener diccionario, reglas de calidad, activos y definiciones actualizados.
- Una validación técnica no implica que los datos sean completos o representativos de la realidad.
- La promoción entre capas requiere controles explícitos y trazabilidad.
- Algunas rutas/carpetas quedan como objetivo documental; se implementarán conforme los datasets y las tareas existan.

## Evidencia de aceptación

La decisión se considera operativa cuando el primer flujo de DENUE conserva la respuesta, genera manifiesto seguro, valida estructura, documenta el perfil y puede repetir la transformación sin modificar el original.
