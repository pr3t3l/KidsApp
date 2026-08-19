> **Histórico — documentación en español.** Archivado el 18 de agosto de 2026. Se conserva para trazabilidad; toda documentación y cambios nuevos deben crearse en inglés.

# Prototipo móvil familiar v0.7

Este artefacto convierte las decisiones de producto, el contenido editorial de ACT-0001 y el estudio visual previo en un recorrido móvil interactivo dirigido al adulto. La revisión v0.7 conserva la PWA instalable de v0.6 y entrega toda la interfaz, los cinco ejercicios, las seis fases del puente, compras, ayudas, seguridad, cierre e instalación en español (`es-US`) e inglés (`en-US`).

- `index.html`: prototipo editable.
- `i18n.js`: bundles de contenido y localización; español e inglés comparten IDs, estado y lógica.
- `prototype-standalone.html`: copia interactiva en un solo archivo.
- `manifest.es.webmanifest`, `manifest.en.webmanifest`, `icon.svg` y `sw.js`: instalación localizada, identidad y cache offline del prototipo servido por HTTPS.
- `vercel.json`: headers mínimos de seguridad y entrega del service worker.
- `.github/workflows/deploy-founder-pilot-pages.yml`: publica únicamente los archivos del shell estático en GitHub Pages; no expone los documentos editoriales ni las capturas de QA dentro del sitio.
- `design-system.html`: espécimen editable de Pocket Workshop.
- `standalone.html`: sistema visual en un solo archivo.
- `research/`: contrato del artefacto y evidencia.
- `design/`: decisiones del sistema visual.
- `handoff/`: límites y guía de implementación.

El contenido familiar completo es sintético. `ACT-0001@0.3.0` es Draft y aparece solo como vista previa para validar la experiencia. La persistencia es local al navegador: no hay cuenta, backend, cifrado de aplicación ni sincronización entre dispositivos. El despliegue temporal no debe recibir fotografías, voz ni información infantil sensible.

## Idioma

La app elige `es-US` o `en-US` desde `?lang=`, la preferencia guardada o el idioma del navegador, en ese orden. El botón `EN`/`ES` guarda la elección en el dispositivo. Cada idioma usa su propio manifiesto instalable. La prueba `qa/i18n-smoke.mjs` recorre las cinco actividades, las seis fases y los overlays para impedir contenido mezclado.

- Español: [https://pr3t3l.github.io/KidsApp/?lang=es](https://pr3t3l.github.io/KidsApp/?lang=es)
- English: [https://pr3t3l.github.io/KidsApp/?lang=en](https://pr3t3l.github.io/KidsApp/?lang=en)

## Acceso web del founder pilot

- Aplicación: [https://pr3t3l.github.io/KidsApp/](https://pr3t3l.github.io/KidsApp/)
- Código: [https://github.com/pr3t3l/KidsApp](https://github.com/pr3t3l/KidsApp)

GitHub Pages se actualiza automáticamente desde `main` con una lista cerrada de archivos estáticos. La URL es pública y no tiene autenticación; se usa únicamente para la prueba de la fundadora con el contenido y fixtures actuales. Antes de invitar familias externas debe migrarse a hosting privado/autenticado.
