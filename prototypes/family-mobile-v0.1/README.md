# Family Mobile Founder-Pilot Prototype

> **Normative documentation language:** English from 18 August 2026 under `DEC-052`. The [Spanish historical README](../../historical/es/prototypes/family-mobile-v0.1/README.es.md) is retained for traceability.

## Purpose

This static prototype validates the adult-facing family journey before production implementation. It covers a five-day founder dry run: planning by available time, opening every planned activity, consolidated shopping, preparation, learning focuses, staged activity facilitation, contextual help, close-out, installation, and offline shell behavior.

It is not the production app. It uses synthetic learner data, local browser persistence, and `Draft` or candidate activity content. It has no account, backend, cross-device synchronization, server-side encryption, payments, community, or real learner-record storage.

## Safety and privacy boundary

The public deployment is only for the founder's controlled test. Do not enter real child photos, voice, sensitive observations, payment information, or private family data. Before external pilot families are invited, the experience must move to authenticated hosting backed by the authorization, retention, and deletion controls defined in the canonical specifications.

## Main files

| File | Purpose |
|---|---|
| `index.html` | Editable application shell |
| `app.js` | Prototype state, screens, interactions, and Spanish source copy |
| `i18n.js` | Complete `en-US` runtime bundle and locale switching |
| `styles.css` | Responsive visual system |
| `prototype-standalone.html` | Generated single-file copy of the interactive prototype |
| `manifest.en.webmanifest` | English install metadata |
| `manifest.es.webmanifest` | Spanish install metadata |
| `sw.js` | Bilingual application-shell cache |
| `design-system.html` | Editable Pocket Workshop visual specimen |
| `standalone.html` | Generated single-file visual-system specimen |
| `qa/` | Smoke tests, PWA tests, capture scripts, and reviewed screenshots |
| `research/evidence.json` | Structured prototype evidence and unresolved observations |
| `vercel.json` | Static-hosting headers prepared for a possible Vercel deployment |

## Run locally

Serve the directory over HTTP rather than opening `file://` when testing installation or the service worker. For example:

```powershell
npx http-server "prototypes/family-mobile-v0.1" -p 4173 -c-1
```

Then open `http://localhost:4173/?lang=en` or `http://localhost:4173/?lang=es`.

## Quality checks

With the prototype served over HTTP(S) and a Chromium browser available for remote debugging:

```powershell
node prototypes/family-mobile-v0.1/qa/flow-smoke.mjs http://localhost:4173
node prototypes/family-mobile-v0.1/qa/i18n-smoke.mjs http://localhost:4173
node prototypes/family-mobile-v0.1/qa/pwa-smoke.mjs http://localhost:4173 en
node prototypes/family-mobile-v0.1/qa/pwa-smoke.mjs http://localhost:4173 es
```

The i18n smoke test traverses all five activities, the complete Paper Bridges flow, help, close-out, Journey, and installation in both languages. English mode fails when known residual Spanish copy appears.

## Deployment

- Founder-pilot app: [https://pr3t3l.github.io/KidsApp/](https://pr3t3l.github.io/KidsApp/)
- Spanish: [https://pr3t3l.github.io/KidsApp/?lang=es](https://pr3t3l.github.io/KidsApp/?lang=es)
- English: [https://pr3t3l.github.io/KidsApp/?lang=en](https://pr3t3l.github.io/KidsApp/?lang=en)
- Repository: [https://github.com/pr3t3l/KidsApp](https://github.com/pr3t3l/KidsApp)

GitHub Pages deploys a closed list of static prototype assets from `main`. The public URL is unauthenticated and must remain fixture-only.

## Relationship to production

The prototype validates interaction and content presentation. Production behavior must be implemented through the [backend handoff](../../docs/BACKEND-HANDOFF.md), [specification map](../../docs/SPECIFICATION-MAP.md), machine-readable schemas, authorization policies, and vertical slices. Prototype state and fixture data are not production persistence contracts.
