# Marco de gobierno de datos de Rendify

**Versión:** 0.1  
**Estado:** propuesta inicial para revisión del equipo  
**Alcance:** fuentes, conjuntos de datos, transformaciones, indicadores y productos analíticos de Rendify.

## 1. Propósito

Rendify aplicará prácticas proporcionales inspiradas en DAMA-DMBOK para que los datos sean comprensibles, trazables, seguros, reutilizables y adecuados para las decisiones que apoyan. Este documento no afirma una implantación completa ni una certificación DAMA; traduce disciplinas relevantes a controles manejables para un equipo de dos personas.

DAMA-DMBOK es un marco de conocimientos de gestión de datos. El esquema medallón, documentado por separado, describe cómo refinar los datos a través de capas. Son complementarios: el medallón organiza el procesamiento; el gobierno establece decisiones, responsabilidades, definiciones y controles.

## 2. Principios

1. **Responsabilidad explícita:** cada fuente y producto de datos tendrá una persona responsable de su definición y otra que pueda revisar los cambios.
2. **Definiciones comunes:** las actividades, unidades geográficas, indicadores y conceptos de negocio se documentarán una sola vez y se versionarán.
3. **Procedencia y linaje:** cada salida debe poder relacionarse con la fuente, periodo, extracción, versión del código y transformaciones que la produjeron.
4. **Calidad por diseño:** las reglas se definen antes de publicar; los fallos se registran y no se ocultan mediante eliminaciones silenciosas.
5. **Mínimo necesario:** se extraen y propagan únicamente los campos necesarios para los casos de uso aprobados.
6. **Seguridad por defecto:** tokens, credenciales y configuraciones sensibles nunca se versionan; los secretos tampoco deben aparecer en URL registradas ni en logs.
7. **Uso responsable:** presencia comercial, estrato de personal ocupado y otros indicadores de contexto no se describirán como rentabilidad o éxito comprobado.
8. **Reproducibilidad:** una transformación debe poder repetirse desde una entrada preservada, con versiones y parámetros documentados.
9. **Proporcionalidad:** se incorporan controles y herramientas cuando atienden un riesgo real; no se exige burocracia empresarial a cada cambio pequeño.

## 3. Responsabilidades y derechos de decisión

Los roles son responsabilidades, no necesariamente puestos separados. En el equipo actual una persona puede asumir más de un rol, pero cada cambio relevante debe tener revisión cruzada.

| Rol | Responsabilidad | Decisiones / controles |
|---|---|---|
| Data Product Owner | Mantiene las preguntas del producto, definiciones de indicadores y uso previsto. | Aprueba el propósito de un producto Gold y el lenguaje utilizado para comunicar sus resultados. |
| Data Steward | Define significado, categorías, claves geográficas, reglas de calidad y criterios de aceptación. | Revisa diccionario, mapeos SCIAN, definiciones y excepciones de calidad. |
| Data Custodian / Data Engineer | Implementa ingestión, almacenamiento, controles técnicos, seguridad operacional y recuperación. | Propone contratos, linaje, particiones, reintentos y controles técnicos. |
| Analítica / ML | Define variables, población objetivo, etiquetas, evaluación y limitaciones del análisis. | Revisa que los conjuntos Gold/features respondan a una pregunta evaluable y no filtren información de forma indebida. |
| Revisor cruzado | Segundo colaborador que revisa cambios de esquema, semántica o calidad. | Acepta o solicita cambios en PR para los activos críticos. |

En un equipo de dos personas, se recomienda que quien implementa un cambio crítico no sea su único revisor. Para prototipos menores puede bastar una revisión ligera, pero los cambios de definición, acceso, licencia, clave primaria o métrica deben revisarse explícitamente.

## 4. Ciclo de vida y puntos de control

### G0 — Alta de una fuente

Antes de ingerir datos, registrar finalidad, propietario/publicador, URL oficial, método de acceso, licencia/condiciones conocidas, periodicidad, nivel geográfico, campos esperados, restricciones y responsable interno. Si hay cuestiones desconocidas, marcar el estado como pendiente, no como validado.

### G1 — Ingesta Bronze

Guardar la respuesta o archivo recibido sin transformaciones de contenido, más un manifiesto de ejecución. El manifiesto registra fecha de extracción, fuente, método, consulta saneada, estado HTTP, cantidad de registros, versión del extractor y checksum cuando proceda. Nunca guardar el token ni otros secretos en el manifiesto.

