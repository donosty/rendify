# Investigación de la API del DENUE para Rendify

- **Fecha de revisión:** 2026-10-21
- **Fuente principal:** [API del DENUE — documentación oficial del INEGI](https://www.inegi.org.mx/servicios/api_denue.html)
- **Información general:** [API del DENUE](https://www.inegi.org.mx/servicios/api-denue/)
- **Estado:** diseño inicial basado en documentación pública. Falta probar con un token válido y guardar una respuesta real de control.

## 1. Objetivo y conclusión

Este documento define métodos, parámetros y propiedades relevantes para una extracción reproducible que permita a Rendify analizar tipos de negocio por colonia, alcaldía/municipio, localidad y entidad; comparar composición de actividades y tamaño aproximado; y preparar cruces con fuentes demográficas y económicas.

**Método principal recomendado: BuscarAreaAct.** Permite filtrar por claves geográficas y códigos de actividad económica. El ejemplo ampliado de salida incluye propiedades geográficas y códigos de actividad que no aparecen en todos los métodos.

Métodos auxiliares:
- **Cuantificar:** contraste de conteos por actividad, área geográfica y estrato.
- **BuscarAreaActEstr:** variante con filtro de estrato de personal ocupado.
- **Ficha:** consulta puntual de un establecimiento mediante su Id.
- **BuscarEntidad:** búsqueda textual acotada a una entidad; no es el extractor principal por actividad.
- **Nombre:** búsqueda puntual por nombre o razón social.
- **Buscar:** consulta alrededor de coordenadas, con radio máximo documentado de 5,000 metros; no es necesario para la primera extracción administrativa.

DENUE proporciona identificación, actividad, ubicación y estrato de personal ocupado. No entrega en esta API ingresos, costos, utilidades ni una etiqueta directa de “éxito”.

## 2. URL y autenticación

La documentación muestra rutas REST con los parámetros en la URL:

~~~text
https://www.inegi.org.mx/app/api/denue/v1/consulta/{METODO}/{PARAMETROS}/{TOKEN}
~~~

El token se obtiene mediante el registro enlazado desde el [portal oficial de la API](https://www.inegi.org.mx/servicios/api_denue.html). En Rendify deberá guardarse en una variable de entorno, por ejemplo DENUE_API_TOKEN, nunca en el código, commits ni logs.

Las respuestas de ejemplo son arreglos JSON de objetos. Códigos y valores numéricos llegan en muchos casos como cadenas: preservar los códigos como texto para no perder ceros iniciales y convertir solo medidas que requieran operaciones matemáticas.

## 3. Métodos y ejemplos

Los ejemplos usan TOKEN como marcador; hay que sustituirlo por un token válido. No se realizó una petición autenticada en esta revisión.

### 3.1 BuscarAreaAct — extracción principal

**Ejemplo oficial documentado:**

~~~text
https://www.inegi.org.mx/app/api/denue/v1/consulta/BuscarAreaAct/01/0/0/0/0/0/0/0/0/oxxo/1/15/0/TOKEN
~~~

Orden de parámetros en la guía:

1. Entidad federativa: clave de dos dígitos; 00 para todas.
2. Municipio: clave de tres dígitos; 0 para todos.
3. Localidad: clave de cuatro dígitos; 0 para todas.
4. AGEB: clave de cuatro dígitos; 0 para todas.
5. Manzana: clave de tres dígitos; 0 para todas.
6. Sector de actividad: dos dígitos; 0 para todos.
7. Subsector: tres dígitos; 0 para todos.
8. Rama: cuatro dígitos; 0 para todas.
9. Clase: seis dígitos; 0 para todas.
10. Nombre del establecimiento: texto; 0 para todos.
11. Registro inicial.
12. Registro final.
13. Id de establecimiento; 0 para todos.
14. Token.

**Muestra para las primeras 15 posiciones de CDMX (entidad 09), sin filtrar actividad:**

~~~text
https://www.inegi.org.mx/app/api/denue/v1/consulta/BuscarAreaAct/09/0/0/0/0/0/0/0/0/0/1/15/0/TOKEN
~~~

Es una muestra de parámetros, no una recomendación definitiva de tamaño de página. La documentación consultada no confirma claramente un máximo de registros por petición ni una tasa de llamadas, así que hay que medirlo en pruebas.

**Muestra para filtrar por una clase SCIAN específica dentro de CDMX:**

~~~text
https://www.inegi.org.mx/app/api/denue/v1/consulta/BuscarAreaAct/09/0/0/0/0/0/0/0/CODIGO_CLASE/0/1/15/0/TOKEN
~~~

Sustituir CODIGO_CLASE por una clave de seis dígitos validada contra el catálogo SCIAN correspondiente. No usar “café” o “restaurante” como sustituto del código si se busca cobertura sistemática: la búsqueda textual puede omitir establecimientos clasificados con otra denominación.

**Por qué se recomienda:** el método permite filtros por entidad, municipio, localidad, AGEB, manzana y niveles SCIAN. El ejemplo ampliado incluye códigos de actividad, AGEB, Manzana, Tipo_Asentamiento, Fecha_Alta y AreaGeo.

### 3.2 BuscarAreaActEstr — filtrar por tamaño

**Ejemplo oficial:**

~~~text
https://www.inegi.org.mx/app/api/denue/v1/consulta/BuscarAreaActEstr/01/0/0/0/0/0/0/0/0/oxxo/1/15/0/1/TOKEN
~~~

Añade Estrato antes del token:
- 0: todos los tamaños.
- 1: de 0 a 5 personas.
- 2: de 6 a 10 personas.
- 3: de 11 a 30 personas.
- 4: de 31 a 50 personas.
- 5: de 51 a 100 personas.
- 6: de 101 a 250 personas.
- 7: 251 personas o más.

No hace falta extraer siete variantes solo para obtener tamaño si Estrato ya viene en la respuesta de BuscarAreaAct. Mantenerlo como herramienta para consultas puntuales por estrato o comprobaciones.

### 3.3 Cuantificar — validar conteos

**Ejemplo oficial:**

~~~text
https://www.inegi.org.mx/app/api/denue/v1/consulta/Cuantificar/111,112/01001,01005/0/TOKEN
~~~

Parámetros:
1. Actividad económica: códigos de sector, subsector, rama, subrama o clase; varias claves separadas por coma; 0 para todas.
2. Área geográfica: clave de dos dígitos para entidad, cinco para municipio y nueve para localidad; varias claves por coma; 0 para todo el país.
3. Estrato de personal ocupado; 0 para todos.
4. Token.

Propiedades de salida del ejemplo:
- AE: código de actividad económica.
- AG: clave de área geográfica.
- Total: conteo de establecimientos para la combinación consultada.

Usar para contrastar conteos en niveles compatibles. La guía documenta claves de entidad, municipio y localidad para Cuantificar; no asumir conteos por colonia, AGEB o manzana.

### 3.4 BuscarEntidad — búsqueda textual

**Ejemplo oficial:**

~~~text
https://www.inegi.org.mx/app/api/denue/v1/consulta/BuscarEntidad/restaurantes/14/1/10/TOKEN
~~~

Parámetros: condición textual, clave de entidad de dos dígitos (00 para todas), posición inicial, posición final y token. La condición busca palabras dentro del nombre, razón social, calle, colonia, clase de actividad, entidad, municipio y localidad. La guía indica usar la palabra todos para solicitar todos los establecimientos.

Es útil para exploración, pero no debe ser el extractor principal de Rendify: el término “restaurantes” no garantiza recuperar toda la actividad clasificada en las categorías objetivo.

### 3.5 Ficha — consulta puntual

**Ejemplo oficial:**

~~~text
https://www.inegi.org.mx/app/api/denue/v1/consulta/Ficha/34185/TOKEN
~~~

Recibe el Id del establecimiento. Usar para inspección o depuración de casos, no para recorrer toda la entidad.

### 3.6 Otros métodos

- **Nombre:** búsqueda por nombre o razón social, acotable por entidad y posiciones de registro.
- **Buscar:** búsqueda por condición alrededor de coordenadas (latitud,longitud), con radio en metros; máximo documentado de 5,000 m. Reservado para validaciones espaciales específicas.

## 4. Campos de salida útiles para Rendify

La documentación general enumera campos básicos; el ejemplo JSON ampliado de BuscarAreaAct incluye propiedades adicionales. Los nombres siguientes son los nombres exactos que aparecen en los ejemplos oficiales.

| Propiedad JSON | Prioridad | Utilidad | Tratamiento |
|---|---|---|---|
| CLEE | Esencial | Identificación y comparación entre extracciones. | Texto; validar unicidad y estabilidad. |
| Id | Esencial | Identificador aceptado por Ficha; deduplicación y consultas puntuales. | Texto; comprobar estabilidad. |
| CLASE_ACTIVIDAD_ID | Esencial si aparece | Código SCIAN de clase para segmentación precisa. | Texto de seis dígitos; verificar en muestra real. |
| Clase_actividad | Esencial | Nombre legible de la actividad. | Conservar. |
| SECTOR_ACTIVIDAD_ID | Útil | Agregación amplia por sector. | Texto si aparece. |
| SUBSECTOR_ACTIVIDAD_ID | Útil | Agregación por subsector. | Texto si aparece. |
| RAMA_ACTIVIDAD_ID | Útil | Agregación por rama. | Texto si aparece. |
| SUBRAMA_ACTIVIDAD_ID | Útil | Agregación intermedia. | Texto; confirmar formato. |
| Estrato | Esencial | Tamaño aproximado por rango de personal ocupado. | Conservar etiqueta y crear categoría normalizada; no equivale a ventas ni rentabilidad. |
| Tipo | Útil | Tipo del establecimiento, como Fijo en el ejemplo. | Conservar y perfilar valores. |
| Ubicacion | Esencial | Cadena descrita como localidad, municipio y entidad federativa. | Conservar original; no dividir con reglas frágiles. |
| Colonia | Esencial para análisis por colonia, si es utilizable | Agrupación nominal por colonia. | Valor original más versión normalizada; no es clave única. |
| Tipo_Asentamiento | Útil | Tipo de asentamiento, por ejemplo COLONIA. | Conservar si aparece. |
| CP | Útil | Validación y agrupación auxiliar. | Texto; no reemplaza colonia o municipio. |
| AreaGeo | Esencial para cruces si se valida | Clave de área geográfica; el ejemplo tiene nueve dígitos (010010001). | Texto con ceros iniciales; contrastar con catálogo geoestadístico. |
| AGEB | Útil | Agregación espacial detallada. | Texto; interpretar con claves superiores y cartografía. |
| Manzana | Útil | Unidad espacial detallada. | Texto y conservar ceros iniciales. |
| Longitud | Útil | Validación de ubicación y métricas espaciales. | Decimal tras validar rango. |
| Latitud | Útil | Validación de ubicación y métricas espaciales. | Decimal tras validar rango. |
| Fecha_Alta | Útil, condicionada | Antigüedad en el directorio y análisis de cambios entre snapshots. | El ejemplo usa AAAA-MM. No asumir fecha real de apertura. |
| Nombre | Auxiliar | Revisión manual, duplicados y calidad. | No usar como predictor inicial. |

### Campos que no pasan a la tabla analítica inicial

Según el método, las respuestas también pueden incluir Razon_social, Tipo_vialidad, Calle, Num_Exterior, Num_Interior, Telefono, Correo_e, Sitio_internet, tipo_corredor_industrial, nom_corredor_industrial, numero_local, CentroComercial, TipoCentroComercial, NumLocal, EDIFICIO_PISO y EDIFICACION. No son necesarios para el primer conjunto de indicadores.

La capa raw puede conservar el JSON original para trazabilidad; la capa curada seleccionará los campos requeridos. Evitar propagar teléfonos, correos y contactos a tablas analíticas, ML o reportes sin necesidad concreta.

## 5. Niveles geográficos que soporta la API

| Nivel | Evidencia documentada | Decisión para Rendify |
|---|---|---|
| Entidad | Filtro de BuscarAreaAct; Cuantificar acepta clave de dos dígitos. | Sí; probar CDMX con clave 09. |
| Municipio/alcaldía | Filtro de tres dígitos en BuscarAreaAct; Cuantificar usa clave geográfica de cinco dígitos. | Sí, validando claves y nombres de alcaldías. |
| Localidad | Filtro de cuatro dígitos en BuscarAreaAct; Cuantificar usa clave de área de nueve dígitos. | Sí con catálogo compatible. |
| Colonia/asentamiento | Colonia y Tipo_Asentamiento aparecen como propiedades; no se documenta una clave única de colonia en el ejemplo. | Sí como dimensión nominal provisional; homologar homónimos y variantes. |
| AGEB/manzana | Filtros y propiedades AGEB y Manzana en el ejemplo ampliado. | Posible; validar cobertura, formatos y unión con cartografía. |
| Entidad/municipio como claves separadas en la salida | Ubicacion reúne localidad, municipio y entidad en una cadena en los ejemplos básicos. | Enriquecer desde claves/catálogos; no depender de partir texto. |

Cuantificar y BuscarAreaAct usan formatos geográficos diferentes. En Cuantificar, la clave de área tiene 2 dígitos para entidad, 5 para municipio y 9 para localidad; en BuscarAreaAct se proporcionan entidad, municipio y localidad en parámetros separados. No intercambiar formatos sin transformación.

## 6. Esquema procesado inicial sugerido

Nombres internos propuestos para Rendify (no son nombres de propiedades que devuelva la API):

~~~text
establishments
- denue_id                 # Id
- clee
- activity_class_id        # CLASE_ACTIVIDAD_ID; nullable hasta confirmar
- activity_class_name      # Clase_actividad
- sector_id                # SECTOR_ACTIVIDAD_ID; nullable
- subsector_id             # SUBSECTOR_ACTIVIDAD_ID; nullable
- branch_id                # RAMA_ACTIVIDAD_ID; nullable
- subbranch_id             # SUBRAMA_ACTIVIDAD_ID; nullable
- staff_size_label         # Estrato
- establishment_type       # Tipo
- state_code               # normalizado con clave geográfica validada
- municipality_code        # normalizado
- locality_code            # AreaGeo u otra clave validada
- neighborhood_raw        # Colonia
- settlement_type          # Tipo_Asentamiento
- postal_code              # CP
- ageb_code                # AGEB; nullable
- block_code               # Manzana; nullable
- longitude
- latitude
- denue_date_added         # Fecha_Alta; no equivale a apertura confirmada
- extracted_at             # generado por Rendify
- source_method            # generado por Rendify
- source_query             # generado por Rendify, sin token
~~~

Para evolución temporal, guardar snapshots o una tabla de observaciones por fecha de extracción en lugar de sobrescribir todo. La ausencia posterior de un Id no demuestra por sí sola que el negocio cerró.

## 7. Prueba de concepto previa a la extracción amplia

1. Guardar el token localmente en DENUE_API_TOKEN, sin versionarlo.
2. Consultar una muestra pequeña con BuscarAreaAct para CDMX y guardar el JSON original.
3. Confirmar qué propiedades aparecen de verdad: CLASE_ACTIVIDAD_ID, SECTOR_ACTIVIDAD_ID, SUBSECTOR_ACTIVIDAD_ID, RAMA_ACTIVIDAD_ID, SUBRAMA_ACTIVIDAD_ID, AreaGeo, AGEB, Manzana, Tipo_Asentamiento y Fecha_Alta.
4. Perfilar vacíos, tipos, duplicados, rangos válidos de coordenadas y etiquetas de Estrato.
5. Confirmar códigos SCIAN exactos para cafeterías y las clases de restaurantes incluidas. Configurar categorías por código y no por coincidencia textual.
6. Probar rangos sucesivos para determinar tamaño práctico de página y manejar respuestas vacías, errores HTTP y contenido no JSON.
7. Contrastar conteos con Cuantificar en el nivel compatible; documentar diferencias.
8. Validar claves y colonias contra catálogos oficiales antes de publicar comparaciones por colonia, alcaldía o AGEB.
9. Fijar un esquema y pruebas de calidad antes de lanzar la extracción completa.

## 8. Discrepancias y cuestiones pendientes

La documentación no es totalmente uniforme entre el listado general, las descripciones de método y algunos ejemplos:

- El listado general contiene campos básicos; el JSON ampliado de BuscarAreaAct añade códigos SCIAN, AGEB, Manzana, Tipo_Asentamiento, Fecha_Alta y AreaGeo.
- Las listas tras algunos ejemplos antiguos no enumeran todas las propiedades visibles en el JSON, incluidas SUBRAMA_ACTIVIDAD_ID y Fecha_Alta.
- BuscarAreaActEstr añade Estrato como filtro, aunque Estrato también aparece en la salida de BuscarAreaAct.
- La guía de Cuantificar menciona inicialmente códigos de actividad de dos a cinco dígitos y después incluye la clase de seis dígitos. Verificar en prueba los códigos admitidos para cada nivel.
- La guía consultada no confirma claramente el máximo de registros por petición ni la tasa de llamadas.
- Fecha_Alta no debe convertirse automáticamente en fecha real de apertura ni etiqueta de supervivencia sin validar su semántica.
- Colonia es un nombre, no una clave única documentada en el ejemplo; la homologación requiere reglas explícitas y una fuente geográfica de referencia.

Estas cuestiones no impiden avanzar; indican que el primer entregable debe ser un extractor pequeño con controles de calidad, no una descarga masiva asumida como completa.

## 9. Referencias oficiales

1. INEGI, API del DENUE — guía para desarrolladores: https://www.inegi.org.mx/servicios/api_denue.html
2. INEGI, API del DENUE — información disponible: https://www.inegi.org.mx/servicios/api-denue/
3. Catálogo Único de Claves Geoestadísticas del INEGI, para validar las claves y unidades geográficas; seleccionar la versión vigente desde el portal oficial de desarrolladores del INEGI.

Consulta registrada el 2026-10-21. Los parámetros y respuestas mostrados proceden de ejemplos publicados por INEGI; verificar todas las propiedades con un token real queda como siguiente tarea.
