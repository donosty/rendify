# Contratos de datos versionados

Esta carpeta contendrá contratos de entrada/salida (por ejemplo, JSON Schema o definiciones de tablas) cuando una respuesta real de DENUE y el esquema de Silver hayan sido verificados.

## Reglas

- Versionar solo contratos revisados, no ejemplos que incluyan tokens o datos de acceso.
- Indicar dataset, versión, propietario funcional, granularidad, propiedades requeridas/opcionales y tipos.
- Mapear cada propiedad de origen al campo canónico del diccionario.
- Documentar cambios incompatibles y actualizar pruebas de contrato.
- No convertir supuestos de la documentación pública en campos obligatorios hasta probar la respuesta real.

Hasta confirmar la muestra del DENUE, el diccionario de datos señala las propiedades candidatas y su estado de verificación.
