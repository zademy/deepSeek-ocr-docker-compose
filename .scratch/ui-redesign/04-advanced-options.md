# 04: Opciones avanzadas plegables

## Parent

Issue #4 — Rediseño de interfaz OCR para personas no técnicas.

## What to build

La persona usuaria ve un panel de "Opciones avanzadas" oculto por defecto. Cuando lo despliega, encuentra el modo de reconocimiento y un campo para prompt personalizado, con explicación breve y ejemplos. Las opciones elegidas se capturan al iniciar la operación y no cambian aunque la persona modifique el panel mientras se procesa.

## Acceptance criteria

- [ ] El panel de opciones avanzadas está plegado por defecto y se abre con teclado o puntero.
- [ ] El modo inicial es "Documento con formato" (modo `markdown`), comprensible en español.
- [ ] El campo de prompt personalizado incluye una etiqueta, un `placeholder` y un texto de ayuda que explique para qué sirve.
- [ ] Cambiar el modo o el prompt después de iniciar una operación no altera la operación en curso; el resultado sigue vinculado a las opciones capturadas al inicio.
- [ ] Cerrar el panel conserva los valores introducidos.
- [ ] Las opciones avanzadas son accesibles con teclado y se anuncian como región expandible.

## Blocked by

- Ticket #6: Flujo básico.
