# Existing-project extraction checklist

Use this checklist when the request starts with a working TYPO3 project. It is a decision record, not a blind copy procedure.

## Preserve deliberately

- Root Composer configuration, lock file, PHP version/platform policy, DDEV/CI/deployment automation, and documented developer commands.
- Sitepackage code: `composer.json`, namespaces, `Configuration/`, `Resources/`, `Classes/`, Content Blocks, and public assets.
- Site Sets and their configuration, including dependency names needed by an imported site configuration.
- A redacted root-page export, referenced FAL assets, and a basic site configuration only when a working demo is a goal.

## Replace or parameterize

- Composer vendor/package names, extension key, PHP namespace, display labels, domain/base URL, email addresses, site identifier, page titles, legal placeholders, and branding.
- CI/deployment identifiers, database names, image tags, and project paths. Parameterize them in documented environment variables or template placeholders rather than embedding production values.
- Package dependencies after checking each one is actually required by the sitepackage or demo content.

## Exclude

- `.env` files with values, credentials, private keys/certificates, tokens, SSH material, and external-service secrets.
- Runtime caches, logs, built dependencies, generated database state, install-tool state, personal `fileadmin` uploads, backups, and temporary import/export folders.
- `be_users`, authentication data, `sys_log`, personal editor settings, production redirects, analytics identifiers, customer data, and media without redistribution rights.

## Sitepackage structure mapping

Use this conventional sitepackage layout to keep imported editorial data separate from version-controlled implementation:

| Existing path | Template role |
| --- | --- |
| `Configuration/Sets/SitePackage/` | Version-controlled Site Set, TypoScript, Page TSconfig, and settings definitions |
| `Resources/Private/` and `Resources/Public/` | Fluid templates, language files, CSS, JavaScript, icons, and other shipped implementation assets |
| `ContentBlocks/` | Reusable custom content elements |
| `Initialisation/data.xml` | Sample pages and content export |
| `Initialisation/data.xml.files/` | Media referenced by that export |
| `Initialisation/Site/main/config.yaml` | Imported basic site configuration whose `rootPageId` matches the exported root page |

Use `Initialisation` with an **s**, matching Core conventions. Adapt the site identifier, package dependency, root-page ID, site title, locale, and base URL as a coherent set; then regenerate and test the demo export.

## Fresh-install acceptance record

Record the exact clean checkout/repository revision, PHP/TYPO3 version, Composer command, `extension:setup` command, chosen site identifier, expected root-page title, and any intentional manual step. Mark the template ready only after a separate empty database/installation shows the site, pages, content, and media correctly.
