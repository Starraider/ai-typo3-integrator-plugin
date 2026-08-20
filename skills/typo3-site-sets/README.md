# TYPO3 Site Config and Sets

## What this skill solves

Decides whether a TYPO3 v14 setting belongs to one concrete site's `config/sites/` files, a reusable Site Set, or a typed setting definition.

## Use when

Use before placing site-handling configuration, reusable TypoScript, Page TSconfig, or package-level settings. It decides ownership and does not replace implementation skills for routing, Extbase, FlexForms, or templates.

## Expected outputs

A clear target file, why it matches the reuse boundary, dependency/override implications, and handoff to the implementation concern where needed.

## Context requirements

Provide the setting's purpose, number of affected sites, owning site package or extension, existing Site Sets/dependencies, and whether editors must change the value per site.

## Installation

Install the enclosing plugin as described in the [plugin README](../../README.md), or copy this directory to `.agents/skills/typo3-site-sets/`. Its `agents/openai.yaml` is optional Codex display metadata.

## Example prompts

- “Should our extension's `detailPid` be a Site Set setting or live in `config/sites/acme/settings.yaml`?”
- “Move reusable page TSconfig and defaults out of one concrete site's configuration.”
- “Put this site's production base URL and root page ID into the reusable extension set.”

## Validation

Check that the selected layer matches the reuse boundary, validate YAML/TypoScript as appropriate, load the Site Set, and verify the site-settings editor does not discard required content. Maintainers can run `new-skill/scripts/validate-skill.sh skills/typo3-site-sets --strict-portable`.

## Related skills

[`typo3-route-enhancers`](../typo3-route-enhancers/README.md), [`typo3-typoscript-conditions`](../typo3-typoscript-conditions/README.md), and [`typo3-xml-sitemap`](../typo3-xml-sitemap/README.md) implement configuration after placement is decided.

## License

Licensed under [CC BY 4.0](../../LICENSE).
