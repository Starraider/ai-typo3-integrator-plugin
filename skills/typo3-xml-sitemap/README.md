# TYPO3 XML Sitemap

This Skill configures TYPO3 v14 XML sitemaps through EXT:seo, including page and record sitemaps, multi-language output, custom providers, and speaking URLs.

## Use it for

- `/sitemap.xml` and PageType route enhancer configuration
- `RecordsXmlSitemapDataProvider` and custom XML sitemap providers
- EXT:news and other record-based sitemap output
- hreflang-aware record URLs and sitemap troubleshooting

## Included material

[SKILL.md](SKILL.md) contains the full workflow. Supporting guides are:

- [configuration patterns](references/configuration-patterns.md)
- [verification](references/verification.md)

## Working approach

Confirm EXT:seo, active site configuration, and speaking detail-page routing first. Configure the sitemap index and providers for the relevant languages, clear caches, then verify both generated XML and the linked detail URLs for every configured provider.

## License

This Skill is licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](../../LICENSE).

Copyright (c) 2026 Sven Kalbhenn ([https://www.skom.de](https://www.skom.de)).
