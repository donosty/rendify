# Reglas de calidad de datos — Rendify

**Versión:** 0.1  
**Estado:** versión inicial de reglas; los detalles específicos de DENUE quedan pendientes de confirmar con una muestra real.

## 1. Propósito y severidad

Las reglas de calidad establecen si un lote o un registro puede avanzar entre capas. El objetivo no es declarar los datos “perfectos”, sino detectar problemas, cuantificarlos y decidir qué usos son aceptables.

- **Bloqueante:** impide promover un lote o dataset al siguiente nivel.
- **Cuarentena:** el registro individual no cumple una regla, pero el resto del lote podría procesarse si el contrato lo permite.
- **Advertencia:** no bloquea automáticamente; se informa y requiere evaluar el impacto.
- **Informativa:** registra una medición para establecer una línea base.

Los umbrales de completitud y cobertura se determinarán a partir de muestras y del comportamiento confirmado de la fuente. No establecer porcentajes arbitrarios antes de tener evidencia.

## 2. Reglas Bronze — integridad de la ingesta

| ID | Regla | Severidad inicial | Evidencia |
|---|---|---|---|
| BRZ-001 | La respuesta original se guarda sin transformar su contenido y se registra la ruta. | Bloqueante | Archivo conservado y manifiesto. |
| BRZ-002 | La petición termina con éxito HTTP y el cuerpo se puede interpretar según el formato esperado. | Bloqueante | Código HTTP, content type y parseo. |
| BRZ-003 | Una respuesta válida vacía se distingue de una respuesta de error o de una respuesta inesperada. | Bloqueante | Estado explícito del resultado. |
| BRZ-004 | El manifiesto registra método, parámetros no secretos, timestamps, run ID y cantidad de registros. | Bloqueante | Validación del manifiesto. |
| BRZ-005 | No aparecen tokens, cabeceras de autenticación ni URL con secretos en archivos o logs. | Bloqueante | Revisión de logs y manifiestos; pruebas de saneamiento. |
| BRZ-006 | Se registra checksum/huella del archivo si la herramienta elegida lo permite. | Informativa al inicio | Hash y algoritmo documentado. |
| BRZ-007 | El esquema observado se compara con el contrato esperado. Un cambio inesperado se registra antes de promocionar. | Bloqueante para promoción | Diff de campos/tipos observados. |

## 3. Reglas Silver — registros normalizados

| ID | Regla | Severidad inicial | Evidencia |
|---|---|---|---|
| SLV-001 | Los códigos de actividad y geografía se almacenan como texto para preservar formato y ceros iniciales. | Bloqueante | Tipo y prueba unitaria. |
| SLV-002 | Cada fila mantiene referencia a su registro/fichero Bronze y a ingestion_run_id. | Bloqueante | Reconciliación de linaje. |
| SLV-003 | El identificador elegido para deduplicación debe validarse como estable y suficientemente único antes de habilitar el control definitivo. | Pendiente de contrato | Perfil de Id y CLEE; no asumir la clave aún. |
| SLV-004 | Latitud/longitud, cuando estén presentes, se convierten a decimal y deben pasar validación de formato/rango. | Cuarentena o advertencia según caso | Conteos de inválidos y regla de rango documentada. |
| SLV-005 | Cada código SCIAN usado debe existir en la versión de catálogo registrada. | Cuarentena / bloqueante si afecta clasificación del producto | Cruce con catálogo versionado. |
| SLV-006 | La clave de entidad y municipio/alcaldía debe validarse con catálogo geoestadístico versionado. | Cuarentena si no puede asignarse con fiabilidad | Código desconocido, fuente y versión del catálogo. |
| SLV-007 | La colonia normalizada no se asigna si el mapeo es ambiguo; el valor original se conserva. | Advertencia / cuarentena de la asignación | Regla y estado de homologación. |
| SLV-008 | Fecha_Alta se mantiene distinta de observation_date; no se transforma en fecha de apertura sin definición oficial válida. | Bloqueante para el uso que afirme apertura | Prueba de semántica y metadatos separados. |
| SLV-009 | Campos de contacto se excluyen del contrato Silver inicial salvo aprobación de una necesidad concreta. | Bloqueante de alcance | Esquema Silver revisado. |
| SLV-010 | Nulos en campos candidatos se perfilan y reportan; su obligatoriedad se decide después de validar la respuesta. | Informativa hasta fijar contrato | Perfil de nulos por campo. |

## 4. Reglas Gold — agregados e indicadores

| ID | Regla | Severidad inicial | Evidencia |
|---|---|---|---|
| GLD-001 | Toda métrica tiene definición, unidad, granularidad, periodo, filtros y versión documentados. | Bloqueante | Registro de métrica. |
| GLD-002 | No se unen datasets con periodos o claves geográficas incompatibles sin una metodología explícita. | Bloqueante | Prueba de compatibilidad y decisión documentada. |
| GLD-003 | El conteo de establecimientos define las reglas de deduplicación y la población de registros incluidos. | Bloqueante | SQL/código y pruebas. |
| GLD-004 | El índice exploratorio no se presenta como rentabilidad o probabilidad de éxito. | Bloqueante | Revisión del producto y documentación. |
| GLD-005 | Cada salida registra fuente, cobertura, fecha, versión de regla y linaje hacia los insumos. | Bloqueante | Metadatos de publicación. |
| GLD-006 | La distribución geográfica no se compara si las unidades no tienen una definición comparable o denominador adecuado. | Bloqueante para comparaciones afectadas | Diccionario y metodología. |
| GLD-007 | Features de ML documentan etiqueta, unidad de observación, fecha, ventana de predicción y riesgos de fuga temporal. | Bloqueante para ML | Especificación del dataset/modelo. |

## 5. Cuarentena y tratamiento de excepciones

Cada registro o lote en cuarentena debe incluir:
- referencia a ejecución y archivo Bronze;
- regla que falló;
- valor observado necesario para investigar, minimizando campos sensibles;
- fecha/hora de detección;
- decisión (corregir, aceptar como excepción, excluir de Silver o reintentar);
- responsable y evidencia de la decisión.

La cuarentena no sustituye conservar el original. No corregir o eliminar registros en Bronze.

## 6. Perfil de calidad mínimo para el primer DENUE

El informe inicial deberá incluir:
- número de registros recibidos y número procesado;
- campos presentes/ausentes y tipos observados;
- identificadores nulos/duplicados, sin fijar una clave oficial hasta validarla;
- nulos por campo prioritario;
- coordenadas ausentes y no válidas;
- distribución observada de códigos/descripciones de actividad y estratos;
- claves geográficas reconocidas/no reconocidas;
- estado de parseo y registros en cuarentena;
- fecha de extracción, metodología y limitaciones de la muestra.

Un perfil de muestra describe únicamente esa muestra; no demuestra automáticamente cobertura completa de CDMX ni de toda la fuente.
