# Rediseño de la interfaz OCR

## Estado y alcance

Diagnóstico estático y plan. La implementación y la aceptación visual quedan pendientes de aprobación.
No se ha ejecutado una nueva validación de navegador en esta etapa.

El usuario confirmó:

- Público principal no técnico; interfaz clara, sobria y en español.
- Tailwind CSS conservando HTML y JavaScript, sin migrar a React.
- Un documento a la vez: subir, procesar y revisar.
- Vista previa junto al resultado; copiar y descargar accesibles.
- Opciones avanzadas plegadas inicialmente.
- Diseño adaptable a móvil, menos emojis, contraste y tipografía legible.
- Preparar diagnóstico, requisitos y plan antes de implementar.

Los términos del producto están en [CONTEXT.md](../CONTEXT.md).
Las decisiones nuevas de esta propuesta no se consideran aprobadas todavía.

## Diagnóstico de la implementación actual

| Prioridad | Evidencia | Fricción y consecuencia |
| --- | --- | --- |
| P0 | `frontend/app.js:89`; `backend/model_lifecycle.py:18` | Se lee `progress.progress`, pero llega `percent`. |
| P0 | `frontend/app.js:35,161,467` | El sondeo de salud sobrescribe la etiqueta demo, pero deja activa la simulación. |
| P0 | `frontend/app.js:282–334` | El botón se bloquea después del chequeo de salud; admite doble envío. |
| P0 | `frontend/app.js:135` | El sondeo de carga no termina ante error y puede solapar peticiones. |
| P0 | `frontend/index.html:43–49`; `backend/ocr_handler.py:62–94` | PDF anunciado sin rasterización de páginas. |
| P1 | `frontend/app.js:236–279,354–395` | Preview y temporizador demo pueden usar una selección obsoleta. |
| P1 | `frontend/index.html:42–55,84–127` | Carga clicable sin acceso equivalente por teclado; estados sin anuncios. |
| P1 | `frontend/index.html:53–91` | Opciones técnicas expuestas desde el inicio; preview separada del resultado. |
| P1 | `frontend/nginx.conf:14–37` | El límite de petición incluye multipart; un archivo de 10 MiB puede excederlo. |
| P1 | `backend/ocr_handler.py:106` | Crea ajustes por defecto en vez de usar los preparados por `main.py:28–44`. |

Los fallos de estado requieren cambios de comportamiento; Tailwind por sí solo no los corrige.
Los hallazgos backend se registran como dependencias, no como permiso para ampliar este trabajo.

## Propuesta de experiencia

### 1. Subir documento

- Encabezado compacto: nombre del producto, estado del modelo y acceso separado al modo demo.
- Zona de carga con botón nativo «Seleccionar imagen» y arrastrar como alternativa.
- Indicar formatos realmente admitidos y tamaño máximo antes de seleccionar.
- Mostrar nombre, tamaño y vista previa; acciones «Cambiar documento» y «Quitar».
- Recomendar inicialmente JPG, PNG y WEBP; PDF requiere la decisión indicada al final.

### 2. Procesar

- Acción principal «Extraer texto», deshabilitada si falta un documento válido o hay una operación activa.
- Mantener el modo Markdown actual como valor inicial, presentado como «Documento con formato».
- Plegable «Opciones avanzadas»: modo y prompt personalizado, con explicación y ejemplos breves.
- No añadir controles de resolución hasta corregir y probar la propagación de ajustes.
- Mostrar preparación del modelo separada del procesamiento del documento.
- Durante inferencia, usar un indicador indeterminado: no existe progreso real por porcentaje.
- Al iniciar, fijar documento y opciones de esa operación para evitar mezclar resultados.

### 3. Revisar resultado

- Escritorio: dos columnas, documento a la izquierda y resultado a la derecha.
- Móvil: documento y resultado apilados, sin desplazamiento horizontal de toda la página.
- Resultado seleccionable, conservando saltos de línea y sin insertar HTML recibido mediante `innerHTML`.
- Acciones «Copiar texto», «Descargar TXT» y «Procesar otro documento».
- Aviso de copia completada o fallida; descarga con nombre reconocible.
- Resultado vacío explícito: «No se encontró texto», sin presentarlo como fallo de conexión.
- En demo: aviso persistente «Resultado simulado: no se ha extraído texto de tu documento».

## Estados y comportamiento requerido

Separar estado del modelo, estado del documento y modo demo; no usar una sola etiqueta para los tres.

| Situación | Respuesta visible | Comportamiento |
| --- | --- | --- |
| Sin documento | Instrucción de carga | No permitir procesar. |
| Documento válido | Preview y opciones | Permitir procesar si el modelo está listo, o en demo. |
| Modelo pendiente | «Preparar modelo» | Explicar descarga inicial; no bloquear probar demo. |
| Modelo cargando | Etapa y porcentaje recibido | Leer `percent`; no afirmar que representa bytes descargados. |
| Procesando documento | «Extrayendo texto…» | Una operación; bloquear cambios que invaliden la selección. |
| Resultado disponible | Texto y acciones | Vincularlo al documento y modo usados al iniciar. |
| Sin texto | Mensaje específico | Permitir otro documento o ajuste de opciones. |
| Error de carga del modelo | Motivo comprensible | Detener sondeo; explicar recuperación que realmente exista. |
| Error de petición | Mensaje con recuperación | Conservar documento y opciones; restablecer controles. |
| Demo activo | Etiqueta persistente y salida explícita | Ningún POST OCR real ni descarga automática del modelo. |

