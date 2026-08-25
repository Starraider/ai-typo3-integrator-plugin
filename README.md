# TYPO3 Integrator Plugin

Portable [Agent Plugin 1.0.0](https://agent-plugins.org/specification) with reusable skills for TYPO3 site-package development, configuration, frontend rendering, testing, deployment, SEO, and editor integration.

## Package contract

- **Plugin:** `ai-typo3-integrator-plugin` (`plugin.json`, schema 1.0.0)
- **Portable components:** 20 immediate-child [Agent Skills](https://agentskills.io/specification) in `skills/`
- **MCP servers:** none
- **License:** CC-BY-4.0; see [LICENSE](LICENSE)

## Skills

| Skill | Focus |
| --- | --- |
| [typo3-content-blocks](skills/typo3-content-blocks/README.md) | Content Blocks configuration, rendering, and troubleshooting |
| [typo3-container](skills/typo3-container/README.md) | `b13/container` CTypes, nested content, and grid rendering |
| [typo3-csp](skills/typo3-csp/README.md) | Content Security Policy rollout and hardening |
| [typo3-deployer-deployment](skills/typo3-deployer-deployment/README.md) | Deployer 8 recipes, upgrades, and GitHub Actions deployments |
| [typo3-favicon-manifest](skills/typo3-favicon-manifest/README.md) | Favicons, app icons, and web manifests |
| [typo3-fluid-patterns](skills/typo3-fluid-patterns/README.md) | Fluid templates, content architecture, accessibility, and JS patterns |
| [typo3-form-yaml](skills/typo3-form-yaml/README.md) | Versioned EXT:form YAML, editor setup, and form styling |
| [typo3-frontend-registration](skills/typo3-frontend-registration/README.md) | Approval-gated frontend registration with CAPTCHA and felogin |
| [typo3-language-menu](skills/typo3-language-menu/README.md) | Language switcher with browser detection and preference persistence |
| [typo3-menu-dataprocessor](skills/typo3-menu-dataprocessor/README.md) | Navigation menus and language menus via data processors |
| [typo3-news-extension](skills/typo3-news-extension/README.md) | EXT:news configuration, templates, and site-package integration |
| [typo3-playwright-ddev](skills/typo3-playwright-ddev/README.md) | Playwright and accessibility test setup in DDEV |
| [typo3-playwright-workflow](skills/typo3-playwright-workflow/README.md) | Focused Playwright and visual-regression verification |
| [typo3-rich-snippets](skills/typo3-rich-snippets/README.md) | schema.org structured data and JSON-LD integration |
| [typo3-route-enhancers](skills/typo3-route-enhancers/README.md) | Speaking URLs and Extbase route enhancers |
| [typo3-rte-ckeditor](skills/typo3-rte-ckeditor/README.md) | CKEditor 5/RTE configuration and presets |
| [typo3-secure-form](skills/typo3-secure-form/README.md) | Secure form setup with CAPTCHA, CSP, and anti-spam controls |
| [typo3-site-sets](skills/typo3-site-sets/README.md) | Site configuration versus reusable Site Sets |
| [typo3-typoscript-conditions](skills/typo3-typoscript-conditions/README.md) | TYPO3 v14 frontend TypoScript conditions |
| [typo3-xml-sitemap](skills/typo3-xml-sitemap/README.md) | EXT:seo XML sitemaps and route integration |

## Compatibility note

Eighteen skills include optional `agents/openai.yaml` files for Codex presentation. Those files are source-client metadata, not portable Agent Plugins components, and are not declared in `plugin.json`. The remaining skills have no client-specific companion files.

Compatible clients discover the portable Skills from `skills/<skill-name>/SKILL.md`. Installation, trust, UI metadata, and client-specific activation are managed by each client.

## Validation

The source tree includes a maintainer-only `evals/evals.json` suite for every Skill, with representative, edge-case, and near-miss prompts. These files are excluded from release archives. From the plugin root, validate the portable package and all Skills with:

```bash
for skill in skills/*; do
  /path/to/new-skill/scripts/validate-skill.sh "$skill" --strict-portable
  skills-ref validate "$skill"
done
python3 /path/to/agent-plugin-builder/scripts/validate_agent_plugin.py . --strict
```

The structural validators do not execute bundled scripts, contact MCP servers, or test a target client's installation state.

## License

This plugin and all included skills are licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](LICENSE).

Copyright (c) 2026 Sven Kalbhenn ([https://www.skom.de](https://www.skom.de)).
