# Family mobile prototype v0.6

> **English translation:** [Spanish source](README.md) is normative for v0.x. This translation preserves requirement IDs, decisions, document status, and uncertainty; it does not approve or supersede the source.


. This device converts the product decisions, the editorial content of ACT-0001 and the previous visual study into an interactive mobile journey aimed at the adult. The v0.6 review retains the navigable weekly plan and the consolidated purchase of v0.5 and adds an installable PWA: caches the interface and preserves locally purchases, preparation and point of activity for dry run from a cell phone.

- `index.html`: editable prototype.
- `prototype-standalone.html`: interactive copy in one file.
- `manifest.webmanifest`, `icon.svg` and `sw.js`: installation, identity and cache offline of the prototype served by HTTPS.
- `vercel.json`: Minimum safety and delivery heads of the service worker.
- `.github/workflows/deploy-founder-pilot-pages.yml`: publishes only static shell files in GitHub Pages; does not display editorial documents or QA captures within the site.
- `design-system.html`: Editable specimen of Pocket Workshop.
- `standalone.html`: visual system in a single file.
- `research/`: contraa of the artifact and evidence.
- `design/`: visual system decisions.
- `handoff/`: limits and implementation guide.

The complete family content is synthetic. `ACT-0001@0.3.0` is Draft and appears only as a preview to validate the experience. Persistence is local to the browser: there is no account, backend, application encryption or synchronization between devices. Temporary deployment should not receive photos, voice or sensitive child information.

## Founder pilot web access

- Application: [https://pr3t3l.github.io/KidsApp/](https://pr3t3l.github.io/KidsApp/)
- Code: [https://github.com/pr3t3l/KidsApp](https://github.com/pr3t3l/KidsApp)

GitHub Pages is automatically updated from `main` with a closed list of static files. The URL is public and has no authentication; it is used only for the founder's test with current content and fixes. Before inviting external families you must migrate to hosting privado/autenticado.
