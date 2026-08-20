# TYPO3 Content Security Policy

This Skill provides a safe rollout and maintenance workflow for TYPO3 v12–v14 Content Security Policies.

## Use it for

- report-only CSP setup and staged enforcement
- `csp.yaml` and extension-level source rules
- interpreting TYPO3 CSP violation reports
- blocked scripts, styles, images, embeds, or fonts

## Included material

The main [SKILL.md](SKILL.md) defines the workflow. Its references provide the detailed implementation procedure, YAML/source syntax, PHP extension API information, and troubleshooting:

- [implementation workflow](references/implementation-workflow.md)
- [YAML syntax and sources](references/yaml-syntax-and-sources.md)
- [PHP extension API](references/php-extension-api.md)
- [troubleshooting](references/troubleshooting.md)

## Working approach

Audit first and enable report-only mode before whitelisting observed legitimate sources. Move to enforcement only after unexpected violations are resolved; validate the result in the TYPO3 backend and representative frontend pages.

## License

This Skill is licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](../../LICENSE).

Copyright (c) 2026 Sven Kalbhenn ([https://www.skom.de](https://www.skom.de)).
