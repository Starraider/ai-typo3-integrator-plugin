# TYPO3 Language Menu

This Skill builds a TYPO3 v13+ language switcher using the `language-menu` data processor, a Fluid partial, and browser-language preference handling.

## Use it for

- language-selection menus in a site package
- first-visit redirects to a browser-preferred language
- persistence of a deliberate language choice in a cookie
- Fluid-to-JavaScript language data attributes

## Included material

The complete procedure is in [SKILL.md](SKILL.md). It is supported by:

- [Fluid template](references/fluid-template.md)
- [CSS patterns](references/css-patterns.md)
- [browser-preference script](assets/language-preference.js)

## Working approach

Confirm the active TYPO3 site languages and language URLs before adding redirect behavior. Preserve a user’s explicit choice, make the menu usable without JavaScript, and test initial visits, manual switches, unavailable translations, and cookie persistence.

## License

This Skill is licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](../../LICENSE).

Copyright (c) 2026 Sven Kalbhenn ([https://www.skom.de](https://www.skom.de)).
