const learners = [
  { id: "sofi", name: "Sofi", initials: "SO", age: "5–6 años", color: "cyan" },
  { id: "mateo", name: "Mateo", initials: "MA", age: "7–8 años", color: "yellow" },
  { id: "leo", name: "Leo", initials: "LE", age: "9–10 años", color: "coral" }
];

const roles = {
  designer: {
    title: "Diseñadora y constructora",
    objective: "Seguir una secuencia de plegado y explicar una decisión.",
    contribution: "Propone la forma del papel y construye el primer modelo.",
    exposure: "formas, estructura, comparación"
  },
  tester: {
    title: "Probador de cargas",
    objective: "Añadir y contar una carga a la vez con una regla estable.",
    contribution: "Prueba cada puente y anuncia el resultado de cada intento.",
    exposure: "conteo, predicción, evidencia"
  },
  coordinator: {
    title: "Coordinador del experimento",
    objective: "Mantener constantes los apoyos y registrar lo que cambia.",
    contribution: "Ayuda a que la comparación sea justa y resume hallazgos.",
    exposure: "medición, control de variables, comunicación"
  }
};

const stages = [
  {
    name: "Descubrir", time: "4 min", eyebrow: "Miren antes de construir",
    title: "¿Por qué una hoja plana se dobla?",
    copy: "Sostengan una hoja entre dos apoyos. Presionen suavemente el centro y describan qué observan.",
    prompt: "Pregunta al grupo: ¿qué tendría que cambiar para que resista más?",
    warning: "Todavía no coloquen objetos pesados. Esta primera prueba se hace solo con un dedo.",
    help: "Si la hoja no se dobla, separen un poco más los apoyos. Mantengan la misma distancia para todas las pruebas."
  },
  {
    name: "Imaginar", time: "4 min", eyebrow: "Una idea por turno",
    title: "Elijan una forma para probar",
    copy: "Comparen un canal, un acordeón o varios pliegues anchos. No hay una respuesta correcta antes de experimentar.",
    prompt: "Cada niño puede proponer; la persona constructora elige la primera forma con ayuda del grupo.",
    warning: "El adulto conserva los bordes de los apoyos alineados y revisa que la superficie sea estable.",
    help: "Si no saben cuál elegir, comiencen con un acordeón de pliegues anchos. Luego cambien una sola cosa."
  },
  {
    name: "Construir", time: "6 min", eyebrow: "Manos compartidas",
    title: "Transformen la hoja",
    copy: "Doblen con cuidado y coloquen el papel sobre los dos apoyos. Una hoja plana será el modelo de comparación.",
    prompt: "El adulto puede ayudar a marcar los pliegues; esa ayuda no reduce el valor del aprendizaje.",
    warning: "Usen papel común, no cartón rígido ni objetos cortantes. Mantengan despejado el borde de la mesa.",
    help: "Si el puente queda inclinado, igualen la altura de los apoyos y vuelvan a centrar la hoja."
  },
  {
    name: "Experimentar", time: "10 min", eyebrow: "Una carga a la vez",
    title: "Prueben con una regla justa",
    copy: "El adulto centra el vaso liviano. El probador añade una carga, cuenta y espera antes de colocar la siguiente.",
    prompt: "Comparen el puente plano y el plegado sin cambiar los apoyos ni el tipo de carga.",
    warning: "Deténganse si un apoyo se mueve, el vaso se inclina o el puente cae. Reorganicen antes de continuar.",
    help: "Un colapso no es un error: retiren las cargas, registren el último número estable y reinicien desde cero."
  },
  {
    name: "Mejorar", time: "8 min", eyebrow: "Cambien una variable",
    title: "Hagan un segundo intento",
    copy: "Elijan solo un cambio: número de pliegues, ancho de los pliegues o posición del puente.",
    prompt: "Antes de probar, cada persona dice qué cree que ocurrirá y por qué.",
    warning: "No cambien el tamaño o peso de las cargas durante la comparación.",
    help: "Si ambas versiones resisten igual, aumenten gradualmente la distancia entre apoyos y repitan."
  },
  {
    name: "Explicar", time: "5 min", eyebrow: "Lo que sabemos ahora",
    title: "Cuenten la historia de la prueba",
    copy: "¿Qué diseño funcionó mejor? Usen una observación concreta: forma, número de cargas o estabilidad.",
    prompt: "Una conclusión útil puede empezar así: «Vimos que…» o «La próxima vez probaríamos…».",
    warning: "No conviertan el resultado en una competencia entre niños. El equipo probó ideas, no personas.",
    help: "Si cuesta explicarlo, comparen dos fotos mentales: cómo se veía antes de doblarse y justo antes de caer."
  }
];

