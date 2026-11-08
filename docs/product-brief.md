# Product brief — Rendify

**Versión:** 0.2  
**Actualización:** 2026-11-07  
**Estado:** definición de producto en validación; la base de ingesta DENUE tiene una implementación inicial.

## 1. Resumen

Rendify busca ser una plataforma de inteligencia comercial geoespacial para ayudar a emprendedores, pequeños negocios y analistas a explorar la distribución de establecimientos y comparar zonas. La primera geografía objetivo es Ciudad de México, priorizando alcaldías. La fuente de establecimientos en desarrollo es DENUE/INEGI.

El repositorio ya contiene una primera pieza de ingeniería: consulta DENUE, persistencia del original en Bronze, manifiesto con trazabilidad e integridad, validación y orquestación con Airflow. Aún no existe el dataset Silver, indicadores Gold ni aplicación para usuarios.

## 2. Problema y alcance

Investigar posibles ubicaciones requiere combinar datos de establecimientos con contexto geográfico, demográfico y económico. Rendify pretende organizar fuentes y comparaciones transparentes, sin sustituir un estudio de mercado ni una evaluación financiera.

Categorías comerciales candidatas: cafeterías, restaurantes, gimnasios y tiendas de artículos (esta última requiere precisión). Las categorías deben mapearse a códigos SCIAN y reglas reproducibles después de validar la fuente.

## 3. Estado de desarrollo

| Área | Estado |
|---|---|
| Cliente DENUE | Implementado para `BuscarAreaAct`. |
| Extracción Bronze | Implementada con original, manifiesto y SHA-256. |
| Validación Bronze | Implementada para estructura, archivo, tamaño, checksum y conteo. |
| DAG Airflow | Implementado para extracción y validación manual de una muestra. |
| Pruebas | Unitarias para cliente, extracción y validación; integración real optativa. |
| Perfilado | Pendiente; script/módulo son placeholders. |
| Silver / Gold | Diseño documentado, sin transformación operativa. |
| Fuentes contextuales | En investigación; sin integración. |
| Aplicación/API | No implementada. |
| ML | No iniciado; primero se necesita objetivo y datos adecuados. |

## 4. Tipos de resultado que el producto debe diferenciar

1. **Descriptivo:** resume lo que registra una fuente en un periodo y nivel geográfico.
2. **Heurístico:** compara señales mediante reglas/pesos explícitos, sin presentarse como probabilidad.
3. **Predictivo:** estimación de modelo con etiquetas y evaluación válidas.

La densidad o cantidad de establecimientos no constituye por sí sola demanda, éxito o rentabilidad. Todo indicador debe exponer definición, cobertura, periodo, fuente y limitaciones.

## 5. Estrategia técnica

Se mantiene el enfoque local-first. La lógica de fuente vive en el paquete Python; Airflow orquesta tareas pequeñas. Bronze conserva el original; Silver y Gold se construirán cuando el contrato y la calidad del origen estén confirmados. Cloud, almacenamiento geoespacial, API y web se valorarán después de contar con un flujo local reproducible.

## 6. Próximos hitos

1. Ejecutar de extremo a extremo el DAG en el entorno Compose y registrar evidencia.
2. Confirmar esquema, campos, filtros y condiciones de uso con respuestas reales.
3. Implementar perfilado y reporte de calidad.
4. Definir e implementar contrato Silver y cuarentena.
5. Crear agregados descriptivos Gold con reglas y linaje.
6. Integrar fuentes demográficas/económicas solo si las claves, periodos y granularidades son comparables.
7. Validar necesidad de ML y producto web con datos y usuarios.
