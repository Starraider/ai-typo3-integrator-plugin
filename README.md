# TYPO3 Integrator Plugin

Portable [Agent Plugin 1.0.0](https://agent-plugins.org/specification) providing reusable skills for TYPO3 site-package development, configuration, frontend rendering, SEO, and editor integration.

## Package contract

- **Plugin:** `ai-typo3-integrator-plugin` (`plugin.json`, schema 1.0.0)
- **Portable components:** 12 immediate-child [Agent Skills](https://agentskills.io/specification) in `skills/`
- **MCP servers:** none
- **License:** CC-BY-4.0; see [LICENSE](LICENSE)

## Skills

| Skill | Focus |
| --- | --- |
| [typo3-content-blocks](skills/typo3-content-blocks/README.md) | Content Blocks configuration, rendering, and troubleshooting |
| [typo3-csp](skills/typo3-csp/README.md) | Content Security Policy rollout and hardening |
| [typo3-favicon-manifest](skills/typo3-favicon-manifest/README.md) | Favicons, app icons, and web manifests |
| [typo3-fluid-patterns](skills/typo3-fluid-patterns/README.md) | Fluid templates, content architecture, accessibility, and JS patterns |
| [typo3-language-menu](skills/typo3-language-menu/README.md) | Language switcher with browser detection and preference persistence |
| [typo3-menu-dataprocessor](skills/typo3-menu-dataprocessor/README.md) | Navigation menus and language menus via data processors |
| [typo3-rich-snippets](skills/typo3-rich-snippets/README.md) | schema.org structured data and JSON-LD integration |
| [typo3-route-enhancers](skills/typo3-route-enhancers/README.md) | Speaking URLs and Extbase route enhancers |
| [typo3-rte-ckeditor](skills/typo3-rte-ckeditor/README.md) | CKEditor 5/RTE configuration and presets |
| [typo3-site-sets](skills/typo3-site-sets/README.md) | Site configuration versus reusable Site Sets |
| [typo3-typoscript-conditions](skills/typo3-typoscript-conditions/README.md) | TYPO3 v14 frontend TypoScript conditions |
| [typo3-xml-sitemap](skills/typo3-xml-sitemap/README.md) | EXT:seo XML sitemaps and route integration |

## Compatibility note

Each Skill retains `agents/openai.yaml` display metadata for Codex. That metadata is not a portable Agent Plugins component and is not declared in `plugin.json`; it remains only for source-client presentation. No client-specific extension is asserted or tested by this package.

Compatible clients discover the portable Skills from `skills/<skill-name>/SKILL.md`. Installation, trust, UI metadata, and client-specific activation are managed by each client.

## Validation

The source tree includes a maintainer-only `evals/evals.json` suite for every Skill, with representative, edge-case, and near-miss prompts. These files are excluded from release archives. From the plugin root, validate the portable package and all Skills with:

```bash
for skill in skills/*; do
  /path/to/new-skill/scripts/validate-skill.sh "$skill" --strict-portable
done
python3 /path/to/agent-plugin-builder/scripts/validate_agent_plugin.py . --strict
```

Run `skills-ref validate skills/<skill-name>` as an additional check where the reference validator is installed.

## License

This project and all contained Agent Skills are licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](LICENSE).

Copyright (c) 2026 Sven Kalbhenn ([https://www.skom.de](https://www.skom.de)).
