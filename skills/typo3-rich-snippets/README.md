# TYPO3 Rich Snippets

This Skill helps choose, generate, validate, and integrate schema.org structured data for TYPO3 pages.

## Use it for

- JSON-LD, Microdata, or RDFa markup
- rich-result eligibility for articles, products, events, FAQs, and organizations
- TYPO3 Fluid or TypoScript integration
- validating structured-data output and SEO-related implementation issues

## Included material

Use [SKILL.md](SKILL.md) for the workflow and decision guidance. Focused references cover:

- [schema reference](references/reference.md)
- [TYPO3 integration](references/typo3-integration.md)
- [testing](references/testing.md)
- [JSON-LD validation script](scripts/validate-jsonld.js)

## Working approach

Identify the page’s real primary content type before selecting a schema. Prefer JSON-LD unless an existing implementation requires another format, output only facts represented by the page, then validate both the generated JSON and the rendered markup.

## License

This Skill is licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](../../LICENSE).

Copyright (c) 2026 Sven Kalbhenn ([https://www.skom.de](https://www.skom.de)).
