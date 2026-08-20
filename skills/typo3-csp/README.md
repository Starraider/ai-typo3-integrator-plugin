# TYPO3 Content Security Policy

## What this skill solves

Provides a staged, evidence-led TYPO3 CSP rollout: observe in report-only mode, allow only justified sources, then enforce after staging verification.

## Use when

Use for `csp.yaml`, extension CSP rules, CSP violation reports, blocked frontend resources, or a planned enforcement rollout in TYPO3 v12–v14. It is not a generic web-security audit or permission to deploy policy changes.

## Expected outputs

A scoped policy change, rationale for every added source, the safe rollout state, and a verification plan covering affected frontend paths.

## Context requirements

Provide TYPO3 version, site identifier, existing feature flags and `csp.yaml`, affected URLs/resources, and whether the change is report-only, staging, or production.

## Installation

Install the enclosing plugin as described in the [plugin README](../../README.md), or copy this directory to `.agents/skills/typo3-csp/` (or another supported client location). `agents/openai.yaml` supplies optional Codex UI metadata only.

## Example prompts

- “Put our TYPO3 site into CSP report-only mode and show the checks before enforcement.”
- “Analyze these blocked Vimeo and Google Fonts violations and propose the smallest `csp.yaml` change.”
- “Enable `unsafe-inline` globally so our legacy page works.”

## Validation

Validate YAML, inspect the TYPO3 CSP reporting module, and retest representative pages before enforcement. Maintainers can run `new-skill/scripts/validate-skill.sh skills/typo3-csp --strict-portable`.

## Related skills

None in this plugin; CSP policy decisions remain separate from favicon, routing, or Fluid-template work.

## License

Licensed under [CC BY 4.0](../../LICENSE).
