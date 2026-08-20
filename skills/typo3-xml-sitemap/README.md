# TYPO3 XML Sitemap

## What this skill solves

Configures and troubleshoots TYPO3 v14 `EXT:seo` XML sitemaps for pages and records, including site routes, language output, canonical detail URLs, and custom providers.

## Use when

Use for `/sitemap.xml`, sitemap PageType routes, `RecordsXmlSitemapDataProvider`, custom providers, record URLs, and sitemap validation. It does not publish non-indexable/internal content or provide a general SEO crawl strategy.

## Expected outputs

The appropriate TypoScript/PHP/site-config changes, scope assumptions for records and languages, and end-to-end XML and URL verification.

## Context requirements

Provide TYPO3/`EXT:seo` version, active site configuration, sitemap names, source table and storage PIDs, detail page/plugin route, language policy, and a reachable frontend URL.

## Installation

Install the enclosing plugin as described in the [plugin README](../../README.md), or copy this directory to `.agents/skills/typo3-xml-sitemap/`. `agents/openai.yaml` provides optional Codex presentation metadata.

## Example prompts

- “Add a record sitemap for `tx_catalog_domain_model_product` with canonical slug detail URLs.”
- “Diagnose why `/sitemap.xml` works but every record URL contains query parameters.”
- “Include hidden drafts and pages excluded from search in every sitemap.”

## Validation

Clear caches, fetch the index and each requested sitemap, parse returned XML, verify representative detail URLs in every site language, and exclude invalid records. Maintainers can run `new-skill/scripts/validate-skill.sh skills/typo3-xml-sitemap --strict-portable`.

## Related skills

[`typo3-route-enhancers`](../typo3-route-enhancers/README.md) configures record detail routes; [`typo3-site-sets`](../typo3-site-sets/README.md) decides reusable configuration placement.

## License

Licensed under [CC BY 4.0](../../LICENSE).
