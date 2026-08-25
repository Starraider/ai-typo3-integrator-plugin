# TYPO3 Container

Use this skill to create and review project-specific grid and nested-content elements with [`b13/container`](https://extensions.typo3.org/extension/container) in TYPO3.

## What this skill solves

It provides a repeatable approach for registering container CTypes, exposing styling controls in TCA, configuring rendering with `ContainerProcessor`, and building Fluid templates that use the project's existing CSS framework. It covers two-column, three-column, and related container layouts, including backend previews and troubleshooting.

## Use when

- Adding `b13/container` to a TYPO3 site package or theme extension.
- Building reusable content grids or nested content-element areas.
- Adding container options such as background, width, spacing, or mobile stacking order.
- Reviewing a container registration, TypoScript setup, TCA override, or Fluid template.

## Expected outputs

- A container CType registration and icon setup in the owning site package.
- TCA fields and configuration for the requested editor-facing options.
- TypoScript and Fluid rendering using Bootstrap, Tailwind, or the detected project framework.
- A concrete backend-preview and frontend verification checklist.

## Context requirements

- TYPO3 version, site-package path, and the installed `b13/container` version.
- Existing CType conventions, icon locations, and TypoScript layout.
- The project's CSS framework and required grid variants.

## Installation

This directory is an Agent Skill supplied by the `typo3-extension-skills` plugin. It uses the portable Agent Skills core and is automatically discoverable by compatible Agent Plugin clients from `skills/typo3-ext-container/`; no Composer package is installed by this skill itself.

## Example prompts

- "Add a two-column b13/container element to our TYPO3 site package."
- "Give editors a background colour and full-width option for our existing container CType."
- "Review our ContainerProcessor and Fluid template for a three-column container on mobile."

## Validation

Follow the checks in `SKILL.md`: confirm the installed dependency and framework, clear TYPO3 caches, and inspect backend and frontend rendering. Read [the detailed container patterns](references/container-patterns.md) for concrete registration, TCA, TypoScript, and Fluid examples.

## Related skills

- `typo3-form-yaml` — for EXT:form YAML content rendered within a container.
- `typo3-secure-form` — for hardening frontend forms placed in a container.

## License

This project and all contained Agent Skills are licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](../../LICENSE).

Copyright (c) 2026 Sven Kalbhenn ([https://www.skom.de](https://www.skom.de)).
