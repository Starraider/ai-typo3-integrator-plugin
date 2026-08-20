# TYPO3 TypoScript Conditions

This Skill adds or repairs TYPO3 v14 frontend TypoScript conditions for page, rootline, site, language, request, version, and user context.

## Use it for

- conditional TypoScript in setup or imported files
- page IDs, rootlines, site identifiers, and locales
- frontend/backend user and group conditions
- safe request, session, and site-setting checks

## Included material

Read [SKILL.md](SKILL.md) for the conditions workflow and syntax. [Criteria catalog](references/criteria-catalog.md) lists focused condition patterns.

## Working approach

Identify the scope and choose the narrowest supported condition. Guard nullable values, use current TYPO3 expression syntax instead of legacy patterns, then clear caches and verify both matching and non-matching frontend contexts.

## License

This Skill is licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](../../LICENSE).

Copyright (c) 2026 Sven Kalbhenn ([https://www.skom.de](https://www.skom.de)).
