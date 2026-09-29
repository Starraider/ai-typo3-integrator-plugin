# TYPO3 StyleX

## What this skill solves

This skill installs `skom/stylex-connector` with Vite in a Composer-based TYPO3 site running under DDEV. It covers the sitepackage entrypoint, Vite sidecar, two build manifests, Fluid class lookup, and CSS alongside Fluid Styled Content, Bootstrap Package, or standalone Bootstrap.

## Use when

Use it for a new installation or to repair an incomplete StyleX pipeline. Conceptual StyleX questions do not need this installation workflow.

## Expected outputs

The result is a rendered development page and a production build whose CSS and JavaScript load through Vite AssetCollector.

## Context requirements

The skill needs the target TYPO3 project root, a working or installable DDEV project, the sitepackage and its actual page layout, and access to the connector documentation. It reads the guides from that project's `packages/stylex_connector/Documentation/` or `vendor/skom/stylex-connector/Documentation/` directory. If neither is present, the installation workflow installs the connector before configuring it.

## Installation

Install the complete plugin through a compatible Agent Plugin client as described in the [plugin README](../../README.md), or copy this whole directory to a client-supported Agent Skills location such as `<project-root>/.agents/skills/typo3-stylex/`. The source copy in this plugin is `skills/typo3-stylex/`. The portable `SKILL.md` works without client-specific metadata. Invoke it by name or ask for a StyleX Connector setup or repair. The workflow changes Composer and Node dependencies, DDEV add-ons, Vite and TYPO3 configuration, and sitepackage files as needed.

## Example prompts

- "Install StyleX Connector with Vite in this TYPO3 14 DDEV site and prove the production assets load."
- "Our TYPO3 site uses Fluid Styled Content. Add StyleX to one content template without dropping FSC's editor behavior."
- "Repair the StyleX build in our Bootstrap Package site; Vite builds, but Fluid classes have no CSS."
- "We include Bootstrap directly in TypoScript. Wire StyleX without duplicate CSS and verify cascade order."

## Validation

From the plugin root, run both validators against the source directory:

```bash
NEW_SKILL_DIR=/path/to/new-skill
"$NEW_SKILL_DIR/scripts/validate-skill.sh" skills/typo3-stylex --strict-portable
skills-ref validate skills/typo3-stylex
```

The source checkout keeps maintainer scenarios in `evals/evals.json`. The structural checks do not prove that a target TYPO3 site renders StyleX; the skill's development and production checks cover that separately.

## Related skills

- [TYPO3 Vite in DDEV](../typo3-ddev-vite/README.md) for the base Vite AssetCollector pipeline when StyleX is not involved.
- [TYPO3 Site Package](../typo3-sitepackage/README.md) for sitepackage structure, page layouts, and Site Sets.
- [TYPO3 Content Blocks](../typo3-content-blocks/README.md) for block definitions when StyleX classes appear in a Content Block template.

## License

Licensed under [CC BY 4.0](../../LICENSE).