### G2 — Promoción a Silver

La transformación debe usar un contrato versionado, tipos documentados, reglas de calidad explícitas y claves territoriales/actividad normalizadas. Los registros no válidos se hacen visibles en cuarentena con el motivo; el original permanece en Bronze. Las excepciones no deben descartarse silenciosamente.

### G3 — Publicación Gold

Cada tabla, indicador o conjunto de features debe documentar propósito, granularidad, unidad de medida, periodo, fórmula, fuentes, filtros, limitaciones, versión y responsable. Las salidas con calidad insuficiente no se publican como resultados confiables.

### G4 — Mantenimiento y retiro

Toda modificación de esquema, mapeo o regla se registra en Git y se evalúa por impacto. Al retirar un dataset, documentar razón, fecha, dependencias y tratamiento de los datos retenidos, respetando las condiciones de la fuente.

## 5. Artefactos de gobierno mínimos

| Artefacto | Ubicación | Uso |
|---|---|---|
| Este marco y responsabilidades | docs/governance/data-governance-charter.md | Principios y decisiones de gobierno. |
| Plan de gestión del ciclo de vida | docs/governance/data-management-plan.md | Cómo se capturan, protegen, transforman, publican y retiran datos. |
| Diccionario de datos | docs/governance/data-dictionary.md | Definiciones de campos, códigos y unidades. |
| Reglas de calidad | docs/governance/data-quality-rules.md | Reglas, severidad, evidencia y aceptación. |
| Catálogo de activos | docs/governance/data-assets-register.md | Inventario de fuentes, capas y productos con propietario y estado. |
| Inventario técnico de fuentes | docs/data-sources.md y docs/denue-api-research.md | Auditoría técnica, métodos, campos y limitaciones de la fuente. |
| Decisiones arquitectónicas | docs/decisions/ | Decisiones relevantes y alternativas consideradas. |

## 6. Correspondencia práctica con disciplinas DAMA-DMBOK

| Disciplina de gestión de datos | Aplicación inicial en Rendify |
|---|---|
| Gobierno de datos | Roles, revisiones, criterios de promoción y decisiones documentadas. |
| Arquitectura de datos | Estructura del pipeline y definición de capas Bronze/Silver/Gold. |
| Modelado y diseño | Diccionario, granularidad de las tablas, claves e identificadores. |
| Almacenamiento y operaciones | Rutas versionadas por ejecución, reejecución y copias reproducibles. |
| Seguridad de datos | Gestión de secretos, permisos mínimos y minimización de contactos. |
| Integración e interoperabilidad | Mapeo SCIAN, claves geográficas y compatibilidad de periodos. |
| Gestión de metadatos | Catálogo de activos, manifiestos, definiciones y linaje. |
| Calidad de datos | Reglas automatizadas, perfilado, cuarentena y reporte de errores. |
| Datos de referencia y maestros | Catálogos de actividad, claves geoestadísticas y reglas de correspondencia. |
| Almacenamiento analítico / BI | Productos Gold con métricas definidas y granularidad explícita. |
| Documentos y contenidos | Preservación de referencias, fichas de fuentes, licencias y evidencia de auditoría. |

La tabla es una adaptación operativa y no sustituye la terminología completa ni el cuerpo de conocimiento de DAMA-DMBOK. Se priorizan las disciplinas que afectan directamente a las primeras entregas.

## 7. Cuándo es obligatorio actualizar la documentación

Abrir un cambio documental cuando se modifique cualquiera de los siguientes elementos: fuente o método de acceso, condiciones de uso, campo publicado en Silver, clave o granularidad, catálogo de actividades, regla de calidad, fórmula de Gold, definición de una etiqueta de ML, permisos, retención o estrategia de almacenamiento.

## 8. Referencias

- [DAMA International — What is Data Management?](https://dama.org/about-dama/what-is-data-management/)
- [DAMA-DMBOK — información oficial](https://dama.org/learning-resources/dama-data-management-body-of-knowledge-dmbok/)
- [Arquitectura medallón y buenas prácticas de fiabilidad — Databricks](https://docs.databricks.com/aws/en/lakehouse-architecture/reliability/best-practices)
