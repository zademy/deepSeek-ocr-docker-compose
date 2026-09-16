# 05: Resultado vacío diferenciado de error de conexión

## Parent

Issue #4 — Rediseño de interfaz OCR para personas no técnicas.

## What to build

La persona usuaria ve un resultado vacío diferenciado de un fallo de conexión: si el modelo no devuelve texto, la interfaz indica "No se encontró texto" y permite procesar otro documento o ajustar opciones, sin presentar el silencio como error de red.

## Acceptance criteria

- [ ] Una operación que termina con texto vacío muestra un mensaje específico de "No se encontró texto", no un error de conexión.
- [ ] El panel ofrece acciones claras para "Procesar otro documento" y "Ajustar opciones".
- [ ] El mensaje distingue entre "sin texto" y "fallo del modelo"; los registros de Docker o la red no se exponen al usuario.
- [ ] Verificación con Playwright MCP usando una respuesta simulada con texto vacío.

## Blocked by

- Ticket #6: Flujo básico.
