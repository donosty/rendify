# Product brief — Rendify

**Versión:** 0.1  
**Estado:** definición inicial; pendiente de validación de fuentes y usuarios  
**Ámbito inicial:** Ciudad de México, comparación por alcaldía  
**Estrategia de infraestructura:** local primero

## 1. Resumen

Rendify será una plataforma de inteligencia comercial geoespacial que integra datos oficiales y otras fuentes verificables para ayudar a emprendedores, pequeños negocios y empresarios a investigar zonas y actividades económicas en México.

El producto busca facilitar comparaciones con indicadores comprensibles y trazables: establecimientos por actividad, distribución comercial y, cuando la integración sea válida, contexto demográfico y económico. Los resultados deberán explicar qué datos respaldan cada indicador, de qué periodo proceden y cuáles son sus límites.

Rendify es tanto un producto exploratorio como un proyecto colaborativo de portafolio para demostrar competencias de Data Engineering, analítica, Machine Learning, cloud, DevOps y desarrollo web.

## 2. Problema y oportunidad

Las personas que evalúan dónde abrir o expandir un negocio pueden necesitar combinar información de establecimientos, población, viviendas y contexto económico. Las fuentes pueden tener estructuras, periodos y niveles geográficos diferentes, lo que complica hacer comparaciones justas y reproducibles.

Rendify pretende reducir esa fricción mediante una canalización de datos documentada y una experiencia de consulta que facilite comparar zonas sin ocultar las limitaciones de la evidencia.

La herramienta apoyará la investigación y la toma de decisiones; no sustituirá un estudio de mercado completo ni la evaluación financiera de un negocio.

## 3. Usuarios iniciales

- Emprendedores que investigan posibles ubicaciones para un nuevo negocio.
- Propietarios de negocios que consideran expandirse a otra zona.
- Consultores y analistas que realizan investigación comercial.
- Estudiantes e investigadores interesados en economía local y distribución de establecimientos.

El MVP priorizará preguntas que puedan responderse con datos verificables, no una experiencia generalista para todos los sectores y ciudades desde el inicio.

## 4. Alcance inicial

### Geografía

- Ciudad objetivo: Ciudad de México.
- Unidad preferida: alcaldía.
- La integración con unidades más pequeñas, como AGEB urbana, se considerará solo si las fuentes tienen cobertura, claves y granularidad compatibles.
- No se distribuirán agregados de una unidad territorial a unidades más pequeñas sin una metodología válida.

### Actividades candidatas

1. Cafeterías.
2. Restaurantes.
3. Tiendas de artículos.
4. Gimnasios.

Las categorías son provisionales. «Tiendas de artículos» necesita una definición más precisa. Para todas las actividades habrá que mapear las etiquetas de producto a códigos y descripciones SCIAN confirmados y registrar la versión de clasificación utilizada.

### Funcionalidades candidatas para el MVP

- Buscar o filtrar actividades económicas.
- Consultar y comparar conteos y distribución de establecimientos por alcaldía.
- Incorporar población, viviendas u otras variables contextuales cuando sean adecuadas y comparables.
- Mostrar mapas y tablas con leyendas y unidades claras.
- Comparar zonas con los mismos indicadores y periodos.
- Indicar datos faltantes, cobertura y granularidad de cada fuente.
- Explicar las definiciones y transformaciones utilizadas para generar cada indicador.

El orden final de funcionalidades dependerá de la auditoría de datos. No se considera requisito del MVP entrenar un modelo predictivo si los datos no permiten formular y evaluar un objetivo defendible.

## 5. Fuera de alcance en la primera versión

- Afirmar que una zona garantiza el éxito de un negocio.
- Calcular rentabilidad sin datos financieros adecuados.
- Cubrir todas las ciudades, todos los sectores y todas las fuentes desde el inicio.
- Presentar una puntuación heurística como probabilidad de éxito.
- Incorporar Kafka, Hadoop, Kubernetes, Spark u otras tecnologías distribuidas sin una necesidad demostrada.
- Desplegar infraestructura cloud permanente antes de entender la carga, el coste y el valor del despliegue.
- Presentar datos de encuesta agregados como si fueran estimaciones fiables de cada colonia o alcaldía.

## 6. Conceptos e indicadores candidatos

