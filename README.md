# Rendify

**Inteligencia comercial geoespacial para apoyar decisiones de ubicación de negocios en México.**

Rendify es un proyecto colaborativo de datos y software que busca ayudar a emprendedores, pequeños negocios y empresarios a explorar y comparar zonas geográficas mediante datos oficiales y otras fuentes verificables. La primera etapa se enfocará en la Ciudad de México y preferirá las alcaldías como unidad inicial de comparación, sujeto a la validación de las fuentes.

> **Estado actual:** existe una prueba de concepto del extractor DENUE que conserva la respuesta en Bronze, escribe un manifiesto y puede validar/perfilar muestras con pruebas unitarias. Aún falta ejecutar una consulta autenticada real y verificar el esquema devuelto. El DAG y el Compose local de Airflow están añadidos, pero el entorno todavía no se ha ejecutado ni validado en una máquina. Silver/Gold siguen pendientes. La cobertura y compatibilidad de las fuentes también están pendientes.

## El problema

Antes de abrir o expandir un negocio, una persona necesita investigar el entorno comercial: qué tipos de establecimientos existen en distintas zonas, cómo se distribuyen y qué características demográficas o económicas pueden ayudar a contextualizar la decisión. Encontrar, combinar y evaluar estos datos puede ser difícil sin herramientas analíticas.

Rendify busca organizar esa información en indicadores comparables, con mapas y explicaciones que permitan investigar oportunidades y formular mejores preguntas de negocio.

## Qué construiremos

El MVP se desarrollará incrementalmente. La intención inicial es permitir:

- Explorar establecimientos por actividad económica y zona.
- Comparar alcaldías con indicadores definidos y trazables.
- Incorporar contexto demográfico y económico cuando las fuentes sean compatibles.
- Visualizar resultados en mapas, tablas y comparaciones.
- Mostrar procedencia, periodo de referencia, cobertura, datos faltantes y limitaciones.
- Explicar los componentes de cualquier índice o puntuación que se publique.

La primera ciudad objetivo es **Ciudad de México**. Las unidades territoriales iniciales serán las **alcaldías**, sin descartar otras geografías si las fuentes permiten una integración válida.

### Actividades económicas candidatas

1. Cafeterías.
2. Restaurantes.
3. Tiendas de artículos —la categoría debe precisarse antes de crear filtros reproducibles.
4. Gimnasios.

Son categorías de producto provisionales, no códigos SCIAN confirmados. Los códigos y sus descripciones se documentarán después de revisar la clasificación y los campos disponibles en las fuentes.

## Qué no promete Rendify

La presencia de establecimientos no demuestra por sí sola que un negocio haya tenido éxito. Una zona con pocos establecimientos no es necesariamente una oportunidad, y una zona con muchos negocios no es necesariamente rentable.

Los datos públicos pueden ayudar a explorar demanda potencial, competencia y contexto local; normalmente no sustituyen información financiera de cada negocio, como ventas, costes, renta, nómina, impuestos y operación. Por eso, el MVP hablará de **indicadores exploratorios u oportunidad comercial estimada**, no de garantías de éxito o rentabilidad.

No presentaremos correlaciones como causalidad, ni una puntuación heurística como si fuera una probabilidad validada. La cobertura, granularidad y periodo de cada fuente deben acompañar las conclusiones.

## Principios de desarrollo

- **Validar antes de diseñar en exceso:** auditar muestras reales antes de fijar contratos y modelos definitivos.
- **Local primero:** desarrollar y reproducir el flujo localmente; incorporar cloud solo cuando aporte valor medible.
- **Trazabilidad:** preservar los datos originales y registrar fuente, parámetros no secretos, fecha de extracción, periodo de referencia y versión.
- **Gobierno de datos inspirado en DAMA-DMBOK:** documentar responsables, fuentes, definiciones, metadatos, calidad, seguridad y criterios de uso, con controles proporcionales al tamaño del equipo.
- **Capas medallón:** Bronze conserva originales; Silver normaliza y valida; Gold publica indicadores con definiciones y linaje. La cuarentena gestiona excepciones sin sustituir el original.
- **Calidad comprobable:** automatizar controles por capa y exigir evidencia antes de promover o publicar datasets.
- **Trazabilidad:** cada salida debe enlazar con la fuente, la ejecución, el contrato y la versión del código.
- **Simplicidad intencional:** no incluir Spark, Kafka, Kubernetes ni otros componentes por moda; cada tecnología debe responder a una necesidad concreta.
- **Responsabilidad:** revisar atribución, condiciones de reutilización, minimización, seguridad y costes antes de publicar.