const ratingScale = [
  { value: 1, label: "Todavía no", detail: "No pudo hacerlo esta vez" },
  { value: 2, label: "Mucha ayuda", detail: "Necesitó guía continua" },
  { value: 3, label: "Alguna ayuda", detail: "Lo hizo con recordatorios" },
  { value: 4, label: "Casi solo", detail: "Solo necesitó una pista" },
  { value: 5, label: "Solo y seguro", detail: "Lo hizo con independencia" }
];

const state = {
  screen: "today",
  time: 45,
  selected: ["sofi", "mateo", "leo"],
  assignments: { sofi: "designer", mateo: "tester", leo: "coordinator" },
  participation: { sofi: "active", mateo: "active", leo: "active" },
  materials: { paper: true, supports: true, crayons: true, cup: false, surface: false },
  stage: 0,
  highestStage: 0,
  offline: false,
  paused: false,
  ratings: {},
  skipped: {},
  note: "",
  roleChanges: [],
  closeStartedAt: null,
  savedElapsed: null
};

const requestedPreview = new URLSearchParams(window.location.search).get("screen");
if (["today", "roles", "prep", "session", "close", "summary", "saved", "plan", "journey", "family"].includes(requestedPreview)) {
  state.screen = requestedPreview;
  if (requestedPreview === "close") state.closeStartedAt = Date.now();
}

const view = document.querySelector("#view");
const app = document.querySelector("#app");
const appHeader = document.querySelector("#appHeader");
const bottomNav = document.querySelector("#bottomNav");
const sheet = document.querySelector("#sheet");
const sheetContent = document.querySelector("#sheetContent");
const scrim = document.querySelector("#scrim");
const toast = document.querySelector("#toast");
const connectionText = document.querySelector("#connectionText");
let lastFocus = null;
let toastTimer = null;
let closeTimer = null;

const icon = (name) => `<svg aria-hidden="true"><use href="#i-${name}"></use></svg>`;
const learnerById = (id) => learners.find((learner) => learner.id === id);
const activeLearners = () => state.selected.map(learnerById).filter(Boolean);
const evaluableLearners = () => activeLearners().filter((learner) => state.participation[learner.id] === "active");
const roleFor = (id) => roles[state.assignments[id]];
const isTopLevel = () => ["today", "plan", "journey", "family"].includes(state.screen);

function avatar(learner) {
  return `<span class="avatar" data-color="${learner.color}" aria-hidden="true">${learner.initials}</span>`;
}

function flowHeader(title, subtitle, backTarget, action = "") {
  return `<header class="flow-header">
    <button data-action="navigate" data-target="${backTarget}" aria-label="Volver">${icon("back")}</button>
    <div><h1>${title}</h1><small>${subtitle}</small></div>
    ${action || "<span></span>"}
  </header>`;
}

function setScreen(screen, options = {}) {
  state.screen = screen;
  if (screen === "close" && !state.closeStartedAt) state.closeStartedAt = Date.now();
  closeSheet();
  render();
  if (!options.preserveScroll) view.scrollTop = 0;
  requestAnimationFrame(() => view.focus({ preventScroll: true }));
}

function render() {
  const topLevel = isTopLevel();
  appHeader.hidden = !topLevel;
  bottomNav.hidden = !topLevel;
  view.classList.toggle("no-bottom", !topLevel);
  app.classList.toggle("is-offline", state.offline);
  connectionText.textContent = state.offline ? "Sin conexión" : "En línea";
  [...bottomNav.querySelectorAll("button")].forEach((button) => button.classList.toggle("is-active", button.dataset.target === state.screen));

  const renderers = {
    today: renderToday,
    plan: renderPlan,
    journey: renderJourney,
    family: renderFamily,
    roles: renderRoles,
    prep: renderPrep,
    session: renderSession,
    close: renderClose,
    summary: renderSummary,
    saved: renderSaved
  };
  view.innerHTML = (renderers[state.screen] || renderToday)();
  if (state.screen === "close") startCloseTimer(); else stopCloseTimer();
}

