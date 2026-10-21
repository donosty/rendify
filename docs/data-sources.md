# Inventario y estrategia de fuentes de datos — Rendify

**Versión:** 0.1  
**Estado de auditoría:** inicial; ninguna fuente se considera validada para el MVP hasta completar las verificaciones descritas abajo.  
**Ámbito inicial propuesto:** Ciudad de México, alcaldías y actividades comerciales candidatas.

## 1. Propósito

Este documento registra las fuentes candidatas de Rendify, qué papel podrían desempeñar, qué compatibilidades deben comprobarse y qué metadatos conservaremos. Su finalidad es evitar que el diseño de la canalización asuma cobertura, campos o granularidad que todavía no se han confirmado.

Una fuente citada aquí es una **candidata de investigación**, no una afirmación de que la consulta funciona, de que existe cobertura completa para todas las alcaldías o actividades, ni de que los datos puedan redistribuirse sin condiciones.

## 2. Fuentes candidatas

| Fuente | Uso previsto | Estado inicial | Documentación |
|---|---|---|---|
| DENUE / API de INEGI | Establecimientos, actividad económica y atributos publicados para explorar distribución comercial | Primera fuente a auditar; campos, método, límites y cobertura por comprobar | [API del DENUE](https://www.inegi.org.mx/servicios/api_denue.html) |
| Censo de Población y Vivienda 2020 | Población, viviendas y variables sociodemográficas al nivel de desagregación disponible | Candidata para contexto; validar variables y nivel territorial | [Programa del Censo 2020](https://www.inegi.org.mx/programas/ccpv/2020/) |
| Censos Económicos 2024 | Indicadores económicos y establecimientos por actividad y geografía publicados | Candidata para benchmarks; revisar tablas, agregación y confidencialidad | [Censos Económicos 2024](https://www.inegi.org.mx/programas/ce/2024/default.html) |
| Catálogo de claves geoestadísticas y cartografía de INEGI | Normalizar claves, identificar unidades geográficas y apoyar mapas y vinculaciones | Candidata para integración espacial; versión y campos por identificar | [INEGI](https://www.inegi.org.mx/) |
| ENIGH 2024 | Contexto de ingresos y gastos de los hogares | Etapa posterior; revisar diseño muestral y alcance antes de valorar su uso | [ENIGH 2024](https://www.inegi.org.mx/programas/enigh/nc/2024/default.html) |

Las referencias y los usos propuestos proceden del plan maestro del proyecto. La disponibilidad, estructura actual, condiciones de acceso y compatibilidad de cada fuente deben comprobarse durante la auditoría.

## 3. Prioridad 1: auditar el DENUE

El DENUE es la primera fuente candidata porque el producto necesita observar establecimientos y su actividad económica. Antes de construir filtros o contratos de datos, debemos revisar la documentación oficial y realizar una consulta de prueba con parámetros válidos.

### Preguntas que debe resolver la auditoría

1. **Acceso:** ¿qué método o endpoint corresponde a la consulta requerida? ¿Necesita token o credenciales? ¿Cuáles son sus condiciones?
2. **Filtros:** ¿cómo consulta por ubicación y actividad? ¿Qué códigos, textos o parámetros acepta?
3. **Campos:** ¿qué nombres, tipos y significados devuelven realmente las respuestas?
4. **Ubicación:** ¿qué coordenadas, claves territoriales y nombres geográficos existen en la respuesta?
5. **Actividad económica:** ¿qué código y descripción de actividad proporciona? ¿Qué versión o nivel SCIAN corresponde?
6. **Volumen:** ¿hay límites, paginación, cuotas, restricciones o estrategias recomendadas para extraer resultados?
7. **Cobertura:** ¿qué periodo o edición representan los datos? ¿Cómo comprobamos la presencia de registros para las actividades y alcaldías de interés?
8. **Reutilización:** ¿qué atribución, condiciones de acceso y restricciones deben respetarse?
9. **Repetibilidad:** ¿cómo identificaremos una ejecución, su consulta y el archivo original?

### Campos candidatos para inspeccionar

No se considera que todos estos campos estén confirmados en el endpoint o en la respuesta que utilizaremos. Son campos que el equipo debe buscar, verificar y documentar:

- Identificador del establecimiento (por ejemplo, ID o CLEE si corresponde a los datos devueltos).
- Código y descripción de actividad económica.
- Nombre del establecimiento, si está disponible y es necesario para el caso de uso.
- Coordenadas geográficas.
- Claves y nombres territoriales.
- Estrato de personal ocupado, cuando exista en la fuente y sea pertinente.
- Atributos adicionales, únicamente después de comprobar su significado y necesidad.

No trataremos un estrato de personal ocupado como ventas, ingresos o rentabilidad. No almacenaremos teléfonos o correos si no aportan al análisis previsto.

### Categorías comerciales iniciales

| Categoría de producto | Trabajo pendiente |
|---|---|
| Cafeterías | Identificar códigos/descripciones SCIAN aplicables y decidir si se necesita un criterio de inclusión específico. |
| Restaurantes | Definir el alcance de restaurantes y cómo tratar subcategorías relacionadas con alimentos. |
| Tiendas de artículos | Precisar el tipo de artículos o familias comerciales; la etiqueta actual es demasiado amplia para un filtro estable. |
| Gimnasios | Confirmar códigos/descripciones que representan gimnasios y actividades relacionadas que deban incluirse o excluirse. |

La lista final debe conservar código, descripción, versión de clasificación y regla de inclusión/exclusión. No se fijarán códigos por intuición.

### Alcance geográfico

La unidad inicial preferida es la alcaldía de Ciudad de México. La auditoría debe establecer cómo se identifica una alcaldía en los datos obtenidos y cómo se relaciona con el catálogo geográfico oficial. Si el método de consulta trabaja con otra unidad, registraremos el procedimiento de vinculación y su precisión.

No asumiremos que es posible filtrar directamente por todas las alcaldías usando la API hasta confirmar los parámetros disponibles. Si se requiere descargar resultados más amplios y filtrar localmente, se documentarán implicaciones de volumen, límites, permisos y coste de operación.

## 4. Fuentes de contexto: requisitos para integrar

### Censo de Población y Vivienda 2020

Se investigará qué variables de población, viviendas y características demográficas pueden usarse al nivel de alcaldía y, si resultara apropiado, en geografías más detalladas. Se registrará el año de referencia y la unidad territorial publicada.

### Censos Económicos 2024

Se revisarán las tablas y los indicadores publicados por actividad y geografía. Antes de integrar, hay que comprobar el nivel de agregación disponible y respetar las notas de confidencialidad. No se distribuirán cifras publicadas a escala municipal o de alcaldía hacia unidades menores sin metodología válida.

### Catálogo geográfico y cartografía

Se identificará el catálogo de claves, la versión de límites y los atributos necesarios para unir fuentes y representar mapas. Las claves oficiales se almacenarán como cadenas para no perder formato. También se conservarán el tipo de unidad y la versión cartográfica cuando corresponda.

### ENIGH 2024

No forma parte de la primera ingesta. Si se considera más adelante, el equipo debe revisar su diseño muestral, variables, periodicidad y alcance territorial. No se atribuirán estimaciones de una encuesta a cada colonia como si fueran observaciones directas.

## 5. Compatibilidad y granularidad

Antes de unir dos fuentes se debe documentar, para cada una:

- Nivel territorial de publicación (por ejemplo, alcaldía, municipio o AGEB, si realmente está disponible).
- Clave geográfica oficial y versión del catálogo.
- Periodo estadístico o fecha de referencia.
- Fecha de publicación y fecha de extracción, registradas por separado cuando existan.
- Unidad de medida, definición y metodología.
- Cobertura y valores faltantes conocidos.

Una unión técnicamente posible no garantiza una comparación estadísticamente válida. Si una variable solo está disponible a nivel de alcaldía, el resultado debe mantenerse en ese nivel. No se debe presentar más precisión geográfica de la que ofrece la fuente.

## 6. Contrato de ingesta y metadatos

Cada ejecución de extracción deberá registrar, como mínimo:

- Nombre e identificador de la fuente.
- URL o método usado y versión/documentación consultada.
- Fecha/hora de extracción en UTC.
- Parámetros no secretos utilizados, o una representación segura de ellos.
- Periodo de referencia de los datos, si lo publica la fuente.
- Ruta del archivo original.
- Hash o checksum del archivo.
- Número de registros y tamaño del archivo cuando pueda calcularse.
- Resultado de validación y errores de extracción.
- Versión del código que produjo el resultado, cuando el mecanismo esté disponible.

Los originales se preservarán sin transformaciones silenciosas, siguiendo el principio Bronze. Las transformaciones y normalizaciones vivirán en pasos posteriores y serán reproducibles.

Los tokens y credenciales no deben quedar en Git, archivos de datos publicados, logs ni imágenes. La configuración sensible se manejará mediante variables de entorno locales o mecanismos adecuados al entorno de ejecución.

## 6.1 Gobierno, catálogo y control de cambios

Este inventario técnico se complementa con los artefactos de gobierno en docs/governance/:

- data-assets-register.md: ID del activo, uso, responsable interno, estado y evidencia pendiente.
- data-dictionary.md: propiedades de origen candidatas y nombres canónicos propuestos.
- data-quality-rules.md: controles por capa y evidencia para promover datos.
- data-management-plan.md: metadatos, seguridad, ciclo de vida e integración.
- data-governance-charter.md: responsabilidades, decisiones y principios.

La fuente se mantendrá como Candidata o En auditoría hasta contar con evidencia reproducible. La revisión de documentación no equivale a validación técnica de endpoint, campos, cobertura ni condiciones de reutilización. Para DENUE, la primera prueba deberá aportar la URL y parámetros sin secretos, fecha de ejecución, respuesta original segura, lista real de propiedades, recuento, informe de calidad y resultados de contraste cuando sea posible.

Todo cambio de método, campo de origen, clave geográfica, mapeo SCIAN, licencia/condición de uso o interpretación de una métrica se registrará mediante una pull request que actualice los documentos y pruebas afectados. No se considerará validado un elemento solo por haberse documentado.

## 7. Reporte de perfilado y calidad

La primera muestra del DENUE deberá producir un informe que responda:

- Número de registros y columnas observados.
- Estructura de los registros y tipos inferidos.
- Campos ausentes y nulos críticos.
- Identificadores duplicados, si hay un identificador adecuado.
- Coordenadas ausentes y coordenadas fuera de rangos válidos.
- Categorías y códigos de actividad realmente observados.
- Claves geográficas disponibles y valores no reconocidos.
- Registros que no puedan asignarse de manera fiable a una alcaldía.
- Fecha o periodo de referencia disponible.
- Limitaciones conocidas y preguntas sin resolver.

Los resultados del reporte deben reflejar la muestra extraída, no generalizarse a toda la ciudad o a todas las ediciones de la fuente sin evidencia.

## 8. Registro de verificación

Actualizar esta tabla conforme avance la auditoría. No cambiar un estado a «Validado» sin evidencia reproducible.

| Elemento | Estado inicial | Evidencia requerida |
|---|---|---|
| Documentación del acceso a DENUE revisada | Pendiente de registrar | URL y notas sobre método, parámetros y requisitos |
| Consulta de prueba ejecutada | No verificada | Parámetros no secretos, fecha y resultado reproducible |
| Estructura de respuesta inspeccionada | No verificada | Muestra segura y listado de campos observados |
| Códigos de actividades confirmados | No verificados | Mapeo documentado a códigos/descripciones SCIAN |
| Cobertura para las alcaldías objetivo | No verificada | Perfilado de datos y comprobaciones de claves/ubicaciones |
| Límites de consulta y volumen entendidos | No verificados | Documentación y pruebas controladas |
| Condiciones de uso/reutilización revisadas | No verificadas | Referencia a términos y decisión documentada |
| Censo y Censos Económicos compatibles | No verificado | Variables, periodos, niveles geográficos y claves comparados |
| Cartografía y catálogo adecuados | No verificados | Catálogo/versionado y prueba de vinculación |
| ENIGH apta para un uso específico | Fuera de la primera fase | Evaluación metodológica antes de incorporarla |

## 9. Referencias oficiales

- [API del DENUE — INEGI](https://www.inegi.org.mx/servicios/api_denue.html)
- [Censo de Población y Vivienda 2020 — INEGI](https://www.inegi.org.mx/programas/ccpv/2020/)
- [Censos Económicos 2024 — INEGI](https://www.inegi.org.mx/programas/ce/2024/default.html)
- [ENIGH 2024 — INEGI](https://www.inegi.org.mx/programas/enigh/nc/2024/default.html)
- [Portal de INEGI y recursos geográficos](https://www.inegi.org.mx/)

Esta documentación es un plan de auditoría. No debe interpretarse como confirmación de cobertura, de nombres de campos de una respuesta real, de compatibilidad geográfica ni de permisos para redistribuir datos. Esas conclusiones solo se incorporarán después de verificarlas.
