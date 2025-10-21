// API Base URL
const API_URL = window.location.origin;

// Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const imagePreview = document.getElementById('imagePreview');
const previewSection = document.getElementById('previewSection');
const clearBtn = document.getElementById('clearBtn');
const modeSelect = document.getElementById('modeSelect');
const customPrompt = document.getElementById('customPrompt');
const processBtn = document.getElementById('processBtn');
const loadingSection = document.getElementById('loadingSection');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');
const statusIndicator = document.getElementById('status-indicator');
const statusText = document.getElementById('status-text');
const modelDownloadSection = document.getElementById('modelDownloadSection');
const downloadModelBtn = document.getElementById('downloadModelBtn');
const downloadProgressContainer = document.getElementById('downloadProgressContainer');
const downloadProgressBar = document.getElementById('downloadProgressBar');
const downloadProgressText = document.getElementById('downloadProgressText');
const demoModeSection = document.getElementById('demoModeSection');
const demoModeBtn = document.getElementById('demoModeBtn');

let selectedFile = null;
let demoMode = false;
let downloadCheckInterval = null;

// Initialize
checkApiHealth();
setupEventListeners();

// Check API health
async function checkApiHealth() {
    try {
        const response = await fetch(`${API_URL}/health`);
        const data = await response.json();
        
        if (data.status === 'healthy') {
            statusIndicator.classList.remove('offline');
            statusIndicator.classList.add('online');
            
            // Mostrar estado del modelo
            if (data.model_loaded) {
                statusIndicator.classList.remove('loading');
                statusText.textContent = 'Modelo cargado ✓';
                modelDownloadSection.classList.add('hidden');
                demoModeSection.classList.add('hidden');
            } else if (data.model_loading) {
                statusIndicator.classList.add('loading');
                statusText.textContent = '⏳ Descargando/Cargando modelo...';
                modelDownloadSection.classList.remove('hidden');
                downloadProgressContainer.classList.remove('hidden');
                downloadModelBtn.classList.add('hidden');
                
                // Mostrar progreso si está disponible
                if (data.download_progress) {
                    updateDownloadProgress(data.download_progress);
                }
            } else if (data.model_error) {
                statusIndicator.classList.remove('loading');
                statusIndicator.classList.add('error');
                statusText.textContent = `⚠️ Error: ${data.model_error.substring(0, 50)}...`;
                modelDownloadSection.classList.add('hidden');
                demoModeSection.classList.remove('hidden');
            } else {
                statusIndicator.classList.remove('loading');
                statusText.textContent = 'Modelo no descargado';
                modelDownloadSection.classList.remove('hidden');
                downloadProgressContainer.classList.add('hidden');
                downloadModelBtn.classList.remove('hidden');
                demoModeSection.classList.remove('hidden');
            }
        } else {
            statusIndicator.classList.remove('online', 'loading');
            statusIndicator.classList.add('offline');
            statusText.textContent = 'API no disponible';
        }
    } catch (error) {
        statusIndicator.classList.remove('online', 'loading');
        statusIndicator.classList.add('offline');
        statusText.textContent = 'API desconectada';
        console.error('Health check failed:', error);
    }
}

// Update download progress
function updateDownloadProgress(progress) {
    if (progress.progress !== undefined) {
        downloadProgressBar.style.width = `${progress.progress}%`;
        downloadProgressText.textContent = `${progress.progress}% - ${progress.message || 'Descargando...'}`;
        
        if (progress.status === 'completed') {
            setTimeout(() => {
                downloadProgressContainer.classList.add('hidden');
                modelDownloadSection.classList.add('hidden');
            }, 2000);
        }
    }
}

