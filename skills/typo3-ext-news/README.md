# TYPO3 News Extension

Use this skill to install, configure, and customize the TYPO3 News Extension, `georgringer/news`, in a TYPO3 project. It follows the repository's own DDEV, asset-build, and browser-test workflow when those tools are present.

## What this skill solves

It guides an implementation from dependency and site-set setup through plugin selection, TypoScript configuration, Fluid template/partial overrides, Tailwind styling, SEO view-helper preservation, and browser or visual-regression verification.

## Use when

- Adding or upgrading `georgringer/news` in a TYPO3 project.
- Wiring News settings through a site set or TypoScript.
- Customizing News list, detail, search, or selected-list templates.
- Creating reusable News Fluid partials or styling News with Tailwind.

## Expected outputs

- Composer and site-package configuration aligned with the installed News version.
- Correct plugin selection and shared `plugin.tx_news` view paths.
- Template and partial overrides that retain News SEO behavior.
- Cache, database-maintenance, and frontend verification steps.

## Context requirements

- TYPO3 and `georgringer/news` versions, plus the DDEV/project command conventions.
- Site-package paths, current Site Set configuration, and intended news pages/plugins.
- Existing templates, CSS tooling, language, routing, and SEO requirements.

## Installation

This directory is an Agent Skill supplied by the `typo3-extension-skills` plugin. It uses the portable Agent Skills core and is automatically discoverable by compatible Agent Plugin clients from `skills/typo3-ext-news/`.

## Example prompts

- "Install EXT:news and configure a list and detail page in our TYPO3 DDEV project."
- "Override the News detail template without breaking its SEO view helpers."
- "Extract reusable News card partials and style them with our Tailwind v4 build."

## Validation

Use the installed Composer package as the concrete source of truth, then clear TYPO3 caches and verify list, detail, and search pages. Consult [plugin configuration patterns](references/plugin-reference.md) and [template patterns](references/template-patterns.md) for the implementation details.

## Related skills

- `typo3-form-yaml` — for versioned TYPO3 forms used alongside News content.
- `typo3-ext-container` — for container layouts that host News plugins.

## License

This project and all contained Agent Skills are licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](../../LICENSE).

Copyright (c) 2026 Sven Kalbhenn ([https://www.skom.de](https://www.skom.de)).
