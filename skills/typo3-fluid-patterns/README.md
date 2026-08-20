# TYPO3 Fluid Patterns

## What this skill solves

Applies maintainable, CMS-first Fluid patterns for TYPO3 v12+ site packages, including template hierarchy, dynamic content, responsive media, accessibility, and progressive JavaScript.

## Use when

Use for page layouts, templates, partials, atoms, content rendering, Fluid links/images, and frontend accessibility patterns. It does not perform CSS-framework migration, visual redesign, or a full content-model redesign.

## Expected outputs

Small changes that fit the existing site-package hierarchy, preserve editor-managed content, and include relevant rendering and accessibility checks.

## Context requirements

Provide the affected templates/partials, current data processors or TypoScript, desired output, breakpoint/accessibility requirements, and existing project conventions.

## Installation

Install the enclosing plugin as described in the [plugin README](../../README.md), or copy this directory to `.agents/skills/typo3-fluid-patterns/`. `agents/openai.yaml` is an optional Codex-only presentation companion.

## Example prompts

- “Refactor this PAGEVIEW layout so editors control header, main, and footer content through `colPos`.”
- “Add an accessible two-level navigation partial with keyboard-safe behavior and translated labels.”
- “Migrate our entire Bootstrap theme to Tailwind.”

## Validation

Render the affected page, exercise editor-managed content, inspect responsive images, and test keyboard paths relevant to the change. Maintainers can run `new-skill/scripts/validate-skill.sh skills/typo3-fluid-patterns --strict-portable`.

## Related skills

[`typo3-menu-dataprocessor`](../typo3-menu-dataprocessor/README.md) supplies TYPO3 navigation data; [`typo3-language-menu`](../typo3-language-menu/README.md) owns the preference-aware language switcher.

## License

Licensed under [CC BY 4.0](../../LICENSE).