Comprobar códigos HTTP antes de leer éxito. Contemplar respuestas no JSON, especialmente errores de Nginx.
El backend actual conserva errores de carga: no prometer reintento de descarga funcional sin corregirlo.
No ofrecer cancelación de inferencia sin soporte backend; abandonar la espera no detiene el procesamiento.

## Dirección visual y accesibilidad

- Base clara, superficies neutras, un color de acción y colores semánticos para estados.
- Tipografía de sistema, texto principal de 16 px y jerarquía breve de títulos.
- Contenido centrado, ancho de lectura acotado y espacio consistente entre acciones.
- Objetivos táctiles de al menos 44 × 44 px como criterio del proyecto.
- Contraste WCAG AA: 4.5:1 en texto normal y 3:1 en texto grande.
- Foco visible, recorrido lógico y ninguna acción disponible solo con ratón.
- Plegable accesible, etiquetas de formulario y preview con alternativa textual en español.
- Anunciar cambios importantes mediante regiones vivas sin repetir cada sondeo.
- Respetar reducción de movimiento; no depender solo del color para comunicar un estado.
- Verificar a 320, 768 y 1280 px, además de zoom al 200 %.

## Integración de Tailwind propuesta

No hay Tailwind ni `package.json` en el frontend actual. Se propone Tailwind v4 con su CLI oficial.
Fijar versión exacta y lockfile al implementar, tras confirmar navegadores objetivo.

- Añadir compilación CSS con `tailwindcss` y `@tailwindcss/cli`.
- Compilar CSS durante la construcción de la imagen; Nginx entrega los archivos estáticos.
- No utilizar Play CDN en la distribución: está destinado a desarrollo.
- Conservar JavaScript nativo y los contratos HTTP existentes, excepto correcciones aprobadas.
- Hacer explícitas las clases de estado para que el compilador pueda encontrarlas.
- Revisar el montaje `./frontend` de Compose: no debe ocultar el CSS compilado dentro de la imagen.
- Comprobar que una construcción limpia funciona sin `node_modules` ni CSS generado en el host.

Referencia consultada: documentación oficial Tailwind CSS v4 mediante Context7.

- [CLI](https://tailwindcss.com/docs/installation/tailwind-cli)
- [Play CDN y su alcance](https://tailwindcss.com/docs/installation/play-cdn)

## Plan de implementación propuesto

1. **Contrato y estados:** pruebas de progreso, demo, doble envío y callbacks obsoletos; corregir esos fallos.
2. **Construcción CSS:** fijar Tailwind/CLI, añadir lockfile y verificar Docker/Nginx/Compose.
3. **Estructura:** carga accesible, disposición documento/resultado y avanzadas plegables.
4. **Contenido y acciones:** español consistente, demo explícito, errores recuperables, copia y descarga.
5. **Validación:** Playwright MCP sobre Compose; Chrome DevTools MCP y logs de Docker para diagnosticar fallos.

Archivos previstos: `frontend/index.html`, `frontend/app.js`, `frontend/styles.css`,
`frontend/Dockerfile`, archivos nuevos de construcción CSS y configuración Compose si requiere ajuste.
La alineación del límite de carga puede implicar `frontend/nginx.conf`.
PDF, reintento de carga y propagación de ajustes backend requieren alcance aprobado explícitamente.

## Criterios de aceptación

- [ ] Una persona completa el flujo básico sin abrir opciones avanzadas.
- [ ] Selección por teclado y arrastre producen el mismo documento vigente.
- [ ] Cambiar A por B o limpiar A no permite que un callback muestre A después.
- [ ] Doble clic produce exactamente un POST `/api/ocr`.
- [ ] Progreso muestra los valores 0, 40 y 100 recibidos en `percent`.
- [ ] Un error detiene el sondeo y no deja controles bloqueados indefinidamente.
- [ ] Demo sigue identificado después de varios chequeos de salud y ofrece salida explícita.
- [ ] Demo no llama `/api/ocr`; su resultado no se presenta como extracción real.
- [ ] Copiar y descargar conservan exactamente el texto del resultado mostrado.
- [ ] Errores 400, 413, 503, desconexión y respuesta no JSON tienen mensajes útiles.
- [ ] No hay overflow de página a 320 px ni acciones inaccesibles con zoom al 200 %.
- [ ] El CSS se sirve correctamente desde una construcción Docker limpia.
- [ ] Prueba real: subir imagen conocida, enviar OCR, recibir texto y descargarlo usando Playwright MCP.

Las pruebas con respuestas simuladas verifican estados de interfaz; no certifican inferencia OCR-2.
La extracción real sigue pendiente: la sesión previa solo completó el flujo demo y registró reinicios
durante carga del modelo en un Docker local con aproximadamente 4 GiB de RAM y sin NVIDIA.
No atribuir esos reinicios a una causa definitiva sin comprobar evidencia del proceso o del contenedor.

## Decisiones pendientes antes de implementar

1. **Formatos:** se recomienda limitar esta entrega a JPG, PNG y WEBP; retirar la promesa actual de PDF.
2. **Compatibilidad:** se recomiendan navegadores actuales; confirmar si hay que soportar versiones antiguas.
3. **Prueba real:** definir un entorno NVIDIA compatible disponible para la aceptación OCR-2 completa.

Fuera de esta entrega propuesta: lotes, historial persistente, cuentas, PDF multipágina y editor enriquecido.
Estos elementos no son requisitos aprobados del rediseño.
