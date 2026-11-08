# Diccionario de datos — Rendify

**Versión:** 0.2  
**Estado:** Bronze implementada; propiedades internas del DENUE aún deben confirmarse con una respuesta real representativa. Silver y Gold son propuestas, no tablas creadas.

## 1. Cómo leerlo

- En Bronze se conserva el JSON original sin renombrar propiedades.
- Las propiedades DENUE listadas en los borradores deben confirmarse en la respuesta del método utilizado.
- Los nombres canónicos son propuestas para una futura capa Silver y no implican que ya existan.
- Códigos e identificadores se tratarán como texto para preservar formato.

## 2. Metadatos técnicos de Bronze (implementados)

El manifiesto `manifest.json` generado por `save_bronze_response()` contiene:

| Campo | Significado |
|---|---|
| source | Fuente; actualmente `DENUE`. |
| method | Método de consulta; actualmente `BuscarAreaAct`. |
| run_id | Identificador de ejecución original. |
| extracted_at | Timestamp UTC de extracción. |
| extraction_date | Fecha UTC de extracción. |
| query_parameters | Parámetros no secretos usados en la consulta. |
| http.status_code | Código HTTP devuelto. |
| http.content_type | Content type de respuesta. |
| record_count | Número de registros parseados. |
| response_size_bytes | Tamaño del cuerpo original en bytes. |
| sha256 | SHA-256 del cuerpo original. |
| files.response | Nombre relativo del archivo con el cuerpo original. |

## 3. Propiedades de origen DENUE por verificar

Entre las propiedades candidatas descritas en los documentos de investigación están `Id`, `CLEE`, códigos y nombres de actividad, estrato de personal ocupado, tipo, nombre, colonia, código postal, claves territoriales, coordenadas y `Fecha_Alta`. No se afirma que todas estén presentes en el método consultado ni que sus significados estén verificados para el esquema real.

Cuando se obtenga una respuesta real, registrar para cada campo nombre exacto, tipo observado, definición de la fuente, nulos, cardinalidad, estabilidad, uso previsto y estado de validación.

## 4. Silver — nombres canónicos propuestos

| Campo propuesto | Significado / regla |
|---|---|
| denue_id | Identificador elegido después de verificar estabilidad de la propiedad fuente. |
| clee | CLEE original, si se confirma su disponibilidad. |
| activity_class_code | Código de actividad normalizado con versión SCIAN. |
| activity_class_name | Descripción de la actividad, preservando texto fuente. |
| staff_size_stratum | Estrato de personal ocupado; no es ingreso ni ventas. |
| establishment_type | Tipo conforme a categorías fuente confirmadas. |
| state_geo_code | Clave oficial de entidad. |
| municipality_geo_code | Clave de municipio/alcaldía, sin convertir tipo de unidad. |
| neighborhood_raw | Valor de colonia tal como lo publica la fuente. |
| neighborhood_normalized | Colonia homologada solo con regla/fuente confiable. |
| postal_code | Código postal como texto. |
| ageb_code / block_code | Claves geográficas verificadas. |
| latitude / longitude | Coordenadas decimales después de validar formato y rango. |
| denue_date_added | Fecha fuente parseada, cuando su semántica sea confirmada. |
| observation_date | Fecha en que Rendify observa el registro. |
| ingestion_run_id | Referencia al run y manifiesto Bronze. |
| quality_status | Resultado de reglas Silver. |

## 5. Gold — dataset candidato

Granularidad propuesta: actividad, unidad geográfica, nivel territorial y periodo. Posibles campos: `period_id`, `geography_level`, `geography_id`, `activity_category_id`, `establishment_count`, distribución por estrato, notas de cobertura, versión de métrica, timestamp de generación y run de linaje.

Ninguna métrica de éxito o rentabilidad está definida. El conteo de establecimientos describe registros observados según una regla, no el éxito de un negocio.

