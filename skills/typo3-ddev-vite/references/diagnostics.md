# Vite AssetCollector diagnostics

Use the first failed boundary as the repair target. Run read-only checks before changing dependencies or configuration, and preserve a working root configuration and package manager.

## Dev server is unavailable or the page uses built assets

1. Run `ddev status` and check the installed DDEV version plus `.ddev/` sidecar configuration.
2. Verify the add-on command from the frontend root: `ddev vite --help`, then run `ddev vite` in the foreground. It must remain running.
3. Verify TYPO3 is in `Development` context and inspect the page’s asset URLs. With the sidecar, the server is exposed at `https://vite.<project>.ddev.site`.
4. Inspect existing extension configuration. The defaults auto-detect vite-sidecar; a stale `devServerUri = http://localhost:5173` can force TYPO3 to the wrong origin. Remove or change it only with authorization and only if it is the demonstrated cause.

For a custom DDEV hostname or a browser origin outside the plugin default, extend `server.cors.origin` with `getDefaultAllowedOrigins()` rather than replacing its defaults. `vite-plugin-typo3` includes `*.ddev.site` by default.

## Entrypoint is not found or no bundle is emitted

1. Validate JSON syntax in `<site-package>/Configuration/ViteEntrypoints.json`.
2. Resolve every JSON path relative to `Configuration/`, not the project root. Confirm the file ends in the declared extension and is a real entrypoint.
3. Confirm the root Vite config uses `typo3()` and that the site package is Composer-discoverable by the TYPO3 project.
4. Run `ddev vite build` from the same directory that contains the root `package.json` and `vite.config.js`; use plugin debug output (`typo3({ debug: true })`) only while collecting evidence.

The standard integration declares entrypoints per extension. A separate root-level `frontend/` asset directory calls for manual Vite configuration, not an attempt to make `vite-plugin-typo3` discover it.

## Fluid page is missing CSS or JavaScript

1. Inspect the rendered HTML and confirm the `vite:asset` tag points to the exact `EXT:<extension-key>/Resources/Private/...` entrypoint path.
2. Verify the AssetCollector namespace is declared on the Fluid root element in the layout that actually renders the page.
3. Search layouts, TypoScript, and page configuration for duplicate legacy CSS/JavaScript inclusions. Retain one asset owner per bundle.
4. Clear TYPO3 caches after changing Fluid or configuration, then re-check page source and the browser network panel.

For both Bootstrap Package and `fluid_styled_content`, place the ViewHelper in the selected site package’s rendered page layout; the base package does not change the ViewHelper contract.

## SCSS does not compile or update

1. Confirm the entrypoint imports the SCSS file using a path relative to the entrypoint.
2. Check that the project’s active Node manifest includes `sass-embedded` (or the already working Sass implementation) as a development dependency.
3. Run the package-manager install in DDEV, then restart `ddev vite` after dependency changes.
4. Read Vite’s terminal output for the source path and Sass error. Fix the first missing import, syntax error, or unresolved alias shown there.

Prefer `EXT:<extension-key>/...` imports in styles and JavaScript when using aliases supplied by `vite-plugin-typo3`; this avoids `@` package-name collisions.

## Manifest or production assets 404

1. Stop `ddev vite` and run `ddev vite build` from the frontend root.
2. Verify the built manifest and assets exist in the location selected by the Vite plugin/default configuration.
3. Compare any custom Vite `build.outDir` or manifest filename with AssetCollector’s `defaultManifest` setting. Change both ends together.
4. Confirm the production deployment runs the build and releases its generated public assets. A local sidecar is a development service, not a production build step.

The Vite AssetCollector default manifest is `_assets/vite/.vite/manifest.json` for the compatible default Vite setup. Vite versions before 5 use a different default; prefer upgrading or explicitly aligning both paths rather than guessing.
