# Diccionario de datos — Rendify

**Versión:** 0.1  
**Estado:** borrador. Las propiedades de DENUE deben confirmarse con una respuesta real antes de considerarse validadas.

## 1. Cómo leer este diccionario

- **Nombre de origen:** propiedad tal como aparece en la respuesta de la fuente.
- **Nombre canónico:** nombre interno propuesto; no implica que exista ya en el código o en una tabla.
- **Granularidad:** qué representa una fila.
- **Estado:** pendiente de muestra, candidato o por validar.
- Los campos opcionales no se convierten automáticamente en obligatorios. La obligatoriedad definitiva se decidirá tras observar respuestas reales y revisar la documentación de la fuente.

## 2. Dataset Bronze: respuesta DENUE

**Definición:** respuesta recibida de la API en su forma original. Se almacena sin renombrar ni convertir campos. La trazabilidad se mantiene a nivel de ejecución y archivo, no mediante cambios a la respuesta original.

| Propiedad de origen candidata | Definición operativa provisional | Tratamiento | Estado |
|---|---|---|---|
| Id | Identificador que la API usa para consultar una ficha. | Preservar como texto. | Pendiente de verificar respuesta. |
| CLEE | Identificador de establecimiento descrito por la fuente. | Preservar como texto; validar estabilidad y unicidad. | Pendiente. |
| CLASE_ACTIVIDAD_ID | Código de actividad a nivel clase, si viene en el método elegido. | Preservar como texto. | Pendiente. |
| Clase_actividad | Descripción textual de la actividad económica. | Preservar literal en Bronze. | Pendiente. |
| SECTOR_ACTIVIDAD_ID | Código del sector, si viene. | Texto. | Pendiente. |
| SUBSECTOR_ACTIVIDAD_ID | Código del subsector, si viene. | Texto. | Pendiente. |
| RAMA_ACTIVIDAD_ID | Código de rama, si viene. | Texto. | Pendiente. |
| SUBRAMA_ACTIVIDAD_ID | Código de subrama, si viene. | Texto. | Pendiente. |
| Estrato | Categoría de personal ocupado publicada por DENUE. | Preservar literalmente y mapear a categoría canónica documentada. | Pendiente. |
| Tipo | Tipo de establecimiento publicado. | Preservar valor original; perfilar categorías reales. | Pendiente. |
| Nombre | Nombre del establecimiento, si aparece. | Conservar en Bronze; acceso/uso downstream justificado. | Pendiente. |
| Colonia | Nombre del asentamiento/zona informado por la fuente. | No tratar como identificador geográfico único. | Pendiente. |
| Tipo_Asentamiento | Tipo de asentamiento, si viene. | Preservar texto. | Pendiente. |
| CP | Código postal. | Texto para preservar formato. | Pendiente. |
| Ubicacion | Cadena compuesta de ubicación, según la documentación de ejemplo. | Preservar original; no parsear sin prueba. | Pendiente. |
| AreaGeo | Clave de área geográfica, si viene. | Texto; validar formato con catálogo. | Pendiente. |
| AGEB | Código/segmento AGEB publicado. | Texto; interpretar junto a claves geográficas superiores. | Pendiente. |
| Manzana | Código de manzana publicado. | Texto. | Pendiente. |
| Latitud | Coordenada de ubicación. | Bronze literal; Silver decimal con validación. | Pendiente. |
| Longitud | Coordenada de ubicación. | Bronze literal; Silver decimal con validación. | Pendiente. |
| Fecha_Alta | Fecha asociada al registro/directorio según el ejemplo. | No asumir que equivale a apertura real; confirmar semántica. | Pendiente. |

La lista anterior es una lista de propiedades a comprobar a partir de la guía del DENUE; no garantiza que todas aparezcan juntas ni que sus nombres sean idénticos entre métodos o versiones. Ver docs/denue-api-research.md.

## 3. Dataset Silver: establecimiento normalizado

**Granularidad esperada:** un registro por establecimiento y versión/observación cuando se necesite historia temporal. La clave natural definitiva no se fija hasta comprobar estabilidad de Id/CLEE entre extracciones.

