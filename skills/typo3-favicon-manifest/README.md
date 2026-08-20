# TYPO3 Favicon and Web Manifest

## What this skill solves

Integrates a real favicon/icon set and web manifest into a TYPO3 v14 site package while keeping asset URLs, head markup, and site routes aligned.

## Use when

Use for missing or incorrect favicons, app icons, `site.webmanifest`, `browserconfig.xml`, head tags, or their root-level routes. It does not create brand assets or redesign a site's visual identity.

## Expected outputs

Exact file placement and head/configuration changes, the resulting public URLs, and browser-visible verification steps.

## Context requirements

Provide the owning site package, active site identifier, actual asset filenames, and whether manifest/browser-config files already exist.

## Installation

Install the enclosing plugin as described in the [plugin README](../../README.md), or copy this directory to `.agents/skills/typo3-favicon-manifest/`. The optional `agents/openai.yaml` affects Codex presentation, not portable behavior.

## Example prompts

- “Add our existing favicon set and `site.webmanifest` to this TYPO3 v14 site package.”
- “The manifest loads but its icon URLs 404 after deployment; diagnose the TYPO3 integration.”
- “Generate a new logo and decide our brand colors from scratch.”

## Validation

Inspect the rendered `<head>`, fetch each configured public URL, parse the manifest JSON, and verify the favicon in a browser after cache clearing. Maintainers can run `new-skill/scripts/validate-skill.sh skills/typo3-favicon-manifest --strict-portable`.

## Related skills

[`typo3-site-config-sets`](../typo3-site-config-sets/README.md) helps decide site-configuration ownership when that is uncertain.

## License

Licensed under [CC BY 4.0](../../LICENSE).
