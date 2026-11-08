# Rendify

**Inteligencia comercial geoespacial para apoyar decisiones de ubicación de negocios en México.**

Rendify es un proyecto colaborativo de ingeniería y análisis de datos que busca ayudar a emprendedores y negocios a explorar y comparar zonas geográficas mediante datos oficiales y otras fuentes verificables. El alcance inicial se concentra en la **Ciudad de México**, con las **alcaldías** como unidad geográfica preferida.

> **Estado del proyecto (7 de noviembre de 2026):** ya existe una primera integración técnica con la API del DENUE. El repositorio contiene un cliente HTTP, extracción y persistencia en Bronze, validación de integridad, un DAG manual de Airflow 3 y pruebas unitarias. La extracción actual es una muestra pequeña de prueba; no representa todavía una ingesta completa de CDMX. Las capas Silver y Gold, el perfilado, los indicadores y la aplicación de usuario siguen pendientes.

## Objetivo

Rendify pretende organizar información sobre establecimientos, actividad económica y contexto territorial para facilitar preguntas como:

- ¿Cómo se distribuyen ciertos tipos de establecimientos entre alcaldías?
- ¿Qué diferencias aparecen entre zonas para una misma actividad?
- ¿Qué contexto demográfico o económico puede ayudar a interpretar esas diferencias?

El producto será una herramienta de exploración y apoyo a la investigación. La presencia de establecimientos no demuestra éxito, demanda, rentabilidad ni probabilidad de supervivencia. Toda comparación deberá exponer su fuente, periodo, granularidad y limitaciones.

## Alcance inicial

- **Geografía:** Ciudad de México; alcaldías como unidad inicial preferida.
- **Actividades candidatas:** cafeterías, restaurantes, gimnasios y tiendas de artículos. Esta última categoría todavía necesita acotarse.
- **Fuente en implementación:** Directorio Estadístico Nacional de Unidades Económicas (DENUE), del INEGI.
- **Fuentes de contexto candidatas:** Censo de Población y Vivienda 2020, Censos Económicos 2024 y catálogos/cartografía geoestadística. ENIGH queda como posible fase posterior.
- **Estrategia técnica:** local primero; cloud solo cuando el flujo y sus necesidades estén mejor definidos.

Las categorías comerciales son etiquetas de producto, no códigos SCIAN confirmados. No se deben fijar filtros reproducibles hasta documentar los códigos, descripciones, versión de clasificación y reglas de inclusión/exclusión.

## Implementación disponible

### 1. Cliente DENUE

En `src/rendify/denue/client.py` se encuentra:

- Construcción de URL para el método `BuscarAreaAct`.
- Codificación de parámetros de ruta.
- Validación del token y del rango inclusivo de registros.
- Petición HTTP con timeout configurable.
- Normalización de errores HTTP, timeout, conexión y JSON inválido mediante `DenueAPIError`.
- Respuesta tipada `DenueAPIResponse`, que conserva código HTTP, content type, bytes originales y registros parseados.

El cliente utiliza la biblioteca estándar de Python (`urllib` y `json`); no usa actualmente `requests` ni `httpx`.

### 2. Extracción y persistencia Bronze

En `src/rendify/denue/extract.py`:

- `extract_denue_to_bronze()` consulta el endpoint y delega la persistencia.
- `save_bronze_response()` conserva los bytes originales en `response.json`.
- Genera un `manifest.json` con fuente, método, run ID, timestamp UTC, parámetros no secretos, metadatos HTTP, conteo, tamaño, checksum SHA-256 y referencia al archivo.
- Evita escribir credenciales en los parámetros del manifiesto.
- Escribe primero la respuesta y después el manifiesto, usando archivos temporales y reemplazo.

Ruta esperada por ejecución:

```text
data/bronze/denue/
└── extraction_date=YYYY-MM-DD/
    └── run_id=<run>/
        ├── response.json
        └── manifest.json
```

Los datos generados son artefactos de ejecución y no deben versionarse en Git.

### 3. Validación Bronze

En `src/rendify/denue/validate.py`, `validate_bronze_response()` comprueba:

- Existencia y lectura del manifiesto.
- Presencia de campos mínimos y tipo de metadatos.
- Fuente y método esperados.
- Ausencia de claves de credenciales en los parámetros.
- Código HTTP 200.
- Referencia segura al archivo de respuesta.
- Existencia, tamaño y checksum del payload.
- JSON UTF-8 válido, lista de objetos y conteo consistente.

La función devuelve un resumen pequeño apto para metadatos de la tarea; no pasa el dataset completo por XCom.

### 4. Orquestación Airflow

`dags/denue_initial_extraction.py` define el DAG `denue_initial_extraction` con la API `airflow.sdk` (estilo Airflow 3):

