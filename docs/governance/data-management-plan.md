# Plan de gestión de datos — Rendify

**Versión:** 0.1  
**Estado:** inicial; revisar en cada sprint y al incorporar una fuente.

## 1. Alcance

Este plan describe cómo gestionar los datos de Rendify durante su ciclo de vida. Es una implementación pragmática de disciplinas de gobierno, arquitectura, metadatos, calidad, integración, almacenamiento y seguridad inspiradas en DAMA-DMBOK. No implica conformidad completa con DAMA.

## 2. Activos y fuentes

La primera fuente candidata es la API del DENUE del INEGI. Censos, estadísticas económicas y catálogo/cartografía geográfica son fuentes candidatas posteriores. El inventario está en docs/governance/data-assets-register.md; la auditoría técnica y preguntas pendientes de DENUE, en docs/denue-api-research.md.

Antes de usar una fuente para resultados publicados, registrar:
- nombre oficial, proveedor, URL y método/endpoint;
- propósito de uso y pregunta que apoya;
- condiciones de acceso, licencia, atribución y restricciones conocidas;
- periodo de referencia, fecha de publicación y frecuencia de actualización, si existen;
- campos, tipos, códigos y unidad geográfica;
- claves para relacionar con otros datasets;
- responsable interno, estado de validación y evidencia;
- riesgos conocidos y decisión sobre reutilización.

## 3. Capas y ciclo de vida medallón

La arquitectura lógica se documenta en docs/architecture/medallion-architecture.md.

- **Bronze:** copia de la respuesta original, sin cambios semánticos; guardar manifiesto de extracción. Reprocesable.
- **Silver:** representación normalizada y validada, con esquema versionado, claves conformed, deduplicación justificada y excepciones trazables.
- **Gold:** agregados de negocio por actividad, unidad geográfica y periodo; más adelante, features de ML con definición y objetivo explícitos.
- **Quarantine:** ruta operacional para registros o lotes que no superan validaciones; conservar referencia al original y motivo de rechazo. No es una capa medallón adicional.

Las salidas se identifican por fuente, dataset, fecha o periodo, ID de ejecución y versión del contrato. El almacenamiento actual será local; si se mueve a GCS/BigQuery u otra plataforma, debe preservarse el significado de cada capa y actualizar el inventario.

## 4. Metadatos obligatorios

Cada ejecución de ingesta debe producir un manifiesto saneado que contenga, cuando proceda:
- source_id y dataset_id;
- método o endpoint de consulta;
- parámetros no secretos o una versión redactada;
- fecha/hora de inicio y fin en UTC;
- ID de ejecución y versión del código;
- versión del esquema/contrato;
- estado final, código HTTP y tipo de contenido;
- cantidad de registros/archivos y checksum;
- fecha de referencia del dato publicada por la fuente, si está disponible;
- incidencias y versión de reglas de calidad.

No registrar tokens, cabeceras de autenticación, URLs con secretos ni valores sensibles. Un manifiesto técnico de ejecución no reemplaza el catálogo de activos ni el diccionario semántico.

## 5. Calidad, errores y promoción

Las reglas iniciales están en docs/governance/data-quality-rules.md. El perfilado de muestra debe registrar campos observados, ausentes, nulos, duplicados, cobertura geográfica, códigos SCIAN y rangos de coordenadas.

- Errores de transporte o respuesta inválida: falla de la ingesta; no promover.
- Esquema inesperado: preservar la respuesta Bronze, registrar la incidencia y detener promoción hasta evaluar el cambio.
- Registro malformado o valores inválidos: enviar a cuarentena con código de motivo; no borrar silenciosamente.
- Problemas no bloqueantes: registrar advertencia y cuantificar impacto.
- Publicación Gold: requiere definiciones, linaje, regla de calidad, periodo, granularidad y revisión.

Los umbrales numéricos de completitud/cobertura no se inventarán: se fijarán después de inspeccionar muestras y entender las reglas de la fuente.

## 6. Identidad, integración geográfica y referencia

Los identificadores y códigos oficiales se almacenarán como texto para preservar ceros iniciales. No asumir que nombre de colonia es una clave única. Las claves de entidad, alcaldía/municipio, localidad, AGEB y manzana se validarán con el catálogo geoestadístico elegido y versionado. La asignación geográfica derivada debe registrar método y versión.

El catálogo de actividades económicas deberá incluir código SCIAN, descripción, versión, regla de inclusión en cada categoría del producto y estado de validación. No se publicarán categorías a partir de coincidencias de texto no documentadas como si fueran clasificación oficial.

## 7. Acceso, privacidad y seguridad

- El repositorio puede contener documentación y código, no datasets descargados completos por defecto.
- La respuesta Bronze y los productos locales se excluyen del control de versiones.
- Los tokens se guardan fuera de Git, mediante variables de entorno o gestor de secretos del entorno.
- No se guardan campos de contacto en Silver/Gold salvo caso de uso aprobado y documentado.
- El acceso a datos y logs se limita a quienes los necesitan.
- Antes de publicar un dataset, informe o modelo, revisar licencia, atribución, condiciones de reutilización y riesgo de exponer información innecesaria.

## 8. Retención, repetibilidad y cambios

Conservar Bronze suficiente para poder repetir transformaciones y explicar resultados, conforme a las condiciones de la fuente y a la capacidad local disponible. No definir una política automática de borrado hasta evaluar el tamaño, utilidad histórica, condiciones de uso y recursos.

Los cambios de esquema o lógica deben ir en PR e incluir, según el impacto, actualización del diccionario, reglas, mapeo de fuente, tests y nota de versión. Los resultados Gold deberán poder vincularse al ID de ejecución Bronze y al commit/código que los produjo.

## 9. Criterios mínimos de aceptación de un dataset

Un dataset no se considera listo para consumo hasta que:
1. tenga propósito, responsable y granularidad documentados;
2. sus nombres, campos y definiciones consten en el diccionario;
3. cumpla las reglas bloqueantes o tenga una excepción aprobada y explicada;
4. incluya metadatos de fuente y periodo;
5. conserve trazabilidad hacia sus entradas;
6. tenga restricciones de acceso/reutilización evaluadas;
7. tenga una versión o fecha de producción identificable.

## 10. Revisión

Revisar el plan al incorporar una fuente nueva, cambiar de almacenamiento local a cloud, preparar un producto Gold público, agregar una etiqueta de ML o modificar la política de retención.