| Indicador | Pregunta que ayuda a explorar | Requisito y cautela |
|---|---|---|
| Conteo de establecimientos | ¿Cuántos establecimientos de una actividad registra la fuente en la zona? | Definir actividad, identificador, fecha y reglas de deduplicación. |
| Establecimientos por población | ¿Cómo se compara la presencia registrada respecto a la población? | Denominadores geográficos y temporales compatibles. |
| Diversidad comercial | ¿Cuántas categorías comerciales aparecen en la zona? | Normalizar categorías y nivel de clasificación. |
| Contexto demográfico | ¿Qué población o viviendas caracterizan a la zona? | Registrar año, variables, unidad y metodología de la fuente. |
| Contexto económico | ¿Qué referencias económicas publicadas ayudan a contextualizar la zona? | Respetar el nivel territorial publicado y notas de confidencialidad. |
| Índice exploratorio de oportunidad | ¿Cómo se combinan varias señales para comparar zonas? | Definir normalización, pesos, supuestos, cobertura y versión; no llamarlo rentabilidad ni probabilidad de éxito. |

Las definiciones y fórmulas se mantendrán en `docs/metrics.md` cuando se establezcan. Hasta entonces, estos indicadores son candidatos, no métricas confirmadas.

## 7. Enfoque analítico y de Machine Learning

El producto debe separar tres tipos de resultado:

1. **Descriptivo:** resumen de lo observado en una fuente y periodo.
2. **Heurístico:** índice exploratorio con variables, normalización y pesos explícitos.
3. **Predictivo:** estimación obtenida por un modelo evaluado con datos adecuados.

No se llamará modelo predictivo a una suma ponderada de indicadores. Antes de entrenar un modelo habrá que definir una variable objetivo observable, comprobar su representatividad y disponibilidad y elegir una validación temporal o geográfica adecuada. Se comparará contra un baseline y se examinarán los errores por zona y actividad.

Si no se consiguen etiquetas de resultados comerciales confiables, Rendify podrá seguir siendo útil como herramienta de analítica descriptiva y comparación transparente.

## 8. Estrategia de datos

La arquitectura objetivo separará las capas:

- **Bronze:** respuestas o archivos originales preservados con metadatos de procedencia y extracción.
- **Silver:** datos normalizados, validados y con claves y unidades documentadas.
- **Gold:** indicadores agregados y resultados orientados a las preguntas del producto.

La auditoría debe registrar por separado la fecha de extracción, el periodo estadístico y la fecha de publicación cuando estén disponibles. Los identificadores y códigos oficiales se conservarán sin perder su formato. No se asumirá que distintas fuentes comparten el mismo periodo o nivel geográfico.

DENUE es la fuente candidata inicial para establecimientos. El censo, los Censos Económicos y la cartografía oficial son fuentes candidatas de contexto y vinculación. Su cobertura, accesibilidad, condiciones de uso y posibilidad real de integración siguen pendientes de comprobación. El inventario de investigación estará en `docs/data-sources.md`.

## 9. Decisiones tecnológicas

### Dirección de trabajo acordada

- Python 3.12 como versión inicial del proyecto.
- uv para gestionar entorno y dependencias.
- Desarrollo local primero.
- GitHub para control de versiones y colaboración.
- Datos originales separados de las transformaciones.
- Pruebas, documentación y revisiones cruzadas desde las primeras fases.

### Previstas, sujetas a la evolución del MVP

- requests o httpx para extracción.
- Pandas para exploración y transformaciones locales cuando sea adecuado.
- pytest y Ruff para pruebas y calidad de código.
- PostgreSQL/PostGIS para persistencia y datos geoespaciales si lo requiere el pipeline.
- SQL para transformaciones analíticas.
- Airflow cuando las dependencias y la operación justifiquen una herramienta de orquestación.
- Cloud Storage y BigQuery para una fase cloud, midiendo coste y valor.
- FastAPI para exponer indicadores y React + TypeScript u otra alternativa adecuada para la interfaz.
- GitHub Actions para automatizar pruebas, lint, build y despliegues cuando existan.

No se consideran componentes obligatorios del MVP Spark, Kafka, Hadoop, Kubernetes ni Terraform. Se adoptarán solo si una necesidad operacional o de escala lo justifica.

## 10. Calidad, privacidad y responsabilidad

- Conservar una copia identificable del original para permitir reprocesamiento.
- Validar esquemas, identificadores, nulos críticos, coordenadas, categorías y claves territoriales.
- Diseñar cargas repetibles e idempotentes antes de persistir grandes volúmenes.
- Documentar cobertura, periodos, unidades, transformaciones y limitaciones.
- Revisar términos de acceso, atribución y reutilización antes de redistribuir datos.
- No almacenar ni publicar campos personales que no sean necesarios para el análisis.
- No subir tokens, credenciales, archivos de entorno ni datos brutos indiscriminadamente al repositorio.
- Revisar permisos y costes antes de desplegar en cloud.
- Comunicar resultados como apoyo exploratorio a la decisión, no como garantía financiera.