1. `extract_denue`: lee `DENUE_API_TOKEN`, consulta DENUE y guarda la respuesta en Bronze.
2. `validate_bronze`: valida el manifiesto y el payload generado por la extracción.

El DAG no tiene schedule automático (`schedule=None`), desactiva catchup y permite una ejecución activa a la vez. La muestra se configura actualmente para la entidad `09` (CDMX), sin filtros adicionales y con registros del 1 al 15. **Es una prueba de conectividad y persistencia, no una extracción completa ni un pipeline analítico.**

El volumen `data` se monta en los contenedores para compartir los archivos entre tareas. La variable `DENUE_API_TOKEN` se inyecta en el worker desde el entorno.

### 5. Pruebas disponibles

| Suite | Qué verifica |
|---|---|
| `tests/denue/test_denue_client.py` | Construcción de URL, codificación, token y límites del rango. |
| `tests/denue/test_denue_extract.py` | Escritura del original, manifiesto, checksum, metadatos y exclusión del token. |
| `tests/denue/test_denue_validate.py` | Validación correcta y rechazo de manifiestos/payloads inconsistentes. |
| `tests/integration/test_denue_api.py` | Consulta real optativa, validación de respuesta y observación de campos. Requiere token y servicio disponible. |

Las pruebas de integración se omiten si no se configura `DENUE_API_TOKEN`. No se debe confundir una prueba unitaria con una verificación del servicio real.

## Estado por componente

| Componente | Estado | Evidencia / pendiente |
|---|---|---|
| Cliente HTTP DENUE | Implementado | `client.py`; pruebas unitarias. |
| Extracción a Bronze | Implementada | `extract.py`; original y manifiesto. |
| Integridad Bronze | Implementada | SHA-256, tamaño, JSON y conteo. |
| DAG inicial Airflow 3 | Implementado | Extracción + validación manual de muestra. |
| Pruebas unitarias DENUE | Implementadas | Tres módulos bajo `tests/denue/`. |
| Prueba contra API real | Implementada como test optativo | Requiere token, conectividad y ejecución explícita. |
| Perfilado de datos | Pendiente | El módulo y el script actuales son plantillas. |
| Silver y contrato canónico | Pendiente | Aún no hay transformación ni esquema confirmado. |
| Cuarentena operativa | Pendiente | Reglas y diseño documentados; flujo no implementado. |
| Gold e indicadores | Pendiente | No hay agregados de negocio. |
| Catálogos SCIAN y geográficos | Pendiente | Deben versionarse después de validar fuentes. |
| PostgreSQL/PostGIS | No implementado para los datos de Rendify | PostgreSQL de Compose es el metastore de Airflow. |
| API, interfaz y mapas | Pendiente | No existe aplicación de producto todavía. |
| Cloud / CI-CD | Pendiente | No desplegado ni automatizado. |

## Arquitectura de datos

El modelo lógico adoptado es medallón:

```text
DENUE API
   |
   v
BRONZE  -> respuesta original + manifiesto
   |
   v
SILVER  -> registros normalizados y validados
   |                    |                  -> QUARANTINE: excepciones trazables
   v
GOLD    -> agregados e indicadores por actividad/zona/periodo
```

A día de hoy, solo la persistencia y validación inicial de Bronze están implementadas en código. Silver, Gold y cuarentena son el diseño objetivo. DAMA-DMBOK inspira el gobierno de fuentes, definiciones, responsables, calidad, metadatos y seguridad; el proyecto aplica prácticas ligeras y no afirma una implantación completa ni certificación.

Documentos principales:

- [Arquitectura medallón](docs/architecture/medallion-architecture.md)
- [Investigación de API DENUE](docs/denue-api-research.md)
- [Inventario de fuentes](docs/data-sources.md)
- [Brief de producto](docs/product-brief.md)
- [Índice de gobierno de datos](docs/governance/README.md)
- [Registro de decisiones (ADR)](docs/decisions/0001-data-governance-and-medallion.md)

## Estructura del repositorio

```text
rendify/
├── dags/
│   └── denue_initial_extraction.py
├── config/reference/
├── data/                         # Datos locales generados; no versionar
├── docs/
│   ├── architecture/
│   ├── decisions/
│   ├── governance/
│   ├── data-sources.md
│   ├── denue-api-research.md
│   └── product-brief.md
├── reports/                      # Reservado para reportes generados/revisados
├── schemas/                      # Contratos pendientes de confirmar
├── scripts/
│   └── profile_denue.py          # Placeholder de perfilado
├── src/rendify/
│   ├── denue/
│   │   ├── client.py
│   │   ├── exceptions.py
│   │   ├── extract.py
│   │   └── validate.py
│   └── profiling/
│       └── denue_profile.py      # Placeholder
├── tests/
│   ├── denue/
│   └── integration/
├── docker-compose.yaml
├── Dockerfile                    # Vacío actualmente
├── pyproject.toml
└── uv.lock
```

