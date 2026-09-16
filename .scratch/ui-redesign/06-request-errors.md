# 06: Errores honestos de carga y petición

## Parent

Issue #4 — Rediseño de interfaz OCR para personas no técnicas.

## What to build

La persona usuaria enfrenta mensajes honestos cuando algo falla. Un error de carga del modelo detiene el sondeo y muestra el mensaje de recuperación que el backend realmente permite, sin prometer un reintento que el backend rechaza. Un error transitorio en `/api/ocr` muestra el motivo, conserva el Documento y las opciones, y permite reintentar sin volver a seleccionar el archivo. Una respuesta no JSON (por ejemplo, un 413 de Nginx) se traduce a un mensaje comprensible y la interfaz no queda en estado "cargando".

## Acceptance criteria

- [ ] Un error de carga del modelo detiene el sondeo y muestra la recuperación que el backend realmente permite; no aparece un botón de reintento de descarga que el backend rechazaría.
- [ ] Un error transitorio en `/api/ocr` muestra el motivo, conserva el Documento y las opciones seleccionadas, y permite reintentar sin reenviar el archivo.
- [ ] La interfaz distingue entre respuesta JSON y respuesta no JSON; nunca se queda en "cargando" tras un error de Nginx.
- [ ] Los códigos HTTP 400, 413 y 503 producen mensajes comprensibles, alineados con el límite de Nginx y el del backend.
- [ ] Verificación con Playwright MCP usando respuestas controladas: 200, 400, 413, 503 y respuesta no JSON.

## Blocked by

- Ticket #6: Flujo básico.
