# 01: Compilación Tailwind y build limpio

## Parent

Issue #4 — Rediseño de interfaz OCR para personas no técnicas.

## What to build

La persona usuaria ve la aplicación construida con CSS compilado de Tailwind, servido correctamente por Nginx desde una imagen Docker limpia. La construcción añade un paso de compilación dentro del build del frontend sin alterar el contrato con el backend ni el flujo HTTP existente.

## Acceptance criteria

- [ ] La imagen Docker del frontend compila CSS con `@tailwindcss/cli` durante `docker build`, sin Play CDN en distribución.
- [ ] Existe un lockfile que fija la versión de Tailwind y sus dependencias; la instalación es reproducible en una máquina limpia.
- [ ] Nginx sirve el CSS compilado y el JavaScript existente; el bind mount del frontend no oculta los artefactos compilados.
- [ ] Una construcción limpia del stack funciona sin `node_modules` ni CSS generado en el host.
- [ ] Verificación con Playwright MCP sobre Compose: la página carga sin errores 404 de assets y la primera interacción no rompe la disposición.
- [ ] Chrome DevTools MCP o `docker logs` solo se usan si la verificación falla.

## Blocked by

None (can start immediately).
