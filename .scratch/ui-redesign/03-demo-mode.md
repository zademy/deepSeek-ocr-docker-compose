# 03: Modo demo persistente y verificable

## Parent

Issue #4 — Rediseño de interfaz OCR para personas no técnicas.

## What to build

La persona usuaria distingue visualmente el Modo demo en todo momento. Mientras está activo, una etiqueta persistente lo indica en el encabezado y el resultado del flujo lleva un aviso explícito de "Resultado simulado". El modo demo no realiza llamadas a `/api/ocr` ni descarga el modelo, y se puede salir con un solo clic. Tras varios ciclos del chequeo de salud, la etiqueta se mantiene mientras la simulación siga activa.

## Acceptance criteria

- [ ] Activar el modo demo muestra una etiqueta persistente en el encabezado y oculta los indicadores de carga del modelo.
- [ ] El botón principal opera en demo aunque el modelo no esté cargado y no realiza ninguna llamada a `/api/ocr`; verificado con Playwright MCP y la red observada.
- [ ] El resultado en demo lleva un aviso claro de "Resultado simulado" para no confundirlo con texto extraído del Documento.
- [ ] Salir del modo demo restaura los indicadores normales sin recargar la página.
- [ ] Después de varios ciclos del chequeo de salud, la etiqueta del modo demo sigue presente mientras la simulación esté activa.

## Blocked by

- Ticket #6: Flujo básico.
