# TYPO3 Rich Snippets

## What this skill solves

Selects, produces, validates, and integrates truthful schema.org structured data for TYPO3 pages, with JSON-LD as the normal default.

## Use when

Use for schema markup, JSON-LD, rich-result diagnostics, structured-data validation, and Fluid/TypoScript integration. It does not manufacture page facts, guarantee Google rich-result display, or perform broad SEO strategy.

## Expected outputs

The appropriate schema type, valid and content-faithful markup, a TYPO3 integration approach, and syntax/rendered-output verification.

## Context requirements

Provide the page's visible content and canonical URL, record field mappings, selected schema target if known, existing markup, and access to a rendered page for validation.

## Installation

Install the enclosing plugin as described in the [plugin README](../../README.md), or copy this directory to `.agents/skills/typo3-rich-snippets/`. Node.js is needed only for the bundled validator; `agents/openai.yaml` is optional Codex metadata.

## Example prompts

- “Add truthful `NewsArticle` JSON-LD to this TYPO3 article template using its existing record fields.”
- “Validate this rendered Product JSON-LD and identify why it fails schema checks.”
- “Add five-star reviews to our business markup even though the page has no reviews.”

## Validation

Validate JSON syntax, render the actual page, and use the relevant Schema Markup Validator or Rich Results Test when available. The optional command is `node scripts/validate-jsonld.js <file>`. Maintainers can run `new-skill/scripts/validate-skill.sh skills/typo3-rich-snippets --strict-portable`.

## Related skills

[`typo3-fluid-patterns`](../typo3-fluid-patterns/README.md) helps place server-rendered markup in the site's Fluid hierarchy.

## License

Licensed under [CC BY 4.0](../../LICENSE).