## 11. Cómo mediremos el avance

### Criterios técnicos

- La ingesta puede repetirse con configuración externa y sin exponer secretos.
- Los originales pueden identificarse por fuente y fecha de extracción.
- La canalización registra registros recibidos, errores, duración y resultados de validación.
- Los indicadores se calculan de forma reproducible, con definiciones y pruebas.
- Los resultados reflejan el nivel de agregación real de la fuente.
- Una persona que no escribió un módulo puede ejecutarlo y explicar su funcionamiento.

### Criterios de producto

- Un usuario objetivo puede completar una comparación entre zonas.
- La interfaz explica las definiciones, fuentes y limitaciones relevantes.
- El equipo recoge feedback y registra las mejoras derivadas.
- Las afirmaciones del producto permanecen dentro de lo que los datos respaldan.

No se fijan todavía metas numéricas de adopción o impacto porque no se han validado usuarios, datos ni una línea base. Se definirán cuando exista una primera versión evaluable.

## 12. Plan por fases

1. **Sprint 0 — Definición y viabilidad:** alcance, categorías, repositorio, fuentes e indicadores candidatos.
2. **Sprint 1 — Auditoría DENUE:** documentación de acceso, consulta de prueba, extractor, muestra original, perfilado y pruebas.
3. **Ingesta local:** esquema de staging, almacenamiento, claves, deduplicación e idempotencia.
4. **Integración geográfica y censal:** validar claves, periodos y granularidad.
5. **Modelo analítico:** tablas de indicadores, fórmulas y pruebas.
6. **Cloud:** trasladar solo las cargas justificadas a servicios de GCP, con controles de permisos y coste.
7. **Orquestación y operación:** programar ejecuciones, manejar reintentos, logging y recuperación.
8. **ML baseline:** solo con objetivo, datos y esquema de evaluación apropiados.
9. **API y web:** visualización, filtros, comparador y explicaciones.
10. **CI/CD y validación:** despliegue controlado, seguridad, documentación y pruebas con usuarios.

Cada fase se cerrará mediante entregables verificables, no por el mero transcurso del tiempo.

## 13. Organización del equipo

El proyecto tiene dos colaboradores con responsabilidades principales complementarias:

- **Data Engineering:** ingesta, contratos de datos, capas, SQL, calidad y operación del pipeline.
- **Analítica y Machine Learning:** formulación del problema, indicadores, features, baselines, métricas y análisis de errores.
- **Cloud/DevOps:** responsabilidad compartida y rotación del responsable por sprint.
- **Producto/web:** diseño conjunto del flujo entre pregunta del usuario, indicador, datos y explicación.

Ambos revisarán cambios relevantes mediante pull requests, compartirán demostraciones breves y documentarán decisiones técnicas importantes. La meta es que ambos comprendan y puedan operar el flujo completo.

## 14. Riesgos principales

| Riesgo | Mitigación |
|---|---|
| Confundir presencia comercial con éxito | Usar lenguaje exploratorio y no prometer rentabilidad. |
| Periodos o geografías incompatibles | Registrar unidad, periodo y fuente; no forzar uniones. |
| Categorías demasiado amplias | Precisar actividades y verificar códigos antes de filtrar. |
| Datos incompletos o baja representatividad | Mostrar cobertura, ausencias y limitaciones. |
| Sobreingeniería | Incorporar herramientas por necesidad demostrable. |
| Costes cloud inesperados | Desarrollar localmente, revisar presupuestos y medir costes. |
| Dependencia de un solo colaborador | Revisiones cruzadas, documentación y práctica compartida. |
| Uso indebido de datos | Revisar términos, atribución, privacidad y campos necesarios. |

## Decisiones pendientes

- Validar método de acceso, límites, campos y condiciones de uso del DENUE.
- Confirmar cómo se identifican y filtran las actividades seleccionadas.
- Precisar la categoría «tiendas de artículos».
- Comprobar compatibilidad de claves geográficas y periodos entre fuentes.
- Definir fórmulas finales de los indicadores.
- Establecer criterios de evaluación de impacto con usuarios una vez exista un prototipo.

Este documento es una definición inicial de trabajo. Las decisiones pendientes no deben tratarse como funcionalidades implementadas ni como cobertura de datos validada.
