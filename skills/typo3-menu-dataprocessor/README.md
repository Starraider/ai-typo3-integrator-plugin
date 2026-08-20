# TYPO3 Menu Data Processors

## What this skill solves

Builds TYPO3 v13+ page-tree navigation with `menu` and `language-menu` data processors and renders their state safely in Fluid.

## Use when

Use for main menus, breadcrumbs, directory/list/category menus, basic language selectors, and multi-level Fluid navigation. It does not own browser-language redirects or a non-TYPO3 application navigation model.

## Expected outputs

A scoped processor configuration, matching accessible Fluid rendering, stated hidden-page behavior, and verification of the requested menu states.

## Context requirements

Provide the target PAGEVIEW/FLUIDTEMPLATE, page-tree scope, required depth and special menu type, whether hidden pages belong in breadcrumbs, and site language requirements.

## Installation

Install the enclosing plugin as described in the [plugin README](../../README.md), or copy this directory to `.agents/skills/typo3-menu-dataprocessor/`. `agents/openai.yaml` is optional Codex presentation metadata.

## Example prompts

- “Create a two-level main menu in PAGEVIEW with active/current states in Fluid.”
- “Fix a breadcrumb that omits a hidden structural page, but only if product agrees it should appear.”
- “Add browser-language auto-detection and persist the selected locale.”

## Validation

Verify active/current state, empty and nested branches, hidden-page treatment, translated links, and keyboard behavior. Maintainers can run `new-skill/scripts/validate-skill.sh skills/typo3-menu-dataprocessor --strict-portable`.

## Related skills

[`typo3-language-menu`](../typo3-language-menu/README.md) owns browser-preference redirects and language-choice persistence; [`typo3-fluid-patterns`](../typo3-fluid-patterns/README.md) covers broader Fluid architecture.

## License

Licensed under [CC BY 4.0](../../LICENSE).
