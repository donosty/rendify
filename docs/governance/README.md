# Gobierno de datos — índice

Esta carpeta reúne los controles de gestión de datos que Rendify aplica de forma gradual, inspirándose en disciplinas de DAMA-DMBOK. Es una adaptación ligera para un equipo pequeño, no una certificación ni una implantación completa del marco.

## Documentos

- [Marco de gobierno de datos](data-governance-charter.md): principios, responsabilidades, derechos de decisión y controles de ciclo de vida.
- [Plan de gestión de datos](data-management-plan.md): cómo registrar, ingerir, transformar, proteger, publicar y retirar activos.
- [Diccionario de datos](data-dictionary.md): definiciones de origen y nombres canónicos propuestos para Bronze, Silver y Gold.
- [Reglas de calidad de datos](data-quality-rules.md): controles, severidad, evidencia y criterios de promoción.
- [Registro de activos de datos](data-assets-register.md): fuentes y productos, responsables, estado y pendientes.

## Flujo de trabajo

1. Registrar la fuente en el inventario de activos antes de ingestas importantes.
2. Revisar documentación, permisos/condiciones de uso, semántica, cobertura y granularidad.
3. Preservar la respuesta de origen en Bronze junto con un manifiesto seguro.
4. Acordar un contrato con campos definidos en el diccionario.
5. Validar y documentar las transformaciones y excepciones al promover a Silver.
6. Aprobar la definición, calidad y limitaciones antes de publicar Gold.
7. Actualizar este conjunto de documentos mediante pull request cuando cambie una fuente, un esquema o una métrica.
