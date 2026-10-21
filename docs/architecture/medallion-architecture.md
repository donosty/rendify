# Arquitectura medallón de Rendify

**Versión:** 0.1  
**Estado:** diseño lógico local-first; las tecnologías físicas finales quedan pendientes.

## 1. Propósito y relación con el gobierno

El patrón medallón organiza los datasets en capas de refinamiento creciente: Bronze conserva lo recibido; Silver contiene datos normalizados y validados; Gold publica datos adaptados a preguntas analíticas o de negocio. Cada capa debe tener propósito, contrato, reglas de calidad, responsable y linaje.

DAMA-DMBOK y el medallón resuelven problemas diferentes y complementarios:
- **DAMA-DMBOK** inspira el marco de gobierno, responsabilidades, arquitectura, modelado, metadatos, calidad, seguridad e integración.
- **Medallón** organiza el flujo técnico de datos y los criterios para promoverlos entre capas.

Este diseño es una adaptación pragmática, no una afirmación de implementación completa de DAMA ni un requisito de utilizar Databricks o Delta Lake.

## 2. Flujo lógico

~~~text
API / archivo fuente
        |
        v
BRONZE — original + manifiesto de ingesta
        |
        v
SILVER — datos normalizados, tipados y validados
        |                    \
        |                     --> QUARANTINE — excepciones trazables
        v
GOLD — agregados por actividad, zona y periodo
        |
        +--> indicadores del producto
        +--> datasets de features para ML, si existe un objetivo válido
~~~

La cuarentena es un flujo lateral de excepciones, no una medalla adicional. El registro original permanece en Bronze.

## 3. Capas, reglas y artefactos

### Bronze — original reproducible

**Propósito:** conservar lo que devuelve la fuente, sin cambios semánticos.

- Guardar el cuerpo original de la respuesta, preferiblemente por petición/página.
- Escribir un manifiesto separado con fuente, método, parámetros saneados, timestamps UTC, run ID, código de estado, conteo, versión del extractor y checksum si procede.
- No incluir tokens, cabeceras de autenticación ni URL con secretos.
- No renombrar propiedades, corregir valores ni eliminar registros.
- Diferenciar una respuesta vacía válida de un fallo HTTP o de una respuesta inesperada.
- Registrar versión o fecha de referencia de fuente cuando se publique.
- Conservar los datos según los términos de uso de la fuente, el riesgo, la capacidad y la política que adopte el equipo.

Ruta local sugerida: data/bronze/denue/extraction_date=AAAA-MM-DD/run_id=ID/. Ajustar el particionado después de medir volúmenes y formatos; evitar miles de archivos diminutos.

Artefactos de gobierno relacionados: registro de activos, ficha técnica de fuente, manifiesto de extracción y evidencia de acceso/reutilización.

### Silver — contrato canónico y validado

**Propósito:** ofrecer registros reutilizables y consistentes.

- Definir el contrato y obligatoriedad de campos después de inspeccionar una respuesta real de DENUE.
- Normalizar tipos y nombres internos; mantener códigos y claves geográficas como texto para preservar ceros iniciales.
- Conservar valores de origen si una normalización puede perder significado o si hace falta rastrear la transformación.
- Deduplicar solo con una regla explícita; validar primero estabilidad/unicidad de Id/CLEE.
- Relacionar códigos SCIAN y claves territoriales con catálogos versionados.
- Conservar linaje a archivo Bronze, run ID, código y versión del contrato.
- No interpretar Fecha_Alta automáticamente como apertura real.
- Excluir datos de contacto de Silver salvo que haya un propósito aprobado y documentado.

Ruta local sugerida: data/silver/denue/. Para historia temporal, conservar observaciones/snapshots en lugar de sobrescribir datos sin evidencia.

### Gold — productos analíticos

**Propósito:** responder preguntas del producto y servir a informes, API o futuros modelos.

Primer producto candidato: indicadores descriptivos por actividad económica, unidad geográfica y periodo. La unidad y el periodo solo se comparan cuando los datos de origen son compatibles.

Cada producto Gold debe declarar:
- ID, nombre, propósito y responsable;
- granularidad de una fila y claves;
- métricas, unidades y filtros de inclusión/exclusión;
- periodo de referencia y fecha de generación;
- fuentes, contratos y versiones de transformación;
- reglas de calidad y excepciones aprobadas;
- cobertura, advertencias y limitaciones de interpretación;
- linaje hacia los insumos de Silver y el run de origen.

