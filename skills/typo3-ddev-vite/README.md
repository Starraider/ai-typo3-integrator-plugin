# TYPO3 Vite in DDEV

## What this skill solves

This skill establishes, maintains, and diagnoses the complete Vite frontend-asset path for a TYPO3 site package in DDEV: Vite AssetCollector, `vite-plugin-typo3`, the Vite configuration, DDEV sidecar, entrypoint declaration, SCSS and JavaScript sources, Fluid output, and production build verification.

It deliberately treats Bootstrap Package and `fluid_styled_content` as equivalent at the Vite boundary. The selected package still owns content rendering; Vite owns the site package’s compiled frontend assets.

## Use when

- A TYPO3 DDEV site package needs its first Vite-based SCSS and JavaScript bundle.
- `vite-asset-collector`, `vite-plugin-typo3`, Vite, Sass, or `ddev-vite-sidecar` is absent or misconfigured.
- `Configuration/ViteEntrypoints.json`, a Vite entrypoint, or the Fluid `<vite:asset>` tag is missing or not being collected.
- Development assets, manifests, SCSS compilation, sidecar access, or production builds fail.

Use [TYPO3 Site Package](../typo3-sitepackage/README.md) for broader site-package scaffolding, rendering-package selection, Site Sets, and template architecture. Use [TYPO3 Playwright Workflow](../typo3-playwright-workflow/README.md) for routine browser verification after this pipeline works.

## Expected outputs

- A root Vite config using `vite-plugin-typo3`.
- A site-package `Configuration/ViteEntrypoints.json`, one JavaScript entrypoint, and SCSS imported from it.
- One Fluid `vite:asset` registration in the actual rendered page layout.
- A DDEV sidecar command path and a verified production build path.
- An evidence-based diagnosis for a broken existing setup, without replacing configuration that already works.

## Context requirements

- A Composer-mode TYPO3 project with DDEV and a site package.
- The project’s DDEV status, site-package path/extension key, and frontend package manager, or repository access sufficient to discover them.
- Permission before changing Composer/Node dependencies, lockfiles, DDEV add-ons, configuration, source files, layouts, or build output.

## Installation

This directory is a portable Agent Skill. Install the complete plugin through a compatible Agent Plugin client, or copy/symlink it into that client’s Agent Skills discovery path. Codex users may retain the bundled `agents/openai.yaml` for UI presentation; portable instructions remain in `SKILL.md`.

Keep `SKILL.md`, `README.md`, `references/`, `evals/`, and `agents/` together when installing from source.

## Example prompts

- “Add Vite to our DDEV TYPO3 site package so `Main.entry.js` compiles our SCSS and JavaScript. We use Bootstrap Package.”
- “Our `fluid_styled_content` site package has Vite dependencies, but the stylesheet is not included in the page. Diagnose it before changing files.”
- “`ddev vite` starts but the page never connects to the Vite server. Repair the DDEV sidecar and AssetCollector integration without replacing our existing Vite config.”
- “Prepare our Vite-backed TYPO3 site package for production and confirm that the manifest works with the dev server stopped.”

## Included resources

- [Troubleshooting diagnostics](references/diagnostics.md) for development-server, manifest, SCSS, entrypoint, and duplicated-asset failures.

## Validation

From the plugin root, validate the portable structure and then inspect the scenario suite:

```bash
/path/to/new-skill/scripts/validate-skill.sh skills/typo3-ddev-vite --strict-portable
skills-ref validate skills/typo3-ddev-vite
```

A live integration is complete only when the DDEV sidecar serves a changed SCSS and JavaScript source in Development context, and `ddev vite build` produces assets that load through the configured manifest with the dev server stopped.

## Sources

- [Vite AssetCollector installation guide](https://docs.typo3.org/p/praetorius/vite-asset-collector/main/en-us/Installation/Index.html)
- [Vite AssetCollector best practices](https://docs.typo3.org/p/praetorius/vite-asset-collector/main/en-us/BestPractices/Index.html)
- [vite-plugin-typo3 README](https://github.com/s2b/vite-plugin-typo3/)
- [ddev-vite-sidecar README](https://github.com/s2b/ddev-vite-sidecar)

## Related skills

- [TYPO3 Site Package](../typo3-sitepackage/README.md) for package layout, Site Sets, and Bootstrap Package versus `fluid_styled_content`.
- [TYPO3 Fluid Patterns](../typo3-fluid-patterns/README.md) for rendering layouts and frontend interaction patterns.
- [TYPO3 Playwright DDEV Setup](../typo3-playwright-ddev/README.md) for adding browser-test infrastructure.
- [TYPO3 Playwright Workflow](../typo3-playwright-workflow/README.md) for focused frontend verification.

## License

Licensed under [CC BY 4.0](../../LICENSE). Copyright (c) 2026 Sven Kalbhenn.