function renderToday() {
  const ready = state.selected.length > 0;
  return `<section class="screen">
    <p class="eyebrow">Domingo · prueba familiar</p>
    <h1>Una tarde para<br>pensar <span style="color:#0b8394">juntos.</span></h1>
    <p class="lead">Elige cuánto tiempo tienen. La actividad se adapta al grupo antes de empezar.</p>

    ${state.offline ? `<div class="offline-banner" style="margin-top:18px">${icon("signal")}<span>El paquete de esta actividad está descargado. Puedes completar la sesión y sincronizar después.</span></div>` : ""}

    <div class="section-head"><h2>Tiempo disponible</h2><span class="caption">incluye cierre</span></div>
    <div class="choice-row" aria-label="Tiempo disponible">
      ${[30, 45, 60].map((minutes) => `<button class="choice ${state.time === minutes ? "is-selected" : ""}" data-action="select-time" data-value="${minutes}">${minutes} min<small>${minutes === 30 ? "versión breve" : minutes === 45 ? "recomendado" : "con extensión"}</small></button>`).join("")}
    </div>

    <div class="section-head"><h2>¿Quiénes participan?</h2><span class="caption">1–4 en producto · 3 en demo</span></div>
    <div class="participant-grid">
      ${learners.map((learner) => `<button class="participant ${state.selected.includes(learner.id) ? "is-selected" : ""}" data-action="toggle-participant" data-id="${learner.id}" aria-pressed="${state.selected.includes(learner.id)}">
        <span class="participant-check">${state.selected.includes(learner.id) ? "✓" : ""}</span>${avatar(learner)}<strong>${learner.name}</strong><small>${learner.age}</small>
      </button>`).join("")}
    </div>

    <div class="section-head"><h2>Actividad sugerida</h2><span class="tag coral">Vista previa · Draft</span></div>
    <article class="hero">
      <div><span class="tag yellow">ACT-0001 · v0.2.2</span><h2>Puentes<br>de <span>papel</span></h2><p>Transformar una hoja, probarla y mejorar el diseño usando materiales cotidianos.</p></div>
      <div class="hero-meta"><div><strong>${state.time}</strong><small>minutos</small></div><div><strong>${state.selected.length}</strong><small>participantes</small></div><div><strong>A</strong><small>riesgo bajo</small></div></div>
    </article>
    <p class="caption" style="margin:10px 2px 0">Este prototipo usa una actividad Draft para validar la experiencia. Una familia real solo recibiría contenido publicado.</p>

    <div class="action-dock"><button class="button primary block" data-action="navigate" data-target="roles" ${ready ? "" : "disabled"}>Revisar el plan ${icon("arrow")}</button></div>
  </section>`;
}

function renderRoles() {
  return `<section class="screen">
    ${flowHeader("Plan del equipo", `${activeLearners().length} participantes · ${state.time} min`, "today")}
    <p class="eyebrow">Roles flexibles</p>
    <h2>Cada quien aporta de una forma distinta.</h2>
    <p class="lead">Estos roles ayudan a organizarse; no son etiquetas. Pueden cambiarlos, compartirlos o solo observar.</p>
    <div class="stack" style="margin-top:18px">
      ${activeLearners().map((learner) => {
        const observing = state.participation[learner.id] === "observer";
        const role = roleFor(learner.id);
        return `<article class="card role-card" data-color="${learner.color}">
          <div class="role-head">${avatar(learner)}<div><strong>${learner.name}</strong><small>${observing ? "Participará observando" : "Objetivo principal de hoy"}</small></div><button class="inline-button" data-action="edit-role" data-id="${learner.id}" aria-label="Cambiar rol de ${learner.name}">${icon("swap")}</button></div>
          <p class="role-title">${observing ? "Observador/a del equipo" : role.title}</p>
          <p class="objective">${observing ? "Mira, pregunta y puede entrar o salir cuando quiera. No se pedirá una valoración final." : role.objective}</p>
          <p class="role-contribution"><strong>${observing ? "Registro:" : "Aporte al equipo:"}</strong> ${observing ? "No se infiere habilidad, dificultad ni exposición por solo observar." : role.contribution}</p>
        </article>`;
      }).join("")}
    </div>
    <article class="card cyan principle-note" style="margin-top:14px"><b>↔</b><div><strong>El rol es una invitación.</strong><p>Si alguien pierde interés o prefiere otra tarea, el adulto puede cambiarlo durante la actividad.</p></div></article>
    <div class="action-dock"><button class="button primary block" data-action="navigate" data-target="prep">Ver preparación ${icon("arrow")}</button></div>
  </section>`;
}

