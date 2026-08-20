# TYPO3 Route Enhancers

## What this skill solves

Configures and troubleshoots TYPO3 speaking URLs with site-config `routeEnhancers`, especially Extbase detail, filter, and pagination routes.

## Use when

Use for `config.yaml` route enhancer work, mismatched Extbase arguments, route aspects, `limitToPages`, cHash behavior, and URLs falling back to query strings. It does not implement a custom routing mapper or turn arbitrary free-text search into a path without explicit scope.

## Expected outputs

An exact scoped configuration block, evidence-backed placeholder mappings, stated assumptions, and two-way route verification steps.

## Context requirements

Provide active site config, host page IDs, real generated GET parameters, extension/plugin/controller/action names, table/slugs, and intended URL variants.

## Installation

Install the enclosing plugin as described in the [plugin README](../../README.md), or copy this directory to `.agents/skills/typo3-route-enhancers/`. The `agents/openai.yaml` companion affects only Codex presentation.

## Example prompts

- “Add a slug-based detail route for our Extbase product plugin on page 45.”
- “Fix this pagination route that still emits `@widget_0[currentPage]` as a query parameter.”
- “Make every arbitrary search query a speaking URL with a built-in mapper.”

## Validation

Parse the site YAML, clear caches, test outbound generation and inbound resolution, then test invalid/missing values and unrelated pages. Maintainers can run `new-skill/scripts/validate-skill.sh skills/typo3-route-enhancers --strict-portable`.

## Related skills

[`typo3-xml-sitemap`](../typo3-xml-sitemap/README.md) depends on detail routes for canonical sitemap URLs; [`typo3-site-sets`](../typo3-site-sets/README.md) clarifies configuration placement.

## License

Licensed under [CC BY 4.0](../../LICENSE).