| Nombre canónico propuesto | Definición | Reglas / notas |
|---|---|---|
| denue_id | Identificador interno basado en Id si se confirma estable. | Texto; no inventar clave si falta. |
| clee | Identificador CLEE de origen. | Texto; evaluar cambio en snapshots. |
| activity_class_code | Código SCIAN de clase normalizado. | Texto y ligado a versión de catálogo. |
| activity_class_name | Descripción de la actividad publicada/normalizada. | Conservar valor fuente además del normalizado. |
| staff_size_stratum | Estrato de personal ocupado. | Categoría, no valor exacto de empleados, ingreso ni rentabilidad. |
| establishment_type | Tipo del registro publicado. | Catálogo controlado una vez se conozcan valores. |
| state_geo_code | Clave geográfica oficial de entidad. | Mantener fuente y versión del catálogo. |
| municipality_geo_code | Clave oficial de municipio/alcaldía. | Tipo de unidad y clave en campos separados. |
| locality_geo_code | Clave de localidad si se identifica de forma fiable. | No asumir que AreaGeo siempre es intercambiable con una clave del catálogo. |
| neighborhood_raw | Valor original de Colonia. | Inmutable; trazable a Bronze. |
| neighborhood_normalized | Colonia homologada si existe regla/fuente fiable. | Nulo/no asignado cuando la correspondencia sea ambigua; incluir estado de homologación. |
| postal_code | CP. | Texto; variable auxiliar. |
| ageb_code | Código AGEB validado. | Nullable si falta. |
| block_code | Código de manzana validado. | Nullable si falta. |
| latitude | Latitud decimal validada. | Nullable si falta o no supera reglas. |
| longitude | Longitud decimal validada. | Nullable si falta o no supera reglas. |
| denue_date_added | Fecha_Alta parseada cuando se valide semántica. | No llamar fecha de apertura. |
| observation_date | Fecha en que Rendify observó el registro. | Generada por Rendify en cada extracción/snapshot. |
| ingestion_run_id | ID de ejecución de ingesta. | Vincular al manifiesto Bronze. |
| source_record_hash | Huella calculada del registro fuente, si se implementa. | No sustituye las claves del origen. |
| quality_status | Estado de reglas de calidad aplicadas. | Aprobado, con advertencias o en cuarentena según contrato. |

## 4. Dataset Gold: actividad por zona y periodo

**Granularidad propuesta:** una fila por actividad económica, unidad geográfica, nivel geográfico y periodo de observación. La periodicidad y el nivel exacto se elegirán según cobertura validada.

| Nombre propuesto | Definición |
|---|---|
| period_id | Periodo de referencia de la observación; no confundir con fecha de extracción. |
| geography_level | Tipo de unidad: entidad, alcaldía/municipio, localidad, colonia homologada u otra unidad validada. |
| geography_id | Clave estable de la unidad geográfica en catálogo versionado. |
| geography_name | Nombre presentado, separado de la clave. |
| activity_category_id | Categoría interna del producto con mapeo SCIAN versionado. |
| establishment_count | Cantidad de registros distintos según regla de deduplicación publicada. |
| stratum_distribution | Distribución de registros por estrato de personal ocupado si la cobertura lo permite. |
| source_coverage_note | Nota de cobertura, fecha y limitaciones relevantes. |
| metric_definition_version | Versión de la fórmula o definición del producto Gold. |
| generated_at | Fecha/hora de generación. |
| lineage_run_id | Ejecución que generó el producto. |

No se asigna todavía una métrica de “éxito”. El número de establecimientos o su distribución por estrato no demuestra supervivencia, rentabilidad ni probabilidad de éxito.

## 5. Metadatos de ejecución obligatorios

El manifiesto de extracción debe documentar: source_id, dataset_id, endpoint/método, parámetros saneados, extraction_started_at, extraction_finished_at, run_id, code_version, contract_version, HTTP status, content type, record_count, archivo/salida, checksum cuando proceda, incidencias y fecha/periodo fuente si se publica.

Los nombres finales del contrato técnico pueden normalizarse a snake_case. El mapeo entre propiedades originales y nombres canónicos se mantendrá versionado.
