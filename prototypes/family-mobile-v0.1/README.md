# Prototipo móvil familiar v0.6

Este artefacto convierte las decisiones de producto, el contenido editorial de ACT-0001 y el estudio visual previo en un recorrido móvil interactivo dirigido al adulto. La revisión v0.6 conserva el plan semanal navegable y la compra consolidada de v0.5 y añade una PWA instalable: cachea la interfaz y conserva localmente compras, preparación y punto de la actividad para el dry run desde un celular.

- `index.html`: prototipo editable.
- `prototype-standalone.html`: copia interactiva en un solo archivo.
- `manifest.webmanifest`, `icon.svg` y `sw.js`: instalación, identidad y cache offline del prototipo servido por HTTPS.
- `vercel.json`: headers mínimos de seguridad y entrega del service worker.
- `.github/workflows/deploy-founder-pilot-pages.yml`: publica únicamente los archivos del shell estático en GitHub Pages; no expone los documentos editoriales ni las capturas de QA dentro del sitio.
- `design-system.html`: espécimen editable de Pocket Workshop.
- `standalone.html`: sistema visual en un solo archivo.
- `research/`: contrato del artefacto y evidencia.
- `design/`: decisiones del sistema visual.
- `handoff/`: límites y guía de implementación.

El contenido familiar completo es sintético. `ACT-0001@0.3.0` es Draft y aparece solo como vista previa para validar la experiencia. La persistencia es local al navegador: no hay cuenta, backend, cifrado de aplicación ni sincronización entre dispositivos. El despliegue temporal no debe recibir fotografías, voz ni información infantil sensible.

## Acceso web del founder pilot

- Aplicación: [https://pr3t3l.github.io/KidsApp/](https://pr3t3l.github.io/KidsApp/)
- Código: [https://github.com/pr3t3l/KidsApp](https://github.com/pr3t3l/KidsApp)

GitHub Pages se actualiza automáticamente desde `main` con una lista cerrada de archivos estáticos. La URL es pública y no tiene autenticación; se usa únicamente para la prueba de la fundadora con el contenido y fixtures actuales. Antes de invitar familias externas debe migrarse a hosting privado/autenticado.