## Roadmap de alto nivel

1. **Sprint 0 — Definición y viabilidad:** delimitar el MVP, revisar el repositorio, documentar fuentes, actividades e indicadores candidatos.
2. **Sprint 1 — Auditoría de datos:** validar el método de acceso al DENUE, ejecutar una consulta de prueba, crear un extractor reproducible y generar un informe de calidad.
3. **Ingesta local:** definir persistencia, configuración, identificadores, idempotencia y almacenamiento en PostgreSQL/PostGIS si resulta apropiado.
4. **Integración y analítica:** evaluar la integración geográfica y censal, diseñar indicadores y añadir pruebas de calidad.
5. **Cloud y operación:** evaluar Cloud Storage, BigQuery y ejecución programada con presupuesto y permisos mínimos.
6. **ML baseline:** formular un objetivo medible y validar si existen etiquetas y observaciones adecuadas; comparar cualquier modelo con una referencia simple.
7. **API y experiencia web:** exponer indicadores validados y ofrecer filtros, mapas, comparaciones y explicaciones.
8. **CI/CD y validación:** automatizar pruebas y builds, documentar el despliegue y evaluar la utilidad con usuarios.

Las fases son una secuencia de trabajo, no una promesa de que todos los componentes serán necesarios. No se pasará a ML antes de disponer de datos fiables y de un objetivo evaluable.

## Stack tecnológico previsto

| Área | Tecnología prevista | Estado |
|---|---|---|
| Lenguaje | Python 3.12 | Configurado como versión del proyecto |
| Entorno y dependencias | uv | Configuración inicial presente; dependencias por definir |
| Extracción | Biblioteca estándar urllib en la prueba de concepto | Implementación inicial; dependencias externas evitadas por ahora |
| Análisis local | Pandas | Pendiente; se usará si aporta valor |
| Calidad y estilo | unittest de Python en esta primera etapa; Ruff por configurar | Pruebas unitarias iniciales añadidas; no se han ejecutado en un entorno local en esta sesión |
| Almacenamiento local | PostgreSQL + PostGIS | Fase posterior |
| Transformación | SQL y Python | Fase posterior |
| Orquestación | Apache Airflow 3.3.2 (imagen Python 3.12) | DAG y Compose de desarrollo añadidos; falta ejecutar el entorno y validar el DAG |
| Cloud | Google Cloud Storage, BigQuery y servicios adecuados de GCP | Después de validar el flujo local |
| API y web | FastAPI; React + TypeScript u otra opción adecuada | Fase posterior |
| CI/CD | GitHub Actions | Pendiente |

## Estructura del repositorio y capas de datos

La estructura del código separa orquestación, lógica de aplicación, pruebas y documentación de gobierno. Las carpetas de datos representan el patrón medallón lógico; los datos generados se crean en tiempo de ejecución y no se versionan.

~~~text
rendify/
├── dags/
│   └── denue_initial_extraction.py  # DAG inicial; pendiente de prueba en Airflow
├── config/
│   └── reference/
│       └── README.md                # Política para catálogos y mapeos versionados
├── data/                            # Resultados locales; no versionar datos generados
│   ├── bronze/denue/                # Respuestas originales + manifiestos
│   ├── silver/denue/                # Registros normalizados y validados
│   ├── gold/area_activity/          # Agregados para comparación por zona/actividad
│   ├── gold/ml_features/            # Solo al definir un caso ML defendible
│   └── quarantine/denue/            # Excepciones con referencia al original
├── docs/
│   ├── architecture/
│   │   └── medallion-architecture.md
│   ├── decisions/
│   │   └── 0001-data-governance-and-medallion.md
│   ├── governance/
│   │   ├── data-governance-charter.md
│   │   ├── data-management-plan.md
│   │   ├── data-dictionary.md
│   │   ├── data-quality-rules.md
│   │   └── data-assets-register.md
│   ├── denue-api-research.md
│   ├── data-sources.md
│   └── product-brief.md
├── reports/                         # Reportes seleccionados de calidad/perfilado
├── schemas/
│   └── README.md                    # Contratos una vez validado el esquema real
├── scripts/
│   ├── extract_denue_sample.py      # Ejecuta la muestra fuera de Airflow
│   └── profile_denue.py             # Plantilla de perfilado anterior
├── src/rendify/
│   ├── denue/                       # Cliente, extracción, transformación y validación
│   └── profiling/                   # Perfilado y reportes de calidad
├── tests/
│   └── denue/                       # Pruebas unitarias con respuestas simuladas
├── .env.example                    # Variables locales, sin token real
├── Dockerfile                      # Reservado; no requerido por el stack actual
├── docker-compose.yaml              # Airflow 3 local con LocalExecutor
├── pyproject.toml
└── uv.lock
~~~