function renderPrep() {
  const entries = [
    ["paper", "6 hojas de papel carta común"],
    ["supports", "2 apoyos iguales (libros o cajas estables)"],
    ["crayons", "8–15 crayones iguales como cargas"],
    ["cup", "1 vaso plástico liviano para contener las cargas"],
    ["surface", "Mesa despejada y seca, lejos del borde"]
  ];
  const checked = entries.filter(([id]) => state.materials[id]).length;
  const ready = checked === entries.length;
  return `<section class="screen">
    ${flowHeader("Preparación", `${checked} de ${entries.length} listos`, "roles")}
    <p class="eyebrow">2–4 minutos del adulto</p><h2>Deja el espacio listo.</h2>
    <p class="lead">Los niños pueden ayudar a reunir y contar. El adulto comprueba la estabilidad de la mesa y los apoyos.</p>
    <div class="progress-meter" style="margin:18px 0 10px"><i style="width:${checked / entries.length * 100}%"></i></div>
    <article class="card"><ul class="checklist">
      ${entries.map(([id, label]) => `<li><label class="check-label"><input type="checkbox" data-action="material" data-id="${id}" ${state.materials[id] ? "checked" : ""}><span class="check-box"></span><span>${label}</span></label></li>`).join("")}
    </ul></article>

    <div class="section-head"><h2>Guía de estructuras</h2><span class="tag cyan">para acompañar</span></div>
    <article class="card">
      <p style="margin:0;font-size:12px;line-height:1.5">Doblar el papel cambia su forma y puede hacerlo más rígido. Invita a probar; no construyas la respuesta por el niño.</p>
      <div class="guide-options">
        <div class="guide-option"><div class="shape channel"></div><strong>Canal</strong><br>Bordes levantados.</div>
        <div class="guide-option"><div class="shape accordion"><i></i><i></i><i></i><i></i></div><strong>Acordeón</strong><br>Varios pliegues.</div>
        <div class="guide-option"><div class="shape wide"><i></i><i></i><i></i></div><strong>Pliegues anchos</strong><br>Pocas crestas.</div>
        <div class="guide-option"><div class="shape guide"></div><strong>Una variable</strong><br>Cambiar de a una.</div>
      </div>
    </article>
    <article class="safety-card" style="margin-top:12px"><b>${icon("alert")}</b><div><strong>Control del adulto</strong><p>El adulto coloca y retira el vaso, estabiliza los apoyos y detiene la prueba si algo se inclina.</p></div></article>
    <div class="action-dock"><button class="button primary block" data-action="start-session" ${ready ? "" : "disabled"}>Empezar actividad ${icon("play")}</button></div>
  </section>`;
}

function renderSession() {
  const stage = stages[state.stage];
  const learner = activeLearners().find((person) => state.participation[person.id] === "active" && state.assignments[person.id] === ["designer", "designer", "designer", "tester", "coordinator", "coordinator"][state.stage]) || evaluableLearners()[0] || activeLearners()[0];
  return `<section class="screen">
    ${flowHeader("Puentes de papel", `${state.stage + 1} de ${stages.length} · ${stage.name}`, "prep", `<button data-action="pause" aria-label="Pausar">${icon(state.paused ? "play" : "pause")}</button>`)}
    ${state.offline ? `<div class="offline-banner">${icon("signal")}<span>Modo sin conexión. Instrucciones y ayuda están disponibles; el cierre se sincronizará después.</span></div>` : ""}
    <div class="step-progress">${stages.map((_, index) => `<i class="${index < state.stage ? "done" : index === state.stage ? "current" : ""}"></i>`).join("")}</div>
    <div class="stage-track" aria-label="Etapas de la actividad">
      ${stages.map((item, index) => `<button class="stage-button ${index === state.stage ? "is-current" : ""}" data-action="stage" data-value="${index}"><strong>${index + 1}. ${item.name}</strong><small>${item.time}</small></button>`).join("")}
    </div>
    <article class="card instruction-card">
      <div class="blueprint"><div class="bridge-diagram"><div class="support"></div><div class="paper-bridge"><i></i><i></i><i></i><i></i><i></i></div><div class="support"></div></div></div>
      <div class="instruction-copy"><p class="eyebrow">${stage.eyebrow}</p><h2>${stage.title}</h2><p class="lead">${stage.copy}</p></div>
    </article>
    ${learner ? `<article class="card actor-card" style="margin-top:12px">${avatar(learner)}<div><strong>${learner.name} puede liderar este paso</strong><small>${stage.prompt}</small></div><button class="inline-button" data-action="change-during" data-id="${learner.id}" aria-label="Cambiar quién lidera">${icon("swap")}</button></article>` : ""}
    <article class="safety-card" style="margin-top:12px"><b>${icon("alert")}</b><div><strong>Durante este paso</strong><p>${stage.warning}</p></div></article>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:12px">
      <button class="button secondary" data-action="help">${icon("help")} Necesito ayuda</button>
      <button class="button secondary" data-action="adapt">Ajustar ritmo</button>
    </div>
    <div class="action-dock" style="display:grid;grid-template-columns:${state.stage > 0 ? "54px 1fr" : "1fr"};gap:8px">
      ${state.stage > 0 ? `<button class="button secondary" data-action="previous-stage" aria-label="Paso anterior">${icon("back")}</button>` : ""}
      <button class="button primary block" data-action="next-stage">${state.stage === stages.length - 1 ? "Cerrar actividad" : `Siguiente: ${stages[state.stage + 1].name}`} ${icon("arrow")}</button>
    </div>
  </section>`;
}