// Start model download
async function startModelDownload() {
    try {
        downloadModelBtn.disabled = true;
        downloadModelBtn.textContent = '⏳ Iniciando...';
        
        const response = await fetch(`${API_URL}/api/download-model`, {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.status === 'started' || data.status === 'downloading') {
            downloadProgressContainer.classList.remove('hidden');
            downloadModelBtn.classList.add('hidden');
            
            // Iniciar polling del progreso
            startProgressPolling();
        } else if (data.status === 'already_loaded') {
            showError('El modelo ya está cargado');
            downloadModelBtn.disabled = false;
            downloadModelBtn.textContent = '📥 Descargar Modelo';
        }
    } catch (error) {
        console.error('Download error:', error);
        showError('Error al iniciar la descarga del modelo');
        downloadModelBtn.disabled = false;
        downloadModelBtn.textContent = '📥 Descargar Modelo';
    }
}

// Start progress polling
function startProgressPolling() {
    if (downloadCheckInterval) {
        clearInterval(downloadCheckInterval);
    }
    
    downloadCheckInterval = setInterval(async () => {
        try {
            const response = await fetch(`${API_URL}/api/download-progress`);
            const data = await response.json();
            
            if (data.progress) {
                updateDownloadProgress(data.progress);
            }
            
            if (data.model_loaded) {
                clearInterval(downloadCheckInterval);
                downloadCheckInterval = null;
                checkApiHealth();
            }
        } catch (error) {
            console.error('Progress check error:', error);
        }
    }, 2000); // Check every 2 seconds
}

// Enable demo mode
function enableDemoMode() {
    demoMode = true;
    statusText.textContent = '🎮 Modo Demo Activado';
    statusIndicator.classList.remove('offline', 'loading', 'error');
    statusIndicator.classList.add('online');
    modelDownloadSection.classList.add('hidden');
    demoModeSection.classList.add('hidden');
    
    alert('🎮 Modo Demo Activado\n\nPuedes probar la interfaz. Al procesar, se simulará un resultado de OCR.\n\nPara usar el OCR real, descarga el modelo.');
}

// Setup event listeners
function setupEventListeners() {
    // Upload area click
    uploadArea.addEventListener('click', () => fileInput.click());
    
    // File input change
    fileInput.addEventListener('change', handleFileSelect);
    
    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('drag-over');
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('drag-over');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });
    
    // Clear button
    clearBtn.addEventListener('click', clearSelection);
    
    // Process button
    processBtn.addEventListener('click', processOCR);
    
    // Copy button
    document.getElementById('copyBtn').addEventListener('click', copyResult);
    
    // Download button
    document.getElementById('downloadBtn').addEventListener('click', downloadResult);
    
    // New OCR button
    document.getElementById('newOcrBtn').addEventListener('click', resetForm);
    
    // Retry button
    document.getElementById('retryBtn').addEventListener('click', () => {
        errorSection.classList.add('hidden');
        processOCR();
    });
    
    // Download model button
    downloadModelBtn.addEventListener('click', startModelDownload);
    
    // Demo mode button
    demoModeBtn.addEventListener('click', enableDemoMode);
}

// Handle file selection
function handleFileSelect(e) {
    const files = e.target.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

// Handle file
function handleFile(file) {
    // Validate file type
    const validTypes = ['image/jpeg', 'image/png', 'image/webp', 'application/pdf'];
    if (!validTypes.includes(file.type)) {
        showError('Tipo de archivo no válido. Use JPG, PNG, WEBP o PDF.');
        return;
    }
    
    // Validate file size (10MB)
    if (file.size > 10 * 1024 * 1024) {
        showError('Archivo muy grande. Máximo 10MB.');
        return;
    }
    
    selectedFile = file;
    
    // Show preview if image
    if (file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            previewSection.classList.remove('hidden');
            uploadArea.classList.add('hidden');
        };
        reader.readAsDataURL(file);
    } else {
        // For PDF, just show filename
        previewSection.classList.remove('hidden');
        uploadArea.classList.add('hidden');
        imagePreview.style.display = 'none';
    }
    
    processBtn.disabled = false;
}

// Clear selection
function clearSelection() {
    selectedFile = null;
    fileInput.value = '';
    previewSection.classList.add('hidden');
    uploadArea.classList.remove('hidden');
    processBtn.disabled = true;
    imagePreview.style.display = 'block';
}

