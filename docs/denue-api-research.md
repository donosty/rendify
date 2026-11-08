# Investigación de la API del DENUE para Rendify

- **Última actualización documental:** 2026-11-07
- **Fuente:** [API del DENUE — INEGI](https://www.inegi.org.mx/servicios/api_denue.html)
- **Estado:** investigación documental más una primera implementación técnica de muestra. Confirmar los detalles de esquema y cobertura con nuevas respuestas reales antes de cerrar el contrato.

## 1. Resumen de implementación

Rendify utiliza el método `BuscarAreaAct` de la API del DENUE. El cliente se encuentra en `src/rendify/denue/client.py`; la extracción y persistencia en `src/rendify/denue/extract.py`; y los controles Bronze en `src/rendify/denue/validate.py`.

El DAG `denue_initial_extraction` ejecuta una consulta de prueba para entidad `09` (CDMX), sin filtros adicionales, y solicita registros del 1 al 15. La respuesta se guarda en Bronze junto con un manifiesto. Esto verifica el diseño básico de consulta y persistencia cuando la ejecución concluye correctamente; no prueba la cobertura completa ni la extracción por alcaldía/actividad.

## 2. Contrato de consulta implementado

El cliente construye una ruta con los parámetros:

- entidad;
- municipio/alcaldía;
- localidad;
- AGEB;
- manzana;
- sector, subsector, rama y clase de actividad;
- nombre del establecimiento;
- registro inicial y final;
- identificador de establecimiento;
- token.

Los parámetros se codifican como segmentos de URL. El cliente rechaza token vacío y rangos inválidos, usa timeout configurable y convierte fallos HTTP, timeout y conexión en `DenueAPIError`. El cuerpo se decodifica como UTF-8 (aceptando BOM), se parsea como JSON y se exige una lista de objetos.

La respuesta `DenueAPIResponse` incluye status HTTP, content type, bytes originales y registros parseados. El almacenamiento utiliza los bytes originales, no una reserialización del objeto JSON.

## 3. Persistencia Bronze

Para cada ejecución se crea:

```text
data/bronze/denue/
└── extraction_date=YYYY-MM-DD/
    └── run_id=<run_id_sanitizado>/
        ├── response.json
        └── manifest.json
```

El manifiesto registra:

- fuente y método;
- run ID original;
- timestamp UTC y fecha de extracción;
- parámetros no secretos;
- código HTTP y content type;
- cantidad de registros;
- tamaño del archivo;
- checksum SHA-256;
- referencia relativa al archivo de respuesta.

La extracción no escribe claves que contengan `token` o `secret` en los parámetros de consulta. La respuesta se escribe antes que el manifiesto para no publicar metadatos de una extracción cuyo archivo aún no exista.

## 4. Validación Bronze implementada

`validate_bronze_response()` comprueba campos obligatorios del manifiesto, origen/método, estructura de parámetros y metadatos HTTP, estado 200, nombre de archivo relativo seguro, existencia y lectura del payload, tamaño, checksum, JSON UTF-8, lista de objetos y número de registros.

Su resultado es un resumen pequeño con rutas, conteo, tamaño, checksum y estado HTTP. No transforma los registros a Silver.

## 5. Pruebas en el repositorio

- `tests/denue/test_denue_client.py`: URL, codificación, token y rango.
- `tests/denue/test_denue_extract.py`: bytes originales, manifiesto, checksum, credenciales y extracción con cliente simulado.
- `tests/denue/test_denue_validate.py`: payload válido, archivo ausente, checksum, conteo y JSON inválido.
- `tests/integration/test_denue_api.py`: test opcional contra el servicio real, con token; comprueba status, content type, estructura y campos observados.

## 6. Limitaciones y trabajo pendiente

- Ejecutar el test de integración y el DAG con credenciales válidas y conservar evidencia sin exponer los datos ni el token.
- Verificar el esquema real y revisar diferencias entre el ejemplo documental y la respuesta del método usado.
- Confirmar límites, paginación, cuotas, filtros y extracción completa.
- Confirmar semántica y estabilidad de identificadores y campos geográficos.
- Mapear actividades de producto a SCIAN versionado.
- Perfilado de nulos, duplicados, coordenadas, códigos y cobertura.
- Implementar Silver, reglas de cuarentena y agregados Gold.
- Revisar condiciones de uso/atribución y política de retención.

No concluir que la prueba de 15 registros acredita cobertura o representatividad de CDMX.

