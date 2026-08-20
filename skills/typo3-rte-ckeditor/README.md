# TYPO3 RTE CKEditor

This Skill configures TYPO3’s `rte_ckeditor` / CKEditor 5 integration, including presets, registration, toolbars, styles, link-browser options, and plugins.

## Use it for

- enabling TYPO3 rich text editing
- RTE YAML preset creation or changes
- `ext_localconf.php`, Page TSconfig, TCA, and preset assignment
- toolbar, content CSS, HTML-processing, or CKEditor plugin changes

## Included material

The full workflow is in [SKILL.md](SKILL.md). For common configurations and implementation details, see [RTE CKEditor patterns](references/rte-ckeditor-patterns.md).

## Working approach

Confirm the TYPO3 version, Composer setup, installed RTE extension, and current preset ownership before editing. Change the smallest relevant configuration layer, test the editor with representative fields and permissions, and validate the frontend HTML produced from saved content.

## License

This Skill is licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](../../LICENSE).

Copyright (c) 2026 Sven Kalbhenn ([https://www.skom.de](https://www.skom.de)).
