# TYPO3 Form YAML

Use this skill for TYPO3 v14 forms built with `typo3/cms-form` and stored as versioned YAML in an extension or site package.

## What this skill solves

It keeps EXT:form configuration and `.form.yaml` definitions in source control, selects the correct TYPO3 v14 registration path, and shows where to apply YAML styling properties or Fluid template overrides. It also covers Tailwind content scanning when YAML supplies utility classes.

## Use when

- Creating or editing a versioned `.form.yaml` definition.
- Configuring YAML persistence or form-set discovery in TYPO3 v14.
- Moving form configuration out of database storage into a site package or extension.
- Styling an EXT:form form with YAML attributes, Fluid overrides, or Tailwind.

## Expected outputs

- Versioned setup under `Configuration/Form/` and form definitions under `Resources/Private/Forms/`.
- A v14.2+ form-set configuration or the correct v14.0–v14.1 fallback.
- Styling configuration that matches the project's asset-build process.
- A cache-clear and browser-verification plan for visible changes.

## Context requirements

- Exact TYPO3 v14 minor version and location of the owning site package or extension.
- The desired form fields, storage policy, and any editor requirements.
- Current CSS framework and asset pipeline, especially for Tailwind classes.

## Installation

This directory is an Agent Skill supplied by the `typo3-extension-skills` plugin. It uses the portable Agent Skills core and is automatically discoverable by compatible Agent Plugin clients from `skills/typo3-form-yaml/`.

## Example prompts

- "Create a versioned contact form YAML file in our TYPO3 14.2 site package."
- "Configure the TYPO3 form editor to save forms into our extension instead of the database."
- "Make Tailwind compile the utility classes used in our TYPO3 form YAML."

## Validation

Read [the TYPO3 v14 form patterns](references/typo3-v14-form-patterns.md) before selecting an auto-discovery or legacy registration path. After configuration changes, rebuild frontend assets where needed, flush TYPO3 caches, and verify the mounted form URL.

## Related skills

- `typo3-secure-form` — for CAPTCHA, honeypot, and form-security requirements.
- `typo3-container` — for placing a form in a reusable b13/container layout.

## License

This project and all contained Agent Skills are licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](../../LICENSE).

Copyright (c) 2026 Sven Kalbhenn ([https://www.skom.de](https://www.skom.de)).
