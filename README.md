# Rendify

**Inteligencia comercial geoespacial para apoyar decisiones de ubicación de negocios en México.**

Rendify es un proyecto colaborativo de datos y software que busca ayudar a emprendedores, pequeños negocios y empresarios a explorar y comparar zonas geográficas mediante datos oficiales y otras fuentes verificables. La primera etapa se enfocará en la Ciudad de México y preferirá las alcaldías como unidad inicial de comparación, sujeto a la validación de las fuentes.

> **Estado actual:** repositorio en etapa de definición y auditoría de datos. La estructura inicial está creada; el extractor, el modelo analítico y la aplicación todavía no están implementados. La cobertura y compatibilidad de las fuentes aún deben verificarse.

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
| Extracción | requests o httpx | Pendiente |
| Análisis local | Pandas | Pendiente; se usará si aporta valor |
| Calidad y estilo | pytest, Ruff | Pendiente de configuración |
| Almacenamiento local | PostgreSQL + PostGIS | Fase posterior |
| Transformación | SQL y Python | Fase posterior |
| Orquestación | Apache Airflow | Planeado desde el primer pipeline orquestado; la lógica de extracción seguirá siendo ejecutable fuera de Airflow |
| Cloud | Google Cloud Storage, BigQuery y servicios adecuados de GCP | Después de validar el flujo local |
| API y web | FastAPI; React + TypeScript u otra opción adecuada | Fase posterior |
| CI/CD | GitHub Actions | Pendiente |

## Estructura del repositorio y capas de datos

La estructura del código separa orquestación, lógica de aplicación, pruebas y documentación de gobierno. Las carpetas de datos representan el patrón medallón lógico; los datos generados se crean en tiempo de ejecución y no se versionan.

~~~text
rendify/
├── dags/
│   └── denue_initial_extraction.py  # Punto de entrada Airflow; implementar
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
│   └── profile_denue.py             # Punto de entrada útil para perfilado local
├── src/rendify/
│   ├── denue/                       # Cliente, extracción, transformación y validación
│   └── profiling/                   # Perfilado y reportes de calidad
├── tests/
│   └── denue/                       # Pruebas de cliente, contrato y calidad
├── pyproject.toml
└── uv.lock
~~~

Los archivos de código existentes en varias de estas rutas son actualmente plantillas vacías; el árbol describe la organización objetivo, no una afirmación de que el pipeline ya funcione. Los directorios de salida de datos se crearán cuando se ejecute la ingesta. Las respuestas originales, datos Silver/Gold y cuarentena no se subirán a Git.

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

En el estado actual, el último comando ejecuta la entrada de plantilla e imprime `Hello from rendify!`. Esto solo comprueba la entrada inicial cuando se ejecuta correctamente; todavía no existe una aplicación funcional de inteligencia comercial.

Cuando se incorporen dependencias, pruebas y herramientas de calidad, sus comandos se documentarán aquí y en los archivos de configuración correspondientes.

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
