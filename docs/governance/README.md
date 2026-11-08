# Gobierno de datos — índice

Esta carpeta reúne prácticas de gestión de datos inspiradas en DAMA-DMBOK, aplicadas de forma gradual y proporcional a un equipo pequeño. No representa una certificación ni una implantación completa.

## Documentos

- [Marco de gobierno](data-governance-charter.md): principios, responsabilidades y decisiones.
- [Plan de gestión](data-management-plan.md): ciclo de vida y controles.
- [Diccionario](data-dictionary.md): metadatos Bronze implementados y contratos Silver/Gold propuestos.
- [Reglas de calidad](data-quality-rules.md): controles Bronze en código y reglas futuras.
- [Registro de activos](data-assets-register.md): fuentes y productos con estado diferenciado.

## Estado técnico relacionado

El primer flujo DENUE implementa cliente, extracción/persistencia Bronze y validación de integridad. Silver, Gold, perfilado y cuarentena todavía no están implementados. El DAG orquesta una muestra manual de 15 registros para CDMX.

## Flujo de gobierno

1. Registrar y auditar fuente, condiciones de uso y cobertura.
2. Preservar original en Bronze con manifiesto sin credenciales.
3. Confirmar los campos y documentar el contrato.
4. Implementar transformaciones y controles de Silver.
5. Registrar excepciones con linaje a Bronze.
6. Aprobar métricas y limitaciones antes de publicar Gold.
7. Mantener cambios por pull request y decisiones trazables.