El cliente, la extracción Bronze, la validación, el perfilado y un DAG de muestra ya tienen una implementación inicial, cubierta por tests unitarios simulados. El esquema real de DENUE y el DAG todavía requieren una ejecución de extremo a extremo. Silver y Gold son etapas futuras; sus rutas son parte de la arquitectura objetivo. Los datos generados no se subirán a Git.

### Cómo se relaciona DAMA con medallón

DAMA-DMBOK inspira las responsabilidades, definiciones, metadatos, seguridad, calidad, integración y decisiones de uso. Medallón organiza el refinamiento técnico de los datos. El equipo implementará ambas cosas de forma ligera; no se afirma una implantación completa ni certificación DAMA.

Documentos de referencia:
- [Marco de gobierno y responsabilidades](docs/governance/data-governance-charter.md)
- [Plan de gestión de datos](docs/governance/data-management-plan.md)
- [Diccionario de datos](docs/governance/data-dictionary.md)
- [Reglas de calidad](docs/governance/data-quality-rules.md)
- [Registro de activos de datos](docs/governance/data-assets-register.md)
- [Arquitectura medallón](docs/architecture/medallion-architecture.md)

## Preparar el entorno

Requisitos iniciales: Git, Python 3.12 y uv.

```bash
git clone git@github.com:donosty/rendify.git
cd rendify
uv sync
uv run rendify
```

El comando `uv run rendify` sigue siendo una entrada de plantilla y puede imprimir `Hello from rendify!`. La extracción se ejecuta por separado con el script de muestra descrito abajo; todavía no existe una aplicación funcional de inteligencia comercial.

Cuando se incorporen dependencias, pruebas y herramientas de calidad, sus comandos se documentarán aquí y en los archivos de configuración correspondientes.

### Prueba de extracción DENUE (muestra pequeña)

Esta prueba de concepto consulta una sola página mediante BuscarAreaAct para CDMX (entidad 09) y guarda la respuesta original en data/bronze/denue/, más un manifiesto JSON con parámetros no secretos, estado, número de registros y checksum. No es una extracción completa ni un contrato definitivo de DENUE.

1. Crea tu archivo local de variables y coloca el token proporcionado por INEGI:

~~~bash
cp .env.example .env
# Edita .env y establece DENUE_API_TOKEN con tu token real.
set -a
source .env
set +a
~~~

No compartas ni subas .env. El token de DENUE forma parte de la ruta de la petición, por lo que no debe registrarse la URL completa.

2. Instala el paquete del proyecto y ejecuta las pruebas unitarias:

~~~bash
uv sync
uv run python -m unittest discover -s tests -v
~~~

Las pruebas usan respuestas simuladas; no necesitan el token y no demuestran que la conexión real a DENUE esté validada.

3. Ejecuta la muestra. Los parámetros predeterminados solicitan registros del 1 al 15 de la entidad 09:

~~~bash
uv run python scripts/extract_denue_sample.py
~~~

Se puede cambiar el rango para pruebas pequeñas:

~~~bash
uv run python scripts/extract_denue_sample.py --entity-code 09 --start-record 1 --end-record 15
~~~

El comando genera tres resultados: respuesta original Bronze, manifest.json y reports/generated/denue_profile_<run_id>.json. Los datos generados están excluidos de Git. Si el manifiesto supera la validación, el perfil informa campos presentes/no observados, nulos, duplicados, coordenadas y valores frecuentes de algunas propiedades.

