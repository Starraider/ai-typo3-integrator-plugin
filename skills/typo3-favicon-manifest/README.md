# TYPO3 Favicon and Web Manifest

This Skill integrates favicons, platform icons, `site.webmanifest`, and `browserconfig.xml` into TYPO3 v14 site packages.

## Use it for

- adding or repairing head icon markup
- Fluid `f:page.headerData` or TypoScript head integration
- `page.shortcutIcon` configuration
- site-level routes for manifest and browser configuration files

## Included material

Read [SKILL.md](SKILL.md) for the end-to-end workflow. Supporting implementation patterns and resource guidance are available in:

- [implementation patterns](references/implementation-patterns.md)
- [resource guidance](references/resources.md)

## Working approach

Identify the site package, active site configuration, and actual asset filenames before generating markup. Keep every tag aligned with the deployed files, add routes only where the package serves them, then inspect the rendered `<head>` and each public asset URL.

## License

This Skill is licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](../../LICENSE).

Copyright (c) 2026 Sven Kalbhenn ([https://www.skom.de](https://www.skom.de)).
