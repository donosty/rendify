# Reglas de calidad de datos — Rendify

**Versión:** 0.2  
**Estado:** controles de integridad Bronze implementados; reglas Silver/Gold documentadas como criterios futuros.

## 1. Severidad

- **Bloqueante:** impide aceptar el lote o promover la capa.
- **Cuarentena:** retiene registros que no cumplen una regla individual.
- **Advertencia:** requiere evaluar impacto.
- **Informativa:** genera línea base sin bloquear.

Los umbrales de completitud se fijarán después de perfilar datos reales.

## 2. Bronze — estado de implementación

| ID | Regla | Estado en código |
|---|---|---|
| BRZ-001 | Preservar el cuerpo de la respuesta en bytes originales. | Implementada en `save_bronze_response()`. |
| BRZ-002 | Parsear JSON UTF-8 como lista de objetos. | Implementada en cliente y validador. |
| BRZ-003 | Guardar manifiesto con fuente, método, run, timestamp, parámetros, status, conteo, tamaño, hash y archivo. | Implementada. |
| BRZ-004 | Evitar token/secret dentro de query_parameters. | Implementada como validación de claves. |
| BRZ-005 | Comprobar código HTTP 200. | Implementada en `validate_bronze_response()`. |
| BRZ-006 | Verificar existencia, referencia relativa segura, tamaño y checksum. | Implementada. |
| BRZ-007 | Comparar esquema recibido contra un contrato DENUE versionado. | Pendiente; no existe contrato de respuesta confirmado. |
| BRZ-008 | Distinguir respuesta válida vacía de cobertura insuficiente. | El cliente admite lista vacía; la interpretación de cobertura está pendiente. |

Los controles actuales prueban estructura e integridad técnica del payload; no confirman exactitud de la fuente ni cobertura geográfica.

## 3. Silver — reglas pendientes de implementación

- Mantener identificadores y claves SCIAN/geográficas como texto.
- Validar claves contra catálogos INEGI/SCIAN versionados.
- Definir deduplicación solo después de comprobar estabilidad y unicidad de Id/CLEE.
- Validar coordenadas y preservar nulos/valores originales necesarios.
- Mantener separado periodo fuente, fecha de extracción y fecha de observación.
- No interpretar `Fecha_Alta` como apertura real sin documentación.
- Conservar linaje a Bronze y run ID.
- Excluir atributos personales/de contacto salvo justificación documentada.

## 4. Gold — reglas pendientes de implementación

Toda métrica debe documentar definición, granularidad, unidad, periodo, filtros, población incluida, fórmula, versión y linaje. No unir geografías o periodos incompatibles sin metodología. No comunicar un conteo o índice exploratorio como rentabilidad/probabilidad de éxito.

## 5. Evidencia de calidad siguiente

Al perfilar una muestra representativa, reportar campos presentes, tipos, nulos, cardinalidad de identificadores, duplicados, coordenadas inválidas, distribución SCIAN, claves geográficas y cobertura de la consulta. Una muestra de 15 registros no establece una línea base representativa de toda la ciudad.
