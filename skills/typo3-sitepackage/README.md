# TYPO3 Site Package

## What this skill solves

Scaffolds and maintains a TYPO3 v13/v14 site package extension — the main theme and configuration layer for a TYPO3 website. Covers the complete file layout, Site Set wiring, page rendering via `PAGEVIEW`, and overriding templates of third-party extensions from within the site package.

## Use when

- Creating a new site package from scratch
- Deciding where a file belongs inside an existing site package
- Overriding templates of `EXT:fluid_styled_content`, `EXT:form`, or any other extension without modifying that extension's files
- Wiring a Site Set into an existing TYPO3 installation (TYPO3 v13+)

Does **not** cover: Extbase controller wiring, route enhancers, CSP headers, or Content Block authoring — use the matching skills for those.

## Expected outputs

A valid TYPO3 Composer-mode site package with:
- `composer.json` and extension metadata
- A Site Set (`Configuration/Sets/SitePackage/`)
- Page rendering via `PAGEVIEW` TypoScript
- Fluid template directory structure
- Override TypoScript for third-party templates where requested

## Context requirements

Provide: the TYPO3 version (v13 or v14), the Composer vendor name, the extension key, and a list of features (content elements to override, existing extensions to depend on, etc.).

## Installation

Install the enclosing plugin as described in the [plugin README](../../README.md), or copy this directory to `.agents/skills/typo3-sitepackage/`.

## Example prompts

- "Create a new TYPO3 site package for vendor `acme`, extension key `acme_site`."
- "Override the Text content element template in my site package."
- "Where should I put the favicon TypoScript in my TYPO3 14 site package?"
- "My site package's Site Set isn't loading — help me wire it into the site config."

## Validation

Check that:
1. `ddev composer require <vendor>/<package>:@dev` succeeds
2. The site set appears in **Sites › Setup** in the TYPO3 backend
3. Frontend renders without "No TypoScript template found" errors
4. Fluid cache is clean after template changes

Maintainers can run `new-skill/scripts/validate-skill.sh skills/typo3-sitepackage --strict-portable`.

## Related skills

- [`typo3-fluid-patterns`](../typo3-fluid-patterns/README.md) — Fluid template hierarchy, `lib.dynamicContent`, responsive images
- [`typo3-site-sets`](../typo3-site-sets/README.md) — Site Set placement decisions and typed settings
- [`typo3-typoscript-conditions`](../typo3-typoscript-conditions/README.md) — TypoScript conditions inside site package setup
- [`typo3-route-enhancers`](../typo3-route-enhancers/README.md) — URL routing in `config/sites/`
- [`typo3-content-blocks`](../typo3-content-blocks/README.md) — Custom content elements via Content Blocks
- [`typo3-playwright-ddev`](../typo3-playwright-ddev/README.md) — Browser testing of the rendered site

## License

Licensed under [CC BY 4.0](../../LICENSE).
