---
name: typo3-ddev-vite
description: Integrate, maintain, or troubleshoot Vite-built SCSS and JavaScript in a TYPO3 site package running in DDEV. Use when installing or repairing praetorius/vite-asset-collector, vite-plugin-typo3, Vite, or ddev-vite-sidecar; adding a root vite.config.js; declaring Configuration/ViteEntrypoints.json; wiring a Fluid vite:asset ViewHelper; or diagnosing missing assets, manifests, dev-server loading, and SCSS compilation. Supports both bk2k/bootstrap-package and typo3/cms-fluid-styled-content; use typo3-sitepackage for the broader package structure.
license: CC-BY-4.0
compatibility: Requires a Composer-mode TYPO3 project with DDEV, a site package, and Node.js plus a supported package manager available in the DDEV web container. Dependency, DDEV add-on, configuration, source, and template changes require user authorization.
---

# TYPO3 Vite in DDEV

Set up or repair the Vite AssetCollector pipeline without coupling it to the selected content-rendering package. The pipeline belongs at the TYPO3 project root, while every participating extension owns its declared entrypoints and source files.

## 1. Discover the working shape

Use read-only checks to identify the DDEV root and status, TYPO3 version, site-package path and extension key, root `composer.json`, root `package.json`/lockfile, package manager, `vite.config.*`, `.ddev/` add-ons, and existing Vite, AssetCollector, Fluid, and asset-loading configuration. Locate the actual page layout that renders `<head>`.

- Treat `bk2k/bootstrap-package` and `typo3/cms-fluid-styled-content` as rendering choices only. The Vite configuration, entrypoint file, and AssetCollector ViewHelper integration are the same for either choice.
- Preserve a working package manager, lockfile, Vite configuration, entrypoint naming, and asset directory structure. Extend them instead of replacing them.
- Check whether legacy CSS or JavaScript is already included through TypoScript, Fluid, or the base package. Plan one deliberate ownership path for each asset so the same bundle is not emitted twice.
- If the site package, extension key, or page layout cannot be established from the project, ask for it before writing paths.

Completion: the exact root command directory, site-package path, source entrypoint, rendered layout, and the missing or broken link in the pipeline are known.

## 2. Make the mutation boundary explicit

Present the smallest required change set and obtain permission immediately before installing packages, adding the sidecar, changing lockfiles/configuration, or creating/editing site-package assets and Fluid templates. A repair begins with the evidence for the failed link rather than a broad reinstall.

Typical writes include root `composer.json` and lockfiles, root Node manifests and lockfiles, `.ddev/`, root `vite.config.js`, `Configuration/ViteEntrypoints.json`, entrypoint/SCSS/JavaScript files, built assets, and a Fluid layout. Never commit generated output, change the production deployment process, or remove an existing asset path unless the user authorizes it.

Completion: the approved change list is no larger than the identified gap.

## 3. Install the pipeline in DDEV

Run dependency commands from the discovered project root through DDEV. Use the existing package manager and retain its lockfile. For a new standard setup, install:

```bash
ddev composer require praetorius/vite-asset-collector
ddev exec npm install --save-dev vite vite-plugin-typo3 sass-embedded
```

For pnpm, Yarn, or Bun, use its equivalent development-dependency command rather than adding npm alongside it. `sass-embedded` is required for SCSS; do not add it when the package already provides a working Sass implementation. Keep Node dependencies at the project root, beside Composer dependencies, unless existing project evidence establishes a different frontend root.

Install the sidecar only when it is absent:

```bash
# DDEV 1.23.5+
ddev add-on get s2b/ddev-vite-sidecar
# Older DDEV
ddev get s2b/ddev-vite-sidecar
ddev restart
```

Completion: Composer and Node manifests/lockfiles agree with the selected packages, and `ddev vite --help` is available from the frontend root.

## 4. Configure root Vite and site-package entrypoints

Create or extend the project-root `vite.config.js`; preserve other plugins and intentional Vite settings. The minimal plugin configuration is:

```js
import { defineConfig } from "vite";
import typo3 from "vite-plugin-typo3";

export default defineConfig({
    plugins: [typo3()],
});
```

Declare the site package’s sources in `<site-package>/Configuration/ViteEntrypoints.json`. Paths are relative to this JSON file. Prefer one JavaScript entrypoint that imports its stylesheet, so TYPO3 emits one coherent application bundle:

```json
[
    "../Resources/Private/JavaScript/Main.entry.js"
]
```

```js
// Resources/Private/JavaScript/Main.entry.js
import "../Styles/Main.scss";

// Application JavaScript starts here.
```

Keep imported SCSS and JavaScript private source files. Let the Vite plugin choose its compatible default output and manifest locations unless project evidence requires an explicit `build.outDir` or manifest setting. If custom locations are necessary, update the AssetCollector manifest configuration and Vite output together; they are one contract.

Completion: the root config loads `typo3()`, the JSON is valid and discovers the entrypoint, and each imported source path resolves from its importing file.

## 5. Render assets once through Fluid

In the site’s actual page layout, add the AssetCollector Fluid namespace and one reference to the entrypoint in `<head>`. Preserve existing namespaces and adapt the layout path for either base package:

```html
<html
    data-namespace-typo3-fluid="true"
    xmlns:vite="http://typo3.org/ns/Praetorius/ViteAssetCollector/ViewHelpers"
>
    <head>
        <vite:asset entry="EXT:my_site_package/Resources/Private/JavaScript/Main.entry.js" />
    </head>
</html>
```

Replace `my_site_package` with the real extension key. Keep Bootstrap Package or `fluid_styled_content` rendering in place; only remove a legacy asset inclusion after proving the Vite bundle covers it. The ViewHelper emits development-server assets in Development context and manifest-backed assets after a production build.

Completion: exactly one layout on the rendered page registers the selected entrypoint and no duplicate stylesheet or script tag is produced.

## 6. Verify both modes

Start the server in the frontend root and keep it running in the foreground:

```bash
ddev vite
```

Use the public `https://<project>.ddev.site` page, with TYPO3 in Development context. Confirm it loads assets from the `https://vite.<project>.ddev.site` origin, a small SCSS change is reflected, and browser console/network output is clean. The AssetCollector and sidecar auto-detect the DDEV development server; avoid a fixed localhost `devServerUri` in this setup.

Then stop the server and verify the production artifact path:

```bash
ddev vite build
```

Confirm a manifest and generated assets exist at the configured/default location, clear TYPO3 caches if template or TypoScript configuration changed, and load the page without the dev server. Keep the build command in the deployment pipeline when the project needs production assets; do not assume development-sidecar output reaches production.

Completion: one SCSS change and one JavaScript change are served in development, and a no-dev-server production-style page resolves the built manifest without 404s.

## Troubleshooting branches

Load [diagnostics](references/diagnostics.md) when the pipeline is already installed, a build/dev request fails, styles do not update, output is missing, or a browser reports connection/CORS/manifest problems. It supplies evidence-led checks for the usual failure boundaries.

## Maintainer evaluation

Scenario coverage is recorded in [evals/evals.json](evals/evals.json). Run the validation commands in the README after editing this skill.
