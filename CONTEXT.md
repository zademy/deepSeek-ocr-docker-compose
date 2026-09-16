# Reconocimiento de documentos

La aplicación permite obtener texto de un documento y revisarlo junto a su vista previa.

## Language

**Documento**:
Contenido seleccionado por la persona para extraer su texto. En el flujo acordado se trabaja uno a la vez.
_Avoid_: Lote, cuando solo hay un documento.

**Resultado OCR**:
Texto obtenido al procesar un documento con el modelo de reconocimiento.
_Avoid_: Resultado real, para una simulación.

**Modo demo**:
Experiencia para probar el flujo con un resultado simulado, sin extraer texto del documento.
_Avoid_: OCR completado, cuando únicamente se ejecutó una simulación.

**Opciones avanzadas**:
Opciones adicionales para ajustar el modo de reconocimiento y la instrucción de procesamiento.
_Avoid_: Configuración obligatoria, para opciones que no son necesarias en el flujo básico.