## Preparar el entorno

### Ejecución del paquete Python

El proyecto requiere Python `>=3.12` y usa `uv`. En el estado actual:

```bash
git clone https://github.com/donosty/rendify.git
cd rendify
uv sync
uv run rendify
```

El comando `uv run rendify` ejecuta la entrada de plantilla que imprime `Hello from rendify!`; no ejecuta el pipeline DENUE.

### Ejecutar pruebas unitarias

Los tests están escritos con `unittest`. El descubrimiento puede ejecutarse con el entorno que tenga el paquete disponible:

```bash
PYTHONPATH=src python -m unittest discover -s tests/denue -v
```

El repositorio todavía no declara en `pyproject.toml` un comando de pruebas ni dependencias de Airflow. Comprueba e instala las dependencias necesarias en el entorno de desarrollo antes de ejecutar las suites. La prueba real de integración está separada y requiere `python-dotenv`, un token válido y acceso a Internet:

```bash
PYTHONPATH=src python -m unittest discover -s tests/integration -v
```

Usa `.env` local para el token; no lo subas al repositorio. Revisa siempre `.gitignore` antes de guardar credenciales.

### Airflow con Docker Compose

El Compose actual está basado en Apache Airflow `3.3.2`, CeleryExecutor, Redis y PostgreSQL. Es configuración local de desarrollo, no producción.

1. Crea un archivo `.env` local con las variables requeridas por el Compose, incluyendo `DENUE_API_TOKEN`, `FERNET_KEY`, `AIRFLOW__API_AUTH__JWT_SECRET` y `AIRFLOW_UID` cuando corresponda. No uses valores de ejemplo en un entorno expuesto.
2. Asegúrate de que el worker pueda instalar/importar las dependencias y el paquete Rendify. El `Dockerfile` está vacío y el Compose usa la imagen oficial por defecto; la imagen personalizada aún debe prepararse para incluir dependencias del proyecto.
3. Inicia los servicios:

```bash
docker compose up airflow-init
docker compose up -d
```

4. Abre la UI local en [http://localhost:8080](http://localhost:8080), activa `denue_initial_extraction` y ejecútalo manualmente.
5. Consulta los logs de `extract_denue` y `validate_bronze`, y revisa los archivos creados en `data/bronze/denue/`.

El DAG necesita que el paquete `rendify` sea importable por los componentes de Airflow; el volumen `src` se monta y `PYTHONPATH=/opt/airflow/src` está declarado, pero las dependencias y permisos del entorno todavía deben verificarse. No damos por garantizada la ejecución en contenedor hasta completar esa validación.

## Variables sensibles

- `DENUE_API_TOKEN`: token para la API.
- `FERNET_KEY`: clave Fernet de Airflow.
- `AIRFLOW__API_AUTH__JWT_SECRET`: secreto JWT para Airflow.

Mantén estas variables fuera de Git y de los manifiestos. No compartas logs que contengan secretos. El manifiesto de Rendify guarda parámetros de consulta no secretos, no el token.

## Próximos pasos técnicos

1. **Cerrar la base de ejecución:** definir dependencias y una imagen reproducible de Airflow que incluya el paquete Rendify.
2. **Ejecutar el DAG de muestra de extremo a extremo:** conservar evidencia de ejecución, validar el manifiesto generado y comprobar el volumen compartido.
3. **Auditar la respuesta real:** confirmar nombres/tipos de campos, cobertura, códigos SCIAN, semántica geográfica, límites y condiciones de uso.
4. **Perfilado reproducible:** implementar el script/módulo de perfilado y guardar un reporte de muestra, sin publicar datos sensibles.
5. **Silver:** aprobar el contrato, normalizar tipos y claves y diseñar cuarentena.
6. **Pruebas y CI:** cubrir cliente, persistencia, validación y transformaciones; automatizar pruebas y lint.
7. **Gold descriptivo:** definir y probar indicadores comparables por alcaldía/actividad/periodo.
8. **Integración de contexto:** estudiar fuentes demográficas y económicas solo después de validar claves, unidades y periodos.
9. **Producto y ML:** diseñar interfaz e investigar un objetivo ML únicamente cuando existan datos y una evaluación defendible.

## Fuentes

- [API del DENUE — INEGI](https://www.inegi.org.mx/servicios/api_denue.html)
- [Censo de Población y Vivienda 2020 — INEGI](https://www.inegi.org.mx/programas/ccpv/2020/)
- [Censos Económicos 2024 — INEGI](https://www.inegi.org.mx/programas/ce/2024/default.html)
- [Documentación de Apache Airflow](https://airflow.apache.org/docs/)
- [Documentación de uv](https://docs.astral.sh/uv/)

