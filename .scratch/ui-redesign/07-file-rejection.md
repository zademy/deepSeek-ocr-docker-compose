# 07: Rechazo claro de archivo no admitido o demasiado grande

## Parent

Issue #4 — Rediseño de interfaz OCR para personas no técnicas.

## What to build

La persona usuaria enfrenta un mensaje claro cuando su archivo es demasiado grande o no se admite. La interfaz no pierde el Documento en caso de error recuperable y distingue entre "tipo no admitido" y "archivo demasiado grande".

## Acceptance criteria

- [ ] Un archivo no admitido muestra el motivo específico y conserva el Documento seleccionado para que la persona pueda reemplazarlo.
- [ ] Un archivo mayor que el límite muestra un mensaje claro con el tamaño aceptado y el del archivo rechazado.
- [ ] La interfaz distingue entre "tipo no admitido" y "archivo demasiado grande" mediante mensajes diferenciados.
- [ ] Verificación con Playwright MCP usando un archivo `.gif` rechazado por extensión y un archivo grande rechazado por tamaño.
- [ ] El estado del modelo y la operación no quedan bloqueados tras un rechazo de archivo.

## Blocked by

- Ticket #6: Flujo básico.