function renderClose() {
  const complete = evaluableLearners().every((learner) => state.ratings[learner.id] || state.skipped[learner.id]);
  return `<section class="screen">
    ${flowHeader("Cierre rápido", "Una observación por niño", "session", `<button data-action="close-info" aria-label="Por qué preguntamos">?</button>`)}
    <div class="close-intro"><p class="eyebrow">Objetivo principal de hoy</p><h2>¿Cuánta ayuda necesitó?</h2><p class="lead">No mide inteligencia ni califica al niño. Describe solamente lo que observaste en esta actividad.</p><p class="timer" id="closeTimer">0:00<small>tiempo de cierre · meta: menos de 20 segundos</small></p></div>
    <div class="stack">
      ${evaluableLearners().map((learner) => {
        const role = roleFor(learner.id);
        const skipped = state.skipped[learner.id];
        return `<article class="card rating-card ${skipped ? "is-skipped" : ""}">
          <div class="rating-head">${avatar(learner)}<div><strong>${learner.name}: ${role.title}</strong><small>${role.objective}</small></div></div>
          <div class="rating-options" role="group" aria-label="Independencia observada de ${learner.name}">
            ${ratingScale.map((option) => `<button class="rating-option ${state.ratings[learner.id] === option.value ? "is-selected" : ""}" data-action="rating" data-id="${learner.id}" data-value="${option.value}" aria-pressed="${state.ratings[learner.id] === option.value}"><b>${option.value}</b><span>${option.label}</span></button>`).join("")}
          </div>
          <div class="rating-exception"><span class="caption">${state.ratings[learner.id] ? ratingScale[state.ratings[learner.id] - 1].detail : skipped ? "No se guardará una conclusión" : "Elige la frase más cercana"}</span><button data-action="skip-rating" data-id="${learner.id}">${skipped ? "Sí pude observar" : "No pude observar"}</button></div>
        </article>`;
      }).join("")}
      ${activeLearners().filter((learner) => state.participation[learner.id] === "observer").map((learner) => `<article class="card cyan receipt-item">${avatar(learner)}<div><strong>${learner.name} observó hoy</strong><small>No pedimos una valoración ni inferimos desempeño.</small></div></article>`).join("")}
    </div>
    <button class="button secondary block" style="margin-top:12px" data-action="voice-note">${icon("mic")} ${state.note ? "Editar observación extra" : "Observación extra por voz o texto"}</button>
    <button class="text-button" style="width:100%;margin-top:8px" data-action="evaluate-more">Evaluar más (opcional)</button>
    <div class="action-dock"><button class="button primary block" data-action="complete-close" ${complete ? "" : "disabled"}>Ver lo que se guardará ${icon("arrow")}</button></div>
  </section>`;
}

function renderSummary() {
  return `<section class="screen">
    ${flowHeader("Antes de guardar", "Puedes corregir cualquier dato", "close")}
    <p class="eyebrow">Registro contextual</p><h2>Esto es lo que aprendimos hoy.</h2>
    <p class="lead">Se guarda la actividad, el rol real y una observación breve. No se crean etiquetas sobre los niños.</p>
    <article class="card dark" style="margin-top:18px"><div class="tag-row"><span class="tag yellow">Puentes de papel</span><span class="tag dark">ACT-0001 · Draft</span></div><h3 style="font-size:24px;margin-top:15px">${activeLearners().length} participantes · ${state.time} min</h3><p style="color:#bdc8ce;font-size:12px;line-height:1.45;margin-bottom:0">Completaron las seis etapas y compararon al menos dos estructuras.</p></article>
    <div class="section-head"><h2>Por niño</h2><span class="caption">editable</span></div>
    <article class="card">
      ${activeLearners().map((learner) => {
        if (state.participation[learner.id] === "observer") return `<div class="receipt-item"><span class="receipt-icon">${learner.initials}</span><div><strong>${learner.name} · Observó</strong><small>Sin objetivo evaluado ni exposición inferida.</small></div></div>`;
        const role = roleFor(learner.id);
        const rating = state.ratings[learner.id] ? ratingScale[state.ratings[learner.id] - 1] : null;
        return `<div class="receipt-item"><span class="receipt-icon">${learner.initials}</span><div><strong>${learner.name} · ${role.title}</strong><small>${rating ? `${rating.value}/5 · ${rating.label}. ${rating.detail}.` : "El adulto indicó que no pudo observar."}<br>Exposiciones: ${role.exposure}.</small></div></div>`;
      }).join("")}
    </article>
    ${state.note ? `<article class="card cyan" style="margin-top:12px"><p class="eyebrow">Observación extra</p><p style="margin:0;font-size:13px;line-height:1.5">“${escapeHtml(state.note)}”</p></article>` : ""}
    <article class="card mint" style="margin-top:12px"><strong>Qué hará el sistema</strong><p style="margin:6px 0 0;font-size:12px;line-height:1.5">Usará estas observaciones, junto con evidencia futura, para variar oportunidades. Una sola sesión nunca determina una conclusión fuerte.</p></article>
    <div class="action-dock"><button class="button primary block" data-action="save-session">Guardar sesión ${icon("check")}</button></div>
  </section>`;
}