Un conteo de establecimientos no es una etiqueta de éxito. Los conjuntos de features para ML deben ser distintos de los agregados descriptivos cuando sea necesario y documentar variable objetivo, unidad de observación, ventana de predicción, linaje y riesgo de fuga temporal.

Rutas locales sugeridas:
- data/gold/area_activity/
- data/gold/ml_features/ cuando se defina un experimento de ML justificado.

### Quarantine — excepciones trazables

Ruta sugerida: data/quarantine/denue/.

Cada excepción conserva referencia al lote/registro Bronze, ID y nombre de regla fallida, motivo, fecha de detección y decisión. Minimizar los valores copiados para diagnosticar. La cuarentena no sustituye a Bronze ni es una excusa para descartar fallos silenciosamente.

## 4. Estructura de carpetas recomendada

~~~text
rendify/
├── dags/                         # Solo definición y orquestación de DAGs
├── src/rendify/
│   ├── denue/                    # Cliente, extracción y adaptación de la fuente
│   ├── profiling/                # Perfilado y reportes de calidad
│   └── ...                       # Normalización, integración y analítica al implementarlas
├── tests/
│   └── denue/                    # Pruebas de cliente, contrato y calidad
├── data/                         # Salidas locales; no versionar datos generados
│   ├── bronze/denue/
│   ├── silver/denue/
│   ├── gold/area_activity/
│   ├── gold/ml_features/
│   └── quarantine/denue/
├── config/
│   └── reference/                # Mapeos SCIAN y claves de referencia versionados
├── schemas/                      # Contratos de datos versionados al confirmar el esquema
├── reports/                      # Reportes seleccionados de calidad/perfilado
└── docs/
    ├── governance/               # Roles, plan, diccionario, calidad y catálogo de activos
    ├── architecture/             # Medallón y diseños técnicos
    ├── decisions/                # Registros de decisiones de arquitectura (ADR)
    └── ...                       # Brief, fuentes y documentación de DENUE
~~~

No es obligatorio crear módulos de código vacíos para todas las etapas. Las carpetas para datos de ejecución pueden crearse cuando el pipeline las use; los contratos, catálogos pequeños y documentación revisados sí se versionan. Nunca versionar datos generados completos, tokens ni secretos.

## 5. Relación con Airflow

Airflow orquesta la ejecución y las transiciones; no define por sí solo los contratos.

DAG completo objetivo cuando las capas existan:
1. extract_denue_to_bronze
2. validate_bronze_manifest
3. transform_denue_to_silver
4. run_silver_quality_checks
5. publish_area_activity_gold
6. write_quality_report

Primer incremento: extraer una muestra a Bronze, comprobar su estructura y producir un perfil de calidad. La promoción Silver se activa cuando el contrato se haya confirmado. No publicar Gold antes de validar actividad, claves geográficas, granularidad y reglas.

Los DAGs deben ser delgados: llaman funciones del paquete Rendify. Evitar operaciones de red, escaneos grandes, llamadas a base de datos o cómputo pesado durante la carga/importación del DAG. Pasar entre tareas metadatos pequeños (rutas, run ID, conteos y estado), no conjuntos enteros de registros por XCom.

## 6. Criterios de promoción

| Transición | Condición mínima |
|---|---|
| Fuente → Bronze | Respuesta capturada; manifiesto completo y sin secretos. |
| Bronze → Silver | Contrato versionado, esquema observado reconocido, transformaciones reproducibles y fallos registrados. |
| Silver → Gold | Definición del producto, calidad suficiente, periodo/granularidad explícitos y revisión de interpretación. |
| Fallo → Quarantine | Regla, motivo, referencia al origen y decisión registrada. |

Una validación técnica correcta no prueba que la fuente represente perfectamente la realidad o que un indicador sea adecuado para inferir éxito económico. Son decisiones distintas.

## 7. Referencias

- [DAMA International — gestión de datos](https://dama.org/about-dama/what-is-data-management/)
- [Databricks — buenas prácticas de fiabilidad y medallón](https://docs.databricks.com/aws/en/lakehouse-architecture/reliability/best-practices)
- [Databricks — qué es la arquitectura medallón](https://www.databricks.com/blog/what-is-medallion-architecture)
- [Airflow — buenas prácticas](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)
