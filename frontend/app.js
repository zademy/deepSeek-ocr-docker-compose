(() => {
  "use strict";

  const $ = (id) => document.getElementById(id);
  const els = {
    form: $("ocrForm"),
    fileInput: $("fileInput"),
    fileError: $("fileError"),
    docCard: $("docCard"),
    docThumb: $("docThumb"),
    docName: $("docName"),
    docSize: $("docSize"),
    clearFileBtn: $("clearFileBtn"),
    uploadFieldset: $("uploadFieldset"),
    advanced: $("advancedOptions"),
    modeSelect: $("modeSelect"),
    promptInput: $("promptInput"),
    extractBtn: $("extractBtn"),
    extractHint: $("extractHint"),
    opProgress: $("opProgress"),
    opProgressText: $("opProgressText"),
    opError: $("opError"),
    opErrorTitle: $("opErrorTitle"),
    opErrorMessage: $("opErrorMessage"),
    retryBtn: $("retryBtn"),
    errorResetBtn: $("errorResetBtn"),
    resultSection: $("resultSection"),
    resultTitle: $("resultTitle"),
    demoResultBanner: $("demoResultBanner"),
    emptyResult: $("emptyResult"),
    emptyNewDocBtn: $("emptyNewDocBtn"),
    emptyAdjustBtn: $("emptyAdjustBtn"),
    resultGrid: $("resultGrid"),
    resultThumb: $("resultThumb"),
    resultFileName: $("resultFileName"),
    resultMode: $("resultMode"),
    resultTime: $("resultTime"),
    resultImageSize: $("resultImageSize"),
    resultText: $("resultText"),
    copyBtn: $("copyBtn"),
    downloadBtn: $("downloadBtn"),
    copyFeedback: $("copyFeedback"),
    newDocBtn: $("newDocBtn"),
    modelPanel: $("modelPanel"),
    modelPanelBody: $("modelPanelBody"),
    modelChip: $("modelChip"),
    modelDot: $("modelDot"),
    modelChipText: $("modelChipText"),
    demoBadge: $("demoBadge"),
    exitDemoBtn: $("exitDemoBtn"),
  };

  const MAX_BYTES = 10 * 1024 * 1024;
  const ACCEPTED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".webp"];
  const MODE_LABELS = {
    markdown: "Documento con formato",
    free_ocr: "Texto sin formato",
    grounding: "Texto con posiciones",
    parse_figure: "Figuras y gráficos",
    detailed: "Descripción de la imagen",
  };

  const state = {
    file: null,
    previewUrl: null,
    demo: false,
    model: { phase: "checking", percent: 0, message: "" },
    op: null,
    result: null,
    nextOpId: 1,
    downloading: false,
  };

  function formatBytes(bytes) {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  }

  function extensionOf(name) {
    const idx = name.lastIndexOf(".");
    return idx === -1 ? "" : name.slice(idx).toLowerCase();
  }

  function show(el) {
    el.hidden = false;
  }
  function hide(el) {
    el.hidden = true;
  }

  function setFileError(message) {
    if (!message) {
      hide(els.fileError);
      els.fileError.textContent = "";
      return;
    }
    els.fileError.textContent = message;
    show(els.fileError);
  }

  function renderDocument() {
    if (!state.file) {
      hide(els.docCard);
      els.docThumb.src = "";
      els.docName.textContent = "";
      els.docSize.textContent = "";
      return;
    }
    els.docName.textContent = state.file.name;
    els.docSize.textContent = formatBytes(state.file.size);
    if (state.previewUrl) {
      els.docThumb.src = state.previewUrl;
    }
    show(els.docCard);
  }

  function validateFile(file) {
    const ext = extensionOf(file.name);
    if (!ACCEPTED_EXTENSIONS.includes(ext)) {
      return `El formato ${ext || "desconocido"} no está admitido. Usa JPG, PNG o WEBP.`;
    }
    if (file.size > MAX_BYTES) {
      return `El archivo pesa ${formatBytes(file.size)} y el máximo es 10 MB. Reduce la imagen o elige otra.`;
    }
    return "";
  }

  function setFile(file) {
    const error = validateFile(file);
    if (error) {
      setFileError(error);
      return;
    }
    setFileError("");
    if (state.previewUrl) URL.revokeObjectURL(state.previewUrl);
    state.file = file;
    state.previewUrl = URL.createObjectURL(file);
    renderDocument();
    updateExtract();
  }

  function clearFile() {
    state.nextOpId += 1;
    state.op = null;
    state.file = null;
    state.result = null;
    if (state.previewUrl) {
      URL.revokeObjectURL(state.previewUrl);
      state.previewUrl = null;
    }
    els.fileInput.value = "";
    setFileError("");
    renderDocument();
    hide(els.opProgress);
    hide(els.opError);
    hide(els.resultSection);
    updateExtract();
  }

  function escapeHtml(value) {
    const div = document.createElement("div");
    div.textContent = String(value ?? "");
    return div.innerHTML;
  }

  function modelPanelHtml() {
    const m = state.model;
    if (m.phase === "ready") return "";
    if (m.phase === "loading") {
      return `
        <div class="space-y-2">
          <div class="h-3 w-full rounded-full bg-slate-200 overflow-hidden">
            <div id="downloadBar" class="h-full bg-indigo-600 transition-all" style="width:${Number(m.percent) || 0}%"></div>
          </div>
          <p id="downloadText">${escapeHtml(m.percent)}% — ${escapeHtml(m.message || "Preparando el modelo…")}</p>
          <p class="text-slate-500">La primera preparación puede tardar varios minutos. Puedes probar el modo demo mientras tanto.</p>
        </div>`;
    }
    if (m.phase === "error") {
      return `
        <p>El modelo no pudo prepararse en el servidor.</p>
        <p class="text-slate-600">${escapeHtml(m.message || "")}</p>
        <p class="text-slate-500">Reinicia el servicio o revisa los registros del servidor para continuar.</p>`;
    }
    if (m.phase === "absent") {
      return `
        <p>El modelo aún no está instalado en el servidor. La primera preparación puede tardar varios minutos.</p>
        <button type="button" id="startDownloadBtn" class="inline-flex items-center min-h-11 px-4 rounded-md bg-indigo-600 text-white font-semibold hover:bg-indigo-700 focus-visible:outline-2 focus-visible:outline-indigo-800 focus-visible:outline-offset-2">Preparar modelo</button>`;
    }
    return '<p class="text-slate-500">Comprobando el servicio…</p>';
  }

  function renderModel() {
    const m = state.model;
    const dotColors = {
      checking: "bg-slate-400",
      ready: "bg-emerald-600",
      loading: "bg-indigo-500",
      absent: "bg-slate-400",
      error: "bg-red-600",
    };
    els.modelDot.className = `inline-block w-2.5 h-2.5 rounded-full ${dotColors[m.phase] || "bg-slate-400"}`;
    const chipTexts = {
      checking: "Comprobando el servicio…",
      ready: "Servicio listo",
      loading: `Preparando modelo (${m.percent}%)`,
      absent: "Modelo no instalado",
      error: "Modelo no disponible",
    };
    els.modelChipText.textContent = chipTexts[m.phase] || "";

    if (m.phase === "ready" || state.demo) {
      hide(els.modelPanel);
      els.modelPanelBody.innerHTML = "";
      return;
    }

    els.modelPanelBody.innerHTML = modelPanelHtml();
    show(els.modelPanel);

    const startBtn = $("startDownloadBtn");
    if (startBtn) startBtn.addEventListener("click", startDownload);

    if (m.phase === "absent" || m.phase === "loading" || m.phase === "error") {
      const wrapper = document.createElement("div");
      wrapper.className = "pt-2";
      const demoEntry = document.createElement("button");
      demoEntry.type = "button";
      demoEntry.textContent = "Probar sin modelo (modo demo)";
      demoEntry.className =
        "inline-flex items-center min-h-11 px-4 rounded-md border border-amber-400 bg-amber-50 text-amber-900 font-medium hover:bg-amber-100 focus-visible:outline-2 focus-visible:outline-amber-700 focus-visible:outline-offset-2";
      demoEntry.addEventListener("click", enterDemo);
      wrapper.appendChild(demoEntry);
      els.modelPanelBody.appendChild(wrapper);
    }
  }

  function renderDemo() {
    if (state.demo) {
      show(els.demoBadge);
    } else {
      hide(els.demoBadge);
    }
  }

  function updateExtract() {
    const busy = Boolean(state.op);
    const hasFile = Boolean(state.file);
    const modelReady = state.demo || state.model.phase === "ready";
    els.extractBtn.disabled = busy || !hasFile || !modelReady;
    if (busy) {
      els.extractHint.textContent = "Procesando el documento actual…";
    } else if (!hasFile) {
      els.extractHint.textContent = "Selecciona una imagen para comenzar.";
    } else if (!modelReady) {
      els.extractHint.textContent = state.demo
        ? ""
        : "Espera a que el modelo esté listo o activa el modo demo.";
    } else {
      els.extractHint.textContent = "";
    }
  }

  async function refreshModel() {
    try {
      const res = await fetch("/health");
      if (!res.ok) throw new Error("health");
      const data = await res.json();
      if (data.model_loaded) {
        state.model = { phase: "ready", percent: 100, message: "" };
      } else if (data.model_loading) {
        const p = data.download_progress || {};
        state.model = {
          phase: "loading",
          percent: Number(p.percent || 0),
          message: p.message || "",
        };
      } else if (data.model_error) {
        state.model = {
          phase: "error",
          percent: 0,
          message: String(data.model_error).slice(0, 140),
        };
      } else {
        state.model = { phase: "absent", percent: 0, message: "" };
      }
    } catch {
      state.model = {
        phase: "error",
        percent: 0,
        message: "No se pudo conectar con el servicio.",
      };
    }
    renderModel();
    updateExtract();
  }

  function pollDownloadProgress() {
    if (state.downloading) return;
    state.downloading = true;
    const timer = setInterval(async () => {
      try {
        const res = await fetch("/api/download-progress");
        if (!res.ok) throw new Error("progress");
        const data = await res.json();
        const p = data.progress || {};
        if (p.status === "completed" || data.model_loaded) {
          clearInterval(timer);
          state.downloading = false;
          await refreshModel();
          return;
        }
        if (p.status === "error") {
          clearInterval(timer);
          state.downloading = false;
          state.model = {
            phase: "error",
            percent: 0,
            message: p.message || "",
          };
          renderModel();
          updateExtract();
          return;
        }
        state.model = {
          phase: "loading",
          percent: Number(p.percent || 0),
          message: p.message || "",
        };
        renderModel();
      } catch {
        clearInterval(timer);
        state.downloading = false;
        await refreshModel();
      }
    }, 2000);
  }

  async function startDownload() {
    try {
      const res = await fetch("/api/download-model", { method: "POST" });
      if (!res.ok) throw new Error("download");
      pollDownloadProgress();
    } catch {
      state.model = {
        phase: "error",
        percent: 0,
        message: "No se pudo iniciar la preparación del modelo.",
      };
      renderModel();
    }
  }

  function enterDemo() {
    state.demo = true;
    renderDemo();
    renderModel();
    updateExtract();
  }

  function exitDemo() {
    state.demo = false;
    renderDemo();
    renderModel();
    updateExtract();
  }

  function demoResultText(op) {
    return [
      "Esto es una simulación de extracción.",
      "",
      `Archivo: ${op.file.name}`,
      `Tipo de extracción: ${MODE_LABELS[op.mode] || op.mode}`,
      "",
      "Para obtener el texto real de tu documento, prepara el modelo y procesa de nuevo.",
    ].join("\n");
  }

  function canExtract() {
    return (
      Boolean(state.file) &&
      !state.op &&
      (state.demo || state.model.phase === "ready")
    );
  }

  function extract() {
    if (!canExtract()) return;
    els.extractBtn.disabled = true;
    setFileError("");

    const op = {
      id: state.nextOpId++,
      file: state.file,
      mode: els.modeSelect.value,
      prompt: els.promptInput.value.trim(),
      kind: state.demo ? "demo" : "real",
    };
    state.op = op;
    state.result = null;

    hide(els.resultSection);
    hide(els.opError);
    hide(els.emptyResult);
    show(els.opProgress);
    els.opProgressText.textContent = "Extrayendo texto…";
    updateExtract();

    if (op.kind === "demo") {
      runDemo(op);
    } else {
      runReal(op);
    }
  }

  function runDemo(op) {
    setTimeout(() => {
      if (!state.op || state.op.id !== op.id) return;
      finish(op, {
        text: demoResultText(op),
        simulated: true,
        mode: op.mode,
        time: null,
        size: null,
        fileName: op.file.name,
      });
    }, 1200);
  }

  async function readErrorMessage(res) {
    let detail = "";
    try {
      const raw = await res.text();
      try {
        const data = JSON.parse(raw);
        detail = data.detail || data.message || "";
      } catch {
        detail = raw.slice(0, 140);
      }
    } catch {
      detail = "";
    }
    if (res.status === 413) {
      return "El servidor rechazó el archivo por tamaño. Reduce la imagen e inténtalo de nuevo.";
    }
    if (res.status === 400) {
      return (
        detail ||
        "El servidor no aceptó el documento. Verifica el formato e inténtalo de nuevo."
      );
    }
    if (res.status === 503) {
      return "El modelo no está disponible en el servidor. Espera a que termine de prepararse o revisa el servicio.";
    }
    return (
      detail ||
      `Error del servidor (${res.status}). Inténtalo de nuevo en unos momentos.`
    );
  }

  async function runReal(op) {
    try {
      const formData = new FormData();
      formData.append("file", op.file, op.file.name);
      formData.append("mode", op.mode);
      if (op.prompt) formData.append("custom_prompt", op.prompt);

      const res = await fetch("/api/ocr", { method: "POST", body: formData });
      if (!state.op || state.op.id !== op.id) return;
      if (!res.ok) {
        throw new Error(await readErrorMessage(res));
      }
      const data = await res.json();
      if (!state.op || state.op.id !== op.id) return;

      finish(op, {
        text: typeof data.text === "string" ? data.text : "",
        simulated: false,
        mode: data.mode || op.mode,
        time: data.processing_time,
        size: data.image_size,
        fileName: op.file.name,
      });
    } catch (err) {
      if (!state.op || state.op.id !== op.id) return;
      failOp(
        err.message ||
          "No se pudo completar la extracción. Inténtalo de nuevo.",
      );
    }
  }

  function modeLabel(mode) {
    return MODE_LABELS[mode] || mode;
  }

  function finish(op, result) {
    state.op = null;
    state.result = result;

    hide(els.opProgress);
    hide(els.opError);
    show(els.resultSection);

    if (result.simulated) {
      show(els.demoResultBanner);
    } else {
      hide(els.demoResultBanner);
    }

    els.resultThumb.src = state.previewUrl || "";
    els.resultFileName.textContent = result.fileName;
    els.resultMode.textContent = modeLabel(result.mode);
    els.resultTime.textContent = result.time != null ? `${result.time} s` : "—";
    els.resultImageSize.textContent = Array.isArray(result.size)
      ? `${result.size[0]} × ${result.size[1]}`
      : "—";

    if (!result.text.trim()) {
      hide(els.resultGrid);
      show(els.emptyResult);
      els.resultText.textContent = "";
    } else {
      hide(els.emptyResult);
      show(els.resultGrid);
      els.resultText.textContent = result.text;
    }

    els.copyFeedback.textContent = "";
    els.resultTitle.focus();
    updateExtract();
  }

  function failOp(message) {
    state.op = null;
    hide(els.opProgress);
    els.opErrorMessage.textContent = message;
    show(els.opError);
    els.opErrorTitle.focus();
    updateExtract();
  }

  async function copyResult() {
    if (!state.result || !state.result.text) return;
    const text = state.result.text;
    try {
      await navigator.clipboard.writeText(text);
      els.copyFeedback.textContent = "Texto copiado.";
    } catch {
      try {
        const ta = document.createElement("textarea");
        ta.value = text;
        ta.style.position = "fixed";
        ta.style.opacity = "0";
        document.body.appendChild(ta);
        ta.select();
        document.execCommand("copy");
        document.body.removeChild(ta);
        els.copyFeedback.textContent = "Texto copiado.";
      } catch {
        els.copyFeedback.textContent =
          "No se pudo copiar automáticamente. Selecciona el texto y cópialo manualmente.";
      }
    }
  }

  function downloadResult() {
    if (!state.result || !state.result.text) return;
    const blob = new Blob([state.result.text], {
      type: "text/plain;charset=utf-8",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    const stamp = new Date().toISOString().replace(/[:.]/g, "-").slice(0, 19);
    a.href = url;
    a.download = `texto-extraido-${stamp}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  function resetAll() {
    clearFile();
    state.result = null;
    hide(els.resultSection);
    hide(els.opError);
    els.fileInput.focus();
  }

  function adjustOptions() {
    els.advanced.open = true;
    els.modeSelect.focus();
  }

  function setupEventListeners() {
    els.fileInput.addEventListener("change", () => {
      const file = els.fileInput.files && els.fileInput.files[0];
      if (file) setFile(file);
    });

    els.clearFileBtn.addEventListener("click", clearFile);
    els.newDocBtn.addEventListener("click", resetAll);
    els.emptyNewDocBtn.addEventListener("click", resetAll);
    els.emptyAdjustBtn.addEventListener("click", adjustOptions);
    els.retryBtn.addEventListener("click", () => {
      hide(els.opError);
      extract();
    });
    els.errorResetBtn.addEventListener("click", resetAll);
    els.copyBtn.addEventListener("click", copyResult);
    els.downloadBtn.addEventListener("click", downloadResult);
    els.exitDemoBtn.addEventListener("click", exitDemo);

    els.form.addEventListener("submit", (e) => {
      e.preventDefault();
      extract();
    });

    const zone = els.uploadFieldset;
    zone.addEventListener("dragover", (e) => {
      e.preventDefault();
      zone.classList.add("border-indigo-600");
    });
    zone.addEventListener("dragleave", () => {
      zone.classList.remove("border-indigo-600");
    });
    zone.addEventListener("drop", (e) => {
      e.preventDefault();
      zone.classList.remove("border-indigo-600");
      const file =
        e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0];
      if (file) setFile(file);
    });
  }

  function init() {
    setupEventListeners();
    renderDemo();
    refreshModel();
    setInterval(refreshModel, 10000);
  }

  init();
})();