function renderSaved() {
  return `<section class="screen saved-screen"><div class="saved-mark">${icon("check")}</div><p class="eyebrow">Sesión guardada</p><h1>Listo. Sigan con su tarde.</h1><p class="lead">${state.offline ? "El registro quedó protegido en este dispositivo y se sincronizará cuando vuelva la conexión." : "El registro se añadió al recorrido familiar."} El cierre tomó ${formatElapsed(state.savedElapsed || 0)}.</p><article class="card" style="text-align:left;margin-top:24px"><strong>Próxima oportunidad</strong><p style="margin:7px 0 0;font-size:12px;line-height:1.5;color:var(--muted)">La siguiente recomendación alternará roles y evitará repetir una conclusión a partir de un solo día.</p></article><button class="button primary block" style="margin-top:20px" data-action="finish">Volver a Hoy ${icon("home")}</button></section>`;
}

function renderPlan() {
  return `<section class="screen secondary-screen"><p class="eyebrow">Semana familiar</p><h1>Plan</h1><p class="lead">Organiza tiempo, no una cuota rígida de actividades.</p><div class="section-head"><h2>Esta semana</h2><span class="tag yellow">90 min</span></div><div class="stack"><article class="card mini-plan"><span class="day-chip">HOY</span><div><strong>Puentes de papel</strong><p class="caption">45 min · estructura, evidencia y mejora</p><div class="opportunity"><i style="width:55%"></i></div></div></article><article class="card mini-plan"><span class="day-chip" style="background:var(--cyan)">MIÉ</span><div><strong>Clasificar semillas</strong><p class="caption">30 min · patrones y categorías</p><div class="opportunity"><i style="width:35%;background:var(--cyan)"></i></div></div></article></div><p class="caption" style="margin-top:14px">Contenido sintético para visualizar el concepto; no representa un calendario guardado.</p></section>`;
}

function renderJourney() {
  return `<section class="screen secondary-screen"><p class="eyebrow">Observaciones, no etiquetas</p><h1>Journey</h1><p class="lead">Una vista del recorrido y de las oportunidades vividas, siempre con contexto.</p><div class="section-head"><h2>Últimas experiencias</h2><span class="caption">familia completa</span></div><article class="card"><div class="receipt-item"><span class="receipt-icon">SO</span><div><strong>Sofi · Construcción</strong><small>Tuvo oportunidades de plegar, comparar y explicar. Evidencia todavía limitada.</small></div></div><div class="receipt-item"><span class="receipt-icon">MA</span><div><strong>Mateo · Medición</strong><small>Dos observaciones recientes muestran mayor independencia; no es un diagnóstico.</small></div></div><div class="receipt-item"><span class="receipt-icon">LE</span><div><strong>Leo · Comunicación</strong><small>Una exposición registrada. Hace falta observar en otros contextos.</small></div></div></article><article class="card yellow" style="margin-top:12px"><strong>Diseño pendiente de validar</strong><p style="font-size:12px;line-height:1.5;margin-bottom:0">Esta pantalla prueba cómo comunicar incertidumbre a familias sin convertirla en un tablero de notas.</p></article></section>`;
}

function renderFamily() {
  return `<section class="screen secondary-screen"><p class="eyebrow">Cuenta del adulto</p><h1>Familia</h1><p class="lead">Perfiles mínimos para adaptar oportunidades y compartir acceso entre cuidadores.</p><div class="section-head"><h2>Niños</h2><span class="caption">datos sintéticos</span></div><div class="stack">${learners.map((learner) => `<article class="card actor-card">${avatar(learner)}<div><strong>${learner.name}</strong><small>${learner.age} · sin fecha de nacimiento completa</small></div><button class="inline-button" data-action="not-built">•••</button></article>`).join("")}</div><div class="section-head"><h2>Adultos con acceso</h2></div><article class="card"><div class="receipt-item"><span class="receipt-icon">AM</span><div><strong>Adulto principal</strong><small>Gestiona suscripción, privacidad y permisos.</small></div></div><div class="receipt-item"><span class="receipt-icon">AP</span><div><strong>Adulto invitado</strong><small>Puede planear y realizar actividades.</small></div></div></article></section>`;
}

