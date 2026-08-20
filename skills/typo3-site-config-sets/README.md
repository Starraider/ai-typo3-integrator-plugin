# TYPO3 Site Config and Sets

This Skill determines where TYPO3 v14 configuration belongs: a concrete site configuration or a reusable Site Set in a site package or extension.

## Use it for

- deciding between `config/sites/<site-id>/` and `Configuration/Sets/<set-name>/`
- reusable TypoScript, Page TSconfig, and typed site settings
- extension and Extbase-plugin configuration placement
- moving configuration to its correct ownership boundary

## Included material

[SKILL.md](SKILL.md) contains the placement rules. [Site-handling placement](references/site-handling-placement.md) provides supporting examples and edge cases.

## Working approach

Classify whether the value identifies one mounted site or is reusable package behavior. Keep per-site values with the site, share defaults through Site Sets, and express dependencies through Site Set metadata rather than cross-extension TypoScript imports.

## License

This Skill is licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](../../LICENSE).

Copyright (c) 2026 Sven Kalbhenn ([https://www.skom.de](https://www.skom.de)).
