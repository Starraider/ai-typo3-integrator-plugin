---
name: typo3-stylex
description: Install and verify skom/stylex-connector with Vite in a Composer TYPO3 project running in DDEV, including Fluid Styled Content, Bootstrap Package, or standalone Bootstrap integration. Use for a complete setup or repair of its StyleX asset pipeline.
license: CC-BY-4.0
compatibility: Requires a Composer-based TYPO3 project with DDEV, a sitepackage, and Node.js with the project's package manager available in the DDEV web container.
---

# TYPO3 StyleX

Carry the installation through to a rendered TYPO3 page and a production build. Work from the project root. Preserve the site's existing package manager, sitepackage, layouts, Vite plugins, and asset imports. Ask for missing site details only after inspecting the project and continuing independent setup work.

## 1. Identify the live configuration

Inspect `composer.json`, the lockfiles, `.ddev/`, site configuration, active Site Sets, sitepackage `composer.json`, page layout, TypoScript asset includes, and any Vite entrypoints/configuration. Determine the TYPO3 version, sitepackage Composer name, extension key and source directory, package manager, actual rendered layout, and whether the site uses Fluid Styled Content, Bootstrap Package, standalone Bootstrap, or a combination. For integration choices, read [integrations.md](references/integrations.md).

Locate the authoritative connector guides at `packages/stylex_connector/Documentation/Vite/SetupDdev.rst` and `packages/stylex_connector/Documentation/Integrations/Index.rst`, or under `vendor/skom/stylex-connector/Documentation/` in an installed project. Read both before editing. If neither source tree exists, confirm DDEV can start, install the connector with `ddev composer require skom/stylex-connector`, then read the installed guides before making other changes. Follow the installed guide's version when details differ from this skill.

Completion: the sitepackage, rendered layout, asset owner, and integration branch are identified from files or the running site.

## 2. Prepare TYPO3 and DDEV

Run `ddev start` and confirm the TYPO3 page, database, and site configuration work. Check Node and package manager in the web container. The sitepackage must be Composer installed, provide a page layout, and have an active Site Set for TYPO3 13/14. For TYPO3 12, import the connector's supplied TypoScript instead of adding a Site Set. Add the sitepackage as a root Composer requirement if it is only a local directory; use a `packages/*` path repository when appropriate.

Completion: TYPO3 renders the site's page layout before asset changes, and DDEV can run the chosen Node package manager.

## 3. Wire Vite asset delivery

Follow `SetupDdev.rst` sections 2–4. For a missing or broken base Vite pipeline independent of StyleX, use the sibling `typo3-ddev-vite` skill. Install `praetorius/vite-asset-collector`, Vite, `vite-plugin-typo3`, and the `s2b/ddev-vite-sidecar` add-on where absent. Use `ddev add-on get s2b/ddev-vite-sidecar` on DDEV 1.23.5+ or `ddev get` on older versions, then restart and check `ddev vite --help`. Keep existing Vite plugins. Ensure the installed sitepackage has `Configuration/ViteEntrypoints.json` pointing to a real private JavaScript entrypoint. That entrypoint imports its CSS and application JavaScript. Add one `<vite:asset>` call for the same `EXT:` entrypoint to the layout TYPO3 actually renders. Remove duplicate inclusion of those same assets.

Completion: one rendered layout registers the entrypoint, and DDEV has a `VITE_SERVER_URI` for its sidecar.

## 4. Wire StyleX compilation and class lookup

Follow `SetupDdev.rst` sections 5–7, adapting every example path and package name. Require `skom/stylex-connector` at the project root and from the sitepackage; update the Composer lockfile. Activate the extension if needed. Install `@stylexjs/stylex`, `@stylexjs/unplugin`, and `@babel/parser` at the project root with the existing Node package manager. Add `skom/stylex-connector` to the sitepackage's existing Site Set dependencies on TYPO3 13/14. Register the StyleX manifest with `StylexRegistry::registerManifest()` in the sitepackage's `ext_localconf.php`.

Configure the StyleX Vite plugin and the post-transform manifest writer exactly as the guide describes. The writer's output path must match the registered `EXT:` manifest path. Give each imported `.stylex.js` file a distinct basename. Import at least one `stylex.create()` source from the entrypoint, load `/virtual:stylex.css` once in development, and use one generated manifest key through `{stylex:class(...)}` in rendered Fluid markup. Keep `StylexConnector.includeCssViaTypoScript` false when Vite delivers built CSS. Apply the integration choice from [integrations.md](references/integrations.md).

Completion: the StyleX manifest has the Fluid key, the build includes its CSS, and no source file or CSS asset is included twice.

## 5. Prove the pipeline works

Run the Vite development server with `ddev vite` and load the TYPO3 page in a browser so its entrypoint and imports execute. Check that the HTML contains a compiled StyleX class and a Vite entrypoint from `https://vite.<project>.ddev.site`. Request `/virtual:stylex.css` after the entrypoint loads; require a nonempty response containing a selector for a known generated StyleX class. An HTTP 200 with an empty body does not prove compilation. When using HTTP requests instead of a browser, request the entrypoint and its imported StyleX modules before checking the virtual CSS. Change one safe StyleX declaration temporarily, confirm the CSS updates, then restore the value.

Stop the development server and confirm its endpoint no longer responds and no project Vite process still occupies the sidecar port. If an in-container process remains, identify its PID and terminate only that process before continuing. Run `ddev vite build` after the server has stopped, then flush TYPO3 caches. Inspect both `public/_assets/vite/.vite/manifest.json` and the registered StyleX manifest. Confirm the Vite entry lists emitted CSS, every referenced asset exists, and the StyleX manifest still contains the Fluid key.

For the HTTP production check, temporarily use TYPO3's Production context or disable the development Vite URI through the project's existing configuration. Record the original setting, flush caches, and request the page while the Vite server is stopped. Require built CSS and JavaScript URLs, successful asset responses, and no Vite development URLs. Restore the original setting and flush caches again even if the check fails. Check a representative FSC or Bootstrap component for the selected integration.

Repair any failed stage and repeat the affected verification. Report the commands and observed results. If DDEV, the database, or browser access is unavailable, identify the exact blocked check and avoid claiming a working installation from file presence alone.
