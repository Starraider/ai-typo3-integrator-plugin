# TYPO3 RTE CKEditor

## What this skill solves

Configures TYPO3 `rte_ckeditor` / CKEditor 5 presets, registration, assignment, toolbar features, allowed markup, and resulting frontend output.

## Use when

Use for RTE YAML, `ext_localconf.php`, Page TSconfig, TCA assignment, toolbar/styles/link-browser changes, content CSS, and compatible CKEditor plugins. It does not make CKEditor 4 plugins compatible or justify disabling content filtering.

## Expected outputs

The smallest correctly owned preset/configuration change, its assignment, any dependency note, and backend/frontend verification steps.

## Context requirements

Provide TYPO3 and RTE versions, Composer status, owning extension/site package, target field/content type, existing preset, and required editor behavior.

## Installation

Install the enclosing plugin as described in the [plugin README](../../README.md), or copy this directory to `.agents/skills/typo3-rte-ckeditor/`. `agents/openai.yaml` provides optional Codex presentation metadata.

## Example prompts

- “Create a sitepackage-owned CKEditor 5 preset with headings, links, and a limited toolbar.”
- “Our RTE accepts a style but TYPO3 strips it on save; fix the processing alignment.”
- “Import this CKEditor 4 plugin into our TYPO3 v14 preset.”

## Validation

Flush caches, confirm the preset is registered and assigned, test it with the intended backend role, save representative content, and inspect frontend HTML. Maintainers can run `new-skill/scripts/validate-skill.sh skills/typo3-rte-ckeditor --strict-portable`.

## Related skills

[`typo3-site-config-sets`](../typo3-site-config-sets/README.md) helps decide whether shared configuration belongs in a reusable set.

## License

Licensed under [CC BY 4.0](../../LICENSE).