function roleSheet(learnerId) {
  const learner = learnerById(learnerId);
  const observing = state.participation[learnerId] === "observer";
  openSheet(`<header><div><p class="eyebrow">Rol de ${learner.name}</p><h2 id="sheetTitle">¿Cómo quiere participar?</h2></div><button class="sheet-close" data-action="close-sheet" aria-label="Cerrar">${icon("close")}</button></header>
    ${Object.entries(roles).map(([id, role]) => `<button class="sheet-option ${!observing && state.assignments[learnerId] === id ? "is-current" : ""}" data-action="choose-role" data-id="${learnerId}" data-value="${id}"><span><strong>${role.title}</strong><small>${role.contribution}</small></span>${!observing && state.assignments[learnerId] === id ? "✓" : ""}</button>`).join("")}
    <button class="sheet-option ${observing ? "is-current" : ""}" data-action="choose-observer" data-id="${learnerId}"><span><strong>Hoy prefiere observar</strong><small>Puede entrar o salir; no se evaluará ni se inferirá exposición.</small></span>${observing ? "✓" : ""}</button>
    <p class="caption">Cambiar un rol actualiza el objetivo principal de esta sesión, no el perfil permanente del niño.</p>`);
}

function helpSheet() {
  const stage = stages[state.stage];
  openSheet(`<header><div><p class="eyebrow">Ayuda contextual</p><h2 id="sheetTitle">Si algo no funciona</h2></div><button class="sheet-close" data-action="close-sheet" aria-label="Cerrar">${icon("close")}</button></header><article class="card cyan"><strong>${stage.name}</strong><p style="font-size:13px;line-height:1.55;margin-bottom:0">${stage.help}</p></article><article class="safety-card" style="margin-top:12px"><b>${icon("alert")}</b><div><strong>Primero la seguridad</strong><p>Si el montaje se vuelve inestable, detengan la prueba. No hace falta completar todas las etapas.</p></div></article><button class="button primary block" style="margin-top:16px" data-action="close-sheet">Entendido</button>`);
}

function adaptSheet() {
  openSheet(`<header><div><p class="eyebrow">Adaptaciones aprobadas</p><h2 id="sheetTitle">Ajustar sin cambiar la seguridad</h2></div><button class="sheet-close" data-action="close-sheet" aria-label="Cerrar">${icon("close")}</button></header>
    <button class="sheet-option" data-action="apply-adaptation" data-value="slow"><span><strong>Ir más despacio</strong><small>Repite la instrucción y divide el paso en dos.</small></span>+</button>
    <button class="sheet-option" data-action="apply-adaptation" data-value="demonstrate"><span><strong>Mostrar una vez</strong><small>El adulto modela el gesto con otra hoja y devuelve el turno.</small></span>+</button>
    <button class="sheet-option" data-action="apply-adaptation" data-value="short"><span><strong>Terminar después de esta prueba</strong><small>Conserva la observación; no obliga a completar el ciclo.</small></span>+</button>
    <p class="caption">La IA no puede añadir materiales, cambiar cargas ni alterar controles de seguridad.</p>`);
}

function pauseSheet() {
  openSheet(`<header><div><p class="eyebrow">Actividad en pausa</p><h2 id="sheetTitle">Tómense el tiempo que necesiten.</h2></div><button class="sheet-close" data-action="close-sheet" aria-label="Cerrar">${icon("close")}</button></header><button class="button primary block" data-action="resume">${icon("play")} Continuar</button><button class="button secondary block" style="margin-top:9px" data-action="finish-early">Terminar y cerrar ahora</button><button class="button danger block" style="margin-top:9px" data-action="abandon">Salir sin guardar</button>`);
}

function noteSheet() {
  openSheet(`<header><div><p class="eyebrow">Opcional</p><h2 id="sheetTitle">Observación extra</h2></div><button class="sheet-close" data-action="close-sheet" aria-label="Cerrar">${icon("close")}</button></header><p class="caption">En el producto real, el adulto podrá dictar, revisar la transcripción y corregirla antes de guardar. Ejemplo: “Cambiaron el diseño cuando vieron que el vaso se inclinaba”.</p><textarea id="noteInput" aria-label="Observación extra">${escapeHtml(state.note)}</textarea><button class="button primary block" style="margin-top:12px" data-action="save-note">Guardar observación</button>`);
  requestAnimationFrame(() => document.querySelector("#noteInput")?.focus());
}

function openSheet(content) {
  lastFocus = document.activeElement;
  sheetContent.innerHTML = content;
  scrim.hidden = false;
  sheet.classList.add("is-open");
  sheet.setAttribute("aria-hidden", "false");
  requestAnimationFrame(() => sheet.querySelector("button, textarea")?.focus());
}

function closeSheet() {
  if (!sheet.classList.contains("is-open")) return;
  sheet.classList.remove("is-open");
  sheet.setAttribute("aria-hidden", "true");
  scrim.hidden = true;
  setTimeout(() => { sheetContent.innerHTML = ""; lastFocus?.focus?.(); }, 230);
}

function showToast(message) {
  clearTimeout(toastTimer);
  toast.textContent = message;
  toast.classList.add("is-visible");
  toastTimer = setTimeout(() => toast.classList.remove("is-visible"), 2600);
}

