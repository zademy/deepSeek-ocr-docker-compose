# 02: Flujo básico de carga, extracción y revisión

## Parent

Issue #4 — Rediseño de interfaz OCR para personas no técnicas.

## What to build

La persona usuaria ve una página clara con un solo botón principal "Extraer texto" y un panel que combina Documento y Resultado OCR en la misma vista en escritorio. La operación se inicia con un solo clic, los estados del modelo y de la operación son comprensibles, y los controles cumplen contraste y navegación por teclado. La barra de progreso refleja los valores reales enviados por el backend y un doble clic produce una sola operación.

## Acceptance criteria

- [ ] El botón principal "Extraer texto" está deshabilitado hasta que hay un Documento válido y un modelo listo o modo demo activo.
- [ ] Doble clic y reentrancy producen exactamente una operación contra `/api/ocr`; verificado con Playwright MCP y la red observada.
- [ ] La barra de progreso refleja los valores 0, 40 y 100 enviados en `percent` por el backend.
- [ ] El botón principal se bloquea antes del primer `await`; limpiar el documento durante la operación la cancela de forma coherente sin resultados colgados.
- [ ] La disposición combina Documento y Resultado OCR en la misma pantalla en escritorio y se apila sin desbordamiento horizontal a 320, 768 y 1280 px.
- [ ] El flujo completo se completa solo con teclado, con foco visible en cada paso y contraste WCAG AA.
- [ ] El modo de reconocimiento se nombra con términos comprensibles en español; los valores técnicos preservados en el contrato HTTP se mantienen como claves internas.
- [ ] El Resultado OCR se muestra como texto seleccionable con `textContent`; no se inyecta HTML recibido del backend.
- [ ] Copiar y descargar conservan exactamente el texto del resultado mostrado.

## Blocked by

- Ticket #6: Compilación Tailwind y build limpio.