**Limitaciones actuales:** por ahora se consulta una única página; no implementa paginación completa, Silver, Gold ni comparación de conteos con Cuantificar. Los campos identificadores requeridos y el esquema continúan sujetos a la verificación de una respuesta real. El DAG de Airflow está creado, pero no se incluye todavía una configuración Docker Compose validada.

### Ejecutar Airflow localmente

El Compose se basa en la plantilla oficial de Airflow 3.3.2, adaptada para usar LocalExecutor y evitar Redis/workers para el primer flujo. Es una configuración de desarrollo, no de producción. Airflow recomienda reservar al menos 4 GB de memoria para su entorno en Docker; el consumo real dependerá de los servicios y la carga. Consulta la [guía oficial de Docker Compose de Airflow](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/).

1. Configura el archivo local:

~~~bash
cp .env.example .env
~~~

Edita .env con tu token de DENUE. En Linux, cambia AIRFLOW_UID al resultado de id -u para que los archivos montados no queden con un propietario inesperado. No subas este archivo al repo.

2. Crea directorios de ejecución e inicializa Airflow:

~~~bash
mkdir -p dags logs plugins config data reports
docker compose up airflow-init
~~~

3. Arranca los servicios:

~~~bash
docker compose up -d
docker compose ps
~~~

Abre http://localhost:8080. Las credenciales de desarrollo iniciales son las especificadas en .env (AIRFLOW_WWW_USER_USERNAME y AIRFLOW_WWW_USER_PASSWORD, por defecto airflow / airflow).

4. En la interfaz, localiza rendify_denue_initial_extraction y lánzalo manualmente. El DAG debe crear datos bajo data/bronze/denue/ y un perfil bajo reports/generated/. Si falla, revisa los logs de las tareas y que DENUE_API_TOKEN esté presente en .env.

Para detener sin borrar la metadata ni los datos:

~~~bash
docker compose down
~~~

Esta configuración aún requiere una prueba real en la máquina de desarrollo. Para borrar la base de metadata local y reiniciar Airflow desde cero, Docker ofrece docker compose down --volumes, pero eso elimina el volumen de PostgreSQL; no ejecutes esa variante si necesitas conservar historial.

## Forma de trabajo

El equipo tendrá dos colaboradores con responsabilidades principales complementarias en Data Engineering y analítica/Machine Learning. Ambos revisarán las decisiones relevantes y deberán poder explicar el flujo completo.

- Trabajar en ramas cortas con nombres descriptivos.
- Abrir pull requests pequeñas y solicitar revisión cruzada.
- Usar commits descriptivos.
- Definir criterios de aceptación para cada tarea.
- Registrar decisiones arquitectónicas relevantes en `docs/decisions/`.
- Hacer una demostración y una revisión de aprendizajes al cerrar cada sprint.

## Fuentes iniciales

- [API del DENUE — INEGI](https://www.inegi.org.mx/servicios/api_denue.html)
- [Censo de Población y Vivienda 2020 — INEGI](https://www.inegi.org.mx/programas/ccpv/2020/)
- [Censos Económicos 2024 — INEGI](https://www.inegi.org.mx/programas/ce/2024/default.html)
- [ENIGH 2024 — INEGI](https://www.inegi.org.mx/programas/enigh/nc/2024/default.html)
- [Documentación de Google Cloud Storage](https://cloud.google.com/storage/docs)
- [Documentación de BigQuery](https://cloud.google.com/bigquery/docs)
- [Documentación de Cloud Run](https://cloud.google.com/run/docs)
- [Documentación de Apache Airflow](https://airflow.apache.org/docs/)

La existencia de una fuente candidata no significa que su cobertura, permisos de uso o granularidad estén validados. Consulta `docs/data-sources.md` para conocer el estado y las preguntas pendientes.

## Criterio de éxito

Rendify deberá permitir que otra persona clone el repositorio, prepare el entorno, ejecute el flujo documentado, compruebe la calidad y procedencia de los datos y entienda cómo se calcularon los indicadores. La utilidad para los usuarios se evaluará con pruebas y feedback; no se asumirá solo por tener una arquitectura técnica.