function formatElapsed(milliseconds) {
  const seconds = Math.max(0, Math.floor(milliseconds / 1000));
  return `${Math.floor(seconds / 60)}:${String(seconds % 60).padStart(2, "0")}`;
}

function startCloseTimer() {
  stopCloseTimer();
  const tick = () => {
    const target = document.querySelector("#closeTimer");
    if (target && state.closeStartedAt) target.firstChild.textContent = formatElapsed(Date.now() - state.closeStartedAt);
  };
  tick();
  closeTimer = setInterval(tick, 1000);
}

function stopCloseTimer() {
  if (closeTimer) clearInterval(closeTimer);
  closeTimer = null;
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"]/g, (character) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[character]);
}

document.addEventListener("click", (event) => {
  const control = event.target.closest("[data-action]");
  if (!control || control.disabled) return;
  const { action, target, id, value } = control.dataset;

  if (action === "tab" || action === "navigate") return setScreen(target);
  if (action === "home") return setScreen("today");
  if (action === "select-time") { state.time = Number(value); return render(); }
  if (action === "toggle-participant") {
    state.selected = state.selected.includes(id) ? state.selected.filter((item) => item !== id) : [...state.selected, id];
    return render();
  }
  if (action === "edit-role" || action === "change-during") return roleSheet(id);
  if (action === "choose-role") {
    const previous = state.assignments[id];
    state.assignments[id] = value;
    state.participation[id] = "active";
    if (previous !== value) state.roleChanges.push({ learnerId: id, from: previous, to: value, atStage: state.stage });
    closeSheet(); render(); showToast("Rol y objetivo actualizados para esta sesión."); return;
  }
  if (action === "choose-observer") {
    state.participation[id] = "observer";
    delete state.ratings[id];
    delete state.skipped[id];
    closeSheet(); render(); showToast("Se registrará como observador, sin evaluación."); return;
  }
  if (action === "start-session") return setScreen("session");
  if (action === "stage") { state.stage = Number(value); state.highestStage = Math.max(state.highestStage, state.stage); return render(); }
  if (action === "previous-stage") { state.stage = Math.max(0, state.stage - 1); return render(); }
  if (action === "next-stage") {
    if (state.stage === stages.length - 1) return setScreen("close");
    state.stage += 1; state.highestStage = Math.max(state.highestStage, state.stage); return render();
  }
  if (action === "help") return helpSheet();
  if (action === "adapt") return adaptSheet();
  if (action === "apply-adaptation") { closeSheet(); showToast(value === "short" ? "La sesión puede cerrarse después de este intento." : "Apoyo añadido para este paso."); return; }
  if (action === "pause") { state.paused = true; return pauseSheet(); }
  if (action === "resume") { state.paused = false; closeSheet(); return render(); }
  if (action === "finish-early") { state.paused = false; closeSheet(); return setScreen("close"); }
  if (action === "abandon") { state.paused = false; closeSheet(); return setScreen("today"); }
  if (action === "rating") { state.ratings[id] = Number(value); state.skipped[id] = false; return render(); }
  if (action === "skip-rating") { state.skipped[id] = !state.skipped[id]; delete state.ratings[id]; return render(); }
  if (action === "voice-note") return noteSheet();
  if (action === "save-note") { state.note = document.querySelector("#noteInput")?.value.trim() || ""; closeSheet(); render(); return; }
  if (action === "evaluate-more") return showToast("Flujo opcional documentado; no se abre por defecto.");
  if (action === "complete-close") { state.savedElapsed = Date.now() - state.closeStartedAt; return setScreen("summary"); }
  if (action === "save-session") return setScreen("saved");
  if (action === "finish") return setScreen("today");
  if (action === "toggle-offline") { state.offline = !state.offline; render(); showToast(state.offline ? "Paquete descargado: modo sin conexión simulado." : "Conexión restaurada: sincronización simulada."); return; }
  if (action === "close-info") return openSheet(`<header><div><p class="eyebrow">Escala de independencia</p><h2 id="sheetTitle">Describe esta ocasión, no al niño.</h2></div><button class="sheet-close" data-action="close-sheet" aria-label="Cerrar">${icon("close")}</button></header>${ratingScale.map((item) => `<div class="receipt-item"><span class="receipt-icon">${item.value}</span><div><strong>${item.label}</strong><small>${item.detail}</small></div></div>`).join("")}`);
  if (action === "not-built") return showToast("Este control está fuera del recorrido que estamos validando.");
  if (action === "close-sheet") return closeSheet();
});

document.addEventListener("change", (event) => {
  const control = event.target.closest('[data-action="material"]');
  if (!control) return;
  state.materials[control.dataset.id] = control.checked;
  render();
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") closeSheet();
});

render();
