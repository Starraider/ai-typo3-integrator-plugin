# TYPO3 TypoScript Conditions

## What this skill solves

Creates and repairs TYPO3 v14 frontend TypoScript conditions for page, language, site, request, version, and frontend/backend-user context.

## Use when

Use for conditional TypoScript in setup/imports and site-setting-aware constants. It does not substitute for authorization checks or support legacy TYPO3 condition APIs in new work.

## Expected outputs

A narrow current-syntax condition, its correct file scope, null-safety precautions, and matching/non-matching verification steps.

## Context requirements

Provide TYPO3 version, exact config file/scope, expected page/site/language/user/request context, and any existing condition to preserve or replace.

## Installation

Install the enclosing plugin as described in the [plugin README](../../README.md), or copy this directory to `.agents/skills/typo3-typoscript-conditions/`. `agents/openai.yaml` is optional Codex UI metadata.

## Example prompts

- “Show a banner only on page 42 in site language 1 with current TYPO3 v14 syntax.”
- “Guard this condition against a missing page argument and test both outcomes.”
- “Use `getTSFE()` and `loginUser()` to write our new v14 condition.”

## Validation

Validate TypoScript through the project workflow, clear caches, and test matching and non-matching frontend contexts. Maintainers can run `new-skill/scripts/validate-skill.sh skills/typo3-typoscript-conditions --strict-portable`.

## Related skills

[`typo3-site-sets`](../typo3-site-sets/README.md) owns configuration placement.

## License

Licensed under [CC BY 4.0](../../LICENSE).
