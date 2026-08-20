# TYPO3 Fluid Patterns

This Skill supplies framework-agnostic Fluid template patterns for TYPO3 v12+ site packages, with a focus on maintainable component structure and accessible frontend output.

## Use it for

- page layouts, templates, partials, and reusable atoms
- CMS-first content rendering and `lib.dynamicContent`
- responsive images, colPos propagation, and progressive JavaScript
- WCAG 2.1 AA-oriented template patterns

## Included material

[SKILL.md](SKILL.md) explains the baseline architecture. Consult the focused references as needed:

- [accessibility patterns](references/accessibility-patterns.md)
- [CMS-first content](references/cms-first-content.md)
- [colPos propagation](references/colpos-propagation.md)
- [JavaScript patterns](references/javascript-patterns.md)
- [responsive image pattern](references/responsive-image-pattern.md)

## Working approach

Inspect the project’s existing site-package hierarchy before adding a convention. Keep content ownership in the CMS, use the narrowest reusable partial or layout, and verify both responsive output and keyboard-accessible behavior after changes.

## License

This Skill is licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](../../LICENSE).

Copyright (c) 2026 Sven Kalbhenn ([https://www.skom.de](https://www.skom.de)).
