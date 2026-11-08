# Arquitectura medallón de Rendify

**Versión:** 0.2  
**Actualización:** 2026-11-07  
**Estado:** Bronze inicial implementada para DENUE; Silver, Gold y cuarentena permanecen como diseño.

## 1. Propósito y relación con el gobierno

El patrón medallón organiza los datasets en capas de refinamiento creciente: Bronze conserva lo recibido; Silver contiene datos normalizados y validados; Gold publica datos adaptados a preguntas analíticas o de negocio. DAMA-DMBOK inspira responsabilidades, definiciones, metadatos, calidad, seguridad e integración; medallón organiza el flujo técnico. Rendify aplica prácticas ligeras, no una implantación completa ni una certificación DAMA.

## 2. Estado real del flujo

```text
DENUE API
   |
   v
BRONZE — implementada: response.json + manifest.json
   |
   v
SILVER — pendiente: contrato, normalización y validación de registros
   |                            |                          --> QUARANTINE — pendiente: excepciones
   v
GOLD — pendiente: agregados por actividad, zona y periodo
```

El DAG actual ejecuta extracción y validación Bronze. No construye Silver ni Gold. La carpeta `data/` está preparada como volumen local y sus salidas se generan en tiempo de ejecución; los datos no se versionan en Git.

## 3. Bronze — implementación actual

Código responsable:

- `src/rendify/denue/client.py`: construye la URL de `BuscarAreaAct`, valida token y rango de registros, realiza la petición HTTP y devuelve una respuesta tipada con status, content type, bytes originales y registros parseados.
- `src/rendify/denue/extract.py`: realiza la consulta y guarda el payload y el manifiesto.
- `src/rendify/denue/validate.py`: valida manifiesto, referencia al archivo, status HTTP, tamaño, SHA-256, JSON y conteo.

Estructura creada por ejecución:

```text
data/bronze/denue/
└── extraction_date=YYYY-MM-DD/
    └── run_id=<run_id_sanitizado>/
        ├── response.json
        └── manifest.json
```

El manifiesto conserva fuente, método, run ID, timestamp UTC, parámetros no secretos, metadata HTTP, conteo, tamaño, checksum y nombre del archivo. Se excluyen claves de parámetros que contengan `token` o `secret`. La escritura del payload precede al manifiesto.

### Controles implementados

| Control | Comportamiento |
|---|---|
| Credenciales | Se rechaza token vacío y se evita incluir claves secretas en parámetros del manifiesto. |
| Reproducibilidad | Se registran parámetros de consulta y run ID. |
| Integridad | Se calcula SHA-256 sobre los bytes originales. |
| Consistencia | Se comprueba el tamaño, checksum y conteo. |
| Formato | Se valida que la respuesta sea JSON UTF-8 con lista de objetos. |
| Seguridad de ruta | El nombre del run y la referencia de archivo se restringen para evitar rutas inválidas/traversal. |

Estos controles prueban integridad técnica del archivo, no veracidad, representatividad ni cobertura del directorio.

## 4. Límites de la prueba actual

El DAG `denue_initial_extraction` en `dags/denue_initial_extraction.py`:

1. Lee `DENUE_API_TOKEN` del entorno del worker.
2. Ejecuta `BuscarAreaAct` para entidad `09` (CDMX), sin filtros adicionales en dimensiones de ubicación/actividad.
3. Solicita registros 1 a 15.
4. Escribe el resultado en Bronze.
5. Valida el manifiesto y el payload.

Se ejecuta manualmente (`schedule=None`), con `catchup=False` y una ejecución activa a la vez. Es un smoke test de acceso y persistencia; no es una carga completa ni acredita cobertura de CDMX.

## 5. Silver — diseño pendiente

Propósito: convertir registros del directorio en un contrato interno consistente y reusable.

Antes de implementar:
- inspeccionar una respuesta real y confirmar el esquema por método;
- documentar campo de origen, tipo, significado y disponibilidad;
- decidir campos requeridos/opcionales con evidencia;
- mantener códigos y claves geográficas como texto;
- definir claves y deduplicación solo después de analizar estabilidad y unicidad;
- preservar procedencia a archivo Bronze y run ID;
- diferenciar fecha de extracción, observación y periodo de referencia;
- no interpretar `Fecha_Alta` como fecha de apertura sin evidencia;
- minimizar atributos personales/de contacto.

Ruta objetivo: `data/silver/denue/`.

## 6. Gold — diseño pendiente

Primer producto candidato: agregados descriptivos por actividad económica, unidad territorial y periodo. Cada métrica debe incluir definición, unidad, filtros, reglas de deduplicación, cobertura, versión, fecha de referencia y linaje.

No se debe llamar “rentabilidad” o “probabilidad de éxito” al conteo de establecimientos ni a un índice heurístico. Las fuentes con granularidad o periodo distintos no se deben unir sin una metodología justificada.

Ruta objetivo: `data/gold/area_activity/`. Las features de ML se considerarán después de definir un objetivo observable y un método de evaluación; ruta posible `data/gold/ml_features/`.

## 7. Quarantine — diseño pendiente

La cuarentena es un flujo lateral, no una cuarta medalla. Cada excepción debe enlazar con su archivo Bronze, run ID, regla fallida, motivo y decisión. No altera ni sustituye el original.

Ruta objetivo: `data/quarantine/denue/`.

## 8. Orquestación y límites operativos

El DAG debe mantener la lógica de extracción/calidad dentro del paquete `rendify` y trasladar entre tareas únicamente rutas y metadatos pequeños. El DAG ya devuelve la ruta del manifiesto como XCom, no el dataset.

El Compose actual configura Airflow 3.3.2 con CeleryExecutor, Redis y PostgreSQL. El volumen `data` se comparte entre contenedores y `src` se monta con `PYTHONPATH`. La imagen Docker personalizada aún no está construida (el Dockerfile está vacío) y hay que verificar las dependencias del paquete en los workers antes de considerar validado el despliegue local.

## 9. Criterios de promoción

| Transición | Criterio |
|---|---|
| Fuente → Bronze | Respuesta capturada, manifiesto seguro y controles de integridad aprobados. |
| Bronze → Silver | Contrato versionado, esquema esperado, transformación reproducible y excepciones cuantificadas. |
| Silver → Gold | Indicador definido, calidad suficiente, granularidad/periodo compatibles y revisión de interpretación. |
| Registro → Quarantine | Regla fallida, motivo y referencia a Bronze conservados. |

## 10. Próximos incrementos

1. Ejecutar y documentar el DAG de muestra end-to-end.
2. Validar una respuesta real y su contrato.
3. Implementar perfilado y producir un reporte.
4. Implementar Silver con pruebas y cuarentena.
5. Diseñar agregados Gold descriptivos.
6. Incorporar catálogos y contexto geográfico/demográfico después de comprobar compatibilidad.

