# Inventario y estrategia de fuentes de datos — Rendify

**Versión:** 0.2  
**Actualización:** 2026-11-07  
**Ámbito inicial:** Ciudad de México; alcaldías como unidad de comparación preferida.

## 1. Estado de fuentes

| Fuente | Uso previsto | Estado actual |
|---|---|---|
| DENUE / API INEGI | Establecimientos y actividad económica | **Integración técnica inicial implementada.** Cliente y pipeline de muestra Bronze/validación existen. La cobertura, campos reales, límites y uso de filtros deben seguir auditándose. |
| Censo de Población y Vivienda 2020 | Contexto de población y vivienda | Candidata; integración no iniciada. |
| Censos Económicos 2024 | Contexto económico agregado | Candidata; integración no iniciada. |
| Catálogo geoestadístico/cartografía INEGI | Claves y geometrías para cruces geográficos | Candidata; versión y compatibilidad por determinar. |
| ENIGH 2024 | Contexto de ingreso/gasto de hogares | Posible fase posterior; no forma parte de la extracción inicial. |

Una integración técnica del endpoint no implica que una fuente esté validada para el producto, que su cobertura sea completa o que se pueda redistribuir libremente.

## 2. DENUE: qué existe en el repositorio

El módulo `src/rendify/denue/client.py` consulta `BuscarAreaAct` y preserva el cuerpo de respuesta en bytes junto con los metadatos HTTP y los registros parseados. `extract.py` genera el payload Bronze y un manifiesto con parámetros no secretos, run ID, timestamp, conteo, tamaño y SHA-256. `validate.py` verifica manifiesto, status, ruta, tamaño, hash, JSON y conteo.

El DAG actual `denue_initial_extraction` prueba entidad `09` (CDMX), sin filtros por alcaldía o actividad y con rango de 1 a 15 registros. Es una muestra de conectividad y persistencia, no un censo de establecimientos ni una auditoría representativa de todas las alcaldías.

## 3. Preguntas pendientes de auditoría DENUE

1. Confirmar con una respuesta real qué campos y tipos devuelve el método utilizado.
2. Identificar semántica y estabilidad de identificadores (por ejemplo, Id/CLEE) antes de definir claves Silver.
3. Confirmar códigos y descripciones SCIAN, versión de clasificación y actividades aplicables.
4. Probar los parámetros necesarios para filtrar por alcaldía/municipio y actividad.
5. Documentar cuotas, límites, paginación, tamaño máximo y comportamiento para resultados vacíos.
6. Identificar periodo de referencia y política de actualización del directorio.
7. Revisar atribución, condiciones de acceso y reutilización de datos.
8. Comprobar cobertura territorial y campos geográficos para las preguntas del MVP.

## 4. Categorías iniciales de producto

| Categoría | Decisión pendiente |
|---|---|
| Cafeterías | Identificar códigos y criterios de inclusión/exclusión. |
| Restaurantes | Determinar subcategorías y alcance. |
| Tiendas de artículos | Precisar qué familias de artículos o comercios comprende. |
| Gimnasios | Confirmar códigos y actividades relacionadas que se incluirán. |

No usar etiquetas de producto como filtros definitivos sin un mapeo SCIAN versionado.

## 5. Criterios de integración geográfica y temporal

Para cada fuente, registrar nivel territorial, clave oficial, versión cartográfica, periodo de referencia, fecha de publicación, fecha de extracción, unidad de medida y cobertura. Una unión técnicamente posible no garantiza una comparación válida. No se debe atribuir precisión subterritorial a datos publicados solo a nivel de alcaldía.

## 6. Metadatos y seguridad

Cada ingesta debe guardar fuente, método, timestamp UTC, parámetros no secretos, run ID, ruta al original, tamaño, checksum, conteo y resultado de validación. Los tokens, cabeceras y URL con secretos no se guardan en Git, manifiestos ni logs.

