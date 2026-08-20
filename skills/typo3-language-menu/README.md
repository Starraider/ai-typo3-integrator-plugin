# TYPO3 Language Menu

## What this skill solves

Builds a TYPO3 v13+ language selector that works without JavaScript and can optionally redirect first-time visitors from their browser preference while retaining a manual choice.

## Use when

Use for a site-package language menu, browser-locale matching, preference cookies, or its Fluid-to-JavaScript data bridge. It does not decide a site's translation architecture or consent policy.

## Expected outputs

TypoScript processor configuration, accessible Fluid markup, optional client-side preference handling, and test cases for language availability and redirects.

## Context requirements

Provide active site languages and URLs, the desired redirect/consent policy, the site package's asset build, and the current language-menu configuration if it exists.

## Installation

Install the enclosing plugin as described in the [plugin README](../../README.md), or copy this directory to `.agents/skills/typo3-language-menu/`. Its `agents/openai.yaml` adds optional Codex UI metadata.

## Example prompts

- “Add an accessible `language-menu` processor and Fluid partial for German and English.”
- “Keep a visitor’s manual English selection and stop the browser-locale redirect loop.”
- “Redirect every visitor to German regardless of their choice or consent.”

## Validation

Test current, available, and unavailable language entries with and without JavaScript; then test first visit, manual switch, saved preference, and redirect-loop prevention. Maintainers can run `new-skill/scripts/validate-skill.sh skills/typo3-language-menu --strict-portable`.

## Related skills

[`typo3-menu-dataprocessor`](../typo3-menu-dataprocessor/README.md) covers ordinary language-menu data processing without preference behavior.

## License

Licensed under [CC BY 4.0](../../LICENSE).
