---
name: typo3-project-template
description: Use when creating or adapting a TYPO3 v14 project template, Composer distribution, or sitepackage that installs a reproducible starter site with sample pages, assets, and site configuration. Covers extracting a template from an existing TYPO3 project and the Introduction Package-style Initialisation payload.
license: CC-BY-4.0
compatibility: Requires a TYPO3 v14 Composer project; creating or verifying Initialisation data needs a clean instance and access to the TYPO3 Export module.
---

# TYPO3 Project Template

## Outcome

Produce a TYPO3 v14 template that can be installed in a clean instance and yields the declared starter site: dependencies, sitepackage, site configuration, sample page tree, content, and assets. Choose the delivery form that matches the request; do not represent a repository skeleton as an Extension Manager distribution.

## Workflow

1. Establish the template contract and delivery form.

   Identify the TYPO3 minor-version range, Composer package/vendor, extension key, namespace, site identifier, target base URL policy, required extensions, and whether the template is a whole-project starter or an installable package. Prefer the smallest form that can satisfy installation and reuse:

   | Need | Delivery form |
   | --- | --- |
   | New repository with DDEV/CI/deployment and project-level Composer configuration | Repository template based on a clean existing project |
   | One installable quick-start package, like the Introduction Package | Distribution extension that requires the sitepackage and its dependencies |
   | A reusable theme with optional demo content | Sitepackage with an `Initialisation/` payload |

   Completion: a short manifest names the delivery form, installation command, expected page-tree root, site identifier, and every intentional sample-data component.

2. Audit the source project before basing a template on it.

   Copy or branch the existing project; retain its working code and Composer lock file. Inventory Composer dependencies, local packages, sitepackage namespace/key, site sets, `config/sites/*`, DDEV/CI/deployment files, database schema requirements, and editor-facing assets. Remove instance-specific material: credentials, API keys, private certificates, production URLs, user uploads, caches, logs, generated runtime configuration, database dumps containing backend users, and customer content that is not licensed for redistribution.

   Treat a site export as generated output. After changing a package name, extension key, site identifier, page IDs, or FAL paths, rebuild the export from a prepared source instance instead of broad text replacement in `data.xml`.

   Completion: the template has a documented source baseline, no secrets or personal backend users, and a deliberate keep/remove list for every project-specific file class.

3. Create the Composer and package boundary.

   In Composer projects, keep the sitepackage as a `typo3-cms-extension` with its extension key in `extra.typo3/cms.extension-key`; declare TYPO3 v14 and runtime dependencies in `require`. For local packages, configure a path repository in the project root and require the package by Composer name. Put frontend code, Site Sets, TypoScript, Page TSconfig, TCA, Content Blocks, templates, and public assets in the sitepackage—never in `fileadmin/`.

   If publishing an Extension Manager distribution is required, make a thin distribution extension depend on the sitepackage. Add legacy EM category/preview metadata only when that channel requires it; TYPO3 v14.2 deprecates `ext_emconf.php`, so Composer metadata remains the source of truth for Composer delivery.

   Completion: `composer validate` succeeds, the package resolves from a clean checkout, and the sitepackage owns all executable/configuration assets.

4. Add declarative starter-site data to the sitepackage.

   Use TYPO3's exact directory spelling: `Initialisation/`, not `Initialization/`:

   ```text
   <sitepackage>/
   ├── Initialisation/
   │   ├── data.xml
   │   ├── data.xml.files/             # FAL files referenced by exported records
   │   ├── Files/                      # optional non-record-referenced editor files
   │   └── Site/<site-identifier>/
   │       └── config.yaml
   ├── Configuration/
   └── Resources/
   ```

   Export the page-tree root through TYPO3's Export module into `Initialisation/data.xml`. Include the intended `pages`, `tt_content`, referenced records, and relations; exclude `be_users`, `sys_log`, temporary export files, and unrelated extensions. Select "Save files in extra folder" so referenced FAL assets are placed in `Initialisation/data.xml.files/`. Place only non-record-referenced files that editors must receive (for example an `ext:form` YAML file) in `Initialisation/Files/`; TYPO3 copies them to `fileadmin/<extension-key>/`.

   Put a basic site configuration at `Initialisation/Site/<site-identifier>/config.yaml`. It must use the imported root page UID and include the sitepackage Composer name under `dependencies` when the package exposes a Site Set. Existing target configuration with the same site identifier is preserved, so document how to choose a new identifier or configure a pre-existing site.

   Completion: each page/content reference resolves, the copied YAML has the expected site identifier and root UID, and every file belongs to exactly one of `Resources/`, `data.xml.files/`, or `Files/` for a stated reason.

5. Use imperative initialization only for work the declarative payload cannot express.

   `vendor/bin/typo3 extension:setup` activates packages, imports Core-recognized initialization data, runs required setup work, and clears caches. Use the PSR-14 `PackageInitializationEvent` only for an idempotent, package-scoped action that must run after activation. Register a service listener and, if it relies on imported data, order it after `ImportExtensionDataOnPackageInitialization`. Guard it by extension key and record/inspect an event storage entry to prevent duplicate work. Keep remote provisioning, secrets, interactive questions, and destructive mutations outside automatic activation.

   Completion: no listener exists when files/configuration/import data suffice; any listener is idempotent, ordered, scoped, and has a testable result.

6. Install and verify on a genuinely fresh TYPO3 v14 instance.

   From a clean checkout, install Composer dependencies and run `vendor/bin/typo3 extension:setup` (or `ddev typo3 extension:setup`). Verify the site exists in Sites, the root page and sample pages appear, frontend rendering has no missing FAL assets, the selected Site Set/dependency is active, and the package can be removed without deleting unrelated files. Re-test by creating a new database/installation rather than merely deleting pages: TYPO3 records completed imports in `sys_registry`.

   Completion: the documented clean-install sequence succeeds without manual database/file copying, and the generated site matches the manifest.

## Safety

Treat template extraction as a publication boundary. Obtain authorization before copying proprietary content, using production data, modifying the source project, or publishing a package. Never ship credentials, backend users, unredacted customer data, or unlicensed media. Make initialization additive and non-destructive: Core does not overwrite an existing same-identifier site configuration, and custom event listeners must follow the same principle.

## Resources

- Read [references/template-options.md](references/template-options.md) for the complete artifact matrix, source-specific caveats, and official TYPO3 links.
- Read [references/existing-project-checklist.md](references/existing-project-checklist.md) when extracting from an existing project.
- Use `typo3-sitepackage` to implement or extend the reusable sitepackage that this skill packages with starter data.
- Use `typo3-site-sets` when deciding whether a configuration value belongs in the imported site configuration or the sitepackage's reusable Site Set.
