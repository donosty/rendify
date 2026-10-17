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
- **Capas separadas:** orientar la evolución hacia Bronze (originales), Silver (datos normalizados y validados) y Gold (indicadores de producto).
- **Calidad comprobable:** automatizar pruebas para extracción, transformación, integridad y consistencia.
- **Simplicidad intencional:** no incluir Spark, Kafka, Kubernetes ni otros componentes por moda; cada tecnología debe responder a una necesidad concreta.
- **Responsabilidad:** revisar atribución, condiciones de reutilización, privacidad, seguridad y costes antes de publicar.

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
| Orquestación | Airflow si hay dependencias que orquestar | Fase posterior; no es requisito de la primera extracción |
| Cloud | Google Cloud Storage, BigQuery y servicios adecuados de GCP | Después de validar el flujo local |
| API y web | FastAPI; React + TypeScript u otra opción adecuada | Fase posterior |
| CI/CD | GitHub Actions | Pendiente |

## Estructura actual del repositorio

La estructura siguiente refleja los archivos que existen actualmente en la rama principal. Los archivos marcados como plantilla o vacíos todavía no contienen una implementación funcional.

```text
rendify/
├── .dockerignore             # Vacío; Docker no está configurado
├── .gitignore                # Reglas iniciales de exclusión
├── .python-version           # Python 3.12
├── Dockerfile                # Vacío; reservado para una etapa posterior
├── README.md                 # Este documento
├── data/
│   └── .gitkeep              # Mantiene el directorio en Git
├── docker-compose.yaml       # Vacío; reservado para una etapa posterior
├── docs/
│   ├── product-brief.md      # Definición del producto
│   └── data-sources.md       # Inventario y auditoría de fuentes
├── pyproject.toml            # Metadatos del paquete y configuración de uv
├── reports/
│   └── .gitkeep              # Mantiene el directorio en Git
├── scripts/
│   └── profile_denue.py      # Vacío; futuro perfilado de datos
├── src/
│   └── rendify/
│       └── __init__.py       # Entrada de plantilla; imprime un saludo
└── uv.lock                   # Lockfile inicial, sin dependencias de aplicación
```

A medida que se implemente el extractor, se añadirá una estructura modular para la ingesta y sus pruebas. No se añadirán directorios vacíos para componentes futuros hasta que exista una tarea concreta que los necesite.

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