// Process OCR
async function processOCR() {
    if (!selectedFile) return;
    
    // Demo mode - simulate OCR
    if (demoMode) {
        processDemoOCR();
        return;
    }
    
    // Verificar estado del modelo primero
    try {
        const healthCheck = await fetch(`${API_URL}/health`);
        const healthData = await healthCheck.json();
        
        if (healthData.model_loading) {
            showError('El modelo aún se está descargando/cargando. Por favor espera y verifica el progreso en la barra superior.');
            return;
        }
        
        if (healthData.model_error) {
            showError(`Error con el modelo: ${healthData.model_error}`);
            return;
        }
        
        if (!healthData.model_loaded) {
            showError('El modelo no está cargado. Por favor descarga el modelo primero o usa el Modo Demo.');
            return;
        }
    } catch (error) {
        console.error('Health check error:', error);
    }
    
    // Hide previous results/errors
    resultsSection.classList.add('hidden');
    errorSection.classList.add('hidden');
    
    // Show loading
    loadingSection.classList.remove('hidden');
    processBtn.disabled = true;
    
    try {
        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('mode', modeSelect.value);
        
        if (customPrompt.value.trim()) {
            formData.append('custom_prompt', customPrompt.value.trim());
        }
        
        const response = await fetch(`${API_URL}/api/ocr`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Error procesando imagen');
        }
        
        const result = await response.json();
        displayResults(result);
        
    } catch (error) {
        console.error('OCR Error:', error);
        showError(error.message || 'Error procesando la imagen. Intente nuevamente.');
    } finally {
        loadingSection.classList.add('hidden');
        processBtn.disabled = false;
    }
}

// Process demo OCR (simulated)
function processDemoOCR() {
    // Hide previous results/errors
    resultsSection.classList.add('hidden');
    errorSection.classList.add('hidden');
    
    // Show loading
    loadingSection.classList.remove('hidden');
    processBtn.disabled = true;
    
    // Simulate processing delay
    setTimeout(() => {
        const demoResult = {
            success: true,
            text: `🎮 MODO DEMO - Resultado Simulado

Esto es una simulación de OCR.
El texto real se extraería de tu imagen usando el modelo DeepSeek-OCR.

Archivo: ${selectedFile.name}
Modo seleccionado: ${modeSelect.value}

Para obtener resultados reales:
1. Descarga el modelo usando el botón en la parte superior
2. Espera a que se complete la descarga
3. Procesa tu imagen nuevamente

Características del OCR real:
- Reconocimiento de texto preciso
- Soporte para múltiples idiomas
- Conversión a Markdown
- Extracción de coordenadas
- Análisis de figuras y gráficos`,
            processing_time: 2.5,
            mode: modeSelect.value,
            image_size: [800, 600],
            file_size: selectedFile.size
        };
        
        displayResults(demoResult);
        loadingSection.classList.add('hidden');
        processBtn.disabled = false;
    }, 2500);
}

// Display results
function displayResults(data) {
    // Update stats
    document.getElementById('processingTime').textContent = `${data.processing_time}s`;
    document.getElementById('usedMode').textContent = data.mode;
    document.getElementById('imageSize').textContent = 
        `${data.image_size[0]} × ${data.image_size[1]}`;
    
    // Update text
    document.getElementById('resultText').textContent = data.text || 'Sin resultados';
    
    // Show results
    resultsSection.classList.remove('hidden');
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// Copy result
async function copyResult() {
    const text = document.getElementById('resultText').textContent;
    try {
        await navigator.clipboard.writeText(text);
        const btn = document.getElementById('copyBtn');
        const originalText = btn.textContent;
        btn.textContent = '✓ Copiado';
        setTimeout(() => {
            btn.textContent = originalText;
        }, 2000);
    } catch (error) {
        console.error('Copy failed:', error);
        alert('No se pudo copiar al portapapeles');
    }
}

// Download result
function downloadResult() {
    const text = document.getElementById('resultText').textContent;
    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `ocr_result_${Date.now()}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Reset form
function resetForm() {
    clearSelection();
    resultsSection.classList.add('hidden');
    errorSection.classList.add('hidden');
    customPrompt.value = '';
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Show error
function showError(message) {
    document.getElementById('errorMessage').textContent = message;
    errorSection.classList.remove('hidden');
    loadingSection.classList.add('hidden');
    
    // Scroll to error
    errorSection.scrollIntoView({ behavior: 'smooth' });
}

// Periodic health check
setInterval(checkApiHealth, 10000); // Every 10 seconds (más frecuente para detectar cambios de estado)
