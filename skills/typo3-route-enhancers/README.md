# TYPO3 Route Enhancers

This Skill configures TYPO3 `routeEnhancers` for speaking URLs, with particular support for Extbase detail pages, filters, pagination, aliases, and cHash-sensitive parameters.

## Use it for

- site `config.yaml` route enhancers
- mapping plugin arguments to human-readable URL paths
- URL generation or resolving that falls back to query strings
- controller/action routes, aspects, requirements, and `limitToPages`

## Included material

[SKILL.md](SKILL.md) contains the main decision flow and examples. Further configuration and ready-made patterns are in:

- [configuration patterns](references/configuration-patterns.md)
- [ready-made patterns](references/ready-made-patterns.md)

## Working approach

Inspect the real plugin namespace and arguments rather than guessing from labels. Model every supported URL variant, restrict routing to the intended page scope, clear TYPO3 caches, and test both URL generation and inbound resolving.

## License

This Skill is licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](../../LICENSE).

Copyright (c) 2026 Sven Kalbhenn ([https://www.skom.de](https://www.skom.de)).
