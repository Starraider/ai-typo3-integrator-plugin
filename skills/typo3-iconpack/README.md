# TYPO3 Iconpack

Install and integrate Quellenform's Iconpack extension and an additional icon provider in a TYPO3 Composer project. This skill covers provider registration, rendering, custom extensions and site packages, backend identifiers, Fluid, assets, CKEditor insertion, stored content, and upgrades.

## What this skill solves

It makes the pack registry, TYPO3 backend identifiers, and editor persistence explicit so configuration uses supported APIs and icons survive rendering and editing.

## Use when

Use it for `quellenform/t3x-iconpack`, including installing Font Awesome, configuring pack YAML, adding icon selectors, and repairing icons that disappear after saving or fail to load. Use the related RTE skill for editor setup that does not involve Iconpack. Core backend icons alone and npm-only icon libraries are outside this skill's scope.

## Expected outputs

It produces versioned Composer/configuration changes in the owning extension, exact rendering examples, and verification evidence for the requested backend/frontend/RTE contexts.

## Context requirements

Supply the TYPO3 version, project path, extension key, desired provider, target fields/templates/modules, and current preset if known. The agent inspects available project files for missing details.

The researched baseline is Iconpack **1.5.5**, Font Awesome provider **1.3.1**, and its bundled Font Awesome **7.1.0**. Modern examples target TYPO3 12–14 with CKEditor 5; legacy examples are explicitly labeled. Composer constraints establish package compatibility, not proof of editor behavior on every TYPO3 patch release. Recheck the installed release and perform a save/reopen/frontend test.

## Installation

Install the enclosing plugin using the [plugin installation guide](../../plugin-installation.md), or copy this entire directory into `.agents/skills/typo3-iconpack/` using the [individual skill guide](../../skill-installation.md). Compatible Agent Skills clients discover its `SKILL.md` description. It uses portable metadata and has no client-specific companion file. Verify discovery in the target client; no installation into a client was performed by authoring these files.

Installing the skill does not install TYPO3 extensions. Composer/PHP and network access are required when the skill is used to change dependencies. Backend access is required for editor validation. Production deployment, destructive cleanup, and content migrations retain the user's authorization boundaries.

## Example prompts

- “Install Iconpack and its Font Awesome provider in our TYPO3 13.4 DDEV site package, with SVG content icons and webfont icons in the RTE.”
- “Use an installed Iconpack SVG for our backend module iconIdentifier and render the same pack in a Fluid frontend plugin.”
- “The CKEditor Iconpack button works, but icons vanish after save. Inspect the preset, stored data-iconfig, and frontend parse function.”
- “Add our own site-package SVG pack and upgrade Font Awesome without breaking existing fa6 references.”

## Guide contents

- [Installation and configuration](references/installation-configuration.md): Composer packages, settings, TypoScript, site sets, YAML overrides and registration.
- [Custom extensions, Fluid and assets](references/extension-fluid-assets.md): PHP/TCA, backend identifiers, legacy ext_tables.php, ViewHelpers, CSS and sprites.
- [RTE integration](references/rte.md): presets, Page TSconfig, plugin/button definition, rendering and persistence.
- [Operations](references/operations.md): troubleshooting, logs, permissions, version pinning, backup and update procedure.
- [Sources and baseline](references/sources.md): release-pinned upstream code and TYPO3 documentation.
- [Evaluation scenarios](evals/evals.json): routing and implementation expectations for maintainers.

## Validation

From the plugin root:

```bash
bash /path/to/new-skill/scripts/validate-skill.sh skills/typo3-iconpack --strict-portable
skills-ref validate skills/typo3-iconpack
python3 /path/to/new-plugin/scripts/validate_agent_plugin.py . --strict
```

Then test a representative TYPO3 site following the operations guide. Static validation and source verification do not certify an installed client's discovery or a live TYPO3 integration.

## Related skills

- [typo3-rte-ckeditor](../typo3-rte-ckeditor/README.md): general CKEditor presets and content processing.
- [typo3-sitepackage](../typo3-sitepackage/README.md): owning extension layout and template configuration.
- [typo3-site-sets](../typo3-site-sets/README.md): reusable configuration on TYPO3 13+.
- [typo3-csp](../typo3-csp/README.md): diagnosing blocked icon assets.

## License

Original skill instructions and examples are licensed under [CC BY 4.0](../../LICENSE). Iconpack/provider implementations retain their upstream GPL-3.0-or-later licenses. Font Awesome assets have their own licenses; preserve the notices shipped by the provider. This skill does not bundle those assets.
